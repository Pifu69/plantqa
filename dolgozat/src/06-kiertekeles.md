# Kiértékelés

Ebben a fejezetben bemutatjuk a fejlesztési iterációkat, a befagyasztott teszthalmazon végzett
végső mérést, a költséget és a késleltetést, a módszerek útvonalait és a jellemző hibákat. Minden
szám a megadott mérésből származik (`docs/eredmenyek.md`).

## Beállítás

Mindhárom módszert mindkét kérdés-válaszoló modellel futtattuk: `z-ai/glm-5.3-flash` és
`openai/gpt-6-luna`, OpenRouteren át, Benedek rögzített paramétereivel. A Luna-pinek Benedek
pin-fájljai, a GLM-hez az ő `pin_low` beállítását és annak magas gondolkodású változatát
használtuk. Minden hívás cache-elt és naplózott; a teljes projekt költsége jóval a 20 USD-s keret
alatt maradt (a pontos összeget az összefoglalás adja). A pontosság a helyes válaszok aránya; a
konfidenciaintervallum 10 000 ismétléses, seedelt percentilis-bootstrap, a módszerpárok
különbségét ugyanazokon a kérdéseken, párosítva számoltuk.

## Fejlesztési iterációk

A dev halmazon (20 kérdés) négy iterációt mértünk (lásd az alábbi ábrát). Az első iterációban
(EXP-010) a Rosemount 3051 Opus-gráfja még nem készült el, ezért a nyomás- és áramlástávadóra
vonatkozó adatlapi kérdések egyik gráfos módszerrel sem voltak megválaszolhatók. A második
iterációban (EXP-011) az M1 Cypher-szintje megkapta a plantdocs A2 lekérdezési szabályait (széles
keresés, eset, lábjegyzet és oldal visszaadása), az M2 és az M3 pedig egy válaszszabályt
(részválasznál a meglévő rész és a hiányzó rész megnevezése, a dokumentumon túli tanács
tilalma); az M2 és az M3 hallucinációi ezzel eltűntek. A harmadik iterációban (EXP-012) a
Rosemount-gráf is bekerült: az M1 pontossága 0,60-ról 0,75-re, az M2-é 0,85-ről 0,95-re nőtt, az
M3-é nem változott, mert nem használja a gráfot. A negyedik iterációban (EXP-013) a befagyasztott
módszereket GPT-6 Lunával mértük: M1 0,60, M2 0,70, M3 0,60.

![A dev halmazon mért pontosság iterációnként (EXP-010–EXP-013).](../../figures/dev_progress.png)

## Végső mérés a teszthalmazon

A befagyasztott teszthalmaz (40 kérdés, családonként 10) mindegyik párosításon egyszer futott
le (EXP-020). Az eredményt az alábbi táblázat és ábra mutatja.

Táblázat: A végső teszt eredménye párosításonként és családonként (EXP-020)
| Módszer | Modell | Helyes | Részben | Rossz | Hallucinált | Pontosság [95% CI] | (a) | (b) | (c) | (d) |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | GLM-5.3 Flash | 25 | 9 | 6 | 0 | 0,625 [0,475–0,775] | 8/10 | 3/10 | 4/10 | 10/10 |
| M2 | GLM-5.3 Flash | 31 | 6 | 3 | 0 | 0,775 [0,625–0,900] | 8/10 | 7/10 | 6/10 | 10/10 |
| M3 | GLM-5.3 Flash | 30 | 1 | 9 | 0 | 0,750 [0,600–0,875] | 9/10 | 5/10 | 6/10 | 10/10 |
| M1 | GPT-6 Luna | 27 | 6 | 7 | 0 | 0,675 [0,525–0,825] | 9/10 | 5/10 | 4/10 | 9/10 |
| M2 | GPT-6 Luna | 28 | 7 | 5 | 0 | 0,700 [0,550–0,850] | 8/10 | 5/10 | 6/10 | 9/10 |
| M3 | GPT-6 Luna | 26 | 6 | 8 | 0 | 0,650 [0,500–0,800] | 8/10 | 4/10 | 5/10 | 9/10 |

![A végső teszt pontossága családonként, a hat párosításon (EXP-020).](../../figures/test_by_family.png)

A legjobb párosítás az M2 GLM-mel (31 helyes a 40-ből). GLM-mel az M1 szignifikánsan elmarad
mind az M2-től (párosított különbség −0,150, 95% CI −0,275 és −0,025 között), mind az M3-tól
(−0,125; −0,225 és −0,025 között), az M2 és az M3 különbsége viszont nem szignifikáns (+0,025;
−0,075 és +0,125 között). Lunával egyik különbség sem szignifikáns. Egyik párosítás sem
hallucinált a teszten; a megválaszolhatatlan kérdéseken (d) mindegyik módszer 9 vagy 10 helyes
választ adott. A különbség a (b) és (c) családon jön ki: az adatlapi kérdéseken az M2 GLM-mel
7/10, az M1 GLM-mel 3/10.

## Költség és késleltetés

Táblázat: Költség, késleltetés és tokenhasználat kérdésenként a végső teszten (EXP-020)
| Módszer | Modell | Költség / kérdés (USD) | Medián késleltetés (s) | Átlagos bemeneti token / kérdés | Átlagos kimeneti token / kérdés |
|---|---|---|---|---|---|
| M1 | GLM-5.3 Flash | 0,00453 | 12,9 | 81 492 | 3 940 |
| M2 | GLM-5.3 Flash | 0,00234 | 16,2 | 33 068 | 2 221 |
| M3 | GLM-5.3 Flash | 0,00029 | 13,2 | 13 264 | 1 820 |
| M1 | GPT-6 Luna | 0,00539 | 13,7 | 56 398 | 1 578 |
| M2 | GPT-6 Luna | 0,00213 | 17,6 | 35 765 | 1 115 |
| M3 | GPT-6 Luna | 0,00182 | 4,2 | 12 901 | 425 |

![Kérdésenkénti költség és medián késleltetés (EXP-020); két külön panel, mert a két mennyiség skálája eltér.](../../figures/test_cost_latency.png)

A legdrágább az M1: a kaszkád első szintje a teljes kétrétegű sémát kapja promptban, és ha nem
fogadják el a válaszát, az ágens is lefut, amely tagenként külön adatlap-hívásokat indít. Az M2
körülbelül feleannyiba kerül, mert csak a szükséges eszközt hívja. Az M3 a legolcsóbb, és
Lunával a leggyorsabb is: egyetlen hívás, de a teljes rajzot és tizenkét adatlap-darabot viszi
magával. Ez a példaüzemen olcsó, mert a rajz kicsi (36 csúcs); Benedek mérései szerint a
ContextRAG költsége a lapszámmal meredeken nő (a plantgraph README-je szerint), ezért az M3
előnye nagyobb üzemen nem várható.

## Útvonalak

Az M1 GLM-mel a 40 tesztkérdésből 21-et a Cypher-szinten zárt le, 7-hez az ágens is kellett
adatlap-hívás nélkül, 12-höz az ágens és legalább egy `datasheet_fact` hívás; Lunával ugyanez
22, 7 és 11 (EXP-020). Az M2 GLM-mel 13 kérdésnél csak a rajzot, 14-nél csak az adatlapot, 13-nál
mindkettőt kérdezte; Lunával 14, 13 és 13.

![Az M1 és az M2 útvonalai a végső teszten (EXP-020).](../../figures/test_routes.png)

## Hibaelemzés

**Az M1 egyetlen lekérdezése.** Az M1 hibáinak nagy része „részben helyes” válasz: a Cypher-szint
egy szűk lekérdezéssel talál egy releváns adatpontot, a kaszkád elfogadja a nem üres eredményt,
és a válaszból kimarad egy feltétel vagy egy második érték. A dev halmazon (EXP-012) például a
szivattyú 266 psi-s burkolatnyomása megvolt, a 100 °F-ig érvényes 250 psi-s üzemi határ nem. Az
elfogadási szabály a rajzi kérdésekre készült, ahol a nem üres sorhalmaz jó jelzés; adatlapi
kérdésnél a hiányos sor is nem üres.

**A rajzi kérdések közös hibái.** A teszt (a) családjában három kérdést több módszer is elrontott.
Az izolációs kérdésnél („To isolate P-1-5 from all upstream equipment, which valves must be
closed?”) a gold válasz egyetlen szelep, a módszerek többsége a felfelé eső összes szelepet
felsorolta. A szabályozókörös kérdésnél („Which control loops act on valves directly connected to
P-2-1?”) az M2 mindkét modellel a szelepet (PV-2-1) adta meg a kör (PIC-2-1) helyett: a router a
rajzeszköznek szabad szöveges kérdést ad, és a válasz alakja ott elcsúszott. A P-2-1-ből lefelé
eső elemek halmazánál az M1 GLM-mel és az M3 Lunával hiányos listát adott.

**Megválaszolhatatlan kérdések.** Mindegyik módszer jól kezelte: a nem létező tagekre és a
dokumentumban nem szereplő tényekre „nincs benne” válasz jött, egyetlen hallucináció nélkül.

**A referencia korlátja.** A (b)–(d) család referenciaválaszait egy modell írta a PDF-ből, és
ember nem ellenőrizte őket; a bíráló ugyanazt a referenciát látta minden módszernél, ezért az
összevetés igazságos, de az abszolút számok a referencia hibáival együtt értendők.
