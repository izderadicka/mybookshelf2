
create or replace function user_roles(user_id bigint) returns table(role varchar) as $$
with recursive all_roles as (
select name, parent_id from role where id in (select role_id from user_roles where user_id=$1)
union 
select p.name, p.parent_id from role p
	join all_roles a on (p.id = a.parent_id) 
)
select name from all_roles 
$$ language SQL;


create or replace function user_has_roles(user_id bigint, roles varchar[]) returns int as $$
select 1 from user_roles($1) where role = ANY ( roles );
$$ language SQL;