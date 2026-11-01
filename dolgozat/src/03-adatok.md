# Adatok és feladat

Ebben a fejezetben bemutatjuk a mérés tárgyát: a példaüzemek rajzát, a tagelt elemeikhez
tartozó gyártói adatlapokat és az üzemenként 60 kérdésből álló kérdéssort. Az első prototípus egy
kis, négylapos üzemen készült. A közös rendszert ezután két fejlesztési üzemen (30 és 50 lap)
hangoltuk, a hangolt és befagyasztott rendszert pedig két tesztüzemen (100 és 1000 lap) mértük
meg, amelyeket a hangolás során nem használtunk.

## A kis példaüzem (az első prototípus)

Az első prototípushoz egy közepesen bonyolult, többlapos P&ID-t generáltunk Kiszely Benedek
generátorával (plantgraph), annak egyszerűbb, első változatával. A generátor véletlenszerűen
dönt; a seed a véletlenszám-generátorának kezdőértéke, és ugyanaz a seed mindig ugyanazt az üzemet
adja, így az üzem pontosan újra előállítható. A valósághűbb, későbbi
változatot azért nem használhattuk, mert csak az első változatban lehet a generált
berendezésosztályokat (a berendezéssúlyokkal) azokra szűkíteni, amelyekhez van gyártói
adatlapunk, és ez az adatlapok hozzárendeléséhez szükséges; a későbbi változat olyan
berendezésosztályokat is generál, amelyekhez nincs adatlapunk. A generátor pyDEXPI-modellt épít, a lapokra bontó a vágott vezetékekből
lapok közötti csatlakozópárokat (off-page connector) képez, és maga a bontás a megoldókulcs. A
generátort nem módosítottuk, két ponton szűkítettünk. Először a berendezéssúlyokkal csak olyan
berendezésosztályokat engedtünk meg, amelyekhez van adatlap (centrifugálszivattyú, hőcserélő).
Másodszor a szabályozóköröket szűrtük. A generátor szabályozóköröket is tesz az üzembe, és
mindegyik kör egy változót szabályoz: áramlást, szintet, nyomást vagy hőmérsékletet. A kör
távadójához adatlap kell, a gyűjteményünk egyetlen távadó-adatlapja (Rosemount 3051) viszont
nyomás- és nyomáskülönbség-távadóé, amely a nyomás és az áramlás mérését lefedi, a szintét és a
hőmérsékletét nem. A kis prototípus-üzemhez ezért csak olyan üzemet fogadtunk el, amelynek minden
köre áramlás- vagy nyomásszabályozó kör. A seedeket sorban (1, 2, 3, …) kipróbáltuk, és az első
olyan üzemet fogadtuk el, amely ezen felül 20–40 tagelt elemet és 2–4 lapot tartalmaz, és
amelyben minden adatlaptípus szerepel (ez a 6-os seed volt). Az üzem 26 tagelt elemből és 4
lapból áll, 4 lapközi csatlakozópárral; a Neo4j-ben tárolt üzemi rétege 36 csúcs és 116
kapcsolat (EXP-002). A visszaépítési ellenőrzés (a lapokból feloldott
üzem azonos-e a generálttal) hibátlan volt.

![A kis példaüzem egyik lapja. A jobb szélen a lapközi csatlakozó.](../../figures/pid_sheet0.png)

## A fejlesztési és a tesztüzemek

A kis üzem négy lapja egy valódi üzemnél nagyságrendekkel kisebb, ezért a közös rendszert négy
nagyobb üzemen hangoltuk és mértük. A két fejlesztési üzem pontosan 30 és 50 lapos; ezeken
hangoltuk a módszereket. A két tesztüzem pontosan 100 és 1000 lapos; ezeket a hangolás során nem
használtuk, és a hangolt, befagyasztott módszereket ezeken mértük meg. Mind a négyet ugyanazzal a
generátorral, ugyanazokkal a berendezéssúlyokkal és ugyanazzal a hét adatlappal generáltuk; az
egységszámot (17, 28, 57, illetve 600) úgy választottuk, hogy a lapszám pontosan elérhető legyen,
és az elfogadási feltétel a pontos lapszám volt (az első elfogadott seed: 13, 5, 12, illetve 1;
EXP-080, EXP-092). A nagyobb üzemeknél nem követeltük meg, hogy minden kör áramlás- vagy
nyomásszabályozó legyen, mert ennyi körnél szinte minden üzemben van szint- és
hőmérséklet-szabályozó kör is, így egyetlen seed sem felelt volna meg. Ehelyett a szint- és
hőmérséklet-távadók egyszerűen nem kapnak adatlapot, ahogy egy valódi üzemben sincs minden elem
adatlapja kéznél.

Táblázat: A fejlesztési és a tesztüzemek (EXP-080, EXP-092)
| Szerep | Lap | Egység | Tagelt elem | Adatlappal | Szabályozófunkció adatlap nélkül | Szint- vagy hőmérséklet-távadó adatlap nélkül |
|---|---|---|---|---|---|---|
| fejlesztési | 30 | 17 | 206 | 174 | 19 | 13 |
| fejlesztési | 50 | 28 | 378 | 324 | 40 | 14 |
| teszt | 100 | 57 | 772 | 644 | 87 | 41 |
| teszt | 1000 | 600 | 7854 | 6641 | 821 | 392 |

Egy adatlap így több tag-et is leír: a 30 lapos üzemen például 53 szivattyú ugyanazt a Gorman-Rupp
adatlapot kapja, ahogy egy valódi üzemben is ugyanaz a típus több helyen beépül. A 30, 100 és
1000 lapos üzem lapszámban 7,5-szer, 25-ször, illetve 250-szer, a tagelt elemek számában
körülbelül 8-szor, 30-szor, illetve 300-szor nagyobb a kis üzemnél. A generátor szabályokra épül
(egységek, berendezések, csővezetékek, ISA-szerű tag-ek, szabályozókörök, lapközi csatlakozók), de
az üzemek nem létező üzemek rajzai: a kapcsolások véletlenszerűek, a technológia nincs méretezve.

## Adatlapok

A tagelt elemek osztálya és szerepe határozza meg az adatlapot (lásd az alábbi táblázatot). A hozzárendelést
program állítja elő a generátor kimenetéből (`data/plant/tag_to_datasheet.json`), nem kézzel. A
szabályozókör által működtetett globe szelep a Fisher ET szabályozószelep, a kör nélküli globe
szelep a GF 165 mágnesszelep (kétutas, globe kialakítású nyitó-záró szelep). A két
szabályozófunkcióhoz (FIC, PIC) nem rendeltünk adatlapot, mert ezek a folyamatirányító
rendszer funkciói, gyártói adatlapjuk nincs.

Táblázat: Elemosztályok és adatlapok a példaüzemben (EXP-002, EXP-006, EXP-007)
| DEXPI-osztály (szerep) | Tag-ek | Adatlap | Oldal |
|---|---|---|---|
| CentrifugalPump | P-1-1 … P-2-3 (8 db) | Gorman-Rupp VGH (0700286) | 6 |
| HeatExchanger | E-1-1, E-2-1, E-2-2, E-2-3 | Alfa Laval M3 | 2 |
| GlobeValve (szabályozókörben) | FV-2-2, PV-2-1 | Fisher ET (D100022X012) | 36 |
| GlobeValve (kör nélkül) | GV-1-1, GV-1-2, GV-2-2 | GF Type 165 mágnesszelep | 6 |
| BallValve | BV-2-1 | Flowserve Worcester F51/F52 | 12 |
| CheckValve | CHV-1-1 … CHV-2-2 (4 db) | Swagelok MS-01-176 | 16 |
| ProcessSignalGeneratingFunction | FT-2-2, PT-2-1 | Rosemount 3051 (00813-0100-4001) | 114 |

Az adatlapokból a plantdocs tíz lépéses folyamata épít ISO 15926 / QUDT szerinti tudásgráfot
(Azure Document Intelligence, rekordok, ábrák, diagramok, célformátum, forrásleírások,
szókészlet, RDF). A korábban feldolgozott négy eszköz közül a Fisher, a GF 165 és a
Gorman-Rupp gráfja a plantdocs Opusszal épített változata. A
Rosemount 3051-et és a három új adatlapot most dolgoztuk fel: a folyamat programlépései
változatlanok, az LLM-lépéseket a claude-opus-5-5 modell végezte (EXP-006). A Rosemount 3051
Opus-gráfja 91 202 tripletből és 3538, az eszközről szóló tényből áll, szemben ugyanennek a
dokumentumnak a plantdocs korábbi, GLM-mel épített gráfjával (20 973 triplet, 626 tény). A három új adatlap gráfja 1102, 16 281 és 66 747 tripletes
(Alfa Laval M3, Worcester F51/F52, Swagelok MS-01-176; EXP-006).

## A kérdéssor

A kis üzem kérdéssora 60 kérdésből áll, négy családban (lásd a második táblázatot ebben a
fejezetben). Családonként 5 kérdés a fejlesztési (dev) halmazba, 10 a teszthalmazba került; a
teszthalmazt az első prototípus fejlesztése előtt befagyasztottuk (sha256-tal rögzítve, EXP-004),
és csak a prototípus végső mérésénél futtattuk. A két fejlesztési és a két tesztüzem kérdéssorát
ugyanaz a program, ugyanazzal a seeddel állította elő (EXP-081, EXP-092). A fejlesztési üzemek
kérdéseit a hangoláshoz használtuk; a tesztüzemek kérdéseit a hangolás alatt nem futtattuk, ott
mind a 60 kérdés tesztkérdés. Minden üzemhez tartozik 12 további, több adatlapot összevető kérdés
is (az (e) család, EXP-009, EXP-081, EXP-092).

Táblázat: A kérdéscsaládok (EXP-004)
| Család | Mit kérdez | Referenciaválasz forrása | Dev / teszt |
|---|---|---|---|
| (a) csak rajz | kapcsolat, áramlási út, felső források, műszerek, típus, egység, lapok | Benedek kérdésgenerátora a gold gráfból | 5 / 10 |
| (b) csak adatlap, tag-en át | „Regarding P-1-3 on the P&ID: …” | Szabó Zsombor egyéni munkájának kérdés–válasz párjai | 5 / 10 |
| (c) összetett | egy topológiai lépés és egy adatlapi tény | programmal összerakva (a) és (b) goldjából | 5 / 10 |
| (d) megválaszolhatatlan | nem létező tag, a dokumentumban nem szereplő tény | Benedek generátora, plantdocs „not in document” párok | 5 / 10 |

Az összetett kérdések topológiai lépését a gold üzemgráfból program számolja: csak egyértelmű
lépés marad (pl. „a P-1-1 előtt közvetlenül álló elem”, „az E-2-1-et mérő távadó”, „a PIC-2-1
kör által működtetett szelep”), és csak olyan, amelynek cél-eleméhez van gold kérdés. A
kérdés szövege a lépés és az eredeti adatlapi kérdés összefűzése. A (b)–(d) családok
referenciaválaszai modellkészítésűek: az adatlapi válaszokat (Szabó Zsombor egyéni munkájából) egy
Opus-modell írta a PDF-ből, és azokat ember nem ellenőrizte. Ezt a korlátot a kiértékelésnél figyelembe
vesszük.

## Pontozás

Ahol a válasz programmal ellenőrizhető, programmal pontozunk. Az (a) család és a rajzos
megválaszolhatatlan kérdések Benedek pontozóját használják (tag-ek halmaza, rendezett út, szám,
igen/nem, tartózkodás). A szabad szöveges kérdéseknél programmal helyes a válasz, ha a gold
minden kötelező eleme számot tartalmaz, és minden szám a mértékegységével együtt megjelenik a
válaszban; programmal rossz a megválaszolható kérdésre adott „nincs benne”, programmal helyes a
megválaszolhatatlanra adott „nincs benne”. Minden más tételt vak bíráló pontoz: a claude-opus-5-5 modell
(vak bírálóként), Szabó Zsombor egyéni munkájának bírálati promptjával szó szerint (helyes, részben helyes, rossz,
hallucinált). A bíráló csak a kérdést, a gold választ és a jelölt választ látja; a tételek
sorrendje kevert, az azonosítójuk nem árulja el, melyik módszer és melyik modell válaszolt.
Pontosságnak a helyes válaszok arányát tekintjük.
