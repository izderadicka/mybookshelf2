--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

-- Started on 2016-04-23 18:08:41 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 2264 (class 0 OID 30126)
-- Dependencies: 187
-- Data for Name: format; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO format VALUES (1, 1, 'application/pdf', 'PDF document', 'pdf');
INSERT INTO format VALUES (2, 1, 'text/plain', 'Plain text document', 'txt');
INSERT INTO format VALUES (3, 1, 'application/x-aportisdoc', 'Palm Document', 'pdb');
INSERT INTO format VALUES (4, 1, 'application/rtf', 'RTF Document', 'rtf');
INSERT INTO format VALUES (5, 1, 'application/msword', 'MS Word Document', 'doc');
INSERT INTO format VALUES (6, 1, 'application/x-mobipocket-ebook', 'Mobipocket Ebook', 'mobi');
INSERT INTO format VALUES (7, 1, 'application/vnd.palm ', 'Palm/Mobipocket Document', 'prc');
INSERT INTO format VALUES (8, 1, 'application/epub+zip', 'Open Publication Structure eBook', 'epub');
INSERT INTO format VALUES (9, 1, 'application/vnd.oasis.opendocument.text ', 'OpenOffice Document', 'odt');
INSERT INTO format VALUES (10, 1, 'image/vnd.djvu', 'DJVU Document', 'djvu');
INSERT INTO format VALUES (11, 1, 'text/html', 'HTML File', 'html');
INSERT INTO format VALUES (12, 1, 'text/html', 'HTML', 'htm');
INSERT INTO format VALUES (13, 1, 'application/octet-stream', 'Compiled HTML', 'chm');
INSERT INTO format VALUES (14, 1, 'application/x-ms-reader ', 'MS Reader Ebook', 'lit');
INSERT INTO format VALUES (15, 1, 'application/x-fictionbook+xml', 'Fiction Book 2', 'fb2');
INSERT INTO format VALUES (16, 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'MS Word XML document', 'docx');
INSERT INTO format VALUES (17, 1, 'application/x-mobi8-ebook', 'Amazon KF8 eBook File', 'azw3');


--
-- TOC entry 2274 (class 0 OID 0)
-- Dependencies: 186
-- Name: format_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('format_id_seq', 17, true);


--
-- TOC entry 2260 (class 0 OID 30093)
-- Dependencies: 183
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO genre VALUES (1, 1, 'Adventure');
INSERT INTO genre VALUES (2, 1, 'Biography');
INSERT INTO genre VALUES (3, 1, 'Business/Investing');
INSERT INTO genre VALUES (4, 1, 'Children''s Books');
INSERT INTO genre VALUES (5, 1, 'Computers/Internet');
INSERT INTO genre VALUES (6, 1, 'Cooking/Food');
INSERT INTO genre VALUES (7, 1, 'Crime/Mystery');
INSERT INTO genre VALUES (8, 1, 'Essay');
INSERT INTO genre VALUES (9, 1, 'Fantasy');
INSERT INTO genre VALUES (10, 1, 'Fiction');
INSERT INTO genre VALUES (11, 1, 'Health');
INSERT INTO genre VALUES (12, 1, 'History');
INSERT INTO genre VALUES (13, 1, 'Horror');
INSERT INTO genre VALUES (14, 1, 'Humor/Satire');
INSERT INTO genre VALUES (15, 1, 'Non-Fiction');
INSERT INTO genre VALUES (16, 1, 'Novels');
INSERT INTO genre VALUES (17, 1, 'Philosophy');
INSERT INTO genre VALUES (18, 1, 'Plays');
INSERT INTO genre VALUES (19, 1, 'Poetry');
INSERT INTO genre VALUES (20, 1, 'Politics');
INSERT INTO genre VALUES (21, 1, 'Psychology');
INSERT INTO genre VALUES (22, 1, 'Religion');
INSERT INTO genre VALUES (23, 1, 'Romance');
INSERT INTO genre VALUES (24, 1, 'Science');
INSERT INTO genre VALUES (25, 1, 'Science Fiction');
INSERT INTO genre VALUES (26, 1, 'Sexuality');
INSERT INTO genre VALUES (27, 1, 'Short Fiction');
INSERT INTO genre VALUES (28, 1, 'Sports');
INSERT INTO genre VALUES (29, 1, 'Thriller');
INSERT INTO genre VALUES (30, 1, 'Travel');
INSERT INTO genre VALUES (31, 1, 'War');
INSERT INTO genre VALUES (32, 1, 'Western');
INSERT INTO genre VALUES (34, 1, 'Educational');
INSERT INTO genre VALUES (35, 1, 'Social Fiction');
INSERT INTO genre VALUES (36, 1, 'Autobiography');
INSERT INTO genre VALUES (37, 1, 'Youth''s Books');
INSERT INTO genre VALUES (38, 1, 'Historical Fiction');
INSERT INTO genre VALUES (39, 1, 'Military');
INSERT INTO genre VALUES (40, 1, 'Hobby');
INSERT INTO genre VALUES (41, 1, 'Mysteries');
INSERT INTO genre VALUES (42, 1, 'Social Sciences');
INSERT INTO genre VALUES (43, 1, 'Espionage');
INSERT INTO genre VALUES (44, 1, 'Post-catastrophic');
INSERT INTO genre VALUES (45, 1, 'Women''s Books');
INSERT INTO genre VALUES (46, 1, 'Nature');
INSERT INTO genre VALUES (47, 1, 'Fairy Tales And Myths');
INSERT INTO genre VALUES (48, 1, 'Military SF');
INSERT INTO genre VALUES (49, 1, 'Urban fantasy');
INSERT INTO genre VALUES (50, 1, 'Comics');
INSERT INTO genre VALUES (51, 1, 'Space Opera');
INSERT INTO genre VALUES (52, 1, 'Magazine');
INSERT INTO genre VALUES (53, 1, 'Action');
INSERT INTO genre VALUES (54, 1, 'Psychological Fiction');
INSERT INTO genre VALUES (55, 1, 'Art');
INSERT INTO genre VALUES (56, 1, 'Mystic');
INSERT INTO genre VALUES (57, 1, 'Alternative');
INSERT INTO genre VALUES (58, 1, 'Technology');


--
-- TOC entry 2275 (class 0 OID 0)
-- Dependencies: 182
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('genre_id_seq', 58, true);


--
-- TOC entry 2268 (class 0 OID 30144)
-- Dependencies: 191
-- Data for Name: language; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO language VALUES (1, 1, 'cs', 'Czech');
INSERT INTO language VALUES (2, 1, 'en', 'English');
INSERT INTO language VALUES (3, 1, 'sk', 'Slovak');
INSERT INTO language VALUES (4, 1, 'ru', 'Russian');


--
-- TOC entry 2276 (class 0 OID 0)
-- Dependencies: 190
-- Name: language_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('language_id_seq', 4, true);


--
-- TOC entry 2266 (class 0 OID 30136)
-- Dependencies: 189
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO role VALUES (1, 1, 'guest', NULL);
INSERT INTO role VALUES (2, 1, 'user', 1);
INSERT INTO role VALUES (3, 1, 'trusted_user', 2);
INSERT INTO role VALUES (4, 1, 'superuser', 3);
INSERT INTO role VALUES (5, 1, 'admin', 4);


--
-- TOC entry 2277 (class 0 OID 0)
-- Dependencies: 188
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('role_id_seq', 5, true);


--
-- TOC entry 2262 (class 0 OID 30103)
-- Dependencies: 185
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO "user" VALUES (1, 1, '2016-04-23 17:44:16.963802', '2016-04-23 17:44:16.963095', 'admin', 'admin@example.com', '$2b$12$kaFp6Wv8kpzOfSV7.yScz.Es.0cv7OS/QqDWk8mTYdc51VzJ5kpyG', true, NULL, NULL);


--
-- TOC entry 2278 (class 0 OID 0)
-- Dependencies: 184
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('user_id_seq', 1, true);


--
-- TOC entry 2269 (class 0 OID 30244)
-- Dependencies: 200
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO user_roles VALUES (1, 5);

--
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('LNG', 'eng', 'en', 1);
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('LNG', 'ces', 'cs', 1);
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('LNG', 'slk', 'sk', 1);
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('GNR', 'Sci-Fi', 'Science Fiction', 1);
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('GNR', 'Humor', 'Humor/Satire', 1);
INSERT INTO synonym (category, other_name, our_name, version_id) VALUES ('GNR', 'Satire', 'Humor/Satire', 1);


-- Completed on 2016-04-23 18:08:41 CEST

--
-- PostgreSQL database dump complete
--

