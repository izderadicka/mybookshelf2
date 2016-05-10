--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

-- Started on 2016-04-24 07:16:01 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 2269 (class 0 OID 31282)
-- Dependencies: 193
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO author VALUES (4920, 1, '2010-07-25 11:35:49', '2010-07-25 11:35:49', 'Bialolecka', 'Ewa', NULL, 1, 1);
INSERT INTO author VALUES (4924, 1, '2010-07-25 11:35:52', '2010-07-25 11:35:52', 'Birdman', 'Shigor', NULL, 1, 1);
INSERT INTO author VALUES (4938, 1, '2010-07-25 11:36:11', '2012-08-03 13:12:39', 'Borovička', 'Václav Pavel', NULL, 1, 1);
INSERT INTO author VALUES (5012, 1, '2010-07-25 11:39:39', '2010-07-25 11:39:39', 'Crichton', 'Michael', NULL, 1, 1);
INSERT INTO author VALUES (5048, 1, '2010-07-25 11:41:09', '2012-07-03 07:43:20', 'Eddings', 'David Carroll', NULL, 1, 1);
INSERT INTO author VALUES (5103, 1, '2010-07-25 11:44:57', '2010-07-25 11:44:57', 'Gemmell', 'David', NULL, 1, 1);
INSERT INTO author VALUES (5133, 1, '2010-07-25 11:46:46', '2012-07-03 07:41:34', 'Hamilton', 'Laurell Kaye', NULL, 1, 1);
INSERT INTO author VALUES (5155, 1, '2010-07-25 11:48:51', '2012-07-03 07:49:59', 'Hendee', 'John Clare', NULL, 1, 1);
INSERT INTO author VALUES (5185, 1, '2010-07-25 11:50:11', '2010-07-25 11:50:11', 'James', 'Peter', NULL, 1, 1);
INSERT INTO author VALUES (5222, 1, '2010-07-25 11:51:34', '2012-07-03 07:40:18', 'King', 'Stephen Edwin', NULL, 1, 1);
INSERT INTO author VALUES (5271, 1, '2010-07-25 11:53:48', '2010-07-25 11:53:48', 'Lumley', 'Brian', NULL, 1, 1);
INSERT INTO author VALUES (5277, 1, '2010-07-25 11:53:54', '2010-07-25 11:53:54', 'Macek', 'Petr', NULL, 1, 1);
INSERT INTO author VALUES (5340, 1, '2010-07-25 11:57:42', '2010-07-25 11:57:42', 'Novik', 'Naomi', NULL, 1, 1);
INSERT INTO author VALUES (5355, 1, '2010-07-25 11:58:01', '2012-08-03 13:13:09', 'Pecinovský', 'Josef', NULL, 1, 1);
INSERT INTO author VALUES (5454, 1, '2010-07-25 12:02:52', '2012-08-03 13:13:04', 'Šlechta', 'Vladimír', NULL, 1, 1);
INSERT INTO author VALUES (5465, 1, '2010-07-25 12:03:15', '2010-07-25 12:03:15', 'Star', 'Trek', NULL, 1, 1);
INSERT INTO author VALUES (5479, 1, '2010-07-25 12:03:46', '2012-08-03 13:12:43', 'Štorch', 'Eduard', NULL, 1, 1);
INSERT INTO author VALUES (5506, 1, '2010-07-25 12:05:05', '2010-07-25 12:05:05', 'Troska', 'Jan Matzal', NULL, 1, 1);
INSERT INTO author VALUES (5521, 1, '2010-07-25 12:05:47', '2010-07-25 12:05:47', 'Verne', 'Jules', NULL, 1, 1);
INSERT INTO author VALUES (5540, 1, '2010-07-25 12:06:47', '2010-07-25 12:06:47', 'Walker', 'Hugh', NULL, 1, 1);
INSERT INTO author VALUES (5556, 1, '2010-07-25 12:07:14', '2012-10-14 10:30:18', 'Wells', 'H. G.', NULL, 1, 1);
INSERT INTO author VALUES (5591, 1, '2010-10-22 16:10:27', '2012-07-03 07:38:17', 'Anderson', 'Kevin J.', NULL, 1, 1);
INSERT INTO author VALUES (5666, 1, '2010-10-22 16:11:46', '2010-10-22 16:11:46', 'Kuttner', 'Henry', NULL, 1, 1);
INSERT INTO author VALUES (5669, 1, '2010-10-22 16:11:51', '2010-10-22 16:11:51', 'Le Guin', 'Ursula Kroeber', NULL, 1, 1);
INSERT INTO author VALUES (5696, 1, '2010-10-22 16:12:50', '2010-10-22 16:12:50', 'Staheff', 'Christopher', NULL, 1, 1);
INSERT INTO author VALUES (5798, 1, '2012-07-03 07:38:38', '2012-07-03 07:38:38', 'May', 'Karl', NULL, 1, 1);
INSERT INTO author VALUES (5912, 1, '2012-07-03 07:39:48', '2012-07-03 07:39:48', 'Šimáček', 'Radovan', NULL, 1, 1);
INSERT INTO author VALUES (5998, 1, '2012-07-03 07:41:17', '2012-08-03 13:12:50', 'Vondruška', 'Vlastimil', NULL, 1, 1);
INSERT INTO author VALUES (6164, 1, '2012-07-03 07:43:36', '2012-07-03 07:43:36', 'Erskine', 'Barbara', NULL, 1, 1);
INSERT INTO author VALUES (6188, 1, '2012-07-03 07:44:20', '2012-07-03 07:44:20', 'Kovanic', 'Jan', NULL, 1, 1);
INSERT INTO author VALUES (6195, 1, '2012-07-03 07:44:24', '2012-08-03 13:15:46', 'Lanczová', 'Lenka', NULL, 1, 1);
INSERT INTO author VALUES (6212, 1, '2012-07-03 07:44:48', '2012-07-03 07:44:48', 'Monroe', 'Lucy', NULL, 1, 1);
INSERT INTO author VALUES (6282, 1, '2012-07-03 07:46:29', '2012-07-03 07:46:29', 'Cordonnier', 'Marie', NULL, 1, 1);
INSERT INTO author VALUES (6432, 1, '2012-07-03 07:48:36', '2012-09-01 15:38:58', 'Strugackij', 'Arkadij Natanovič', NULL, 1, 1);
INSERT INTO author VALUES (6433, 1, '2012-07-03 07:48:36', '2012-09-01 15:38:58', 'Strugackij', 'Boris Natanovič', NULL, 1, 1);
INSERT INTO author VALUES (6489, 1, '2012-07-03 07:49:59', '2012-07-03 07:49:59', 'Hendee', 'Barb', NULL, 1, 1);
INSERT INTO author VALUES (6526, 1, '2012-07-03 07:50:45', '2012-07-03 07:50:45', 'Cartland', 'Barbara', NULL, 1, 1);
INSERT INTO author VALUES (6598, 1, '2012-07-03 07:52:27', '2012-07-03 07:52:27', 'Hall', 'Robert Lee', NULL, 1, 1);
INSERT INTO author VALUES (6700, 1, '2012-07-03 07:54:17', '2012-07-03 07:54:17', 'Varšavskij', 'Ilja Iosifovič', NULL, 1, 1);
INSERT INTO author VALUES (6772, 1, '2012-07-03 07:55:52', '2012-07-03 07:55:52', 'Nienacki', 'Zbigniew', NULL, 1, 1);
INSERT INTO author VALUES (6837, 1, '2012-07-03 07:56:44', '2012-07-03 07:56:44', 'Druon', 'Maurice', NULL, 1, 1);
INSERT INTO author VALUES (6839, 1, '2012-07-03 07:56:46', '2012-07-03 07:56:46', 'Lenormand', 'Frédéric', NULL, 1, 1);
INSERT INTO author VALUES (6918, 1, '2012-07-03 07:58:11', '2012-07-03 07:58:11', 'Benchley', 'Peter', NULL, 1, 1);
INSERT INTO author VALUES (6980, 1, '2012-07-03 07:59:20', '2012-07-03 07:59:20', 'Hand', 'Elizabeth', NULL, 1, 1);
INSERT INTO author VALUES (7046, 1, '2012-07-03 08:00:48', '2012-07-03 08:00:48', 'Peters', 'Ellis', NULL, 1, 1);
INSERT INTO author VALUES (7072, 1, '2012-07-03 08:01:25', '2012-08-03 13:16:19', 'Rudiš', 'Jaroslav', NULL, 1, 1);
INSERT INTO author VALUES (7106, 1, '2012-07-03 08:02:12', '2012-07-03 08:02:12', 'Ubieto Arteta', 'Antonio', NULL, 1, 1);
INSERT INTO author VALUES (7296, 1, '2012-07-03 08:04:51', '2012-07-03 08:04:51', 'Leclaire', 'Day', NULL, 1, 1);
INSERT INTO author VALUES (7297, 1, '2012-07-03 08:04:54', '2012-07-03 08:04:54', 'Ruiz', 'Don Miguel', NULL, 1, 1);
INSERT INTO author VALUES (7319, 1, '2012-07-03 08:05:24', '2012-07-03 08:05:24', 'Neff', 'Vladimír', NULL, 1, 1);
INSERT INTO author VALUES (7410, 1, '2012-07-03 08:07:37', '2012-07-03 08:07:37', 'Wilkins', 'Gina', NULL, 1, 1);
INSERT INTO author VALUES (7417, 1, '2012-07-03 08:07:44', '2012-07-03 08:07:44', 'James', 'Ellen', NULL, 1, 1);
INSERT INTO author VALUES (7438, 1, '2012-07-03 08:08:04', '2012-07-03 08:08:04', 'Barton', 'Beverly', NULL, 1, 1);
INSERT INTO author VALUES (7444, 1, '2012-07-03 08:08:05', '2012-07-03 08:08:05', 'Dalton', 'Margot', NULL, 1, 1);
INSERT INTO author VALUES (7445, 1, '2012-07-03 08:08:05', '2012-07-03 08:08:05', 'Young', 'Karen', NULL, 1, 1);
INSERT INTO author VALUES (7472, 1, '2012-07-03 08:08:26', '2012-07-03 08:08:26', 'Orwig', 'Sara', NULL, 1, 1);
INSERT INTO author VALUES (7486, 1, '2012-07-03 08:08:38', '2012-07-03 08:08:38', 'Neels', 'Betty', NULL, 1, 1);
INSERT INTO author VALUES (7598, 1, '2012-07-03 08:10:11', '2012-07-03 08:10:11', 'Bacigalupi', 'Paolo', NULL, 1, 1);
INSERT INTO author VALUES (7620, 1, '2012-07-03 08:10:43', '2012-07-03 08:10:43', 'Allen', 'Louise', NULL, 1, 1);
INSERT INTO author VALUES (7643, 1, '2012-07-03 08:11:03', '2012-07-03 08:11:03', 'Kaku', 'Michio', NULL, 1, 1);
INSERT INTO author VALUES (7698, 1, '2012-07-03 08:11:46', '2012-07-03 08:11:46', 'McEwan', 'Ian', NULL, 1, 1);
INSERT INTO author VALUES (7732, 1, '2012-07-03 08:12:40', '2012-07-03 08:12:40', 'Karásek ze Lvovic', 'Jiří', NULL, 1, 1);
INSERT INTO author VALUES (7738, 1, '2012-07-03 08:12:46', '2012-07-03 08:12:46', 'Brittain', 'William', NULL, 1, 1);
INSERT INTO author VALUES (7939, 1, '2012-07-03 08:15:29', '2012-07-03 08:15:29', 'Gordon', 'Victoria', NULL, 1, 1);
INSERT INTO author VALUES (8015, 1, '2012-07-03 08:17:01', '2012-07-03 08:17:01', 'Dark', 'Jason', NULL, 1, 1);
INSERT INTO author VALUES (8185, 1, '2012-07-03 08:20:36', '2012-07-03 08:20:36', 'Adrian', 'Lara', NULL, 1, 1);
INSERT INTO author VALUES (8186, 1, '2012-07-03 08:20:39', '2012-07-03 08:20:39', 'Mills', 'Kyle', NULL, 1, 1);
INSERT INTO author VALUES (8636, 1, '2012-07-03 08:30:16', '2012-08-03 13:13:05', 'Ježek', 'Jan', NULL, 1, 1);
INSERT INTO author VALUES (8949, 1, '2012-07-03 08:35:58', '2012-07-03 08:35:58', 'Repka', 'Marian', NULL, 1, 1);
INSERT INTO author VALUES (9148, 1, '2012-07-03 08:40:11', '2012-07-03 08:40:11', 'Giffin', 'Emily', NULL, 1, 1);
INSERT INTO author VALUES (9160, 1, '2012-07-03 08:40:26', '2012-07-03 08:40:26', 'Frankl', 'Viktor', NULL, 1, 1);
INSERT INTO author VALUES (9281, 1, '2012-07-03 08:42:57', '2012-07-03 08:42:57', 'Gill', 'Judy', NULL, 1, 1);
INSERT INTO author VALUES (9394, 1, '2012-07-03 08:45:30', '2012-07-03 08:45:30', 'Gibson', 'Walter B.', NULL, 1, 1);
INSERT INTO author VALUES (9513, 1, '2012-07-03 08:47:45', '2012-07-03 08:47:45', 'Mandulová', 'Kateřina', NULL, 1, 1);
INSERT INTO author VALUES (9615, 1, '2012-07-03 08:50:00', '2012-07-03 08:50:00', 'Valentine', 'Zena', NULL, 1, 1);
INSERT INTO author VALUES (9616, 1, '2012-07-03 08:50:01', '2012-07-03 08:50:01', 'Pludra', 'Benno', NULL, 1, 1);
INSERT INTO author VALUES (9661, 1, '2012-07-03 08:51:03', '2012-07-03 08:51:03', 'Sharpe', 'Tom', NULL, 1, 1);
INSERT INTO author VALUES (9681, 1, '2012-07-03 08:51:33', '2012-08-03 13:16:10', 'Štych', 'Jiří', NULL, 1, 1);
INSERT INTO author VALUES (9789, 1, '2012-08-03 13:14:34', '2012-08-03 13:14:34', 'Sullivan', 'Maxine', NULL, 1, 1);
INSERT INTO author VALUES (9810, 1, '2012-08-03 13:14:51', '2012-08-03 13:14:51', 'Franz', 'Raymond', NULL, 1, 1);
INSERT INTO author VALUES (9948, 1, '2012-08-03 13:17:07', '2012-08-03 13:17:07', 'Adornetto', 'Alexandra', NULL, 1, 1);
INSERT INTO author VALUES (9949, 1, '2012-08-03 13:17:09', '2012-08-03 13:17:09', 'Evarts', 'Hal George', NULL, 1, 1);
INSERT INTO author VALUES (10062, 1, '2012-08-03 13:19:26', '2012-08-03 13:19:26', 'Andrlík', 'František Josef', NULL, 1, 1);
INSERT INTO author VALUES (10195, 1, '2012-08-20 11:33:37', '2012-08-20 11:33:37', 'Selinko', 'Annemarie', NULL, 1, 1);
INSERT INTO author VALUES (10203, 1, '2012-08-20 11:33:56', '2012-08-20 11:33:56', 'Kellerman', 'Jonathan', NULL, 1, 1);
INSERT INTO author VALUES (10297, 1, '2012-09-27 10:34:34', '2012-09-27 10:34:34', 'Lindsay', 'Yvonne', NULL, 1, 1);
INSERT INTO author VALUES (10356, 1, '2012-10-05 18:36:55', '2012-10-05 18:36:55', 'Tenkrat', 'Friedrich', NULL, 1, 1);
INSERT INTO author VALUES (10420, 1, '2012-10-14 10:30:07', '2012-10-14 10:30:07', 'Eugenides', 'Jeffrey', NULL, 1, 1);
INSERT INTO author VALUES (10964, 1, '2013-02-22 07:36:42', '2013-02-22 07:36:42', 'Čáka', 'Jan', NULL, 1, 1);
INSERT INTO author VALUES (11098, 1, '2013-03-16 11:47:07', '2013-03-16 11:47:07', 'Hofman', 'Vladimír', NULL, 1, 1);
INSERT INTO author VALUES (11152, 1, '2013-03-16 11:47:38', '2013-03-16 11:47:38', 'Tepes', 'Vlad', NULL, 1, 1);
INSERT INTO author VALUES (11184, 1, '2013-03-29 08:14:24', '2013-03-29 08:14:24', 'Gilmore', 'Robert', NULL, 1, 1);
INSERT INTO author VALUES (11205, 1, '2013-03-29 08:14:34', '2013-03-29 08:14:34', 'Stanek', 'William R.', NULL, 1, 1);
INSERT INTO author VALUES (11465, 1, '2013-05-04 07:33:42', '2013-05-04 07:33:42', 'Hartley', 'Andrew James', NULL, 1, 1);
INSERT INTO author VALUES (11591, 1, '2013-05-31 08:16:27', '2013-05-31 08:16:27', 'Albieri', 'Pavel', NULL, 1, 1);
INSERT INTO author VALUES (12016, 1, '2013-10-04 09:22:58', '2013-10-04 09:22:58', 'Brown', 'Graham', NULL, 1, 1);
INSERT INTO author VALUES (12188, 1, '2013-11-04 20:48:41', '2013-11-04 20:48:41', 'Sásková', 'Lucia', NULL, 1, 1);
INSERT INTO author VALUES (12673, 1, '2014-04-13 11:00:56', '2014-04-13 11:00:56', 'Kissinger', 'Henry', NULL, 1, 1);
INSERT INTO author VALUES (12885, 1, '2014-07-19 14:58:22', '2014-07-19 14:58:22', 'Taylor', 'David', NULL, 1, 1);
INSERT INTO author VALUES (12949, 1, '2014-08-31 18:28:14', '2014-08-31 18:28:14', 'Hodkin', 'Michelle', NULL, 1, 1);
INSERT INTO author VALUES (12982, 1, '2014-08-31 18:29:20', '2014-08-31 18:29:20', 'Tibitanzl', 'Jiří', NULL, 1, 1);
INSERT INTO author VALUES (13922, 1, '2015-08-30 11:14:43', '2015-08-30 11:14:43', 'Hallenga', 'Uwe', NULL, 1, 1);


--
-- TOC entry 2282 (class 0 OID 0)
-- Dependencies: 192
-- Name: author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('author_id_seq', 14545, true);


--
-- TOC entry 2271 (class 0 OID 31304)
-- Dependencies: 195
-- Data for Name: series; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO series VALUES (6, 1, '2010-09-18 21:34:25', '2010-10-01 16:30:57', 'Anita Blaková', NULL, NULL, 1, 1);
INSERT INTO series VALUES (176, 1, '2012-07-03 07:41:17', '2012-07-03 07:41:17', 'Letopisy královské komory', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1556, 1, '2012-07-26 21:43:15', '2012-07-26 21:43:15', 'Zápas s nebem', NULL, NULL, 1, 1);
INSERT INTO series VALUES (305, 1, '2012-07-03 07:44:08', '2012-07-03 07:44:08', 'Příběhy Sherlocka Holmese (Jota)', NULL, NULL, 1, 1);
INSERT INTO series VALUES (331, 1, '2012-07-03 07:45:02', '2012-07-03 07:45:02', 'Drenajská sága', NULL, NULL, 1, 1);
INSERT INTO series VALUES (332, 1, '2012-07-03 07:45:03', '2012-07-03 07:45:03', 'Krvavé pohraničí - Gordonova země', NULL, NULL, 1, 1);
INSERT INTO series VALUES (511, 1, '2012-07-03 07:49:59', '2012-07-03 07:49:59', 'Vznešení mrtví I', NULL, NULL, 1, 1);
INSERT INTO series VALUES (587, 1, '2012-07-03 07:52:03', '2012-07-03 07:52:03', 'Nekroskop', NULL, NULL, 1, 1);
INSERT INTO series VALUES (716, 1, '2012-07-03 07:55:52', '2012-07-03 07:55:52', 'Pán Tragáčik', NULL, NULL, 1, 1);
INSERT INTO series VALUES (739, 1, '2012-07-03 07:56:46', '2012-07-03 07:56:46', 'Nové případy soudce Ti', NULL, NULL, 1, 1);
INSERT INTO series VALUES (800, 1, '2012-07-03 07:58:44', '2012-07-03 07:58:44', 'Star Wars BBY', NULL, NULL, 1, 1);
INSERT INTO series VALUES (838, 1, '2012-07-03 08:00:48', '2012-07-03 08:00:48', 'Případy bratra Cadfaela', NULL, NULL, 1, 1);
INSERT INTO series VALUES (989, 1, '2012-07-03 08:09:41', '2012-07-03 08:09:41', 'Akta X', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1034, 1, '2012-07-03 08:12:40', '2012-07-03 08:12:40', 'Romány tří mágů', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1174, 1, '2012-07-03 08:20:36', '2012-07-03 08:20:36', 'Půlnoční rasa', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1203, 1, '2012-07-03 08:22:26', '2012-07-03 08:22:26', 'Thorsen Brothers', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1333, 1, '2012-07-03 08:33:40', '2012-07-03 08:33:40', 'Nevěsty od Středozemního moře', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1383, 1, '2012-07-03 08:37:39', '2012-07-03 08:37:39', 'Odstupné za lásku', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1474, 1, '2012-07-03 08:45:04', '2012-07-03 08:45:04', 'Tajemství starého rodu', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1488, 1, '2012-07-03 08:46:39', '2012-07-03 08:46:39', 'Roy Grace', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1534, 1, '2012-07-03 08:50:08', '2012-07-03 08:50:08', 'Kroniky nové Země', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1548, 1, '2012-07-03 08:51:03', '2012-07-03 08:51:03', 'Henry Wilt', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1609, 1, '2012-08-03 13:17:07', '2012-08-03 13:17:07', 'Zář', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1614, 1, '2012-08-03 13:17:43', '2012-08-03 13:17:43', 'Magira', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1633, 1, '2012-08-03 13:18:43', '2012-08-03 13:18:43', 'Na stopě hrůzy', NULL, NULL, 1, 1);
INSERT INTO series VALUES (1674, 1, '2012-09-01 15:38:59', '2012-09-01 15:38:59', 'Alex Delaware', NULL, NULL, 1, 1);
INSERT INTO series VALUES (2048, 1, '2013-10-04 09:22:58', '2013-10-04 09:22:58', 'Danielle Laidlawová', NULL, NULL, 1, 1);
INSERT INTO series VALUES (2301, 1, '2014-08-31 18:28:14', '2014-08-31 18:28:14', 'Mara Dyer', NULL, NULL, 1, 1);


--
-- TOC entry 2273 (class 0 OID 31391)
-- Dependencies: 202
-- Data for Name: ebook; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO ebook VALUES (33258, 1, '2010-07-25 11:35:49', '2010-07-25 11:35:49', 'Tkac iluzi', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (33344, 1, '2010-07-25 11:36:14', '2012-07-03 08:23:03', 'Záhadné policejní případy', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (33837, 1, '2010-07-25 11:39:51', '2012-07-03 07:48:55', 'Let číslo TPA 545', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (34087, 1, '2010-07-25 11:41:21', '2010-07-25 11:41:21', 'Malloreon 1 - Strazci Zapadu', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (34513, 1, '2010-07-25 11:44:59', '2012-07-03 08:15:13', 'Legenda', NULL, 1, 331, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (55325, 1, '2012-12-22 08:22:46', '2012-12-22 08:22:46', 'Letopisy královské komory I.', '', 1, 176, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56396, 1, '2013-02-22 07:36:42', '2013-02-22 07:36:42', 'Střední Brdy - krajina neznámá', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (35341, 1, '2010-07-25 11:51:44', '2010-07-25 11:51:44', 'Odvykaci a s', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (35485, 1, '2010-07-25 11:52:43', '2010-10-25 22:04:06', 'Prokleté město', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (35515, 1, '2010-07-25 11:52:51', '2010-10-25 22:05:20', 'Svet je les les je svet', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (35671, 1, '2010-07-25 11:53:54', '2010-07-25 11:53:54', 'StarTrek Nova Generace - Zrcadla', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (36214, 1, '2010-07-25 11:57:42', '2010-07-25 11:57:42', 'Temeraire 2 - Nefritovy trun', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (36253, 1, '2010-07-25 11:58:01', '2010-07-25 11:58:01', 'Kupte si svět', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (64726, 1, '2015-03-19 17:50:05', '2015-03-19 17:50:05', 'Smrt čínského kuchaře', NULL, 1, 739, 6, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (37038, 1, '2010-07-25 12:03:18', '2010-07-25 12:03:18', 'Gene DeWeese - Strážci míru', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (37116, 1, '2010-07-25 12:03:46', '2010-07-25 12:03:46', 'Bronzovy poklad', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (37157, 1, '2010-07-25 12:03:59', '2012-08-21 08:23:27', 'Noc na Marse', '', 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (37867, 1, '2010-10-22 16:10:34', '2010-10-22 16:10:34', 'Po druhy do stejny reky', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (38921, 1, '2010-10-22 16:12:50', '2010-10-22 16:12:50', 'Carodej 05 - Carodej rozzureny', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (39072, 1, '2010-10-22 16:13:09', '2012-07-03 08:23:27', 'Válka světů a jiné příběhy z neskutečna', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (40773, 1, '2012-07-03 07:45:03', '2012-07-03 07:45:03', 'Ploty z kostí', NULL, 1, 332, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (41749, 1, '2012-07-03 07:50:20', '2012-07-03 07:50:21', 'Zrádce krve', NULL, 1, 511, 4, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (42163, 1, '2012-07-03 07:52:27', '2012-07-03 07:52:28', 'Sherlock Holmes odchází', NULL, 1, 305, 14, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (42314, 1, '2012-07-03 07:53:06', '2012-07-03 07:53:06', 'Děti kapitána Granta 1. díl', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (42537, 1, '2012-07-03 07:54:17', '2012-07-03 07:54:17', 'Experiment', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43023, 1, '2012-07-03 07:56:34', '2012-07-03 08:30:46', 'Pán Tragáčik a Kapitán Nemo', NULL, 3, 716, 7, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43529, 1, '2012-07-03 07:59:20', '2012-07-03 07:59:20', 'Boba Fett 3: Labyrint klamu', NULL, 1, 800, 22, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43662, 1, '2012-07-03 08:00:10', '2012-07-03 08:00:10', 'Úkryt před světlem', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43908, 1, '2012-07-03 08:01:57', '2012-07-03 08:16:15', 'Zločin na Zlenicích hradě L.P. 1318', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43933, 1, '2012-07-03 08:02:12', '2012-07-03 08:02:12', 'Dějiny Španělska', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (43992, 1, '2012-07-03 08:02:32', '2012-07-03 08:02:32', 'Prznitelé', NULL, 1, 587, 12, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (45202, 1, '2012-07-03 08:09:43', '2012-07-03 08:31:41', 'Protilátky', NULL, 1, 989, 5, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (45446, 1, '2012-07-03 08:11:20', '2012-07-03 08:11:20', 'Milenky a hříšníci', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (45643, 1, '2012-07-03 08:12:40', '2012-07-03 08:12:40', 'Ganymedes', NULL, 1, 1034, 3, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (45668, 1, '2012-07-03 08:12:47', '2012-09-02 18:13:27', 'Päť litrov benzínu', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (46064, 1, '2012-07-03 08:15:29', '2012-07-03 08:15:29', 'Láska a zákon', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (46818, 1, '2012-07-03 08:20:36', '2012-07-03 08:36:53', 'Polibek půlnoci', NULL, 1, 1174, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (47602, 1, '2012-07-03 08:26:44', '2012-07-03 08:27:07', 'Konec punku v Helsinkách', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (48552, 1, '2012-07-03 08:32:10', '2012-07-03 08:32:10', 'Štyri dohody', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (48728, 1, '2012-07-03 08:32:58', '2012-07-03 08:32:58', 'Láska k nepříteli', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (48818, 1, '2012-07-03 08:33:40', '2012-07-03 08:33:40', 'Španělova milenka', NULL, 1, 1333, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (49134, 1, '2012-07-03 08:35:58', '2012-07-03 08:35:59', 'Fenomén múdrosť', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (49138, 1, '2012-07-03 08:36:00', '2012-08-03 13:13:24', 'Malomocný u svatého Jiljí', NULL, 1, 838, 5, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (49667, 1, '2012-07-03 08:40:12', '2012-07-03 08:40:12', 'Something Borrowed', NULL, 2, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50118, 1, '2012-07-03 08:42:57', '2012-07-03 08:42:57', 'Něžný dobyvatel', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50495, 1, '2012-07-03 08:45:30', '2012-07-03 08:45:30', 'Úplná příručka triků a kouzel pro začátečníky', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50556, 1, '2012-07-03 08:45:46', '2012-07-03 08:45:46', 'Tajná zbraň', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50641, 1, '2012-07-03 08:46:05', '2012-07-03 08:46:05', 'Kinoautomat svět', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50729, 1, '2012-07-03 08:46:39', '2012-07-03 08:46:39', 'Po stopách mrtvého', NULL, 1, 1488, 4, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50868, 1, '2012-07-03 08:47:18', '2012-07-03 08:47:19', 'Obyčejný den', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (50935, 1, '2012-07-03 08:47:45', '2012-07-03 08:47:45', 'Vladivostop', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (51267, 1, '2012-07-03 08:50:02', '2012-07-03 08:50:02', 'Tambari', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (51398, 1, '2012-07-03 08:51:03', '2012-08-03 13:14:37', 'Nový život Henryho Wilta', NULL, 1, 1548, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (51460, 1, '2012-07-03 08:51:33', '2012-08-03 13:16:10', 'Král termitů', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (51962, 1, '2012-08-03 13:14:51', '2012-08-03 13:14:51', 'Hledání křesťanské svobody', NULL, 1, NULL, 0, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (52468, 1, '2012-08-03 13:17:10', '2012-08-03 13:17:10', 'Právo tomahavku 02', NULL, 1, NULL, 0, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (52594, 1, '2012-08-03 13:17:43', '2012-08-03 13:17:43', 'Věčná bitva', NULL, 1, 1614, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (52846, 1, '2012-08-03 13:18:27', '2012-08-03 13:19:13', 'Jablíčko lásky', NULL, 1, 1203, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (52963, 1, '2012-08-03 13:18:54', '2013-04-13 15:12:57', 'Obsidiánový motýl', '', 1, 6, 9, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (53722, 1, '2012-09-27 10:34:45', '2012-09-27 10:34:45', 'Ledové srdce', NULL, 1, 1674, 17, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (53819, 1, '2012-10-05 18:35:56', '2012-10-05 18:35:56', 'Půlnoční přípitek', NULL, 1, 1633, 81, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (53963, 1, '2012-10-05 18:37:04', '2012-10-05 18:37:04', 'Uvězněná láska', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (54183, 1, '2012-10-14 10:30:07', '2012-10-14 10:30:07', 'Middlesex', NULL, 2, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (54788, 1, '2012-11-19 19:15:02', '2012-11-19 19:15:02', 'Džentlmen pirátem', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (54933, 1, '2012-11-19 19:16:11', '2012-11-19 19:16:11', 'Výkřik v hrobce', NULL, 1, 1633, 190, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (55153, 1, '2012-12-22 06:30:47', '2012-12-22 06:30:47', 'Sám proti peklu', NULL, 1, 1633, 203, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (55217, 1, '2012-12-22 06:30:54', '2012-12-22 06:30:54', 'Satanova řeka', NULL, 1, 1633, 316, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56159, 1, '2013-02-10 09:15:52', '2013-02-10 09:15:52', 'Zásvětí', NULL, 1, 1609, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56253, 1, '2013-02-10 09:16:29', '2014-09-06 20:48:20', 'Vejce s ozvěnou', '', 1, 1534, 1, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56297, 1, '2013-02-10 09:16:45', '2013-02-10 09:16:45', 'Pozvání  na víkend', NULL, 1, 1383, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56528, 1, '2013-03-03 07:35:09', '2013-03-03 07:35:09', 'Désirée', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (56885, 1, '2013-03-16 11:47:38', '2013-03-16 11:47:38', 'Prvá krv', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (57113, 1, '2013-03-29 08:14:24', '2013-03-29 08:14:24', 'O ľuďoch a jaštericiach', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (57216, 1, '2013-03-29 08:15:07', '2013-03-29 08:15:07', 'Microsoft Exchange Server 2003', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (57939, 1, '2013-05-04 07:33:52', '2013-05-04 07:33:52', 'Paralelní světy', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (58235, 1, '2013-05-31 08:16:27', '2013-05-31 08:16:27', 'Z různého šiku', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (58694, 1, '2013-06-28 21:32:11', '2013-06-28 21:32:11', 'Podobni bohům', NULL, 1, 1556, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (58699, 1, '2013-06-28 21:32:12', '2013-06-28 21:32:12', 'Za uměním', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (58909, 1, '2013-07-14 11:06:44', '2013-07-14 11:06:44', 'V osidlech temných intrik', NULL, 1, 1474, 3, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (59887, 1, '2013-11-01 07:05:38', '2013-11-01 07:05:39', 'Černé slunce', NULL, 1, 2048, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (60209, 1, '2013-11-04 20:48:41', '2013-11-04 20:48:41', 'Zlatokopka', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (60406, 1, '2013-11-15 19:01:05', '2013-11-15 19:01:05', 'Hlubina', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (61048, 1, '2014-02-06 16:46:51', '2014-02-06 16:46:51', 'Zlomená pečeť', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (61800, 1, '2014-03-28 08:48:40', '2014-03-28 08:48:40', 'Velká lež', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (61944, 1, '2014-04-13 11:00:56', '2014-04-13 11:00:56', 'Roky v Bílém domě', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (62241, 1, '2014-05-17 14:36:08', '2014-05-17 14:36:08', 'Alenka v říši kvant - Alegorie kvantové fyziky', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (62616, 1, '2014-07-19 14:58:22', '2014-07-19 14:58:22', 'Veterinářem v zoo', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (62546, 1, '2014-06-30 17:45:40', '2014-06-30 17:45:40', 'Valentinky 2000 2', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (62974, 1, '2014-08-31 18:29:20', '2014-08-31 18:29:20', 'Krvavě rudé slunce', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (63404, 1, '2014-11-03 17:42:05', '2014-11-03 17:42:05', 'Cesty osudu/Svádění z pomsty', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (64619, 1, '2015-02-15 09:10:16', '2015-02-15 09:10:16', 'Potopená města', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (64935, 1, '2015-03-19 17:55:34', '2015-03-19 17:55:34', 'Miluji tě neustále - Polibky z Nizozemí', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (64957, 1, '2015-03-19 17:55:40', '2015-03-19 17:55:40', 'Pohostinnosť cudzincov', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (65066, 1, '2015-05-04 21:27:50', '2015-05-04 21:27:50', 'Malý velikán', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (65824, 1, '2015-08-30 11:13:12', '2015-08-30 11:13:12', 'Faktor strachu', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (65975, 1, '2015-08-30 11:14:43', '2015-08-30 11:14:44', 'Malá větrná elektrárna - Návod ke stavbě s konstrukčními výkresy', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (66634, 1, '2015-12-27 09:21:56', '2015-12-27 09:21:56', 'Proměna Mary Dyerové', NULL, 1, 2301, 2, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (66677, 1, '2015-12-27 09:22:12', '2015-12-27 09:22:12', 'Sváteční nevěsta', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (66804, 1, '2015-12-27 09:23:13', '2015-12-27 09:23:13', 'Prekliati králi 7 - Keď kráľ prehrá Francúzsko', NULL, 3, NULL, NULL, NULL, NULL, NULL, 1, 1);
INSERT INTO ebook VALUES (67157, 1, '2016-02-05 08:39:49', '2016-02-05 08:39:49', 'Vůle ke smyslu - Vybrané přednášky o logoterapii.', NULL, 1, NULL, NULL, NULL, NULL, NULL, 1, 1);


--
-- TOC entry 2277 (class 0 OID 31509)
-- Dependencies: 208
-- Data for Name: ebook_authors; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO ebook_authors VALUES (33258, 4920);
INSERT INTO ebook_authors VALUES (33344, 4938);
INSERT INTO ebook_authors VALUES (33837, 5012);
INSERT INTO ebook_authors VALUES (34087, 5048);
INSERT INTO ebook_authors VALUES (34513, 5103);
INSERT INTO ebook_authors VALUES (55325, 5998);
INSERT INTO ebook_authors VALUES (56396, 10964);
INSERT INTO ebook_authors VALUES (35341, 5222);
INSERT INTO ebook_authors VALUES (35485, 5666);
INSERT INTO ebook_authors VALUES (35515, 5669);
INSERT INTO ebook_authors VALUES (35671, 5277);
INSERT INTO ebook_authors VALUES (36214, 5340);
INSERT INTO ebook_authors VALUES (36253, 5355);
INSERT INTO ebook_authors VALUES (64726, 6839);
INSERT INTO ebook_authors VALUES (37038, 5465);
INSERT INTO ebook_authors VALUES (37116, 5479);
INSERT INTO ebook_authors VALUES (37157, 6432);
INSERT INTO ebook_authors VALUES (37157, 6433);
INSERT INTO ebook_authors VALUES (37867, 4924);
INSERT INTO ebook_authors VALUES (38921, 5696);
INSERT INTO ebook_authors VALUES (39072, 5556);
INSERT INTO ebook_authors VALUES (40773, 5454);
INSERT INTO ebook_authors VALUES (41749, 5155);
INSERT INTO ebook_authors VALUES (41749, 6489);
INSERT INTO ebook_authors VALUES (42163, 6598);
INSERT INTO ebook_authors VALUES (42314, 5521);
INSERT INTO ebook_authors VALUES (42537, 6700);
INSERT INTO ebook_authors VALUES (43023, 6772);
INSERT INTO ebook_authors VALUES (43529, 6980);
INSERT INTO ebook_authors VALUES (43662, 6164);
INSERT INTO ebook_authors VALUES (43908, 5912);
INSERT INTO ebook_authors VALUES (43933, 7106);
INSERT INTO ebook_authors VALUES (43992, 5271);
INSERT INTO ebook_authors VALUES (45202, 5591);
INSERT INTO ebook_authors VALUES (45446, 6195);
INSERT INTO ebook_authors VALUES (45643, 7732);
INSERT INTO ebook_authors VALUES (45668, 7738);
INSERT INTO ebook_authors VALUES (46064, 7939);
INSERT INTO ebook_authors VALUES (46818, 8185);
INSERT INTO ebook_authors VALUES (47602, 7072);
INSERT INTO ebook_authors VALUES (48552, 7297);
INSERT INTO ebook_authors VALUES (48728, 7417);
INSERT INTO ebook_authors VALUES (48818, 6212);
INSERT INTO ebook_authors VALUES (49134, 8949);
INSERT INTO ebook_authors VALUES (49138, 7046);
INSERT INTO ebook_authors VALUES (49667, 9148);
INSERT INTO ebook_authors VALUES (50118, 9281);
INSERT INTO ebook_authors VALUES (50495, 9394);
INSERT INTO ebook_authors VALUES (50556, 7438);
INSERT INTO ebook_authors VALUES (50641, 6188);
INSERT INTO ebook_authors VALUES (50729, 5185);
INSERT INTO ebook_authors VALUES (50868, 8636);
INSERT INTO ebook_authors VALUES (50935, 9513);
INSERT INTO ebook_authors VALUES (51267, 9616);
INSERT INTO ebook_authors VALUES (51398, 9661);
INSERT INTO ebook_authors VALUES (51460, 9681);
INSERT INTO ebook_authors VALUES (51962, 9810);
INSERT INTO ebook_authors VALUES (52468, 9949);
INSERT INTO ebook_authors VALUES (52594, 5540);
INSERT INTO ebook_authors VALUES (52846, 7296);
INSERT INTO ebook_authors VALUES (52963, 5133);
INSERT INTO ebook_authors VALUES (53722, 10203);
INSERT INTO ebook_authors VALUES (53819, 8015);
INSERT INTO ebook_authors VALUES (53963, 6526);
INSERT INTO ebook_authors VALUES (54183, 10420);
INSERT INTO ebook_authors VALUES (54788, 7620);
INSERT INTO ebook_authors VALUES (54933, 8015);
INSERT INTO ebook_authors VALUES (55153, 8015);
INSERT INTO ebook_authors VALUES (55153, 10356);
INSERT INTO ebook_authors VALUES (55217, 8015);
INSERT INTO ebook_authors VALUES (56159, 9948);
INSERT INTO ebook_authors VALUES (56253, 5355);
INSERT INTO ebook_authors VALUES (56297, 7472);
INSERT INTO ebook_authors VALUES (56528, 10195);
INSERT INTO ebook_authors VALUES (56885, 11152);
INSERT INTO ebook_authors VALUES (57113, 11098);
INSERT INTO ebook_authors VALUES (57216, 11205);
INSERT INTO ebook_authors VALUES (57939, 7643);
INSERT INTO ebook_authors VALUES (58235, 11591);
INSERT INTO ebook_authors VALUES (58694, 5506);
INSERT INTO ebook_authors VALUES (58699, 10062);
INSERT INTO ebook_authors VALUES (58909, 5798);
INSERT INTO ebook_authors VALUES (59887, 12016);
INSERT INTO ebook_authors VALUES (60209, 12188);
INSERT INTO ebook_authors VALUES (60406, 6918);
INSERT INTO ebook_authors VALUES (61048, 11465);
INSERT INTO ebook_authors VALUES (61800, 6282);
INSERT INTO ebook_authors VALUES (61944, 12673);
INSERT INTO ebook_authors VALUES (62241, 11184);
INSERT INTO ebook_authors VALUES (62616, 12885);
INSERT INTO ebook_authors VALUES (62546, 7444);
INSERT INTO ebook_authors VALUES (62546, 7410);
INSERT INTO ebook_authors VALUES (62546, 7445);
INSERT INTO ebook_authors VALUES (62974, 12982);
INSERT INTO ebook_authors VALUES (63404, 10297);
INSERT INTO ebook_authors VALUES (63404, 9789);
INSERT INTO ebook_authors VALUES (64619, 7598);
INSERT INTO ebook_authors VALUES (64935, 7486);
INSERT INTO ebook_authors VALUES (64957, 7698);
INSERT INTO ebook_authors VALUES (65066, 7319);
INSERT INTO ebook_authors VALUES (65824, 8186);
INSERT INTO ebook_authors VALUES (65975, 13922);
INSERT INTO ebook_authors VALUES (66634, 12949);
INSERT INTO ebook_authors VALUES (66677, 9615);
INSERT INTO ebook_authors VALUES (66804, 6837);
INSERT INTO ebook_authors VALUES (67157, 9160);


--
-- TOC entry 2274 (class 0 OID 31460)
-- Dependencies: 205
-- Data for Name: ebook_genres; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO ebook_genres VALUES (33344, 7);
INSERT INTO ebook_genres VALUES (33344, 15);
INSERT INTO ebook_genres VALUES (33344, 16);
INSERT INTO ebook_genres VALUES (33837, 7);
INSERT INTO ebook_genres VALUES (33837, 29);
INSERT INTO ebook_genres VALUES (34513, 9);
INSERT INTO ebook_genres VALUES (55325, 7);
INSERT INTO ebook_genres VALUES (55325, 38);
INSERT INTO ebook_genres VALUES (56396, 15);
INSERT INTO ebook_genres VALUES (64726, 7);
INSERT INTO ebook_genres VALUES (37157, 16);
INSERT INTO ebook_genres VALUES (37157, 25);
INSERT INTO ebook_genres VALUES (39072, 1);
INSERT INTO ebook_genres VALUES (39072, 4);
INSERT INTO ebook_genres VALUES (40773, 9);
INSERT INTO ebook_genres VALUES (41749, 9);
INSERT INTO ebook_genres VALUES (42163, 7);
INSERT INTO ebook_genres VALUES (42163, 25);
INSERT INTO ebook_genres VALUES (42314, 1);
INSERT INTO ebook_genres VALUES (42314, 10);
INSERT INTO ebook_genres VALUES (42537, 25);
INSERT INTO ebook_genres VALUES (43023, 4);
INSERT INTO ebook_genres VALUES (43023, 7);
INSERT INTO ebook_genres VALUES (43529, 25);
INSERT INTO ebook_genres VALUES (43662, 13);
INSERT INTO ebook_genres VALUES (43662, 23);
INSERT INTO ebook_genres VALUES (43662, 38);
INSERT INTO ebook_genres VALUES (43908, 1);
INSERT INTO ebook_genres VALUES (43908, 4);
INSERT INTO ebook_genres VALUES (43908, 7);
INSERT INTO ebook_genres VALUES (43908, 12);
INSERT INTO ebook_genres VALUES (43933, 12);
INSERT INTO ebook_genres VALUES (43933, 34);
INSERT INTO ebook_genres VALUES (43992, 9);
INSERT INTO ebook_genres VALUES (43992, 13);
INSERT INTO ebook_genres VALUES (45202, 7);
INSERT INTO ebook_genres VALUES (45202, 41);
INSERT INTO ebook_genres VALUES (45446, 10);
INSERT INTO ebook_genres VALUES (45446, 45);
INSERT INTO ebook_genres VALUES (45643, 10);
INSERT INTO ebook_genres VALUES (45668, 7);
INSERT INTO ebook_genres VALUES (46064, 45);
INSERT INTO ebook_genres VALUES (46818, 23);
INSERT INTO ebook_genres VALUES (46818, 49);
INSERT INTO ebook_genres VALUES (47602, 36);
INSERT INTO ebook_genres VALUES (48552, 11);
INSERT INTO ebook_genres VALUES (48552, 47);
INSERT INTO ebook_genres VALUES (48728, 23);
INSERT INTO ebook_genres VALUES (48728, 45);
INSERT INTO ebook_genres VALUES (48818, 23);
INSERT INTO ebook_genres VALUES (48818, 45);
INSERT INTO ebook_genres VALUES (49134, 21);
INSERT INTO ebook_genres VALUES (49134, 56);
INSERT INTO ebook_genres VALUES (49138, 7);
INSERT INTO ebook_genres VALUES (49667, 45);
INSERT INTO ebook_genres VALUES (50118, 23);
INSERT INTO ebook_genres VALUES (50118, 45);
INSERT INTO ebook_genres VALUES (50495, 34);
INSERT INTO ebook_genres VALUES (50495, 56);
INSERT INTO ebook_genres VALUES (50556, 23);
INSERT INTO ebook_genres VALUES (50556, 45);
INSERT INTO ebook_genres VALUES (50641, 9);
INSERT INTO ebook_genres VALUES (50641, 13);
INSERT INTO ebook_genres VALUES (50641, 25);
INSERT INTO ebook_genres VALUES (50641, 52);
INSERT INTO ebook_genres VALUES (50729, 7);
INSERT INTO ebook_genres VALUES (50729, 29);
INSERT INTO ebook_genres VALUES (50868, 52);
INSERT INTO ebook_genres VALUES (50935, 30);
INSERT INTO ebook_genres VALUES (51267, 1);
INSERT INTO ebook_genres VALUES (51398, 14);
INSERT INTO ebook_genres VALUES (51460, 7);
INSERT INTO ebook_genres VALUES (51962, 22);
INSERT INTO ebook_genres VALUES (52468, 1);
INSERT INTO ebook_genres VALUES (52594, 9);
INSERT INTO ebook_genres VALUES (52846, 45);
INSERT INTO ebook_genres VALUES (52963, 26);
INSERT INTO ebook_genres VALUES (52963, 49);
INSERT INTO ebook_genres VALUES (53722, 29);
INSERT INTO ebook_genres VALUES (53819, 7);
INSERT INTO ebook_genres VALUES (53819, 9);
INSERT INTO ebook_genres VALUES (53819, 13);
INSERT INTO ebook_genres VALUES (53963, 23);
INSERT INTO ebook_genres VALUES (53963, 45);
INSERT INTO ebook_genres VALUES (54788, 23);
INSERT INTO ebook_genres VALUES (54788, 45);
INSERT INTO ebook_genres VALUES (54933, 7);
INSERT INTO ebook_genres VALUES (54933, 9);
INSERT INTO ebook_genres VALUES (54933, 13);
INSERT INTO ebook_genres VALUES (55153, 7);
INSERT INTO ebook_genres VALUES (55153, 9);
INSERT INTO ebook_genres VALUES (55153, 13);
INSERT INTO ebook_genres VALUES (55217, 7);
INSERT INTO ebook_genres VALUES (55217, 9);
INSERT INTO ebook_genres VALUES (55217, 13);
INSERT INTO ebook_genres VALUES (56159, 9);
INSERT INTO ebook_genres VALUES (56159, 25);
INSERT INTO ebook_genres VALUES (56253, 25);
INSERT INTO ebook_genres VALUES (56253, 44);
INSERT INTO ebook_genres VALUES (56297, 23);
INSERT INTO ebook_genres VALUES (56297, 45);
INSERT INTO ebook_genres VALUES (56528, 38);
INSERT INTO ebook_genres VALUES (56885, 9);
INSERT INTO ebook_genres VALUES (56885, 16);
INSERT INTO ebook_genres VALUES (56885, 25);
INSERT INTO ebook_genres VALUES (56885, 52);
INSERT INTO ebook_genres VALUES (57113, 9);
INSERT INTO ebook_genres VALUES (57113, 16);
INSERT INTO ebook_genres VALUES (57113, 25);
INSERT INTO ebook_genres VALUES (57113, 52);
INSERT INTO ebook_genres VALUES (57216, 5);
INSERT INTO ebook_genres VALUES (57939, 24);
INSERT INTO ebook_genres VALUES (58235, 27);
INSERT INTO ebook_genres VALUES (58235, 39);
INSERT INTO ebook_genres VALUES (58694, 25);
INSERT INTO ebook_genres VALUES (58699, 16);
INSERT INTO ebook_genres VALUES (58699, 37);
INSERT INTO ebook_genres VALUES (58909, 1);
INSERT INTO ebook_genres VALUES (58909, 23);
INSERT INTO ebook_genres VALUES (58909, 45);
INSERT INTO ebook_genres VALUES (59887, 25);
INSERT INTO ebook_genres VALUES (60209, 10);
INSERT INTO ebook_genres VALUES (60209, 26);
INSERT INTO ebook_genres VALUES (60406, 1);
INSERT INTO ebook_genres VALUES (60406, 29);
INSERT INTO ebook_genres VALUES (61048, 29);
INSERT INTO ebook_genres VALUES (61800, 23);
INSERT INTO ebook_genres VALUES (61800, 45);
INSERT INTO ebook_genres VALUES (61944, 12);
INSERT INTO ebook_genres VALUES (61944, 20);
INSERT INTO ebook_genres VALUES (62241, 24);
INSERT INTO ebook_genres VALUES (62616, 14);
INSERT INTO ebook_genres VALUES (62616, 24);
INSERT INTO ebook_genres VALUES (62546, 23);
INSERT INTO ebook_genres VALUES (62546, 45);
INSERT INTO ebook_genres VALUES (62974, 7);
INSERT INTO ebook_genres VALUES (62974, 52);
INSERT INTO ebook_genres VALUES (63404, 23);
INSERT INTO ebook_genres VALUES (63404, 45);
INSERT INTO ebook_genres VALUES (64619, 25);
INSERT INTO ebook_genres VALUES (64935, 23);
INSERT INTO ebook_genres VALUES (64935, 45);
INSERT INTO ebook_genres VALUES (64957, 10);
INSERT INTO ebook_genres VALUES (65066, 10);
INSERT INTO ebook_genres VALUES (65824, 29);
INSERT INTO ebook_genres VALUES (65975, 58);
INSERT INTO ebook_genres VALUES (66634, 23);
INSERT INTO ebook_genres VALUES (66634, 37);
INSERT INTO ebook_genres VALUES (66677, 23);
INSERT INTO ebook_genres VALUES (66677, 45);
INSERT INTO ebook_genres VALUES (66804, 12);
INSERT INTO ebook_genres VALUES (67157, 21);


--
-- TOC entry 2283 (class 0 OID 0)
-- Dependencies: 201
-- Name: ebook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('ebook_id_seq', 67929, true);


--
-- TOC entry 2284 (class 0 OID 0)
-- Dependencies: 194
-- Name: series_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('series_id_seq', 2734, true);


--
-- TOC entry 2276 (class 0 OID 31479)
-- Dependencies: 207
-- Data for Name: source; Type: TABLE DATA; Schema: public; Owner: ebooks
--

INSERT INTO source VALUES (41654, 1, '2010-07-25 11:35:49', '2010-07-25 11:35:49', 33258, 'Bialolecka, Ewa/Tkac iluzi/Bialolecka, Ewa - Tkac iluzi.pdb', NULL, 3, 409682, '8da9ebe840236b5ee014f32dff25926c4a40a037', NULL, 1, 1);
INSERT INTO source VALUES (41655, 1, '2010-07-25 11:35:50', '2010-07-25 11:35:50', 33258, 'Bialolecka, Ewa/Tkac iluzi/Bialolecka, Ewa - Tkac iluzi.doc', NULL, 5, 1211392, 'a1acd529a282587c1a89a2109f002122992861ba', NULL, 1, 1);
INSERT INTO source VALUES (41765, 1, '2010-07-25 11:36:14', '2010-07-25 11:36:14', 33344, 'Borovicka, Vaclav Pavel/Zahadne policejni pripady/Borovicka, Vaclav Pavel - Zahadne policejni pripady.pdb', NULL, 3, 362889, '08470e245641873d14885d0a5ae362a7467f7b00', NULL, 1, 1);
INSERT INTO source VALUES (42441, 1, '2010-07-25 11:39:51', '2012-08-03 16:45:12', 33837, 'Crichton, Michael/Let cislo TPA 545/Crichton, Michael - Let cislo TPA 545.pdb', NULL, 3, 385711, '2909069af41b64a51f946b6cd4b550450a3cef47', NULL, 1, 1);
INSERT INTO source VALUES (42448, 1, '2010-07-25 11:39:56', '2012-08-03 16:45:12', 33837, 'Crichton, Michael/Let cislo TPA 545/Crichton, Michael - Let cislo TPA 545.doc', NULL, 5, 1993728, '836f7033527030db4e2e8e6f8531459ddc15222c', NULL, 1, 1);
INSERT INTO source VALUES (42737, 1, '2010-07-25 11:41:24', '2012-08-03 16:45:21', 34087, 'Eddings, David Carroll/Malloreon 1 - Strazci Zapadu/Eddings, David Carroll - Malloreon 1 - Strazci Zapadu.doc', NULL, 5, 2404352, '9aba9ed83f5a4f773f093744f2c4447125833693', NULL, 1, 1);
INSERT INTO source VALUES (42754, 1, '2010-07-25 11:41:29', '2012-08-03 16:45:21', 34087, 'Eddings, David Carroll/Malloreon 1 - Strazci Zapadu/Eddings, David Carroll - Malloreon 1 - Strazci Zapadu.pdb', NULL, 3, 490454, '7e59b98ce51396cad7e7524c1c6098950e83ff1f', NULL, 1, 1);
INSERT INTO source VALUES (42774, 1, '2010-07-25 11:41:41', '2012-08-03 16:45:21', 34087, 'Eddings, David Carroll/Malloreon 1 - Strazci Zapadu/Eddings, David Carroll - Malloreon 1 - Strazci Zapadu (1).doc', NULL, 5, 1629696, '952918e421daea1d475eb9ee3b0fe4a883fb1295', NULL, 1, 1);
INSERT INTO source VALUES (43290, 1, '2010-07-25 11:44:59', '2012-08-03 16:45:31', 34513, 'Gemmell, David/Drenajska saga/Drenajska saga 1 - Legenda/Gemmell, David - Drenajska saga 1 - Legenda.pdb', NULL, 3, 425366, 'aded7e5aa837205282435517c0ae7fdf1b5e0315', NULL, 1, 1);
INSERT INTO source VALUES (43307, 1, '2010-07-25 11:45:05', '2012-08-03 16:45:31', 34513, 'Gemmell, David/Drenajska saga/Drenajska saga 1 - Legenda/Gemmell, David - Drenajska saga 1 - Legenda.doc', NULL, 5, 1611264, '06cdb76ab8e346497c0c0a944b58a748470b28d3', NULL, 1, 1);
INSERT INTO source VALUES (44363, 1, '2010-07-25 11:51:44', '2012-08-03 16:45:51', 35341, 'King, Stephen Edwin/Odvykaci a s/King, Stephen Edwin - Odvykaci a s.pdb', NULL, 3, 28792, '4f68cf9126c889e4b285d1bf1fb74016cd98a76d', NULL, 1, 1);
INSERT INTO source VALUES (44539, 1, '2010-07-25 11:52:44', '2010-10-31 10:58:24', 35485, 'Kuttner, Henry/Proklete mesto/Kuttner, Henry - Proklete mesto.doc', NULL, 5, 92672, '60836f19cef8c06c7a2f85c67391e4a3ecaa163d', NULL, 1, 1);
INSERT INTO source VALUES (44574, 1, '2010-07-25 11:52:51', '2010-10-31 10:58:24', 35515, 'Le Guin, Ursula Kroeber/Svet je les les je svet/Le Guin, Ursula Kroeber - Svet je les les je svet.pdb', NULL, 3, 153643, '1ea184964b79974432307768dfa2faf9792cb5e1', NULL, 1, 1);
INSERT INTO source VALUES (44774, 1, '2010-07-25 11:53:54', '2010-07-25 11:53:54', 35671, 'Macek, Petr/StarTrek Nova Generace - Zrcadla/Macek, Petr - StarTrek Nova Generace - Zrcadla.pdb', NULL, 3, 248735, 'b7a29f0fc3605fcdbaeb7fb1991652c695e2e790', NULL, 1, 1);
INSERT INTO source VALUES (45448, 1, '2010-07-25 11:57:42', '2010-07-25 11:57:42', 36214, 'Novik, Naomi/Temeraire 2 - Nefritovy trun/Novik, Naomi - Temeraire 2 - Nefritovy trun.pdb', NULL, 3, 453287, '914251d584c72ed3e1fd879313b5d47730548b04', NULL, 1, 1);
INSERT INTO source VALUES (45492, 1, '2010-07-25 11:58:01', '2010-07-25 11:58:01', 36253, 'Pecinovsky, Josef/Kupte si svet/Pecinovsky, Josef - Kupte si svet.doc', NULL, 5, 73211, '0e425b7f774305cdf42d979401a240d090f90a5c', NULL, 1, 1);
INSERT INTO source VALUES (46393, 1, '2010-07-25 12:03:18', '2010-07-25 12:03:18', 37038, 'Star, Trek/Gene DeWeese - Strazci miru/Star, Trek - Gene DeWeese - Strazci miru.doc', NULL, 5, 765440, 'ff4f6b511b6a543497b1b1e74a60b52fbf9d4d32', NULL, 1, 1);
INSERT INTO source VALUES (46481, 1, '2010-07-25 12:03:46', '2010-07-25 12:03:46', 37116, 'Storch, Eduard/Bronzovy poklad/Storch, Eduard - Bronzovy poklad.pdb', NULL, 3, 172792, 'a06d7ea75cde9a05890104a8b458771f0b6572c8', NULL, 1, 1);
INSERT INTO source VALUES (46519, 1, '2010-07-25 12:03:59', '2011-05-27 21:26:16', 37157, 'Strugacki, Arkadij a Boris/Noc Na Marse/Strugacki, Arkadij a Boris - Noc Na Marse.doc', NULL, 5, 96256, '90188c9656d7bccf246ba7788c17486ddf5ec787', NULL, 1, 1);
INSERT INTO source VALUES (46688, 1, '2010-07-25 12:05:04', '2013-06-28 22:09:40', 58694, 'Troska, Jan Matzal/Zapas s nebem/Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum/Troska, Jan Matzal - Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum.doc', NULL, 5, 4470272, '211ed452f028a4142b6d514fe18e48ac4b7233a4', NULL, 1, 1);
INSERT INTO source VALUES (46700, 1, '2010-07-25 12:05:07', '2013-06-28 22:09:40', 58694, 'Troska, Jan Matzal/Zapas s nebem/Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum/Troska, Jan Matzal - Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum.pdb', NULL, 3, 301848, '155c6a5c239b59290036641d4600b09187ca216d', NULL, 1, 1);
INSERT INTO source VALUES (47478, 1, '2010-10-22 16:10:33', '2010-10-22 16:10:33', 33258, 'Bialolecka, Ewa/Tkac iluzi/Bialolecka, Ewa - Tkac iluzi.txt', NULL, 2, 568785, 'e4f8083d2eb22e04457c44bf9a228e15f513aef1', NULL, 1, 1);
INSERT INTO source VALUES (47497, 1, '2010-10-22 16:10:34', '2010-10-22 16:10:34', 37867, 'Birdman, Shigor/Po druhy do stejny reky/Birdman, Shigor - Po druhy do stejny reky.txt', NULL, 2, 7269, 'a7addacc41a32b1ddf0b46f094868cfb8695b430', NULL, 1, 1);
INSERT INTO source VALUES (47535, 1, '2010-10-22 16:10:36', '2010-10-22 16:10:36', 33344, 'Borovicka, Vaclav Pavel/Zahadne policejni pripady/Borovicka, Vaclav Pavel - Zahadne policejni pripady.txt', NULL, 2, 551746, '6e2a398bbf6962b58d59e644257afc291f21fcb8', NULL, 1, 1);
INSERT INTO source VALUES (47822, 1, '2010-10-22 16:11:00', '2012-09-13 18:23:51', 33837, 'Crichton, Michael/Let cislo TPA 545/Crichton, Michael - Let cislo TPA 545.txt', NULL, 2, 560979, '0deadb7f76082eae12e9e0335f346b9369b5ecc4', NULL, 1, 1);
INSERT INTO source VALUES (48050, 1, '2010-10-22 16:11:16', '2012-09-27 14:53:31', 34513, 'Gemmell, David/Drenajska saga 1 - Legenda/Gemmell, David - Drenajska saga 1 - Legenda.txt', NULL, 2, 630023, 'cd1ce6869336af6a1b06061b70431ca96f903d2d', NULL, 1, 1);
INSERT INTO source VALUES (48556, 1, '2010-10-22 16:11:51', '2010-10-31 22:44:57', 35515, 'Le Guin, Ursula Kroeber/Svet je les les je svet/Le Guin, Ursula Kroeber - Svet je les les je svet.txt', NULL, 2, 219003, '41be9e6fb2a6c69c8b062acd7d72832444a1e837', NULL, 1, 1);
INSERT INTO source VALUES (49202, 1, '2010-10-22 16:12:50', '2010-10-22 16:12:50', 38921, 'Staheff, Christopher/Carodej 05 - Carodej rozzureny/Staheff, Christopher - Carodej 05 - Carodej rozzureny.txt', NULL, 2, 449378, '2f379f32305557c018ef56bda9e2a5e787fbf752', NULL, 1, 1);
INSERT INTO source VALUES (49321, 1, '2010-10-22 16:12:57', '2013-06-28 22:09:40', 58694, 'Troska, Jan Matzal/Zapas s nebem/Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum/Troska, Jan Matzal - Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum.txt', NULL, 2, 421545, 'aa4a147436c9d972980ba7e95f108a6f762e0471', NULL, 1, 1);
INSERT INTO source VALUES (49458, 1, '2010-10-22 16:13:09', '2010-10-22 16:13:09', 39072, 'Wells, Herbert George/Valka svetu a jine pribehy z neskutecna/Wells, Herbert George - Valka svetu a jine pribehy z neskutecna.txt', NULL, 2, 695736, 'b39e4fc321d923f5b931cf10c0b113f1bf2a53b0', NULL, 1, 1);
INSERT INTO source VALUES (51691, 1, '2012-07-03 07:45:03', '2012-07-03 07:45:03', 40773, 'Slechta, Vladimir/Krvave pohranici - Gordonova zeme/Krvave pohranici - Gordonova zeme 2 - Ploty z kosti/Slechta, Vladimir - Krvave pohranici - Gordonova zeme 2 - Ploty z kosti.doc', NULL, 5, 2972672, '0601830e937c08eea6edda50636457e3d6d1b93d', 40, 1, 1);
INSERT INTO source VALUES (53044, 1, '2012-07-03 07:50:20', '2012-07-03 07:50:20', 41749, 'Hendee, John Clare/Vzneseni mrtvi I/Vzneseni mrtvi I 4 - Zradce krve/Hendee, John Clare - Vzneseni mrtvi I 4 - Zradce krve.doc', NULL, 5, 1738240, '136fb562dc9453f948d8459255303fbf58a066d4', 40, 1, 1);
INSERT INTO source VALUES (53045, 1, '2012-07-03 07:50:21', '2012-07-03 07:50:21', 41749, 'Hendee, John Clare/Vzneseni mrtvi I/Vzneseni mrtvi I 4 - Zradce krve/Hendee, John Clare - Vzneseni mrtvi I 4 - Zradce krve.epub', NULL, 8, 2298641, '67a5c172fdc8d0b2355e38bc95ad6b956dd4950b', 40, 1, 1);
INSERT INTO source VALUES (53613, 1, '2012-07-03 07:52:28', '2012-07-03 07:52:28', 42163, 'Hall, Robert Lee/Pribehy Sherlocka Holmese (Jota)/Pribehy Sherlocka Holmese (Jota) 14 - Sherlock Holmes odchazi/Hall, Robert Lee - Pribehy Sherlocka Holmese (Jota) 14 - Sherlock Holmes odchazi.doc', NULL, 5, 1632256, 'baad4f71c8c09189fc508d714e7f48514cae0fb1', 40, 1, 1);
INSERT INTO source VALUES (53800, 1, '2012-07-03 07:53:06', '2012-07-03 07:53:06', 42314, 'Verne, Jules/Deti kapitana Granta 1. dil/Verne, Jules - Deti kapitana Granta 1. dil.doc', NULL, 5, 4883456, 'fdbed4d571fff4fe4337c56ba366f6a08f34dfd9', 40, 1, 1);
INSERT INTO source VALUES (54096, 1, '2012-07-03 07:54:17', '2012-07-03 07:54:17', 42537, 'Varsavskij, Ilja Iosifovic/Experiment/Varsavskij, Ilja Iosifovic - Experiment.doc', NULL, 5, 73728, '446a83976c374c4cd8cef85b61f0485afce44392', 60, 1, 1);
INSERT INTO source VALUES (54463, 1, '2012-07-03 07:55:41', '2013-06-28 22:09:40', 58694, 'Troska, Jan Matzal/Zapas s nebem/Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum/Troska, Jan Matzal - Zapas s nebem 2 - Zapas s nebem 2 - Podobni bohum.epub', NULL, 8, 253636, 'a64a13fef9a80be1f24911a713cd894453f5f4ee', 90, 1, 1);
INSERT INTO source VALUES (54702, 1, '2012-07-03 07:56:34', '2012-07-03 07:56:34', 43023, 'Nienacki, Zbigniew/Pan Tragacik/Pan Tragacik 7 - Pan Tragacik a Kapitan Nemo/Nienacki, Zbigniew - Pan Tragacik 7 - Pan Tragacik a Kapitan Nemo.pdf', NULL, 1, 1133113, '7c283c537c4a4917beb78b0e17e2576b4c72607b', 40, 1, 1);
INSERT INTO source VALUES (55402, 1, '2012-07-03 07:59:20', '2012-08-03 16:45:36', 43529, 'Hand, Elizabeth/Star Wars BBY/Star Wars BBY 22 - Boba Fett 3 Labyrint klamu/Hand, Elizabeth - Star Wars BBY 22 - Boba Fett 3 Labyrint klamu.doc', NULL, 5, 376320, 'fe2118f12cc2a4ebb77892bdd591601d4084e9a5', 20, 1, 1);
INSERT INTO source VALUES (55403, 1, '2012-07-03 07:59:20', '2012-08-03 16:45:36', 43529, 'Hand, Elizabeth/Star Wars BBY/Star Wars BBY 22 - Boba Fett 3 Labyrint klamu/Hand, Elizabeth - Star Wars BBY 22 - Boba Fett 3 Labyrint klamu.pdb', NULL, 3, 77836, '0c5e3b1805ad87aa3cfb6d389201eb261aed13c9', 10, 1, 1);
INSERT INTO source VALUES (55587, 1, '2012-07-03 08:00:10', '2012-07-03 08:00:10', 43662, 'Erskine, Barbara/Ukryt pred svetlem/Erskine, Barbara - Ukryt pred svetlem.doc', NULL, 5, 2340352, 'b2651456543b82f8090ec89f7dee3a014cb0b283', 60, 1, 1);
INSERT INTO source VALUES (55879, 1, '2012-07-03 08:01:57', '2012-07-03 08:01:57', 43908, 'Simacek, Radovan/Zlocin na Zlenicich hrade L.P. 1318/Simacek, Radovan - Zlocin na Zlenicich hrade L.P. 1318.doc', NULL, 5, 2395648, 'c3e8052dfef4acad956fa4c139782f99f3acbaeb', 80, 1, 1);
INSERT INTO source VALUES (55880, 1, '2012-07-03 08:01:57', '2012-07-03 08:01:57', 43908, 'Simacek, Radovan/Zlocin na Zlenicich hrade L.P. 1318/Simacek, Radovan - Zlocin na Zlenicich hrade L.P. 1318.pdb', NULL, 3, 235149, '5a1967704d82f4b11768f30425f2e238c6efce65', 20, 1, 1);
INSERT INTO source VALUES (55937, 1, '2012-07-03 08:02:12', '2012-07-03 08:02:12', 43933, 'Ubieto Arteta, Antonio/Dejiny Spanelska/Ubieto Arteta, Antonio - Dejiny Spanelska.docx', NULL, 16, 13472566, 'f3f6ddae322969677d0da4ba42d27058d8148c1a', 40, 1, 1);
INSERT INTO source VALUES (56003, 1, '2012-07-03 08:02:32', '2012-07-03 08:02:32', 43992, 'Lumley, Brian/Nekroskop/Nekroskop 12 - Prznitele/Lumley, Brian - Nekroskop 12 - Prznitele.doc', NULL, 5, 2678272, 'b7f10c4744f6bc45510bdcda0e98de62975205d6', 20, 1, 1);
INSERT INTO source VALUES (56540, 1, '2012-07-03 08:04:41', '2012-07-03 08:04:41', 43908, 'Simacek, Radovan/Zlocin na Zlenicich hrade L.P. 1318/Simacek, Radovan - Zlocin na Zlenicich hrade L.P. 1318 (1).doc', NULL, 5, 4567552, 'e8af145c866a259c0bf606cf8df0126faac8b6fb', 80, 1, 1);
INSERT INTO source VALUES (57677, 1, '2012-07-03 08:09:43', '2012-07-03 08:09:43', 45202, 'Anderson, Kevin J./Akta X/Akta X 5 - Protilatky/Anderson, Kevin J. - Akta X 5 - Protilatky.rtf', NULL, 4, 476090, '117a95bba4376d01ec3948085801ea2705d4ceca', 20, 1, 1);
INSERT INTO source VALUES (58070, 1, '2012-07-03 08:11:20', '2012-07-03 08:11:20', 45446, 'Lanczova, Lenka/Milenky a hrisnici/Lanczova, Lenka - Milenky a hrisnici.doc', NULL, 5, 1295872, '4f3a853eb8f1920ac425b18eb405a0a597014fb2', 40, 1, 1);
INSERT INTO source VALUES (58390, 1, '2012-07-03 08:12:40', '2012-07-03 08:12:40', 45643, 'Karasek ze Lvovic, Jiri/Romany tri magu/Romany tri magu 3 - Ganymedes/Karasek ze Lvovic, Jiri - Romany tri magu 3 - Ganymedes.doc', NULL, 5, 899584, '4a13c326ff84ae31d2a4f68fed0bcfcca04e585c', 40, 1, 1);
INSERT INTO source VALUES (58419, 1, '2012-07-03 08:12:47', '2012-07-03 08:12:47', 45668, 'Brittain, William/Pat litrov benzinu/Brittain, William - Pat litrov benzinu.docx', NULL, 16, 26667, 'c573fd040ab7ff12254c1a047075352ce7c30fb1', 90, 1, 1);
INSERT INTO source VALUES (59026, 1, '2012-07-03 08:15:13', '2012-07-03 08:15:13', 34513, 'Gemmell, David/Drenajska saga/Drenajska saga 1 - Legenda/Gemmell, David - Drenajska saga 1 - Legenda.mobi', NULL, 6, 673993, '0d395e259246a0c6814d521e820673fc06580807', 40, 1, 1);
INSERT INTO source VALUES (59077, 1, '2012-07-03 08:15:29', '2012-07-03 08:15:29', 46064, 'Gordon, Victoria/Laska a zakon/Gordon, Victoria - Laska a zakon.pdf', NULL, 1, 7881676, 'b581ab366aae996cb91f67a094c3a6837e52f73e', 0, 1, 1);
INSERT INTO source VALUES (59245, 1, '2012-07-03 08:16:15', '2012-07-03 08:16:15', 43908, 'Simacek, Radovan/Zlocin na Zlenicich hrade L.P. 1318/Simacek, Radovan - Zlocin na Zlenicich hrade L.P. 1318.mobi', NULL, 6, 1459801, 'c7fb0f41d2193c4cb7c697fcd11642e4b6ab32c6', 80, 1, 1);
INSERT INTO source VALUES (60310, 1, '2012-07-03 08:20:36', '2012-07-03 08:20:36', 46818, 'Adrian, Lara/Pulnocni rasa/Pulnocni rasa 1 - Polibek pulnoci/Adrian, Lara - Pulnocni rasa 1 - Polibek pulnoci.doc', NULL, 5, 1690624, '9a5c7007c8170210ba3ba7144a17bbd2c5cc6a7b', 40, 1, 1);
INSERT INTO source VALUES (61018, 1, '2012-07-03 08:23:27', '2012-07-03 08:23:27', 39072, 'Wells, Herbert George/Valka svetu a jine pribehy z neskutecna/Wells, Herbert George - Valka svetu a jine pribehy z neskutecna.mobi', NULL, 6, 897973, 'c1876709bf23e235c42a381fe780491ad820c628', 80, 1, 1);
INSERT INTO source VALUES (61766, 1, '2012-07-03 08:26:45', '2012-07-03 08:26:45', 47602, 'Rudis, Jaroslav/Konec punku v Helsinkach/Rudis, Jaroslav - Konec punku v Helsinkach.pdf', NULL, 1, 11108999, '3e3916952a7bc80f69c7f4ff892f3c09837c0c52', 0, 1, 1);
INSERT INTO source VALUES (61854, 1, '2012-07-03 08:27:03', '2012-07-03 08:27:03', 47602, 'Rudis, Jaroslav/Konec punku v Helsinkach/Rudis, Jaroslav - Konec punku v Helsinkach.docx', NULL, 16, 362778, 'da6a98db71d94f3ef894a0d1d38c15a7e545f0d1', 80, 1, 1);
INSERT INTO source VALUES (61867, 1, '2012-07-03 08:27:07', '2012-07-03 08:27:07', 47602, 'Rudis, Jaroslav/Konec punku v Helsinkach/Rudis, Jaroslav - Konec punku v Helsinkach.mobi', NULL, 6, 348601, 'a863fb3c38d189605d49974dc5ad3ea2715b1ec6', 70, 1, 1);
INSERT INTO source VALUES (62725, 1, '2012-07-03 08:30:46', '2012-07-03 08:30:46', 43023, 'Nienacki, Zbigniew/Pan Tragacik/Pan Tragacik 7 - Pan Tragacik a Kapitan Nemo/Nienacki, Zbigniew - Pan Tragacik 7 - Pan Tragacik a Kapitan Nemo.doc', NULL, 5, 6714368, '13bcb1e06dfa402a674c6408e3aed1d50a879318', 0, 1, 1);
INSERT INTO source VALUES (63062, 1, '2012-07-03 08:31:41', '2012-07-03 08:31:41', 45202, 'Anderson, Kevin J./Akta X/Akta X 5 - Protilatky/Anderson, Kevin J. - Akta X 5 - Protilatky.pdf', NULL, 1, 1267706, 'bf07f53c20b88574223eaed7682e31b8de9fbf7a', 40, 1, 1);
INSERT INTO source VALUES (63174, 1, '2012-07-03 08:32:10', '2012-07-03 08:32:10', 48552, 'Ruiz, Don Miguel/Styri dohody/Ruiz, Don Miguel - Styri dohody.pdf', NULL, 1, 1628177, '4dc80743d4c02d62a1723e43af611bb9fe6402c4', 80, 1, 1);
INSERT INTO source VALUES (63406, 1, '2012-07-03 08:32:59', '2012-07-03 08:32:59', 48728, 'James, Ellen/Laska k nepriteli/James, Ellen - Laska k nepriteli.pdf', NULL, 1, 8453506, '67fb904f0809d7504542e78767367d1ae5a71710', 0, 1, 1);
INSERT INTO source VALUES (63546, 1, '2012-07-03 08:33:40', '2012-07-03 08:33:40', 48818, 'Monroe, Lucy/Nevesty od Stredozemniho more/Nevesty od Stredozemniho more 2 - Spanelova milenka/Monroe, Lucy - Nevesty od Stredozemniho more 2 - Spanelova milenka.doc', NULL, 5, 534016, 'f73fc9767758604adc9b35996c7614611f7ca265', 60, 1, 1);
INSERT INTO source VALUES (64067, 1, '2012-07-03 08:35:59', '2012-07-03 08:35:59', 49134, 'Repka, Marian/Fenomen mudrost/Repka, Marian - Fenomen mudrost.pdf', NULL, 1, 8441339, 'c6651c5051112e9e138f0a0c5d89cbb7a350eff0', 0, 1, 1);
INSERT INTO source VALUES (64069, 1, '2012-07-03 08:35:59', '2012-07-03 08:35:59', 49134, 'Repka, Marian/Fenomen mudrost/Repka, Marian - Fenomen mudrost.doc', NULL, 5, 749056, '841e91c41fd645491f0bbc820cd126e58e1e70b2', 0, 1, 1);
INSERT INTO source VALUES (64073, 1, '2012-07-03 08:36:00', '2012-07-03 08:36:00', 49138, 'Peters, Ellis/Pripady bratra Cadfaela/Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji/Peters, Ellis - Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji.doc', NULL, 5, 1185280, 'e0d1db4367ec285b69396fb9168ff7ce6b646ec9', 40, 1, 1);
INSERT INTO source VALUES (64292, 1, '2012-07-03 08:36:53', '2012-07-03 08:36:53', 46818, 'Adrian, Lara/Pulnocni rasa/Pulnocni rasa 1 - Polibek pulnoci/Adrian, Lara - Pulnocni rasa 1 - Polibek pulnoci (1).doc', NULL, 5, 1509376, '3e0d5883e9e2dcc5da4de53f126de5fd36fd3f87', 80, 1, 1);
INSERT INTO source VALUES (65049, 1, '2012-07-03 08:40:12', '2012-07-03 08:40:12', 49667, 'Giffin, Emily/Something Borrowed/Giffin, Emily - Something Borrowed.mobi', NULL, 6, 483227, '4271061ceaa99d377c471296d2fe3ad4735b4474', 20, 1, 1);
INSERT INTO source VALUES (65050, 1, '2012-07-03 08:40:12', '2012-07-03 08:40:12', 49667, 'Giffin, Emily/Something Borrowed/Giffin, Emily - Something Borrowed.epub', NULL, 8, 339239, '272601965d3cfdce14fe8e166e188464027b6683', 10, 1, 1);
INSERT INTO source VALUES (65461, 1, '2012-07-03 08:41:45', '2012-07-03 08:41:45', 49138, 'Peters, Ellis/Pripady bratra Cadfaela/Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji/Peters, Ellis - Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji.mobi', NULL, 6, 371387, '1bebec5d5caa0a3a1bc051fb851aaf086dc5c6e7', 80, 1, 1);
INSERT INTO source VALUES (65727, 1, '2012-07-03 08:42:57', '2012-07-03 08:42:57', 50118, 'Gill, Judy/Nezny dobyvatel/Gill, Judy - Nezny dobyvatel.doc', NULL, 5, 6883328, 'a939648f1a3ab04dd974461182166130c20d9ef4', 20, 1, 1);
INSERT INTO source VALUES (66329, 1, '2012-07-03 08:45:30', '2012-07-03 08:45:30', 50495, 'Gibson, Walter B./Uplna prirucka triku a kouzel pro zacatecniky/Gibson, Walter B. - Uplna prirucka triku a kouzel pro zacatecniky.djvu', NULL, 10, 3254676, 'b8ef7087d2a9ef16f509a522f7d10aade19f759b', 0, 1, 1);
INSERT INTO source VALUES (66401, 1, '2012-07-03 08:45:46', '2012-07-03 08:45:46', 50556, 'Barton, Beverly/Tajna zbran/Barton, Beverly - Tajna zbran.doc', NULL, 5, 993280, '9fb0cf99eccea0bd18398a50651bbdd954e656e0', 40, 1, 1);
INSERT INTO source VALUES (66504, 1, '2012-07-03 08:46:05', '2012-07-03 08:46:05', 50641, 'Kovanic, Jan/Kinoautomat svet/Kovanic, Jan - Kinoautomat svet.docx', NULL, 16, 25450, '586f988e5869d49294458a79e39095e7f7028ed9', 10, 1, 1);
INSERT INTO source VALUES (66640, 1, '2012-07-03 08:46:39', '2012-07-03 08:46:39', 50729, 'James, Peter/Roy Grace/Roy Grace 4 - Po stopach mrtveho/James, Peter - Roy Grace 4 - Po stopach mrtveho.doc', NULL, 5, 2103808, 'caea1222e80009957420c18c02c435504c854c7e', 80, 1, 1);
INSERT INTO source VALUES (66838, 1, '2012-07-03 08:47:19', '2012-07-03 08:47:19', 50868, 'Jezek, Jan/Obycejny den/Jezek, Jan - Obycejny den.docx', NULL, 16, 43274, '55377ee4237cf7e2a771ea2594f96bc7c90b1776', 10, 1, 1);
INSERT INTO source VALUES (66955, 1, '2012-07-03 08:47:45', '2012-07-03 08:47:45', 50935, 'Mandulova, Katerina/Vladivostop/Mandulova, Katerina - Vladivostop.djvu', NULL, 10, 6475335, 'c625d0f0d078ea05969a0a67bff67d541aed29cf', 0, 1, 1);
INSERT INTO source VALUES (67523, 1, '2012-07-03 08:50:02', '2012-07-03 08:50:02', 51267, 'Pludra, Benno/Tambari/Pludra, Benno - Tambari.doc', NULL, 5, 3828736, '3968905a02d97a895e63eb6bab9b6e2374acf49c', 40, 1, 1);
INSERT INTO source VALUES (67552, 1, '2012-07-03 08:50:08', '2014-09-06 20:48:01', 56253, 'Pecinovsky, Josef/Kroniky nove Zeme/Kroniky nove Zeme 1 - Vejce s ozvenou/Pecinovsky, Josef - Kroniky nove Zeme 1 - Vejce s ozvenou.pdb', NULL, 3, 213347, 'dc4a3e40f28f8cca73e630ac5bc1093c0a688d7c', 10, 1, 1);
INSERT INTO source VALUES (67760, 1, '2012-07-03 08:51:03', '2012-07-03 08:51:03', 51398, 'Sharpe, Tom/Henry Wilt/Henry Wilt 1 - Novy zivot Henryho Wilta/Sharpe, Tom - Henry Wilt 1 - Novy zivot Henryho Wilta.docx', NULL, 16, 1525883, 'fd313bc9f2c0597fa785cf25472d49af1aead04c', 20, 1, 1);
INSERT INTO source VALUES (67877, 1, '2012-07-03 08:51:33', '2012-07-03 08:51:33', 51460, 'Stych, Jiri/Kral termitu/Stych, Jiri - Kral termitu.doc', NULL, 5, 1100800, '5ddb515a5bbdce39efd86ebfd03f52c1c738581c', 40, 1, 1);
INSERT INTO source VALUES (68269, 1, '2012-08-03 13:13:24', '2012-08-03 13:13:24', 49138, 'Peters, Ellis/Pripady bratra Cadfaela/Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji/Peters, Ellis - Pripady bratra Cadfaela 5 - Malomocny u svateho Jilji.odt', NULL, 9, 191586, 'ddf29d0d2300cf4398ddc47306ed18dd86abb4eb', 70, 1, 1);
INSERT INTO source VALUES (68669, 1, '2012-08-03 13:14:37', '2012-08-03 13:14:37', 51398, 'Sharpe, Tom/Henry Wilt/Henry Wilt 1 - Novy zivot Henryho Wilta/Sharpe, Tom - Henry Wilt 1 - Novy zivot Henryho Wilta (1).docx', NULL, 16, 993338, 'd722d14a1ec225f4ad4fad24b75ce807bfb9c1fd', 40, 1, 1);
INSERT INTO source VALUES (68738, 1, '2012-08-03 13:14:51', '2012-08-03 13:14:51', 51962, 'Franz, Raymond/Hledani krestanske svobody/Franz, Raymond - Hledani krestanske svobody.pdf', NULL, 1, 7715766, 'e339cc80b347621c441aed05a5f81e9943e3e752', 0, 1, 1);
INSERT INTO source VALUES (69214, 1, '2012-08-03 13:16:10', '2012-08-03 13:16:10', 51460, 'Stych, Jiri/Kral termitu/Stych, Jiri - Kral termitu.djvu', NULL, 10, 2636699, '0131ab743a17b2fe7e02dbf2c97e09b09b489424', 0, 1, 1);
INSERT INTO source VALUES (69580, 1, '2012-08-03 13:17:10', '2012-08-03 13:17:10', 52468, 'Evarts, Hal George/Pravo tomahavku 02/Evarts, Hal George - Pravo tomahavku 02.doc', NULL, 5, 177152, '459856247fd9114e2aa089e7d5e9baf4fd7f4613', 60, 1, 1);
INSERT INTO source VALUES (69745, 1, '2012-08-03 13:17:43', '2012-08-03 13:17:43', 52594, 'Walker, Hugh/Magira/Magira 2 - Vecna bitva/Walker, Hugh - Magira 2 - Vecna bitva.doc', NULL, 5, 1491456, 'fd08a96e9c8a033db48fdb18c01690a8b29a04ae', 10, 1, 1);
INSERT INTO source VALUES (70040, 1, '2012-08-03 13:18:27', '2012-08-03 13:18:27', 52846, 'Leclaire, Day/Thorsen Brothers/Thorsen Brothers 1 - Jablicko lasky/Leclaire, Day - Thorsen Brothers 1 - Jablicko lasky.doc', NULL, 5, 903168, '4a91945d516e83e34ef905cfdf4693f2216bc094', 40, 1, 1);
INSERT INTO source VALUES (70211, 1, '2012-08-03 13:18:54', '2012-08-03 13:18:54', 52963, 'Hamilton, Laurell Kaye/Anita Blake/Anita Blake 9 - Obsidianovy motyl/Hamilton, Laurell Kaye - Anita Blake 9 - Obsidianovy motyl.doc', NULL, 5, 3621888, '28c9c99c43d2e5e4afa9ef09825c956fb765ed44', 80, 1, 1);
INSERT INTO source VALUES (70327, 1, '2012-08-03 13:19:13', '2012-08-03 13:19:13', 52846, 'Leclaire, Day/Thorsen Brothers/Thorsen Brothers 1 - Jablicko lasky/Leclaire, Day - Thorsen Brothers 1 - Jablicko lasky.djvu', NULL, 10, 1427584, '5d1115780dcb094d631619894f616aa4258f4fb3', 0, 1, 1);
INSERT INTO source VALUES (72020, 1, '2012-09-27 10:34:45', '2012-09-27 10:34:45', 53722, 'Kellerman, Jonathan/Alex Delaware/Alex Delaware 17 - Ledove srdce/Kellerman, Jonathan - Alex Delaware 17 - Ledove srdce.docx', NULL, 16, 662605, 'c75381c8279ddf498da471a3f698b1e0fb95db64', 20, 1, 1);
INSERT INTO source VALUES (72201, 1, '2012-10-05 18:35:56', '2012-10-05 18:35:56', 53819, 'Dark, Jason/Na stope hruzy/Na stope hruzy 81 - Pulnocni pripitek/Dark, Jason - Na stope hruzy 81 - Pulnocni pripitek.doc', NULL, 5, 695296, '6164c95867f0666bdf21e5cc3fd700438fe52ac6', 20, 1, 1);
INSERT INTO source VALUES (72387, 1, '2012-10-05 18:37:04', '2012-10-05 18:37:04', 53963, 'Cartland, Barbara/Uveznena laska/Cartland, Barbara - Uveznena laska.docx', NULL, 16, 485317, '9c0b59345959c200338c0507762f56e38ba99ada', 40, 1, 1);
INSERT INTO source VALUES (72660, 1, '2012-10-14 10:30:07', '2012-10-14 10:30:07', 54183, 'Eugenides, Jeffrey/Middlesex/Eugenides, Jeffrey - Middlesex.epub', NULL, 8, 536705, 'de1db43d80c63635c581c0506e2996102e83fe55', NULL, 1, 1);
INSERT INTO source VALUES (73455, 1, '2012-11-19 19:15:02', '2012-11-19 19:15:02', 54788, 'Allen, Louise/Dzentlmen piratem/Allen, Louise - Dzentlmen piratem.docx', NULL, 16, 587005, '80040397da5b438370cf1bfea994a80312956b04', 20, 1, 1);
INSERT INTO source VALUES (73674, 1, '2012-11-19 19:16:11', '2012-11-19 19:16:11', 54933, 'Dark, Jason/Na stope hruzy/Na stope hruzy 190 - Vykrik v hrobce/Dark, Jason - Na stope hruzy 190 - Vykrik v hrobce.doc', NULL, 5, 835072, 'cdbe717e53226a6361495a833dbc4c46751a3217', 20, 1, 1);
INSERT INTO source VALUES (74027, 1, '2012-12-22 06:30:47', '2012-12-22 06:30:47', 55153, 'Dark, Jason/Na stope hruzy/Na stope hruzy 203 - Sam proti peklu/Dark, Jason - Na stope hruzy 203 - Sam proti peklu.doc', NULL, 5, 505856, '11ef59a1b6610071d1c99d232afda107ad1ff750', 20, 1, 1);
INSERT INTO source VALUES (74100, 1, '2012-12-22 06:30:54', '2012-12-22 06:30:54', 55217, 'Dark, Jason/Na stope hruzy/Na stope hruzy 316 - Satanova reka/Dark, Jason - Na stope hruzy 316 - Satanova reka.doc', NULL, 5, 542720, 'f7c2a170a0b508bae82d475f562311bfcd761ab6', 20, 1, 1);
INSERT INTO source VALUES (74312, 1, '2012-12-22 08:22:46', '2012-12-22 08:22:46', 55325, 'Vondruska, Vlastimil/Letopisy kralovske komory/Letopisy kralovske komory 1 - Letopisy kralovske komory I./Vondruska, Vlastimil - Letopisy kralovske komory 1 - Letopisy kralovske komory I..docx', NULL, 16, 733332, 'f837a2e5931befe44bb4bcbeef5864e924f6dd2e', NULL, 1, 1);
INSERT INTO source VALUES (75514, 1, '2013-02-10 09:15:52', '2013-02-10 09:15:52', 56159, 'Adornetto, Alexandra/Zar/Zar 2 - Zasveti/Adornetto, Alexandra - Zar 2 - Zasveti.pdf', NULL, 1, 6554695, '37207ad2c4718de69afcb350ccb2d65e2b2eeb5f', 0, 1, 1);
INSERT INTO source VALUES (75692, 1, '2013-02-10 09:16:29', '2013-02-10 09:16:29', 56253, 'Pecinovsky, Josef/Kroniky nove Zeme/Kroniky nove Zeme 1 - Vejce s ozvenou 1991-11/Pecinovsky, Josef - Kroniky nove Zeme 1 - Vejce s ozvenou 1991-11.doc', NULL, 5, 1769984, '90280c852ea87a09d1318226bbb6e256b342a6ac', 40, 1, 1);
INSERT INTO source VALUES (75772, 1, '2013-02-10 09:16:45', '2013-02-10 09:16:45', 56297, 'Orwig, Sara/Odstupne za lasku/Odstupne za lasku 2 - Pozvani  na vikend/Orwig, Sara - Odstupne za lasku 2 - Pozvani  na vikend.doc', NULL, 5, 1834496, '3492abaf1920c0c1da2088e8ec533173eb541797', 20, 1, 1);
INSERT INTO source VALUES (75952, 1, '2013-02-22 07:36:42', '2013-02-22 07:36:42', 56396, 'Caka, Jan/Stredni Brdy - krajina neznama/Caka, Jan - Stredni Brdy - krajina neznama.pdf', NULL, 1, 18816334, 'ac46b6c1a0058d071694021f1079c698279d4ce5', 0, 1, 1);
INSERT INTO source VALUES (76207, 1, '2013-03-03 07:35:09', '2013-03-03 07:35:09', 56528, 'Selinko, Annemarie/Desiree/Selinko, Annemarie - Desiree (1).docx', NULL, 16, 834480, '56534d260bc2dead8878f74ca0c81dbdf85ac0d8', 10, 1, 1);
INSERT INTO source VALUES (76437, 1, '2013-03-16 11:46:14', '2013-03-16 11:46:14', 42163, 'Hall, Robert Lee/Pribehy Sherlocka Holmese (Jota)/Pribehy Sherlocka Holmese (Jota) 14 - Sherlock Holmes odchazi/Hall, Robert Lee - Pribehy Sherlocka Holmese (Jota) 14 - Sherlock Holmes odchazi.djvu', NULL, 10, 3218144, 'cc980d2d662c092640eb8b94117663b97b9b43fe', 0, 1, 1);
INSERT INTO source VALUES (76805, 1, '2013-03-16 11:47:38', '2013-03-16 11:47:38', 56885, 'Tepes, Vlad/Prva krv/Tepes, Vlad - Prva krv.docx', NULL, 16, 19976, '8267ba3d359eac35f8b1452d1dfe4bc311b69c33', 10, 1, 1);
INSERT INTO source VALUES (77075, 1, '2013-03-29 08:14:24', '2013-03-29 08:14:24', 57113, 'Hofman, Vladimir/O ludoch a jastericiach/Hofman, Vladimir - O ludoch a jastericiach.docx', NULL, 16, 17471, '4d2397626890634340aa6747ebfe33348aaad76b', 10, 1, 1);
INSERT INTO source VALUES (77209, 1, '2013-03-29 08:15:07', '2013-03-29 08:15:07', 57216, 'Stanek, William R./Microsoft Exchange Server 2003/Stanek, William R. - Microsoft Exchange Server 2003.djvu', NULL, 10, 11519680, '6c1dfb42f4dd1c0a2f4c6bfb7ad77654d1655242', 0, 1, 1);
INSERT INTO source VALUES (78067, 1, '2013-04-26 19:27:20', '2013-04-26 19:27:20', 55325, 'Vondruska, Vlastimil/Letopisy kralovske komory/Letopisy kralovske komory 1 - Letopisy kralovske komory I./Vondruska, Vlastimil - Letopisy kralovske komory 1 - Letopisy kralovske komory I..doc', NULL, 5, 1782784, '769ae43a0056f8be636b5581cf0e90734187f5b0', 80, 1, 1);
INSERT INTO source VALUES (78440, 1, '2013-05-04 07:33:52', '2013-05-04 07:33:52', 57939, 'Kaku, Michio/Paralelni svety/Kaku, Michio - Paralelni svety.djvu', NULL, 10, 3791637, 'b816666fb1014583d9f99ec1027630010b8e8ab5', 0, 1, 1);
INSERT INTO source VALUES (78974, 1, '2013-05-31 08:16:27', '2013-05-31 08:16:27', 58235, 'Albieri, Pavel/Z ruzneho siku/Albieri, Pavel - Z ruzneho siku.djvu', NULL, 10, 7787847, '83e12eadeb603e5ea2163a2edf162db7436adece', 0, 1, 1);
INSERT INTO source VALUES (79729, 1, '2013-06-28 21:32:11', '2013-06-28 21:32:11', 58694, 'Troska, Jan Matzal/Zapas s nebem/Zapas s nebem 2 - Podobni bohum/Troska, Jan Matzal - Zapas s nebem 2 - Podobni bohum.doc', NULL, 5, 5241344, '210f401ec64367a2a6da47aa11546190d1686bcb', 40, 1, 1);
INSERT INTO source VALUES (79735, 1, '2013-06-28 21:32:12', '2013-06-28 21:32:12', 58699, 'Andrlik, Frantisek Josef/Za umenim/Andrlik, Frantisek Josef - Za umenim.djvu', NULL, 10, 1545174, 'b6833693e7a9276ff12c7b9c6f5f9d22c6eb7e20', 0, 1, 1);
INSERT INTO source VALUES (80148, 1, '2013-07-14 11:06:44', '2013-07-14 11:06:44', 58909, 'May, Karl/Tajemstvi stareho rodu/Tajemstvi stareho rodu 3 - V osidlech temnych intrik/May, Karl - Tajemstvi stareho rodu 3 - V osidlech temnych intrik.epub', NULL, 8, 342518, 'e60f3cb75cd843ad4dad6217572fdb41326ed21b', 20, 1, 1);
INSERT INTO source VALUES (80149, 1, '2013-07-14 11:06:44', '2013-07-14 11:06:44', 58909, 'May, Karl/Tajemstvi stareho rodu/Tajemstvi stareho rodu 3 - V osidlech temnych intrik/May, Karl - Tajemstvi stareho rodu 3 - V osidlech temnych intrik.mobi', NULL, 6, 852585, 'b3cb8122437610f34feb0197a9b7e777baa7f064', 20, 1, 1);
INSERT INTO source VALUES (80379, 1, '2013-08-11 14:04:09', '2013-08-11 14:04:09', 53722, 'Kellerman, Jonathan/Alex Delaware/Alex Delaware 17 - Ledove srdce/Kellerman, Jonathan - Alex Delaware 17 - Ledove srdce (1).docx', NULL, 16, 1440030, '64ed0eda508f5031fa2a7b87805b618806c69e07', 40, 1, 1);
INSERT INTO source VALUES (80425, 1, '2013-08-11 14:04:27', '2013-08-11 14:04:27', 58909, 'May, Karl/Tajemstvi stareho rodu/Tajemstvi stareho rodu 3 - V osidlech temnych intrik/May, Karl - Tajemstvi stareho rodu 3 - V osidlech temnych intrik.doc', NULL, 5, 2082816, '343832d25e4f8fbf388dd93789cbcee1cd7d845e', 20, 1, 1);
INSERT INTO source VALUES (81691, 1, '2013-10-31 18:17:36', '2013-10-31 18:17:36', 56528, 'Selinko, Annemarie/Desiree/Selinko, Annemarie - Desiree.odt', NULL, 9, 615436, '9843b912eab414e65878134097661fa5ab122be9', 10, 1, 1);
INSERT INTO source VALUES (81692, 1, '2013-10-31 18:17:36', '2013-10-31 18:17:36', 56528, 'Selinko, Annemarie/Desiree/Selinko, Annemarie - Desiree (1).mobi', NULL, 6, 1260441, '5fd7d471efed8ce7f1f499c8a4b82a6ceeba8ccf', 10, 1, 1);
INSERT INTO source VALUES (82067, 1, '2013-11-01 07:05:39', '2013-11-01 07:05:39', 59887, 'Brown, Graham/Danielle Laidlawova/Danielle Laidlawova 2 - Cerne slunce/Brown, Graham - Danielle Laidlawova 2 - Cerne slunce.djvu', NULL, 10, 4430828, 'd0001d651218d86e66a4b34ded7d8416d049928a', 0, 1, 1);
INSERT INTO source VALUES (82074, 1, '2013-11-01 07:05:40', '2013-11-01 07:05:40', 59887, 'Brown, Graham/Danielle Laidlawova/Danielle Laidlawova 2 - Cerne slunce/Brown, Graham - Danielle Laidlawova 2 - Cerne slunce.doc', NULL, 5, 2004992, 'e1327427dc84883f220b030a1e645613ef040181', 40, 1, 1);
INSERT INTO source VALUES (82075, 1, '2013-11-01 07:05:40', '2013-11-01 07:05:40', 59887, 'Brown, Graham/Danielle Laidlawova/Danielle Laidlawova 2 - Cerne slunce/Brown, Graham - Danielle Laidlawova 2 - Cerne slunce (1).djvu', NULL, 10, 3764333, '52d898af5366df9f7d7651e15c8f2815ef9e4064', 0, 1, 1);
INSERT INTO source VALUES (82585, 1, '2013-11-04 20:48:41', '2013-11-04 20:48:41', 60209, 'Saskova, Lucia/Zlatokopka/Saskova, Lucia - Zlatokopka.doc', NULL, 5, 9934336, '246a73ee359beb99548e5f98497f334e426416ef', 40, 1, 1);
INSERT INTO source VALUES (82586, 1, '2013-11-04 20:48:43', '2013-11-04 20:48:43', 60209, 'Saskova, Lucia/Zlatokopka/Saskova, Lucia - Zlatokopka.pdf', NULL, 1, 6104308, '6618a98e15104121ed7272d8f1b0e08f6c808130', 0, 1, 1);
INSERT INTO source VALUES (82902, 1, '2013-11-15 19:01:05', '2013-11-15 19:01:05', 60406, 'Benchley, Peter/Hlubina/Benchley, Peter - Hlubina.docx', NULL, 16, 312134, '510e63dea8e5b4694d0b07696a832c29675e330c', 40, 1, 1);
INSERT INTO source VALUES (84241, 1, '2014-02-06 16:46:51', '2014-02-06 16:46:51', 61048, 'Hartley, Andrew James/Zlomena pecet/Hartley, Andrew James - Zlomena pecet.pdf', NULL, 1, 6072671, '1f023dfe9f7a61b6a15403a321c0617788c469e1', 0, 1, 1);
INSERT INTO source VALUES (84244, 1, '2014-02-06 16:46:52', '2014-02-06 16:46:52', 61048, 'Hartley, Andrew James/Zlomena pecet/Hartley, Andrew James - Zlomena pecet.docx', NULL, 16, 636640, '056f47a5e009aaa9a9e92e416da60d6c521f04b9', 20, 1, 1);
INSERT INTO source VALUES (84477, 1, '2014-02-06 16:47:43', '2014-02-06 16:47:43', 37116, 'Storch, Eduard/Bronzovy poklad/Storch, Eduard - Bronzovy poklad.pdf', NULL, 1, 897393, 'c01da50f7e29e7c1b8b16ca1e19246cb12c3c8d8', 10, 1, 1);
INSERT INTO source VALUES (84803, 1, '2014-02-24 19:03:53', '2014-02-24 19:03:53', 56253, 'Pecinovsky, Josef/Kroniky nove Zeme/Kroniky nove Zeme 1 - Vejce s ozvenou 1991-11/Pecinovsky, Josef - Kroniky nove Zeme 1 - Vejce s ozvenou 1991-11.djvu', NULL, 10, 4441687, 'bf1dc194bf22260223255ac1c9020eb0034e852c', 0, 1, 1);
INSERT INTO source VALUES (85749, 1, '2014-03-28 08:48:40', '2014-03-28 08:48:40', 61800, 'Cordonnier, Marie/Velka lez/Cordonnier, Marie - Velka lez.doc', NULL, 5, 407010, '891e323ab4ebc48addaf58e7a2e438633894ff34', 20, 1, 1);
INSERT INTO source VALUES (86037, 1, '2014-04-13 11:00:56', '2014-04-13 11:00:56', 61944, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome.docx', NULL, 16, 9594762, 'c496d84066a0024cd21864018d2279381607f1ce', 40, 1, 1);
INSERT INTO source VALUES (86058, 1, '2014-05-06 10:32:01', '2014-05-06 10:32:01', 61944, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome.pdf', NULL, 1, 11819150, '4f7871bfeaafe20e39afb33b8d60731f4dfbb436', 0, 1, 1);
INSERT INTO source VALUES (86060, 1, '2014-05-06 10:32:02', '2014-05-06 10:32:02', 61944, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome.epub', NULL, 8, 3147900, '802d2b831271af2fb8fc08e068553cb2cb8b09b4', 20, 1, 1);
INSERT INTO source VALUES (86063, 1, '2014-05-06 10:32:02', '2014-05-06 10:32:02', 61944, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome (1).docx', NULL, 16, 9596984, '7e591808ca13c6eb858a5c6fec70be074bee4f34', 40, 1, 1);
INSERT INTO source VALUES (86671, 1, '2014-05-17 14:36:08', '2014-05-17 14:36:08', 62241, 'Gilmore, Robert/Alenka v risi kvant - Alegorie kvantove fyziky/Gilmore, Robert - Alenka v risi kvant - Alegorie kvantove fyziky.epub', NULL, 8, 1079913, '1d7b2795666a03a3c2f5ccbad239b5a78d25d08f', 40, 1, 1);
INSERT INTO source VALUES (87362, 1, '2014-06-30 17:45:40', '2014-06-30 17:45:40', 62546, 'Dalton, Margot/Valentinky 2000 2/Dalton, Margot - Valentinky 2000 2.docx', NULL, 16, 660674, '5bad65237c003599ebc93954693278aaa7800031', 40, 1, 1);
INSERT INTO source VALUES (87490, 1, '2014-07-19 14:58:22', '2014-07-19 14:58:22', 62616, 'Taylor, David/Veterinarem v zoo/Taylor, David - Veterinarem v zoo.doc', NULL, 5, 2567168, 'c506f64e9ebb88b57b545ab97cf8bafaab480835', 20, 1, 1);
INSERT INTO source VALUES (88299, 1, '2014-08-31 18:29:20', '2014-08-31 18:29:20', 62974, 'Tibitanzl, Jiri/Krvave rude slunce/Tibitanzl, Jiri - Krvave rude slunce.djvu', NULL, 10, 924609, '375423f508400bfd8177122c3c14d54477f1e2cb', 0, 1, 1);
INSERT INTO source VALUES (88300, 1, '2014-08-31 18:29:20', '2014-08-31 18:29:20', 62974, 'Tibitanzl, Jiri/Krvave rude slunce/Tibitanzl, Jiri - Krvave rude slunce.doc', NULL, 5, 502272, 'caa79eda4cf0d74a103d05d5579b387abf488854', 40, 1, 1);
INSERT INTO source VALUES (89178, 1, '2014-11-03 17:42:05', '2014-11-03 17:42:05', 63404, 'Lindsay, Yvonne/Cesty osudu/Svadeni z pomsty/Lindsay, Yvonne - Cesty osudu/Svadeni z pomsty.doc', NULL, 5, 3294720, '815f4541c17caba62c7f0aa38e2539b0f2a7fa37', 20, 1, 1);
INSERT INTO source VALUES (90344, 1, '2014-12-20 12:21:54', '2014-12-20 12:21:54', 46818, 'Adrian, Lara/Pulnocni rasa/Pulnocni rasa 1 - Polibek pulnoci/Adrian, Lara - Pulnocni rasa 1 - Polibek pulnoci.epub', NULL, 8, 787046, '8c15cb5d194ab6cc22c054685d9666a683b18603', 80, 1, 1);
INSERT INTO source VALUES (91602, 1, '2015-02-15 09:10:16', '2015-02-15 09:10:16', 64619, 'Bacigalupi, Paolo/Potopena mesta/Bacigalupi, Paolo - Potopena mesta.djvu', NULL, 10, 4487582, 'd4eea375b0888784a32266abe148b3388f076110', 0, 1, 1);
INSERT INTO source VALUES (91603, 1, '2015-02-15 09:10:16', '2015-02-15 09:10:16', 64619, 'Bacigalupi, Paolo/Potopena mesta/Bacigalupi, Paolo - Potopena mesta.pdf', NULL, 1, 8502271, '58bc7fcb93493d916b583742d54b9a90f96d61e3', 0, 1, 1);
INSERT INTO source VALUES (91606, 1, '2015-02-15 09:10:17', '2015-02-15 09:10:17', 64619, 'Bacigalupi, Paolo/Potopena mesta/Bacigalupi, Paolo - Potopena mesta.docx', NULL, 16, 1003695, '716652b4792b0eab0c5c8c036d53d5f36c5e7624', 40, 1, 1);
INSERT INTO source VALUES (91712, 1, '2015-02-15 09:10:42', '2015-02-15 09:10:42', 50556, 'Barton, Beverly/Tajna zbran/Barton, Beverly - Tajna zbran.pdf', NULL, 1, 10547352, '390109b66b0d1649b3f6dbe90a8c171ff78c5436', 0, 1, 1);
INSERT INTO source VALUES (91875, 1, '2015-03-19 17:50:05', '2015-03-19 17:50:05', 64726, 'Lenormand, Frederic/Nove pripady soudce Ti/Nove pripady soudce Ti 6 - Smrt cinskeho kuchare/Lenormand, Frederic - Nove pripady soudce Ti 6 - Smrt cinskeho kuchare.doc', NULL, 5, 1086464, '1d264572bdfe243061570772d8fc7156269a9441', 40, 1, 1);
INSERT INTO source VALUES (92241, 1, '2015-03-19 17:55:23', '2015-03-19 17:55:23', 46064, 'Gordon, Victoria/Laska a zakon/Gordon, Victoria - Laska a zakon.doc', NULL, 5, 581120, '9d879bdd0fe80478ca5f5e5734179b961c977522', 20, 1, 1);
INSERT INTO source VALUES (92274, 1, '2015-03-19 17:55:34', '2015-03-19 17:55:34', 64935, 'Neels, Betty/Miluji te neustale - Polibky z Nizozemi/Neels, Betty - Miluji te neustale - Polibky z Nizozemi.doc', NULL, 5, 2522112, 'a18f1c75c4994a62b92ed4d48bb0297d3943bc99', 20, 1, 1);
INSERT INTO source VALUES (92314, 1, '2015-03-19 17:55:40', '2015-03-19 17:55:40', 64957, 'McEwan, Ian/Pohostinnost cudzincov/McEwan, Ian - Pohostinnost cudzincov.pdf', NULL, 1, 2295148, '92fb495a044c7592398f12b25a43528f7ae5da8a', 0, 1, 1);
INSERT INTO source VALUES (92510, 1, '2015-05-04 21:27:50', '2015-05-04 21:27:50', 65066, 'Neff, Vladimir/Maly velikan/Neff, Vladimir - Maly velikan.docx', NULL, 16, 4555030, 'ef529fb401770d1af940ed2a5eacbfdd2332d581', 40, 1, 1);
INSERT INTO source VALUES (92511, 1, '2015-05-04 21:27:51', '2015-05-04 21:27:51', 65066, 'Neff, Vladimir/Maly velikan/Neff, Vladimir - Maly velikan.djvu', NULL, 10, 11073310, '262a833c10be289834b381818533f3d3c6ce3029', 0, 1, 1);
INSERT INTO source VALUES (94097, 1, '2015-08-30 11:13:12', '2015-08-30 11:13:12', 65824, 'Mills, Kyle/Faktor strachu/Mills, Kyle - Faktor strachu.pdf', NULL, 1, 5787421, 'a618744692cdd2a924960117400f26fd6252610d', 0, 1, 1);
INSERT INTO source VALUES (94098, 1, '2015-08-30 11:13:12', '2015-08-30 11:13:12', 65824, 'Mills, Kyle/Faktor strachu/Mills, Kyle - Faktor strachu.mobi', NULL, 6, 1477379, '882db159f19c8c5689682c8600fd79da8b52207f', 20, 1, 1);
INSERT INTO source VALUES (94099, 1, '2015-08-30 11:13:12', '2015-08-30 11:13:12', 65824, 'Mills, Kyle/Faktor strachu/Mills, Kyle - Faktor strachu.docx', NULL, 16, 3489158, '2a5636ec9f74e3110e54db087624de85f1eadaf7', 20, 1, 1);
INSERT INTO source VALUES (94631, 1, '2015-08-30 11:14:44', '2015-08-30 11:14:44', 65975, 'Hallenga, Uwe/Mala vetrna elektrarna - Navod ke stavbe s konstrukcnimi vykresy/Hallenga, Uwe - Mala vetrna elektrarna - Navod ke stavbe s konstrukcnimi vykresy.pdf', NULL, 1, 4863144, '4d5ac85b3ef077a74fd0665b0228dd100218bb4d', 40, 1, 1);
INSERT INTO source VALUES (95931, 1, '2015-12-27 09:21:56', '2015-12-27 09:21:56', 66634, 'Hodkin, Michelle/Mara Dyer/Mara Dyer 2 - Promena Mary Dyerove/Hodkin, Michelle - Mara Dyer 2 - Promena Mary Dyerove.djvu', NULL, 10, 9077041, '322a35d9d3787324aff87a5944215b8381cd96e7', 0, 1, 1);
INSERT INTO source VALUES (95932, 1, '2015-12-27 09:21:56', '2015-12-27 09:21:56', 66634, 'Hodkin, Michelle/Mara Dyer/Mara Dyer 2 - Promena Mary Dyerove/Hodkin, Michelle - Mara Dyer 2 - Promena Mary Dyerove.docx', NULL, 16, 589818, '63d61ff9be199800699b83b82b728dcb04cd04f5', 40, 1, 1);
INSERT INTO source VALUES (95997, 1, '2015-12-27 09:22:12', '2015-12-27 09:22:12', 66677, 'Valentine, Zena/Svatecni nevesta/Valentine, Zena - Svatecni nevesta.docx', NULL, 16, 390163, 'd379328c1be5634b90cdb9781576fc6a554b6f7d', 40, 1, 1);
INSERT INTO source VALUES (96248, 1, '2015-12-27 09:23:13', '2015-12-27 09:23:13', 66804, 'Druon, Maurice/Prekliati krali 7 - Ked kral prehra Francuzsko/Druon, Maurice - Prekliati krali 7 - Ked kral prehra Francuzsko.docx', NULL, 16, 1278903, '442b78820aa5fa31e7b3b8dbeb6a83d3e8f01910', 40, 1, 1);
INSERT INTO source VALUES (97016, 1, '2016-02-05 08:39:49', '2016-02-05 08:39:49', 67157, 'Frankl, Viktor/Vule ke smyslu - Vybrane prednasky o logoterapii./Frankl, Viktor - Vule ke smyslu - Vybrane prednasky o logoterapii..docx', NULL, 16, 1319423, '8161b23030735110c7af17bc082fdb4a6512e90a', 10, 1, 1);
INSERT INTO source VALUES (97251, 1, '2016-02-05 08:40:32', '2016-02-05 08:40:32', 52963, 'Hamilton, Laurell Kaye/Anita Blakova/Anita Blakova 9 - Obsidianovy motyl/Hamilton, Laurell Kaye - Anita Blakova 9 - Obsidianovy motyl.rtf', NULL, 4, 1543732, '86714dd779346de4a7ff3fef42e554de433ce01b', 0, 1, 1);
INSERT INTO source VALUES (97567, 1, '2016-02-05 08:41:36', '2016-02-05 08:41:36', 48728, 'James, Ellen/Laska k nepriteli/James, Ellen - Laska k nepriteli.doc', NULL, 5, 552960, '7ab1c94e6b6af4b54defb819a4f02a4514e898a5', 20, 1, 1);
INSERT INTO source VALUES (97670, 1, '2016-02-05 08:42:15', '2016-02-05 08:42:15', 59887, 'Brown, Graham/Danielle Laidlawova/Danielle Laidlawova 2 - Cerne slunce/Brown, Graham - Danielle Laidlawova 2 - Cerne slunce.epub', NULL, 8, 453528, '753e2614dfbf0638f201833b9b53e673cabc903d', 60, 1, 1);
INSERT INTO source VALUES (98510, 1, '2016-03-20 15:16:41', '2016-03-20 15:16:41', 37116, 'Storch, Eduard/Bronzovy poklad/Storch, Eduard - Bronzovy poklad.docx', NULL, 16, 2191684, '85d89411276d378304460acb2031c4c66a6673aa', 40, 1, 1);


--
-- TOC entry 2285 (class 0 OID 0)
-- Dependencies: 206
-- Name: source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ebooks
--

SELECT pg_catalog.setval('source_id_seq', 98599, true);


-- test users

INSERT INTO "user" VALUES (2, 1, '2016-05-10 15:10:11.615486', '2016-05-10 15:10:11.615486', 'user', 'user@example.com', '$2b$12$c5keCrAWjpt6C0RnnW8O/efKZW.3UJL3GT5XkHpFqM1IPf0szmlGm', true, NULL, NULL);
INSERT INTO "user" VALUES (3, 1, '2016-05-10 15:10:53.09485', '2016-05-10 15:10:53.09485', 'superuser', 'superuser@example.com', '$2b$12$ZEB5wNYyQeTLFzL3R/Mj7uMDVzU1UHRDxQkd/WIC53iO9aJlHykP.', true, NULL, NULL);
INSERT INTO "user" VALUES (4, 1, '2016-05-10 15:11:41.069144', '2016-05-10 15:11:41.069144', 'trusted_user', 'trusted@example.com', '$2b$12$FSgx6n6ZrTa1sDctpui..uGpMoehy4Pg3pawNBmcFYRQIl4syfu0.', true, NULL, NULL);
INSERT INTO "user" VALUES (5, 1, '2016-05-10 15:12:53.166223', '2016-05-10 15:12:53.166223', 'guest', 'guest@example.com', '$2b$12$cZNvnRbo04q1dU.WjSBY6uEKpc5NJZ6FU8ZQU4fu.bszuZOChWL26', true, NULL, NULL);

SELECT pg_catalog.setval('user_id_seq', 5, true);

INSERT INTO user_roles VALUES (2, 2);
INSERT INTO user_roles VALUES (3, 4);
INSERT INTO user_roles VALUES (4, 3);
INSERT INTO user_roles VALUES (5, 1);


-- Completed on 2016-04-24 07:16:01 CEST

--
-- PostgreSQL database dump complete
--

