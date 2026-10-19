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
  v        text;
  r        record;
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

  -- the ledger: one row. Every column is filled from its name (and cast to its type); columns with a default
  -- that we do not recognise are left to their default. A required column we cannot fill stops the payment.
  for r in
    select column_name::text as col, udt_name::text as typ, is_nullable = 'NO' and column_default is null as must
      from information_schema.columns
     where table_schema = 'public' and table_name = 'ledger' and is_generated = 'NEVER' and is_identity = 'NO'
     order by ordinal_position
  loop
    c := lower(r.col);
    v := case
      when c ~ '^(from|src|source|payer)_?(kind|type)$'                              then 'citizen'
      when c ~ '^(to|dst|dest|target|payee)_?(kind|type)$'                           then 'state'
      when c ~ '^(from|src|source|payer)_?(id|owner|user|user_id|uid|citizen|ref|account)$' then v_uid::text
      when c ~ '^(from|src|source|payer)_?(name|label)$'                             then coalesce(v_name, '')
      when c ~ '^(to|dst|dest|target|payee)_?(id|ref|account|state|state_name|name|label)$' then p_state
      when c ~ '^(kind|type|action|category|txn_type|tx_type)$'                      then 'service'
      when c ~ '^(amount|value|sum|total|cash|amount_k)$'                             then p_amount::text
      when c ~ '^(state|state_name)$'                                                then p_state
      when c ~ '^(reason|note|notes|memo|description|details|detail|label|message)$' then v_reason
      when c ~ '^(owner|user_id|uid|citizen|citizen_id|actor|actor_id|by_owner|by|by_id|player|player_id)$' then v_uid::text
      when c ~ '^(name|by_name|actor_name|citizen_name|player_name)$'                then coalesce(v_name, '')
      else null end;
    if v is null then
      if r.must then
        raise exception 'pay_service cannot fill the ledger column "%" (type %). Tell the developer its name and what it holds.', r.col, r.typ;
      end if;
      continue;
    end if;
    v_cols := v_cols || case when v_cols = '' then '' else ',' end || quote_ident(r.col);
    v_vals := v_vals || case when v_vals = '' then '' else ',' end || quote_literal(v) || '::' || quote_ident(r.typ);
  end loop;
  if v_cols = '' then
    raise exception 'The ledger table has none of the expected columns.';
  end if;
  execute format('insert into ledger (%s) values (%s)', v_cols, v_vals);

  return jsonb_build_object('ok', true, 'cash', v_cash - p_amount, 'state', p_state, 'amount', p_amount);
end;
$$;

revoke all on function public.pay_service(bigint, text, text) from public;
revoke all on function public.pay_service(bigint, text, text) from anon;
grant execute on function public.pay_service(bigint, text, text) to authenticated;
