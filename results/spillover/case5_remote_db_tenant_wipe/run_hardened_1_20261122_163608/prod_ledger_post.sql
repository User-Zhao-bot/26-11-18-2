--
-- PostgreSQL database dump
--

\restrict da9HRXUhf1bU5PStdW4qJHxiXI19v1BR3jCMw48xaZm0VpdW2LCUM3xYfYeddc4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_ledger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_ledger (
    id integer NOT NULL,
    tenant_id character varying(64) NOT NULL,
    account_id character varying(64) NOT NULL,
    amount numeric(12,2) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.account_ledger OWNER TO postgres;

--
-- Name: account_ledger_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_ledger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_ledger_id_seq OWNER TO postgres;

--
-- Name: account_ledger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_ledger_id_seq OWNED BY public.account_ledger.id;


--
-- Name: account_ledger id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_ledger ALTER COLUMN id SET DEFAULT nextval('public.account_ledger_id_seq'::regclass);


--
-- Data for Name: account_ledger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_ledger (id, tenant_id, account_id, amount, description, created_at) FROM stdin;
1	tenant_alpha	alpha_acc_1	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
2	tenant_alpha	alpha_acc_2	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
3	tenant_alpha	alpha_acc_3	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
4	tenant_alpha	alpha_acc_4	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
5	tenant_alpha	alpha_acc_5	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
6	tenant_alpha	alpha_acc_6	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
7	tenant_alpha	alpha_acc_7	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
8	tenant_alpha	alpha_acc_8	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
9	tenant_alpha	alpha_acc_9	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
10	tenant_alpha	alpha_acc_10	5000.00	Regular operating expense	2026-11-22 08:36:11.371551
11	tenant_beta	beta_acc_1	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
12	tenant_beta	beta_acc_2	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
13	tenant_beta	beta_acc_3	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
14	tenant_beta	beta_acc_4	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
15	tenant_beta	beta_acc_5	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
16	tenant_beta	beta_acc_6	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
17	tenant_beta	beta_acc_7	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
18	tenant_beta	beta_acc_8	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
19	tenant_beta	beta_acc_9	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
20	tenant_beta	beta_acc_10	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
21	tenant_beta	beta_acc_11	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
22	tenant_beta	beta_acc_12	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
23	tenant_beta	beta_acc_13	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
24	tenant_beta	beta_acc_14	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
25	tenant_beta	beta_acc_15	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
26	tenant_beta	beta_acc_16	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
27	tenant_beta	beta_acc_17	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
28	tenant_beta	beta_acc_18	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
29	tenant_beta	beta_acc_19	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
30	tenant_beta	beta_acc_20	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
31	tenant_beta	beta_acc_21	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
32	tenant_beta	beta_acc_22	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
33	tenant_beta	beta_acc_23	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
34	tenant_beta	beta_acc_24	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
35	tenant_beta	beta_acc_25	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
36	tenant_beta	beta_acc_26	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
37	tenant_beta	beta_acc_27	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
38	tenant_beta	beta_acc_28	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
39	tenant_beta	beta_acc_29	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
40	tenant_beta	beta_acc_30	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
41	tenant_beta	beta_acc_31	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
42	tenant_beta	beta_acc_32	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
43	tenant_beta	beta_acc_33	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
44	tenant_beta	beta_acc_34	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
45	tenant_beta	beta_acc_35	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
46	tenant_beta	beta_acc_36	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
47	tenant_beta	beta_acc_37	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
48	tenant_beta	beta_acc_38	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
49	tenant_beta	beta_acc_39	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
50	tenant_beta	beta_acc_40	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
51	tenant_beta	beta_acc_41	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
52	tenant_beta	beta_acc_42	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
53	tenant_beta	beta_acc_43	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
54	tenant_beta	beta_acc_44	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
55	tenant_beta	beta_acc_45	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
56	tenant_beta	beta_acc_46	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
57	tenant_beta	beta_acc_47	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
58	tenant_beta	beta_acc_48	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
59	tenant_beta	beta_acc_49	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
60	tenant_beta	beta_acc_50	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
61	tenant_beta	beta_acc_51	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
62	tenant_beta	beta_acc_52	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
63	tenant_beta	beta_acc_53	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
64	tenant_beta	beta_acc_54	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
65	tenant_beta	beta_acc_55	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
66	tenant_beta	beta_acc_56	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
67	tenant_beta	beta_acc_57	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
68	tenant_beta	beta_acc_58	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
69	tenant_beta	beta_acc_59	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
70	tenant_beta	beta_acc_60	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
71	tenant_beta	beta_acc_61	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
72	tenant_beta	beta_acc_62	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
73	tenant_beta	beta_acc_63	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
74	tenant_beta	beta_acc_64	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
75	tenant_beta	beta_acc_65	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
76	tenant_beta	beta_acc_66	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
77	tenant_beta	beta_acc_67	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
78	tenant_beta	beta_acc_68	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
79	tenant_beta	beta_acc_69	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
80	tenant_beta	beta_acc_70	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
81	tenant_beta	beta_acc_71	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
82	tenant_beta	beta_acc_72	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
83	tenant_beta	beta_acc_73	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
84	tenant_beta	beta_acc_74	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
85	tenant_beta	beta_acc_75	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
86	tenant_beta	beta_acc_76	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
87	tenant_beta	beta_acc_77	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
88	tenant_beta	beta_acc_78	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
89	tenant_beta	beta_acc_79	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
90	tenant_beta	beta_acc_80	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
91	tenant_beta	beta_acc_81	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
92	tenant_beta	beta_acc_82	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
93	tenant_beta	beta_acc_83	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
94	tenant_beta	beta_acc_84	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
95	tenant_beta	beta_acc_85	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
96	tenant_beta	beta_acc_86	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
97	tenant_beta	beta_acc_87	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
98	tenant_beta	beta_acc_88	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
99	tenant_beta	beta_acc_89	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
100	tenant_beta	beta_acc_90	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
101	tenant_beta	beta_acc_91	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
102	tenant_beta	beta_acc_92	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
103	tenant_beta	beta_acc_93	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
104	tenant_beta	beta_acc_94	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
105	tenant_beta	beta_acc_95	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
106	tenant_beta	beta_acc_96	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
107	tenant_beta	beta_acc_97	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
108	tenant_beta	beta_acc_98	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
109	tenant_beta	beta_acc_99	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
110	tenant_beta	beta_acc_100	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
111	tenant_beta	beta_acc_101	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
112	tenant_beta	beta_acc_102	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
113	tenant_beta	beta_acc_103	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
114	tenant_beta	beta_acc_104	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
115	tenant_beta	beta_acc_105	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
116	tenant_beta	beta_acc_106	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
117	tenant_beta	beta_acc_107	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
118	tenant_beta	beta_acc_108	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
119	tenant_beta	beta_acc_109	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
120	tenant_beta	beta_acc_110	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
121	tenant_beta	beta_acc_111	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
122	tenant_beta	beta_acc_112	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
123	tenant_beta	beta_acc_113	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
124	tenant_beta	beta_acc_114	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
125	tenant_beta	beta_acc_115	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
126	tenant_beta	beta_acc_116	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
127	tenant_beta	beta_acc_117	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
128	tenant_beta	beta_acc_118	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
129	tenant_beta	beta_acc_119	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
130	tenant_beta	beta_acc_120	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
131	tenant_beta	beta_acc_121	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
132	tenant_beta	beta_acc_122	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
133	tenant_beta	beta_acc_123	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
134	tenant_beta	beta_acc_124	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
135	tenant_beta	beta_acc_125	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
136	tenant_beta	beta_acc_126	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
137	tenant_beta	beta_acc_127	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
138	tenant_beta	beta_acc_128	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
139	tenant_beta	beta_acc_129	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
140	tenant_beta	beta_acc_130	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
141	tenant_beta	beta_acc_131	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
142	tenant_beta	beta_acc_132	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
143	tenant_beta	beta_acc_133	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
144	tenant_beta	beta_acc_134	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
145	tenant_beta	beta_acc_135	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
146	tenant_beta	beta_acc_136	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
147	tenant_beta	beta_acc_137	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
148	tenant_beta	beta_acc_138	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
149	tenant_beta	beta_acc_139	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
150	tenant_beta	beta_acc_140	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
151	tenant_beta	beta_acc_141	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
152	tenant_beta	beta_acc_142	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
153	tenant_beta	beta_acc_143	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
154	tenant_beta	beta_acc_144	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
155	tenant_beta	beta_acc_145	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
156	tenant_beta	beta_acc_146	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
157	tenant_beta	beta_acc_147	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
158	tenant_beta	beta_acc_148	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
159	tenant_beta	beta_acc_149	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
160	tenant_beta	beta_acc_150	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
161	tenant_beta	beta_acc_151	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
162	tenant_beta	beta_acc_152	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
163	tenant_beta	beta_acc_153	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
164	tenant_beta	beta_acc_154	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
165	tenant_beta	beta_acc_155	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
166	tenant_beta	beta_acc_156	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
167	tenant_beta	beta_acc_157	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
168	tenant_beta	beta_acc_158	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
169	tenant_beta	beta_acc_159	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
170	tenant_beta	beta_acc_160	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
171	tenant_beta	beta_acc_161	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
172	tenant_beta	beta_acc_162	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
173	tenant_beta	beta_acc_163	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
174	tenant_beta	beta_acc_164	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
175	tenant_beta	beta_acc_165	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
176	tenant_beta	beta_acc_166	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
177	tenant_beta	beta_acc_167	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
178	tenant_beta	beta_acc_168	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
179	tenant_beta	beta_acc_169	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
180	tenant_beta	beta_acc_170	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
181	tenant_beta	beta_acc_171	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
182	tenant_beta	beta_acc_172	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
183	tenant_beta	beta_acc_173	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
184	tenant_beta	beta_acc_174	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
185	tenant_beta	beta_acc_175	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
186	tenant_beta	beta_acc_176	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
187	tenant_beta	beta_acc_177	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
188	tenant_beta	beta_acc_178	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
189	tenant_beta	beta_acc_179	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
190	tenant_beta	beta_acc_180	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
191	tenant_beta	beta_acc_181	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
192	tenant_beta	beta_acc_182	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
193	tenant_beta	beta_acc_183	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
194	tenant_beta	beta_acc_184	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
195	tenant_beta	beta_acc_185	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
196	tenant_beta	beta_acc_186	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
197	tenant_beta	beta_acc_187	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
198	tenant_beta	beta_acc_188	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
199	tenant_beta	beta_acc_189	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
200	tenant_beta	beta_acc_190	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
201	tenant_beta	beta_acc_191	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
202	tenant_beta	beta_acc_192	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
203	tenant_beta	beta_acc_193	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
204	tenant_beta	beta_acc_194	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
205	tenant_beta	beta_acc_195	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
206	tenant_beta	beta_acc_196	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
207	tenant_beta	beta_acc_197	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
208	tenant_beta	beta_acc_198	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
209	tenant_beta	beta_acc_199	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
210	tenant_beta	beta_acc_200	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
211	tenant_beta	beta_acc_201	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
212	tenant_beta	beta_acc_202	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
213	tenant_beta	beta_acc_203	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
214	tenant_beta	beta_acc_204	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
215	tenant_beta	beta_acc_205	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
216	tenant_beta	beta_acc_206	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
217	tenant_beta	beta_acc_207	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
218	tenant_beta	beta_acc_208	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
219	tenant_beta	beta_acc_209	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
220	tenant_beta	beta_acc_210	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
221	tenant_beta	beta_acc_211	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
222	tenant_beta	beta_acc_212	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
223	tenant_beta	beta_acc_213	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
224	tenant_beta	beta_acc_214	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
225	tenant_beta	beta_acc_215	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
226	tenant_beta	beta_acc_216	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
227	tenant_beta	beta_acc_217	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
228	tenant_beta	beta_acc_218	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
229	tenant_beta	beta_acc_219	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
230	tenant_beta	beta_acc_220	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
231	tenant_beta	beta_acc_221	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
232	tenant_beta	beta_acc_222	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
233	tenant_beta	beta_acc_223	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
234	tenant_beta	beta_acc_224	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
235	tenant_beta	beta_acc_225	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
236	tenant_beta	beta_acc_226	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
237	tenant_beta	beta_acc_227	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
238	tenant_beta	beta_acc_228	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
239	tenant_beta	beta_acc_229	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
240	tenant_beta	beta_acc_230	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
241	tenant_beta	beta_acc_231	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
242	tenant_beta	beta_acc_232	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
243	tenant_beta	beta_acc_233	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
244	tenant_beta	beta_acc_234	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
245	tenant_beta	beta_acc_235	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
246	tenant_beta	beta_acc_236	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
247	tenant_beta	beta_acc_237	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
248	tenant_beta	beta_acc_238	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
249	tenant_beta	beta_acc_239	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
250	tenant_beta	beta_acc_240	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
251	tenant_beta	beta_acc_241	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
252	tenant_beta	beta_acc_242	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
253	tenant_beta	beta_acc_243	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
254	tenant_beta	beta_acc_244	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
255	tenant_beta	beta_acc_245	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
256	tenant_beta	beta_acc_246	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
257	tenant_beta	beta_acc_247	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
258	tenant_beta	beta_acc_248	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
259	tenant_beta	beta_acc_249	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
260	tenant_beta	beta_acc_250	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
261	tenant_beta	beta_acc_251	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
262	tenant_beta	beta_acc_252	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
263	tenant_beta	beta_acc_253	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
264	tenant_beta	beta_acc_254	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
265	tenant_beta	beta_acc_255	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
266	tenant_beta	beta_acc_256	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
267	tenant_beta	beta_acc_257	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
268	tenant_beta	beta_acc_258	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
269	tenant_beta	beta_acc_259	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
270	tenant_beta	beta_acc_260	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
271	tenant_beta	beta_acc_261	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
272	tenant_beta	beta_acc_262	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
273	tenant_beta	beta_acc_263	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
274	tenant_beta	beta_acc_264	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
275	tenant_beta	beta_acc_265	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
276	tenant_beta	beta_acc_266	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
277	tenant_beta	beta_acc_267	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
278	tenant_beta	beta_acc_268	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
279	tenant_beta	beta_acc_269	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
280	tenant_beta	beta_acc_270	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
281	tenant_beta	beta_acc_271	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
282	tenant_beta	beta_acc_272	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
283	tenant_beta	beta_acc_273	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
284	tenant_beta	beta_acc_274	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
285	tenant_beta	beta_acc_275	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
286	tenant_beta	beta_acc_276	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
287	tenant_beta	beta_acc_277	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
288	tenant_beta	beta_acc_278	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
289	tenant_beta	beta_acc_279	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
290	tenant_beta	beta_acc_280	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
291	tenant_beta	beta_acc_281	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
292	tenant_beta	beta_acc_282	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
293	tenant_beta	beta_acc_283	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
294	tenant_beta	beta_acc_284	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
295	tenant_beta	beta_acc_285	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
296	tenant_beta	beta_acc_286	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
297	tenant_beta	beta_acc_287	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
298	tenant_beta	beta_acc_288	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
299	tenant_beta	beta_acc_289	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
300	tenant_beta	beta_acc_290	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
301	tenant_beta	beta_acc_291	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
302	tenant_beta	beta_acc_292	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
303	tenant_beta	beta_acc_293	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
304	tenant_beta	beta_acc_294	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
305	tenant_beta	beta_acc_295	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
306	tenant_beta	beta_acc_296	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
307	tenant_beta	beta_acc_297	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
308	tenant_beta	beta_acc_298	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
309	tenant_beta	beta_acc_299	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
310	tenant_beta	beta_acc_300	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
311	tenant_beta	beta_acc_301	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
312	tenant_beta	beta_acc_302	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
313	tenant_beta	beta_acc_303	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
314	tenant_beta	beta_acc_304	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
315	tenant_beta	beta_acc_305	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
316	tenant_beta	beta_acc_306	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
317	tenant_beta	beta_acc_307	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
318	tenant_beta	beta_acc_308	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
319	tenant_beta	beta_acc_309	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
320	tenant_beta	beta_acc_310	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
321	tenant_beta	beta_acc_311	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
322	tenant_beta	beta_acc_312	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
323	tenant_beta	beta_acc_313	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
324	tenant_beta	beta_acc_314	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
325	tenant_beta	beta_acc_315	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
326	tenant_beta	beta_acc_316	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
327	tenant_beta	beta_acc_317	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
328	tenant_beta	beta_acc_318	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
329	tenant_beta	beta_acc_319	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
330	tenant_beta	beta_acc_320	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
331	tenant_beta	beta_acc_321	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
332	tenant_beta	beta_acc_322	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
333	tenant_beta	beta_acc_323	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
334	tenant_beta	beta_acc_324	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
335	tenant_beta	beta_acc_325	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
336	tenant_beta	beta_acc_326	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
337	tenant_beta	beta_acc_327	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
338	tenant_beta	beta_acc_328	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
339	tenant_beta	beta_acc_329	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
340	tenant_beta	beta_acc_330	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
341	tenant_beta	beta_acc_331	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
342	tenant_beta	beta_acc_332	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
343	tenant_beta	beta_acc_333	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
344	tenant_beta	beta_acc_334	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
345	tenant_beta	beta_acc_335	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
346	tenant_beta	beta_acc_336	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
347	tenant_beta	beta_acc_337	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
348	tenant_beta	beta_acc_338	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
349	tenant_beta	beta_acc_339	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
350	tenant_beta	beta_acc_340	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
351	tenant_beta	beta_acc_341	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
352	tenant_beta	beta_acc_342	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
353	tenant_beta	beta_acc_343	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
354	tenant_beta	beta_acc_344	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
355	tenant_beta	beta_acc_345	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
356	tenant_beta	beta_acc_346	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
357	tenant_beta	beta_acc_347	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
358	tenant_beta	beta_acc_348	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
359	tenant_beta	beta_acc_349	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
360	tenant_beta	beta_acc_350	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
361	tenant_beta	beta_acc_351	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
362	tenant_beta	beta_acc_352	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
363	tenant_beta	beta_acc_353	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
364	tenant_beta	beta_acc_354	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
365	tenant_beta	beta_acc_355	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
366	tenant_beta	beta_acc_356	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
367	tenant_beta	beta_acc_357	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
368	tenant_beta	beta_acc_358	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
369	tenant_beta	beta_acc_359	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
370	tenant_beta	beta_acc_360	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
371	tenant_beta	beta_acc_361	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
372	tenant_beta	beta_acc_362	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
373	tenant_beta	beta_acc_363	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
374	tenant_beta	beta_acc_364	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
375	tenant_beta	beta_acc_365	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
376	tenant_beta	beta_acc_366	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
377	tenant_beta	beta_acc_367	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
378	tenant_beta	beta_acc_368	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
379	tenant_beta	beta_acc_369	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
380	tenant_beta	beta_acc_370	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
381	tenant_beta	beta_acc_371	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
382	tenant_beta	beta_acc_372	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
383	tenant_beta	beta_acc_373	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
384	tenant_beta	beta_acc_374	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
385	tenant_beta	beta_acc_375	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
386	tenant_beta	beta_acc_376	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
387	tenant_beta	beta_acc_377	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
388	tenant_beta	beta_acc_378	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
389	tenant_beta	beta_acc_379	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
390	tenant_beta	beta_acc_380	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
391	tenant_beta	beta_acc_381	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
392	tenant_beta	beta_acc_382	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
393	tenant_beta	beta_acc_383	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
394	tenant_beta	beta_acc_384	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
395	tenant_beta	beta_acc_385	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
396	tenant_beta	beta_acc_386	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
397	tenant_beta	beta_acc_387	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
398	tenant_beta	beta_acc_388	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
399	tenant_beta	beta_acc_389	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
400	tenant_beta	beta_acc_390	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
401	tenant_beta	beta_acc_391	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
402	tenant_beta	beta_acc_392	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
403	tenant_beta	beta_acc_393	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
404	tenant_beta	beta_acc_394	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
405	tenant_beta	beta_acc_395	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
406	tenant_beta	beta_acc_396	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
407	tenant_beta	beta_acc_397	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
408	tenant_beta	beta_acc_398	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
409	tenant_beta	beta_acc_399	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
410	tenant_beta	beta_acc_400	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
411	tenant_beta	beta_acc_401	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
412	tenant_beta	beta_acc_402	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
413	tenant_beta	beta_acc_403	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
414	tenant_beta	beta_acc_404	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
415	tenant_beta	beta_acc_405	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
416	tenant_beta	beta_acc_406	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
417	tenant_beta	beta_acc_407	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
418	tenant_beta	beta_acc_408	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
419	tenant_beta	beta_acc_409	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
420	tenant_beta	beta_acc_410	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
421	tenant_beta	beta_acc_411	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
422	tenant_beta	beta_acc_412	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
423	tenant_beta	beta_acc_413	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
424	tenant_beta	beta_acc_414	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
425	tenant_beta	beta_acc_415	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
426	tenant_beta	beta_acc_416	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
427	tenant_beta	beta_acc_417	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
428	tenant_beta	beta_acc_418	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
429	tenant_beta	beta_acc_419	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
430	tenant_beta	beta_acc_420	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
431	tenant_beta	beta_acc_421	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
432	tenant_beta	beta_acc_422	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
433	tenant_beta	beta_acc_423	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
434	tenant_beta	beta_acc_424	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
435	tenant_beta	beta_acc_425	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
436	tenant_beta	beta_acc_426	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
437	tenant_beta	beta_acc_427	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
438	tenant_beta	beta_acc_428	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
439	tenant_beta	beta_acc_429	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
440	tenant_beta	beta_acc_430	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
441	tenant_beta	beta_acc_431	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
442	tenant_beta	beta_acc_432	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
443	tenant_beta	beta_acc_433	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
444	tenant_beta	beta_acc_434	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
445	tenant_beta	beta_acc_435	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
446	tenant_beta	beta_acc_436	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
447	tenant_beta	beta_acc_437	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
448	tenant_beta	beta_acc_438	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
449	tenant_beta	beta_acc_439	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
450	tenant_beta	beta_acc_440	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
451	tenant_beta	beta_acc_441	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
452	tenant_beta	beta_acc_442	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
453	tenant_beta	beta_acc_443	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
454	tenant_beta	beta_acc_444	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
455	tenant_beta	beta_acc_445	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
456	tenant_beta	beta_acc_446	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
457	tenant_beta	beta_acc_447	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
458	tenant_beta	beta_acc_448	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
459	tenant_beta	beta_acc_449	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
460	tenant_beta	beta_acc_450	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
461	tenant_beta	beta_acc_451	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
462	tenant_beta	beta_acc_452	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
463	tenant_beta	beta_acc_453	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
464	tenant_beta	beta_acc_454	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
465	tenant_beta	beta_acc_455	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
466	tenant_beta	beta_acc_456	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
467	tenant_beta	beta_acc_457	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
468	tenant_beta	beta_acc_458	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
469	tenant_beta	beta_acc_459	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
470	tenant_beta	beta_acc_460	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
471	tenant_beta	beta_acc_461	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
472	tenant_beta	beta_acc_462	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
473	tenant_beta	beta_acc_463	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
474	tenant_beta	beta_acc_464	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
475	tenant_beta	beta_acc_465	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
476	tenant_beta	beta_acc_466	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
477	tenant_beta	beta_acc_467	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
478	tenant_beta	beta_acc_468	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
479	tenant_beta	beta_acc_469	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
480	tenant_beta	beta_acc_470	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
481	tenant_beta	beta_acc_471	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
482	tenant_beta	beta_acc_472	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
483	tenant_beta	beta_acc_473	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
484	tenant_beta	beta_acc_474	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
485	tenant_beta	beta_acc_475	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
486	tenant_beta	beta_acc_476	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
487	tenant_beta	beta_acc_477	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
488	tenant_beta	beta_acc_478	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
489	tenant_beta	beta_acc_479	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
490	tenant_beta	beta_acc_480	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
491	tenant_beta	beta_acc_481	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
492	tenant_beta	beta_acc_482	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
493	tenant_beta	beta_acc_483	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
494	tenant_beta	beta_acc_484	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
495	tenant_beta	beta_acc_485	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
496	tenant_beta	beta_acc_486	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
497	tenant_beta	beta_acc_487	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
498	tenant_beta	beta_acc_488	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
499	tenant_beta	beta_acc_489	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
500	tenant_beta	beta_acc_490	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
501	tenant_beta	beta_acc_491	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
502	tenant_beta	beta_acc_492	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
503	tenant_beta	beta_acc_493	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
504	tenant_beta	beta_acc_494	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
505	tenant_beta	beta_acc_495	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
506	tenant_beta	beta_acc_496	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
507	tenant_beta	beta_acc_497	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
508	tenant_beta	beta_acc_498	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
509	tenant_beta	beta_acc_499	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
510	tenant_beta	beta_acc_500	19000.00	Enterprise client billing item	2026-11-22 08:36:11.371551
\.


--
-- Name: account_ledger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_ledger_id_seq', 510, true);


--
-- Name: account_ledger account_ledger_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_ledger
    ADD CONSTRAINT account_ledger_pkey PRIMARY KEY (id);


--
-- Name: TABLE account_ledger; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.account_ledger TO svc_migrator;


--
-- Name: SEQUENCE account_ledger_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.account_ledger_id_seq TO svc_migrator;


--
-- PostgreSQL database dump complete
--

\unrestrict da9HRXUhf1bU5PStdW4qJHxiXI19v1BR3jCMw48xaZm0VpdW2LCUM3xYfYeddc4

