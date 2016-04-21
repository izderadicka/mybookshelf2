create extension if not exists  unaccent;
DROP TEXT SEARCH CONFIGURATION  IF EXISTS custom CASCADE;
CREATE TEXT SEARCH CONFIGURATION custom ( COPY = english );
alter text search configuration custom alter mapping for hword, hword_part, word with unaccent, english_stem;
drop index if exists full_text_search_idx;
create index  full_text_search_idx on ebook using gin(full_text);

create or replace function ebook_full_title(ebook_id bigint) returns varchar(2048) as $$ 
select coalesce(string_agg(coalesce(first_name || ' ', '')|| a.last_name, ', '), '') ||': ' || b.title || 
case when min(s.title) is not null then ' ('||min(s.title)|| ' ' || b.series_index ||')' else '' end as full_title 
from ebook b left outer join series s on b.series_id = s.id left outer join ebook_authors on ebook_authors.ebook_id = b.id  
left outer join author a on ebook_authors.author_id= a.id where b.id=$1 group by b.id $$ language sql;

-- ebook table
create or replace function update_ebook_full_text() returns trigger as $$
begin
update ebook set full_text=to_tsvector('custom', ebook_full_title(NEW.id)) where id = NEW.id;
return null;
end;
$$ language plpgsql;


drop trigger if exists ebook_ts_insert on ebook;

create trigger ebook_ts_insert after insert	
on ebook
for each row
execute procedure update_ebook_full_text();

drop trigger if exists ebook_ts_update on ebook;

create trigger ebook_ts_update after update
on ebook
for each row
when (NEW.title != OLD.title or NEW.series_id != OLD.series_id or NEW.series_id is null and OLD.series_id is not null 
	or NEW.series_id is not null and OLD.series_id is null)
execute procedure update_ebook_full_text();

-- ebook_authors table 
create or replace function update_ebook_full_text2() returns trigger as $$
declare 
ebook_id bigint;
begin
if TG_OP = 'DELETE' then
ebook_id=OLD.ebook_id;
else
ebook_id=NEW.ebook_id;
end if;
update ebook set full_text=to_tsvector('custom', ebook_full_title(ebook_id)) where id = ebook_id;
return null;
end;
$$ language plpgsql;

drop trigger if exists ebook_ts_update on ebook_authors;

create trigger ebook_ts_update after insert or update or delete
on ebook_authors
for each row
execute procedure update_ebook_full_text2();


-- series table
create or replace function update_ebook_full_text3() returns trigger as $$
declare
book_id bigint;
begin
for book_id in select id from ebook where series_id=NEW.ID loop
update ebook set full_text=to_tsvector('custom', ebook_full_title(book_id)) where id = book_id;
end loop;
return null;
end;
$$ language plpgsql;

drop trigger if exists ebook_ts_update on series;

create trigger ebook_ts_update after update
on series
for each row
execute procedure update_ebook_full_text3();

-- author table
create or replace function update_ebook_full_text4() returns trigger as $$
declare
up_id bigint;
begin

for up_id in select ebook_id from ebook_authors where author_id=NEW.ID loop
--raise notice 'Updating ebook %', up_id ;
update ebook set full_text=to_tsvector('custom', ebook_full_title(up_id)) where id = up_id;
end loop;
return null;
end;
$$ language plpgsql;

drop trigger if exists ebook_ts_update on author;

create trigger ebook_ts_update after update
on author
for each row
execute procedure update_ebook_full_text4();




