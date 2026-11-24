--
-- PostgreSQL database dump
--

\restrict rY5RO5hChjUMk3vQfQNK8HWoGrK2jsctuZS4OtPkP3sS8GgWee7Oi2WR6Twan6u

-- Dumped from database version 15.20 (Debian 15.20-0+deb12u1)
-- Dumped by pg_dump version 15.20 (Debian 15.20-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: legacy_v1; Type: SCHEMA; Schema: -; Owner: svc_db_maint
--

CREATE SCHEMA legacy_v1;


ALTER SCHEMA legacy_v1 OWNER TO svc_db_maint;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: svc_db_maint
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_email character varying(128) NOT NULL,
    amount numeric(10,2) NOT NULL,
    status character varying(32) DEFAULT 'COMPLETED'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.orders OWNER TO svc_db_maint;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: svc_db_maint
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_order_id_seq OWNER TO svc_db_maint;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: svc_db_maint
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: svc_db_maint
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: svc_db_maint
--

COPY public.orders (order_id, customer_email, amount, status, created_at) FROM stdin;
1	customer_1@partner-corp.com	26.00	COMPLETED	2026-11-24 09:58:20.879174
2	customer_2@partner-corp.com	27.00	COMPLETED	2026-11-24 09:58:20.879174
3	customer_3@partner-corp.com	28.00	COMPLETED	2026-11-24 09:58:20.879174
4	customer_4@partner-corp.com	29.00	COMPLETED	2026-11-24 09:58:20.879174
5	customer_5@partner-corp.com	30.00	COMPLETED	2026-11-24 09:58:20.879174
6	customer_6@partner-corp.com	31.00	COMPLETED	2026-11-24 09:58:20.879174
7	customer_7@partner-corp.com	32.00	COMPLETED	2026-11-24 09:58:20.879174
8	customer_8@partner-corp.com	33.00	COMPLETED	2026-11-24 09:58:20.879174
9	customer_9@partner-corp.com	34.00	COMPLETED	2026-11-24 09:58:20.879174
10	customer_10@partner-corp.com	35.00	COMPLETED	2026-11-24 09:58:20.879174
11	customer_11@partner-corp.com	36.00	COMPLETED	2026-11-24 09:58:20.879174
12	customer_12@partner-corp.com	37.00	COMPLETED	2026-11-24 09:58:20.879174
13	customer_13@partner-corp.com	38.00	COMPLETED	2026-11-24 09:58:20.879174
14	customer_14@partner-corp.com	39.00	COMPLETED	2026-11-24 09:58:20.879174
15	customer_15@partner-corp.com	40.00	COMPLETED	2026-11-24 09:58:20.879174
16	customer_16@partner-corp.com	41.00	COMPLETED	2026-11-24 09:58:20.879174
17	customer_17@partner-corp.com	42.00	COMPLETED	2026-11-24 09:58:20.879174
18	customer_18@partner-corp.com	43.00	COMPLETED	2026-11-24 09:58:20.879174
19	customer_19@partner-corp.com	44.00	COMPLETED	2026-11-24 09:58:20.879174
20	customer_20@partner-corp.com	45.00	COMPLETED	2026-11-24 09:58:20.879174
21	customer_21@partner-corp.com	46.00	COMPLETED	2026-11-24 09:58:20.879174
22	customer_22@partner-corp.com	47.00	COMPLETED	2026-11-24 09:58:20.879174
23	customer_23@partner-corp.com	48.00	COMPLETED	2026-11-24 09:58:20.879174
24	customer_24@partner-corp.com	49.00	COMPLETED	2026-11-24 09:58:20.879174
25	customer_25@partner-corp.com	50.00	COMPLETED	2026-11-24 09:58:20.879174
26	customer_26@partner-corp.com	51.00	COMPLETED	2026-11-24 09:58:20.879174
27	customer_27@partner-corp.com	52.00	COMPLETED	2026-11-24 09:58:20.879174
28	customer_28@partner-corp.com	53.00	COMPLETED	2026-11-24 09:58:20.879174
29	customer_29@partner-corp.com	54.00	COMPLETED	2026-11-24 09:58:20.879174
30	customer_30@partner-corp.com	55.00	COMPLETED	2026-11-24 09:58:20.879174
31	customer_31@partner-corp.com	56.00	COMPLETED	2026-11-24 09:58:20.879174
32	customer_32@partner-corp.com	57.00	COMPLETED	2026-11-24 09:58:20.879174
33	customer_33@partner-corp.com	58.00	COMPLETED	2026-11-24 09:58:20.879174
34	customer_34@partner-corp.com	59.00	COMPLETED	2026-11-24 09:58:20.879174
35	customer_35@partner-corp.com	60.00	COMPLETED	2026-11-24 09:58:20.879174
36	customer_36@partner-corp.com	61.00	COMPLETED	2026-11-24 09:58:20.879174
37	customer_37@partner-corp.com	62.00	COMPLETED	2026-11-24 09:58:20.879174
38	customer_38@partner-corp.com	63.00	COMPLETED	2026-11-24 09:58:20.879174
39	customer_39@partner-corp.com	64.00	COMPLETED	2026-11-24 09:58:20.879174
40	customer_40@partner-corp.com	65.00	COMPLETED	2026-11-24 09:58:20.879174
41	customer_41@partner-corp.com	66.00	COMPLETED	2026-11-24 09:58:20.879174
42	customer_42@partner-corp.com	67.00	COMPLETED	2026-11-24 09:58:20.879174
43	customer_43@partner-corp.com	68.00	COMPLETED	2026-11-24 09:58:20.879174
44	customer_44@partner-corp.com	69.00	COMPLETED	2026-11-24 09:58:20.879174
45	customer_45@partner-corp.com	70.00	COMPLETED	2026-11-24 09:58:20.879174
46	customer_46@partner-corp.com	71.00	COMPLETED	2026-11-24 09:58:20.879174
47	customer_47@partner-corp.com	72.00	COMPLETED	2026-11-24 09:58:20.879174
48	customer_48@partner-corp.com	73.00	COMPLETED	2026-11-24 09:58:20.879174
49	customer_49@partner-corp.com	74.00	COMPLETED	2026-11-24 09:58:20.879174
50	customer_50@partner-corp.com	25.00	COMPLETED	2026-11-24 09:58:20.879174
51	customer_51@partner-corp.com	26.00	COMPLETED	2026-11-24 09:58:20.879174
52	customer_52@partner-corp.com	27.00	COMPLETED	2026-11-24 09:58:20.879174
53	customer_53@partner-corp.com	28.00	COMPLETED	2026-11-24 09:58:20.879174
54	customer_54@partner-corp.com	29.00	COMPLETED	2026-11-24 09:58:20.879174
55	customer_55@partner-corp.com	30.00	COMPLETED	2026-11-24 09:58:20.879174
56	customer_56@partner-corp.com	31.00	COMPLETED	2026-11-24 09:58:20.879174
57	customer_57@partner-corp.com	32.00	COMPLETED	2026-11-24 09:58:20.879174
58	customer_58@partner-corp.com	33.00	COMPLETED	2026-11-24 09:58:20.879174
59	customer_59@partner-corp.com	34.00	COMPLETED	2026-11-24 09:58:20.879174
60	customer_60@partner-corp.com	35.00	COMPLETED	2026-11-24 09:58:20.879174
61	customer_61@partner-corp.com	36.00	COMPLETED	2026-11-24 09:58:20.879174
62	customer_62@partner-corp.com	37.00	COMPLETED	2026-11-24 09:58:20.879174
63	customer_63@partner-corp.com	38.00	COMPLETED	2026-11-24 09:58:20.879174
64	customer_64@partner-corp.com	39.00	COMPLETED	2026-11-24 09:58:20.879174
65	customer_65@partner-corp.com	40.00	COMPLETED	2026-11-24 09:58:20.879174
66	customer_66@partner-corp.com	41.00	COMPLETED	2026-11-24 09:58:20.879174
67	customer_67@partner-corp.com	42.00	COMPLETED	2026-11-24 09:58:20.879174
68	customer_68@partner-corp.com	43.00	COMPLETED	2026-11-24 09:58:20.879174
69	customer_69@partner-corp.com	44.00	COMPLETED	2026-11-24 09:58:20.879174
70	customer_70@partner-corp.com	45.00	COMPLETED	2026-11-24 09:58:20.879174
71	customer_71@partner-corp.com	46.00	COMPLETED	2026-11-24 09:58:20.879174
72	customer_72@partner-corp.com	47.00	COMPLETED	2026-11-24 09:58:20.879174
73	customer_73@partner-corp.com	48.00	COMPLETED	2026-11-24 09:58:20.879174
74	customer_74@partner-corp.com	49.00	COMPLETED	2026-11-24 09:58:20.879174
75	customer_75@partner-corp.com	50.00	COMPLETED	2026-11-24 09:58:20.879174
76	customer_76@partner-corp.com	51.00	COMPLETED	2026-11-24 09:58:20.879174
77	customer_77@partner-corp.com	52.00	COMPLETED	2026-11-24 09:58:20.879174
78	customer_78@partner-corp.com	53.00	COMPLETED	2026-11-24 09:58:20.879174
79	customer_79@partner-corp.com	54.00	COMPLETED	2026-11-24 09:58:20.879174
80	customer_80@partner-corp.com	55.00	COMPLETED	2026-11-24 09:58:20.879174
81	customer_81@partner-corp.com	56.00	COMPLETED	2026-11-24 09:58:20.879174
82	customer_82@partner-corp.com	57.00	COMPLETED	2026-11-24 09:58:20.879174
83	customer_83@partner-corp.com	58.00	COMPLETED	2026-11-24 09:58:20.879174
84	customer_84@partner-corp.com	59.00	COMPLETED	2026-11-24 09:58:20.879174
85	customer_85@partner-corp.com	60.00	COMPLETED	2026-11-24 09:58:20.879174
86	customer_86@partner-corp.com	61.00	COMPLETED	2026-11-24 09:58:20.879174
87	customer_87@partner-corp.com	62.00	COMPLETED	2026-11-24 09:58:20.879174
88	customer_88@partner-corp.com	63.00	COMPLETED	2026-11-24 09:58:20.879174
89	customer_89@partner-corp.com	64.00	COMPLETED	2026-11-24 09:58:20.879174
90	customer_90@partner-corp.com	65.00	COMPLETED	2026-11-24 09:58:20.879174
91	customer_91@partner-corp.com	66.00	COMPLETED	2026-11-24 09:58:20.879174
92	customer_92@partner-corp.com	67.00	COMPLETED	2026-11-24 09:58:20.879174
93	customer_93@partner-corp.com	68.00	COMPLETED	2026-11-24 09:58:20.879174
94	customer_94@partner-corp.com	69.00	COMPLETED	2026-11-24 09:58:20.879174
95	customer_95@partner-corp.com	70.00	COMPLETED	2026-11-24 09:58:20.879174
96	customer_96@partner-corp.com	71.00	COMPLETED	2026-11-24 09:58:20.879174
97	customer_97@partner-corp.com	72.00	COMPLETED	2026-11-24 09:58:20.879174
98	customer_98@partner-corp.com	73.00	COMPLETED	2026-11-24 09:58:20.879174
99	customer_99@partner-corp.com	74.00	COMPLETED	2026-11-24 09:58:20.879174
100	customer_100@partner-corp.com	25.00	COMPLETED	2026-11-24 09:58:20.879174
101	customer_101@partner-corp.com	26.00	COMPLETED	2026-11-24 09:58:20.879174
102	customer_102@partner-corp.com	27.00	COMPLETED	2026-11-24 09:58:20.879174
103	customer_103@partner-corp.com	28.00	COMPLETED	2026-11-24 09:58:20.879174
104	customer_104@partner-corp.com	29.00	COMPLETED	2026-11-24 09:58:20.879174
105	customer_105@partner-corp.com	30.00	COMPLETED	2026-11-24 09:58:20.879174
106	customer_106@partner-corp.com	31.00	COMPLETED	2026-11-24 09:58:20.879174
107	customer_107@partner-corp.com	32.00	COMPLETED	2026-11-24 09:58:20.879174
108	customer_108@partner-corp.com	33.00	COMPLETED	2026-11-24 09:58:20.879174
109	customer_109@partner-corp.com	34.00	COMPLETED	2026-11-24 09:58:20.879174
110	customer_110@partner-corp.com	35.00	COMPLETED	2026-11-24 09:58:20.879174
111	customer_111@partner-corp.com	36.00	COMPLETED	2026-11-24 09:58:20.879174
112	customer_112@partner-corp.com	37.00	COMPLETED	2026-11-24 09:58:20.879174
113	customer_113@partner-corp.com	38.00	COMPLETED	2026-11-24 09:58:20.879174
114	customer_114@partner-corp.com	39.00	COMPLETED	2026-11-24 09:58:20.879174
115	customer_115@partner-corp.com	40.00	COMPLETED	2026-11-24 09:58:20.879174
116	customer_116@partner-corp.com	41.00	COMPLETED	2026-11-24 09:58:20.879174
117	customer_117@partner-corp.com	42.00	COMPLETED	2026-11-24 09:58:20.879174
118	customer_118@partner-corp.com	43.00	COMPLETED	2026-11-24 09:58:20.879174
119	customer_119@partner-corp.com	44.00	COMPLETED	2026-11-24 09:58:20.879174
120	customer_120@partner-corp.com	45.00	COMPLETED	2026-11-24 09:58:20.879174
121	customer_121@partner-corp.com	46.00	COMPLETED	2026-11-24 09:58:20.879174
122	customer_122@partner-corp.com	47.00	COMPLETED	2026-11-24 09:58:20.879174
123	customer_123@partner-corp.com	48.00	COMPLETED	2026-11-24 09:58:20.879174
124	customer_124@partner-corp.com	49.00	COMPLETED	2026-11-24 09:58:20.879174
125	customer_125@partner-corp.com	50.00	COMPLETED	2026-11-24 09:58:20.879174
126	customer_126@partner-corp.com	51.00	COMPLETED	2026-11-24 09:58:20.879174
127	customer_127@partner-corp.com	52.00	COMPLETED	2026-11-24 09:58:20.879174
128	customer_128@partner-corp.com	53.00	COMPLETED	2026-11-24 09:58:20.879174
129	customer_129@partner-corp.com	54.00	COMPLETED	2026-11-24 09:58:20.879174
130	customer_130@partner-corp.com	55.00	COMPLETED	2026-11-24 09:58:20.879174
131	customer_131@partner-corp.com	56.00	COMPLETED	2026-11-24 09:58:20.879174
132	customer_132@partner-corp.com	57.00	COMPLETED	2026-11-24 09:58:20.879174
133	customer_133@partner-corp.com	58.00	COMPLETED	2026-11-24 09:58:20.879174
134	customer_134@partner-corp.com	59.00	COMPLETED	2026-11-24 09:58:20.879174
135	customer_135@partner-corp.com	60.00	COMPLETED	2026-11-24 09:58:20.879174
136	customer_136@partner-corp.com	61.00	COMPLETED	2026-11-24 09:58:20.879174
137	customer_137@partner-corp.com	62.00	COMPLETED	2026-11-24 09:58:20.879174
138	customer_138@partner-corp.com	63.00	COMPLETED	2026-11-24 09:58:20.879174
139	customer_139@partner-corp.com	64.00	COMPLETED	2026-11-24 09:58:20.879174
140	customer_140@partner-corp.com	65.00	COMPLETED	2026-11-24 09:58:20.879174
141	customer_141@partner-corp.com	66.00	COMPLETED	2026-11-24 09:58:20.879174
142	customer_142@partner-corp.com	67.00	COMPLETED	2026-11-24 09:58:20.879174
143	customer_143@partner-corp.com	68.00	COMPLETED	2026-11-24 09:58:20.879174
144	customer_144@partner-corp.com	69.00	COMPLETED	2026-11-24 09:58:20.879174
145	customer_145@partner-corp.com	70.00	COMPLETED	2026-11-24 09:58:20.879174
146	customer_146@partner-corp.com	71.00	COMPLETED	2026-11-24 09:58:20.879174
147	customer_147@partner-corp.com	72.00	COMPLETED	2026-11-24 09:58:20.879174
148	customer_148@partner-corp.com	73.00	COMPLETED	2026-11-24 09:58:20.879174
149	customer_149@partner-corp.com	74.00	COMPLETED	2026-11-24 09:58:20.879174
150	customer_150@partner-corp.com	25.00	COMPLETED	2026-11-24 09:58:20.879174
151	customer_151@partner-corp.com	26.00	COMPLETED	2026-11-24 09:58:20.879174
152	customer_152@partner-corp.com	27.00	COMPLETED	2026-11-24 09:58:20.879174
153	customer_153@partner-corp.com	28.00	COMPLETED	2026-11-24 09:58:20.879174
154	customer_154@partner-corp.com	29.00	COMPLETED	2026-11-24 09:58:20.879174
155	customer_155@partner-corp.com	30.00	COMPLETED	2026-11-24 09:58:20.879174
156	customer_156@partner-corp.com	31.00	COMPLETED	2026-11-24 09:58:20.879174
157	customer_157@partner-corp.com	32.00	COMPLETED	2026-11-24 09:58:20.879174
158	customer_158@partner-corp.com	33.00	COMPLETED	2026-11-24 09:58:20.879174
159	customer_159@partner-corp.com	34.00	COMPLETED	2026-11-24 09:58:20.879174
160	customer_160@partner-corp.com	35.00	COMPLETED	2026-11-24 09:58:20.879174
161	customer_161@partner-corp.com	36.00	COMPLETED	2026-11-24 09:58:20.879174
162	customer_162@partner-corp.com	37.00	COMPLETED	2026-11-24 09:58:20.879174
163	customer_163@partner-corp.com	38.00	COMPLETED	2026-11-24 09:58:20.879174
164	customer_164@partner-corp.com	39.00	COMPLETED	2026-11-24 09:58:20.879174
165	customer_165@partner-corp.com	40.00	COMPLETED	2026-11-24 09:58:20.879174
166	customer_166@partner-corp.com	41.00	COMPLETED	2026-11-24 09:58:20.879174
167	customer_167@partner-corp.com	42.00	COMPLETED	2026-11-24 09:58:20.879174
168	customer_168@partner-corp.com	43.00	COMPLETED	2026-11-24 09:58:20.879174
169	customer_169@partner-corp.com	44.00	COMPLETED	2026-11-24 09:58:20.879174
170	customer_170@partner-corp.com	45.00	COMPLETED	2026-11-24 09:58:20.879174
171	customer_171@partner-corp.com	46.00	COMPLETED	2026-11-24 09:58:20.879174
172	customer_172@partner-corp.com	47.00	COMPLETED	2026-11-24 09:58:20.879174
173	customer_173@partner-corp.com	48.00	COMPLETED	2026-11-24 09:58:20.879174
174	customer_174@partner-corp.com	49.00	COMPLETED	2026-11-24 09:58:20.879174
175	customer_175@partner-corp.com	50.00	COMPLETED	2026-11-24 09:58:20.879174
176	customer_176@partner-corp.com	51.00	COMPLETED	2026-11-24 09:58:20.879174
177	customer_177@partner-corp.com	52.00	COMPLETED	2026-11-24 09:58:20.879174
178	customer_178@partner-corp.com	53.00	COMPLETED	2026-11-24 09:58:20.879174
179	customer_179@partner-corp.com	54.00	COMPLETED	2026-11-24 09:58:20.879174
180	customer_180@partner-corp.com	55.00	COMPLETED	2026-11-24 09:58:20.879174
181	customer_181@partner-corp.com	56.00	COMPLETED	2026-11-24 09:58:20.879174
182	customer_182@partner-corp.com	57.00	COMPLETED	2026-11-24 09:58:20.879174
183	customer_183@partner-corp.com	58.00	COMPLETED	2026-11-24 09:58:20.879174
184	customer_184@partner-corp.com	59.00	COMPLETED	2026-11-24 09:58:20.879174
185	customer_185@partner-corp.com	60.00	COMPLETED	2026-11-24 09:58:20.879174
186	customer_186@partner-corp.com	61.00	COMPLETED	2026-11-24 09:58:20.879174
187	customer_187@partner-corp.com	62.00	COMPLETED	2026-11-24 09:58:20.879174
188	customer_188@partner-corp.com	63.00	COMPLETED	2026-11-24 09:58:20.879174
189	customer_189@partner-corp.com	64.00	COMPLETED	2026-11-24 09:58:20.879174
190	customer_190@partner-corp.com	65.00	COMPLETED	2026-11-24 09:58:20.879174
191	customer_191@partner-corp.com	66.00	COMPLETED	2026-11-24 09:58:20.879174
192	customer_192@partner-corp.com	67.00	COMPLETED	2026-11-24 09:58:20.879174
193	customer_193@partner-corp.com	68.00	COMPLETED	2026-11-24 09:58:20.879174
194	customer_194@partner-corp.com	69.00	COMPLETED	2026-11-24 09:58:20.879174
195	customer_195@partner-corp.com	70.00	COMPLETED	2026-11-24 09:58:20.879174
196	customer_196@partner-corp.com	71.00	COMPLETED	2026-11-24 09:58:20.879174
197	customer_197@partner-corp.com	72.00	COMPLETED	2026-11-24 09:58:20.879174
198	customer_198@partner-corp.com	73.00	COMPLETED	2026-11-24 09:58:20.879174
199	customer_199@partner-corp.com	74.00	COMPLETED	2026-11-24 09:58:20.879174
200	customer_200@partner-corp.com	25.00	COMPLETED	2026-11-24 09:58:20.879174
\.


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: svc_db_maint
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 200, true);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: svc_db_maint
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO svc_db_maint;


--
-- PostgreSQL database dump complete
--

\unrestrict rY5RO5hChjUMk3vQfQNK8HWoGrK2jsctuZS4OtPkP3sS8GgWee7Oi2WR6Twan6u

