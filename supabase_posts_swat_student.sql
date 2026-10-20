-- Delta City RP: two more government posts in gov_posts.
--
--   * Swat: a state job at the same pay level as a Sergeant; clocks in at Police Operations in their state's police building.
--   * Student: a state job with no salary; clocks in at the university's Lecture Halls.
--
-- Run the whole file once in the Supabase SQL editor. Running it again is safe (a post that already exists is left alone).
--
-- How: each new post is a copy of the Sergeant's row (so it has every column your gov_posts table has, with the same
-- scope and pay), with its title, its key and its workplace changed, and for the Student every pay column set to 0.
-- Columns the database fills in itself (an id, a serial number) are not copied. The game itself decides the room
-- where each post clocks in, from its title (docs/workplaces.md).

do $$
declare
  cols text;
  sel  text;
  c    record;
  p    record;
begin
  if to_regclass('public.gov_posts') is null then
    raise exception 'There is no gov_posts table in this database.';
  end if;
  if not exists (select 1 from gov_posts where title = 'Sergeant') then
    raise exception 'The Sergeant post is not in gov_posts, so its pay cannot be copied. Add it first.';
  end if;

  for p in select * from (values
      ('Swat',    'swat',    'place:police',     false),
      ('Student', 'student', 'place:university', true)) as t(title, key, workplace, unpaid)
  loop
    if exists (select 1 from gov_posts where title = p.title) then
      raise notice '% is already a post; left as it is', p.title;
      continue;
    end if;
    cols := ''; sel := '';
    for c in
      select column_name, data_type from information_schema.columns
       where table_schema = 'public' and table_name = 'gov_posts'
         and coalesce(column_default, '') not like 'nextval(%'
         and is_identity = 'NO' and is_generated = 'NEVER'
       order by ordinal_position
    loop
      cols := cols || case when cols = '' then '' else ', ' end || quote_ident(c.column_name);
      sel  := sel  || case when sel  = '' then '' else ', ' end ||
        case
          when c.column_name = 'title'     then quote_literal(p.title)
          when c.column_name = 'key'       then quote_literal(p.key)
          when c.column_name = 'workplace' then quote_literal(p.workplace)
          when p.unpaid and (c.column_name ~* '(pay|salary|wage)') and c.data_type in ('integer','bigint','numeric','real','double precision','smallint') then '0'
          else quote_ident(c.column_name)
        end;
    end loop;
    execute format('insert into gov_posts (%s) select %s from gov_posts where title = %L limit 1', cols, sel, 'Sergeant');
    raise notice '% added', p.title;
  end loop;
end $$;

select * from gov_posts where title in ('Sergeant', 'Swat', 'Student');
