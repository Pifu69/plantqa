# Adatok és feladat

Egy összevont tudásgráf értékét csak olyan kérdéseken lehet lemérni, amelyeknek ismert a helyes
válasza. Ebben a fejezetben bemutatjuk a mérés tárgyát: a példaüzemek rajzát, a tagelt elemekhez
tartozó gyártói adatlapokat, az üzemenként 60 kérdésből álló kérdéssort és azt, hogyan pontozzuk
a válaszokat. Az üzemeket három célra használtuk. Az első prototípus egy kis, négylapos üzemen
készült; a közös rendszert ezután két fejlesztési üzemen (30 és 50 lap) hangoltuk; végül a
hangolt és befagyasztott rendszert két tesztüzemen (100 és 1000 lap) mértük meg, amelyeket a
hangolás során nem használtunk.

## A példaüzemek

Mind az öt üzemet a plantgraph generátorának egyszerűbb, első változatával készítettük. A két
változat abban különbözik, hogy az első hat berendezésosztállyal (centrifugálszivattyú,
kompresszor, tartály, nyomástartó edény, oszlop, hőcserélő) és háromféle szeleppel (globe, golyós,
visszacsapó) dolgozik, a berendezéseket véletlen faszerkezetben köti össze, és műszer csak a
szabályozókörökben van. A későbbi változat valódi folyamategységek mintáiból építi az üzemet
(például oszloprendszer, kompresszorfokozat, tartálypark), a berendezések köré a szokásos
kiegészítő elrendezéseket rajzolja (biztonsági szelep, leürítők, légtelenítők), és az elemek
között jelöletlen idomok is állnak. Ez valószerűbb rajzot ad, de csak az első változatban lehet a
generált berendezésosztályokat azokra szűkíteni, amelyekhez van gyártói adatlapunk, és erre a
hozzárendeléshez szükség van.

A generátort nem módosítottuk, csak két ponton szűkítettük a kimenetét. Először csak olyan
berendezésosztályokat engedtünk meg, amelyekhez van adatlap (centrifugálszivattyú, hőcserélő).
Másodszor a szabályozóköröket szűrtük. A generátor minden köre egy változót szabályoz (áramlást,
szintet, nyomást vagy hőmérsékletet), és a kör távadójához adatlap kell; egyetlen
távadó-adatlapunk (Rosemount 3051) viszont nyomás- és nyomáskülönbség-távadóé, amely a nyomás és
az áramlás mérését lefedi, a szintét és a hőmérsékletét nem. A kis prototípus-üzemhez ezért csak
olyan üzemet fogadtunk el, amelynek minden köre áramlás- vagy nyomásszabályozó kör. A seedeket
sorban (1, 2, 3, …) kipróbáltuk, és az első olyan üzemet fogadtuk el, amely ezen felül 20–40
tagelt elemet és 2–4 lapot tartalmaz, és amelyben minden adatlaptípus szerepel; ez a 6-os seed
volt. Az üzem 26 tagelt elemből és 4 lapból áll, a lapok között 4 lapközi csatlakozópár van, és
a lapokból visszaépített üzem hibátlanul egyezett a generálttal.

![A kis példaüzem egyik lapja. A jobb szélen a lapközi csatlakozó.](../../figures/pid_sheet0.png)

Négy lap egy valódi üzemnél nagyságrendekkel kevesebb, ezért a közös rendszert négy nagyobb üzemen
hangoltuk és mértük. A két fejlesztési üzem pontosan 30 és 50, a két tesztüzem pontosan 100 és
1000 lapos. Mind a négyet ugyanazokkal a beállításokkal és ugyanazzal a hét adatlappal
generáltuk; az egységek számát (17, 28, 57, illetve 600) úgy választottuk, hogy a lapszám
pontosan elérhető legyen, és az elfogadás feltétele a pontos lapszám volt. A nagyobb üzemeknél
nem követeltük meg, hogy minden kör áramlás- vagy nyomásszabályozó legyen, mert ennyi körnél
szinte minden üzemben van szint- és hőmérséklet-szabályozó kör is, így egyetlen seed sem felelt
volna meg. Ehelyett a szint- és hőmérséklet-távadók egyszerűen nem kapnak adatlapot, ahogy egy
valódi üzemben sincs minden elem adatlapja kéznél.

Táblázat: A fejlesztési és a tesztüzemek
| Szerep | Lap | Egység | Tagelt elem | Adatlappal | Szabályozófunkció adatlap nélkül | Szint- vagy hőmérséklet-távadó adatlap nélkül |
|---|---|---|---|---|---|---|
| fejlesztési | 30 | 17 | 206 | 174 | 19 | 13 |
| fejlesztési | 50 | 28 | 378 | 324 | 40 | 14 |
| teszt | 100 | 57 | 772 | 644 | 87 | 41 |
| teszt | 1000 | 600 | 7854 | 6641 | 821 | 392 |

Elsőre furcsának tűnhet, hogy több ezer rajzi elemhez csak hét adatlap tartozik, de ez nem
ellentmondás: egy adatlap egy eszköztípust (egy gyártó katalógusában szereplő modellt) ír le, és
az azonos típusú rajzi elemek ugyanazt az adatlapot kapják. A 30 lapos üzemen például 53 szivattyú
kapja ugyanazt a Gorman-Rupp adatlapot, ahogy egy valódi üzemben is ugyanaz a szivattyúmodell sok
helyen be van építve. Az üzemek nem létező üzemek rajzai: a generátor szabályokra épül (egységek,
berendezések, csővezetékek, szabványos tag-ek, szabályozókörök, lapközi csatlakozók), de a
kapcsolások véletlenszerűek, és a technológia nincs méretezve. A rajz tehát véletlenszerű, de
belsőleg következetes és teljesen ismert: a generátor minden elemet, kapcsolatot és szabályozókört
pontosan ismer. Éppen ezért lehet minden kérdéshez egyértelmű, ellenőrizhető választ számolni; ehhez
nem szükséges, hogy a technológia valószerű legyen.

## Adatlapok

A tagelt elemek osztálya és szerepe határozza meg az adatlapot (lásd az alábbi táblázatot); a
hozzárendelést program állítja elő a generátor kimenetéből. A szabályozókör által működtetett
globe szelep a Fisher ET szabályozószelep, a kör nélküli globe szelep a GF 165 mágnesszelep
(kétutas, globe kialakítású nyitó-záró szelep). A szabályozófunkciókhoz (például FIC, PIC) nem
rendeltünk adatlapot, mert ezek a folyamatirányító rendszer funkciói, gyártói adatlapjuk nincs.

Táblázat: Elemosztályok és adatlapok a kis példaüzemben
| Elemosztály (szerep) | Tag-ek | Adatlap | Oldal |
|---|---|---|---|
| centrifugálszivattyú | P-1-1 … P-2-3 (8 db) | Gorman-Rupp VGH (0700286) | 6 |
| hőcserélő | E-1-1, E-2-1, E-2-2, E-2-3 | Alfa Laval M3 | 2 |
| globe szelep (szabályozókörben) | FV-2-2, PV-2-1 | Fisher ET (D100022X012) | 36 |
| globe szelep (kör nélkül) | GV-1-1, GV-1-2, GV-2-2 | GF Type 165 mágnesszelep | 6 |
| golyóscsap | BV-2-1 | Flowserve Worcester F51/F52 | 12 |
| visszacsapó szelep | CHV-1-1 … CHV-2-2 (4 db) | Swagelok MS-01-176 | 16 |
| távadó | FT-2-2, PT-2-1 | Rosemount 3051 (00813-0100-4001) | 114 |

Az adatlapokból a plantdocs feldolgozó folyamata épít tudásgráfot (4. fejezet). A Fisher, a
GF 165 és a Gorman-Rupp adatlapjának gráfja a plantdocs-ból származik; a másik négy adatlapot
(Rosemount 3051, Alfa Laval M3, Worcester F51/F52, Swagelok MS-01-176) mi dolgoztuk fel ugyanezzel
a folyamattal. Az így kapott gráfok mérete 91 202 (Rosemount 3051), 1102 (Alfa Laval M3), 16 281
(Worcester F51/F52) és 66 747 (Swagelok MS-01-176) hármas.

## A kérdéssor

Minden üzemhez egy 60 kérdésből álló, négy családra bontott kérdéssor tartozik (lásd az alábbi
táblázatot). Az (a) család csak a rajzról kérdez, a (b) csak egy adatlapról (a tag megnevezésével),
a (c) a kettőt köti össze, a (d) pedig olyan kérdéseket tartalmaz, amelyekre a dokumentumok nem
adnak választ, és ezért a helyes válasz annak kimondása, hogy nincs benne. A kis üzemen
családonként 5 kérdés a fejlesztési, 10 a teszthalmazba került; a teszthalmazt az első prototípus
fejlesztése előtt rögzítettük, és csak a végső mérésnél futtattuk. A fejlesztési és a tesztüzemek
kérdéssorát ugyanaz a program, ugyanazzal a seeddel állította elő; a fejlesztési üzemek kérdéseit a
hangoláshoz használtuk, a tesztüzemekét a hangolás alatt nem futtattuk, ott mind a 60 kérdés
tesztkérdés. Minden üzemhez tartozik továbbá 12 olyan kérdés is, amelyhez a rajzon több elemet kell
bejárni, és több adatlapot kell összevetni (az (e) család); ezeket külön értékeljük.

Táblázat: A kérdéscsaládok
| Család | Mit kérdez | Referenciaválasz forrása | Fejlesztési / teszt (kis üzem) |
|---|---|---|---|
| (a) csak rajz | kapcsolat, áramlási út, felső források, műszerek, típus, egység, lapok | program számolja a generált üzem pontos leírásából | 5 / 10 |
| (b) csak adatlap, tag-en át | „Regarding P-1-3 on the P&ID: …” | a plantdocs kérdés–válasz párjai | 5 / 10 |
| (c) összetett | egy topológiai lépés és egy adatlapi tény | program rakja össze az (a) és a (b) referenciáiból | 5 / 10 |
| (d) megválaszolhatatlan | nem létező tag, a dokumentumban nem szereplő tény | a generátor, illetve a plantdocs „nincs benne” párjai | 5 / 10 |

Az összetett kérdések topológiai lépését a generált üzem pontos leírásából program számolja. Csak
egyértelmű lépés marad (például „a P-1-1 előtt közvetlenül álló elem”, „az E-2-1-et mérő
távadó”, „a PIC-2-1 kör által működtetett szelep”), és csak olyan, amelynek cél-eleméhez van
referenciaválasszal ellátott adatlapi kérdés; a kérdés szövege a lépés és az adatlapi kérdés
összefűzése. A rajzi kérdések referenciáját tehát program számolja, az adatlapi kérdésekét egy
nyelvi modell írta az adatlap PDF-jéből, és ezeket ember nem ellenőrizte; ezt a korlátot a 8.
fejezetben tárgyaljuk.

## Pontozás

Ahol a válasz programmal ellenőrizhető, programmal pontozunk. A rajzi és a rajzra vonatkozó
megválaszolhatatlan kérdések válaszát egy program a válasz típusa szerint veti össze a
referenciával: egy tag-halmaznak halmazként pontosan egyeznie kell, egy útnak ugyanazokat az
elemeket kell tartalmaznia ugyanabban a sorrendben, egy számnak és egy igen/nem válasznak
egyeznie kell, a megválaszolhatatlan kérdésekre pedig a „nincs benne” a helyes válasz. A szabad
szöveges kérdéseknél a válasz programmal helyes, ha a referencia minden kötelező eleme számot
tartalmaz, és minden szám a mértékegységével együtt megjelenik a válaszban.

A többi választ egy vak bíróként működő nyelvi modell pontozza, rögzített utasítással. A bíró csak
a kérdést, a referenciát és a jelölt választ látja, kevert sorrendben, és nem tudja, melyik módszer
és melyik modell adta a választ. Négy ítélet lehetséges: helyes, részben helyes, rossz és
hallucinált (a válasz olyan tényt állít, amely nincs benne a dokumentumokban). Pontosságnak a
helyes válaszok arányát tekintjük. Ezzel a mérés tárgya rögzített; a következő fejezet azt
mutatja be, hogyan épül fel az a gráf, amelyen a kérdésekre válaszolunk.
