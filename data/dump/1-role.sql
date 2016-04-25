--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

-- Started on 2016-04-23 09:53:48 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 19351)
-- Name: role; Type: TABLE; Schema: public; Owner: ebooks
--

CREATE TABLE role (
    id bigint NOT NULL,
    version_id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE role OWNER TO ebooks;

--
-- TOC entry 184 (class 1259 OID 19349)
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: ebooks
--

CREATE SEQUENCE role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE role_id_seq OWNER TO ebooks;

--
-- TOC entry 2234 (class 0 OID 0)
-- Dependencies: 184
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ebooks
--

ALTER SEQUENCE role_id_seq OWNED BY role.id;


--
-- TOC entry 2111 (class 2604 OID 19354)
-- Name: id; Type: DEFAULT; Schema: public; Owner: ebooks
--

ALTER TABLE ONLY role ALTER COLUMN id SET DEFAULT nextval('role_id_seq'::regclass);


--
-- TOC entry 2229 (class 0 OID 19351)
-- Dependencies: 185
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: ebooks
--

COPY role (id, version_id, name) FROM stdin;
1	1	admin
\.


--
-- TOC entry 2235 (class 0 OID 0)
-- Dependencies: 184
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('role_id_seq', 1, true);


--
-- TOC entry 2113 (class 2606 OID 19356)
-- Name: role_pkey; Type: CONSTRAINT; Schema: public; Owner: ebooks
--

ALTER TABLE ONLY role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


-- Completed on 2016-04-23 09:53:48 CEST

--
-- PostgreSQL database dump complete
--

