-- Delta City RP: paying for services (mechanic repairs, the tow truck, and later other businesses).
--
-- pay_service(p_amount, p_state, p_reason) takes p_amount from the signed-in citizen's cash, adds it to that state's
-- row in state_accounts, and records the payment in ledger, all in one transaction: if any step fails, nothing is
-- taken. It refuses if the citizen cannot afford it. Returns {"ok": true, "cash": <cash left>, "state": ..., "amount": ...}.
--
-- The money table columns are found by name when the function runs, so it fits the tables already in the database:
--   characters:     owner (the signed-in user), cash, name
--   state_accounts: the state's name in state / state_name / name, its money in balance / amount / cash
--   ledger:         fills whichever of these it has: kind or type or action, amount, state or state_name,
--                   reason or note or memo or description, owner or user_id or citizen or by_owner, name or by_name
-- If state_accounts or ledger has a required column the function cannot fill, the payment is refused with the
-- database's message and nothing is charged.
--
-- Run the whole file once in the Supabase SQL editor. Running it again is safe.

create or replace function public.pay_service(p_amount bigint, p_state text, p_reason text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_uid    uuid := auth.uid();
  v_cash   bigint;
  v_name   text;
  v_scol   text;
  v_bcol   text;
  v_n      int;
  v_cols   text := '';
  v_vals   text := '';
  v_reason text := left(coalesce(nullif(trim(p_reason), ''), 'Service'), 200);
  c        text;
begin
  if v_uid is null then
    raise exception 'Sign in to pay.';
  end if;
  if p_amount is null or p_amount <= 0 then
    raise exception 'The amount must be more than zero.';
  end if;
  if p_amount > 1000000000 then
    raise exception 'That amount is too large for one payment.';
  end if;
  if p_state is null or p_state not in ('Asaba', 'Warri', 'Ozoro', 'Agbor') then
    raise exception 'Unknown state: %', coalesce(p_state, '(none)');
  end if;

  -- the citizen's cash, locked so two payments at once cannot both spend it
  select cash, name into v_cash, v_name from characters where owner = v_uid for update;
  if not found then
    raise exception 'No citizen record for this account.';
  end if;
  if coalesce(v_cash, 0) < p_amount then
    raise exception 'Not enough cash: you have K%, this costs K%.',
      to_char(coalesce(v_cash, 0), 'FM999,999,999,990'), to_char(p_amount, 'FM999,999,999,990');
  end if;

  -- the state account's columns
  select column_name into v_scol from information_schema.columns
    where table_schema = 'public' and table_name = 'state_accounts' and column_name in ('state', 'state_name', 'name')
    order by array_position(array['state', 'state_name', 'name'], column_name::text) limit 1;
  select column_name into v_bcol from information_schema.columns
    where table_schema = 'public' and table_name = 'state_accounts' and column_name in ('balance', 'amount', 'cash')
    order by array_position(array['balance', 'amount', 'cash'], column_name::text) limit 1;
  if v_scol is null or v_bcol is null then
    raise exception 'state_accounts needs a state column and a balance column.';
  end if;

  update characters set cash = cash - p_amount where owner = v_uid;

  execute format('update state_accounts set %I = coalesce(%I, 0) + $1 where %I = $2', v_bcol, v_bcol, v_scol)
    using p_amount, p_state;
  get diagnostics v_n = row_count;
  if v_n = 0 then
    raise exception 'No account for % in state_accounts.', p_state;     -- rolls back the cash taken above
  end if;

  -- the ledger: one row, in whichever of the usual columns this table has
  for c in
    select x.col from (values
      ('kind'), ('type'), ('action'), ('amount'), ('state'), ('state_name'), ('reason'), ('note'), ('memo'),
      ('description'), ('owner'), ('user_id'), ('citizen'), ('by_owner'), ('name'), ('by_name')) as x(col)
    where exists (select 1 from information_schema.columns
                  where table_schema = 'public' and table_name = 'ledger' and column_name = x.col)
  loop
    -- one column for each meaning: the first that exists
    if (c in ('type', 'action') and v_cols ~ '(^|,)kind(,|$)')
       or (c = 'action' and v_cols ~ '(^|,)type(,|$)')
       or (c = 'state_name' and v_cols ~ '(^|,)state(,|$)')
       or (c in ('note', 'memo', 'description') and v_cols ~ '(^|,)(reason|note|memo)(,|$)')
       or (c in ('user_id', 'citizen', 'by_owner') and v_cols ~ '(^|,)(owner|user_id|citizen)(,|$)')
       or (c = 'by_name' and v_cols ~ '(^|,)name(,|$)') then
      continue;
    end if;
    v_cols := v_cols || case when v_cols = '' then '' else ',' end || c;
    v_vals := v_vals || case when v_vals = '' then '' else ',' end || case
      when c in ('kind', 'type', 'action') then quote_literal('service')
      when c = 'amount' then p_amount::text
      when c in ('state', 'state_name') then quote_literal(p_state)
      when c in ('reason', 'note', 'memo', 'description') then quote_literal(v_reason)
      when c in ('owner', 'user_id', 'citizen', 'by_owner') then quote_literal(v_uid::text)
      when c in ('name', 'by_name') then quote_literal(coalesce(v_name, ''))
    end;
  end loop;
  if v_cols = '' then
    raise exception 'The ledger table has none of the expected columns.';
  end if;
  execute format('insert into ledger (%s) values (%s)',
    (select string_agg(quote_ident(x), ',') from unnest(string_to_array(v_cols, ',')) as x), v_vals);

  return jsonb_build_object('ok', true, 'cash', v_cash - p_amount, 'state', p_state, 'amount', p_amount);
end;
$$;

revoke all on function public.pay_service(bigint, text, text) from public;
revoke all on function public.pay_service(bigint, text, text) from anon;
grant execute on function public.pay_service(bigint, text, text) to authenticated;
