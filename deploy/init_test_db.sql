create extension if not exists unaccent;

DROP TEXT SEARCH CONFIGURATION  IF EXISTS custom CASCADE;
CREATE TEXT SEARCH CONFIGURATION custom ( COPY = english );
alter text search configuration custom alter mapping for hword, hword_part, word with unaccent, english_stem;
