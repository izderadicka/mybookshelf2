To create test db run in psql as superuser

test=# create database ebooks_test;
CREATE DATABASE
test=# create user ebooks_test password 'ebooks';
CREATE ROLE
test=# grant all on database ebooks_test to ebooks_test;
GRANT
test=# \c ebooks_test
You are now connected to database "ebooks_test" as user "ivan".
ebooks_test=# create extension unaccent;
