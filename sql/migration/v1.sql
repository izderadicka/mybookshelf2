
CREATE SEQUENCE bookshelf_rating_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE ebook_rating_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE series_rating_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE source_quality_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE version_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE TABLE bookshelf_rating (
	id bigint DEFAULT nextval('bookshelf_rating_id_seq'::regclass) NOT NULL,
	version_id integer NOT NULL,
	created timestamp without time zone NOT NULL,
	modified timestamp without time zone NOT NULL,
	bookshelf_id bigint NOT NULL,
	rating double precision,
	description text,
	modified_by_id bigint,
	created_by_id bigint
);

CREATE TABLE ebook_rating (
	id bigint DEFAULT nextval('ebook_rating_id_seq'::regclass) NOT NULL,
	version_id integer NOT NULL,
	created timestamp without time zone NOT NULL,
	modified timestamp without time zone NOT NULL,
	ebook_id bigint NOT NULL,
	rating double precision,
	description text,
	modified_by_id bigint,
	created_by_id bigint
);

CREATE TABLE series_rating (
	id bigint DEFAULT nextval('series_rating_id_seq'::regclass) NOT NULL,
	version_id integer NOT NULL,
	created timestamp without time zone NOT NULL,
	modified timestamp without time zone NOT NULL,
	series_id bigint NOT NULL,
	rating double precision,
	description text,
	modified_by_id bigint,
	created_by_id bigint
);

CREATE TABLE source_quality (
	id bigint DEFAULT nextval('source_quality_id_seq'::regclass) NOT NULL,
	version_id integer NOT NULL,
	created timestamp without time zone NOT NULL,
	modified timestamp without time zone NOT NULL,
	source_id bigint NOT NULL,
	quality double precision,
	description text,
	modified_by_id bigint,
	created_by_id bigint
);

CREATE TABLE version (
	id bigint DEFAULT nextval('version_id_seq'::regclass) NOT NULL,
	version_id integer NOT NULL,
	version integer
);

ALTER TABLE bookshelf
	ADD COLUMN rating_count integer,
	ALTER COLUMN description TYPE text /* TYPE change - table: bookshelf original: character varying new: text */;

ALTER TABLE conversion_batch
	ADD COLUMN zip_location character varying(512);

ALTER TABLE ebook
	ADD COLUMN rating_count integer,
	ADD COLUMN downloads integer;

ALTER TABLE series
	ADD COLUMN rating_count integer;

ALTER TABLE source
	ADD COLUMN quality_count integer;

ALTER SEQUENCE bookshelf_rating_id_seq
	OWNED BY bookshelf_rating.id;

ALTER SEQUENCE ebook_rating_id_seq
	OWNED BY ebook_rating.id;

ALTER SEQUENCE series_rating_id_seq
	OWNED BY series_rating.id;

ALTER SEQUENCE source_quality_id_seq
	OWNED BY source_quality.id;

ALTER SEQUENCE version_id_seq
	OWNED BY version.id;

ALTER TABLE bookshelf_rating
	ADD CONSTRAINT bookshelf_rating_pkey PRIMARY KEY (id);

ALTER TABLE ebook_rating
	ADD CONSTRAINT ebook_rating_pkey PRIMARY KEY (id);

ALTER TABLE series_rating
	ADD CONSTRAINT series_rating_pkey PRIMARY KEY (id);

ALTER TABLE source_quality
	ADD CONSTRAINT source_quality_pkey PRIMARY KEY (id);

ALTER TABLE version
	ADD CONSTRAINT version_pkey PRIMARY KEY (id);

ALTER TABLE bookshelf_rating
	ADD CONSTRAINT bookshelf_rating_bookshelf_id_fkey FOREIGN KEY (bookshelf_id) REFERENCES bookshelf(id);

ALTER TABLE bookshelf_rating
	ADD CONSTRAINT bookshelf_rating_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES "user"(id);

ALTER TABLE bookshelf_rating
	ADD CONSTRAINT bookshelf_rating_modified_by_id_fkey FOREIGN KEY (modified_by_id) REFERENCES "user"(id);

ALTER TABLE ebook_rating
	ADD CONSTRAINT ebook_rating_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES "user"(id);

ALTER TABLE ebook_rating
	ADD CONSTRAINT ebook_rating_ebook_id_fkey FOREIGN KEY (ebook_id) REFERENCES ebook(id);

ALTER TABLE ebook_rating
	ADD CONSTRAINT ebook_rating_modified_by_id_fkey FOREIGN KEY (modified_by_id) REFERENCES "user"(id);

ALTER TABLE series_rating
	ADD CONSTRAINT series_rating_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES "user"(id);

ALTER TABLE series_rating
	ADD CONSTRAINT series_rating_modified_by_id_fkey FOREIGN KEY (modified_by_id) REFERENCES "user"(id);

ALTER TABLE series_rating
	ADD CONSTRAINT series_rating_series_id_fkey FOREIGN KEY (series_id) REFERENCES series(id);

ALTER TABLE source_quality
	ADD CONSTRAINT source_quality_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES "user"(id);

ALTER TABLE source_quality
	ADD CONSTRAINT source_quality_modified_by_id_fkey FOREIGN KEY (modified_by_id) REFERENCES "user"(id);

ALTER TABLE source_quality
	ADD CONSTRAINT source_quality_source_id_fkey FOREIGN KEY (source_id) REFERENCES source(id);

CREATE INDEX ix_bookshelf_rating_modified ON bookshelf_rating USING btree (modified);

CREATE INDEX ix_ebook_rating_modified ON ebook_rating USING btree (modified);

CREATE INDEX ix_series_rating_modified ON series_rating USING btree (modified);

CREATE INDEX ix_source_quality_modified ON source_quality USING btree (modified);

insert into version (version, version_id) values (1,1);
