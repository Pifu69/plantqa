# Kiértékelés

Az előző két fejezetben felépített gráfot és módszereket most a 3. fejezetben leírt kérdéseken
mérjük meg. A fejezet a kutatási kérdések sorrendjét követi: előbb azt mutatjuk be, hogy az
összevont gráf a nagy üzemeken is felépíthető, majd azt, hogyan teljesítenek rajta a módszerek a
két tesztüzemen, végül azt, hogyan változik a pontosság és a költség az üzem méretével, és milyen
hibák jellemzők az egyes módszerekre.

## Beállítás

Mindhárom módszert mindkét modellel futtattuk: a GLM-5.3 Flash (a továbbiakban GLM) és a GPT-6
Luna (a továbbiakban Luna) modellt az OpenRouter szolgáltatón át értük el, a rajzoldali rendszer
rögzített beállításaival. A pontosság a helyes válaszok aránya. A konfidenciaintervallumokat
bootstrap-módszerrel számoltuk: a kérdéseket 10 000-szer újramintavételeztük visszatevéssel, és az
így kapott pontosságok középső 95%-a adja az intervallumot. Két módszer különbségét ugyanazokon a
kérdéseken, párosítva számoltuk; ha a különbség intervalluma tartalmazza a nullát, a különbség nem
szignifikáns. A teljes projekt fizetős költése 18,8923 USD volt; ebből a fejlesztési üzemek mérése
és a hangolás az 50 lapos üzemen 1,2599 USD, a két tesztüzem mérése 2,8544 USD.

Az összevont gráf a nagy üzemeken is gond nélkül felépült. Mérete az üzemmel nő, az adatlapi réteg
változatlan (27 615 csúcs, 103 366 él): a 30 lapos üzemen 274 rajzi csúcs, 931 rajzi él és 174
összekötő él jött létre, az 50 lapos üzemen 498, 1713 és 324, a 100 lapos üzemen 1018, 3515 és 644,
az 1000 lapos üzemen 10 277, 35 603 és 6641. Az 1000 lapos üzem betöltése 80,7 másodpercig tartott.

## Az első prototípus a kis üzemen

A kis üzem 20 kérdéses fejlesztési halmazán négy iterációban alakítottuk ki a módszerek első
változatát; a 40 kérdéses teszthalmazon a legjobb az M2 volt GLM-mel (31 helyes), a gráf nélküli
M3 30, az M1 25 helyes választ adott. A részleteket a Függelék G írja le.

## Hangolás a fejlesztési üzemeken

A prototípus módszereit a 30 és az 50 lapos fejlesztési üzem mind a 60 kérdésén és 12 több
adatlapos kérdésén futtattuk. Az alábbi
táblázat a hangolás előtti eredményt mutatja; a gráf nélküli M3-at nem hangoltuk, ezért csak a 30
lapos üzemen futott.

Táblázat: A fejlesztési üzemek eredménye a hangolás előtt (helyes válaszok, 60 kérdés; (e): 12 kérdés)
| Módszer | Modell | 30 lap | 50 lap | (e), 30 lap | (e), 50 lap |
|---|---|---|---|---|---|
| M1 | GLM-5.3 Flash | 45 | 47 | 2 | 3 |
| M2 | GLM-5.3 Flash | 50 | 52 | 3 | 5 |
| M3 | GLM-5.3 Flash | 41 | – | 0 | – |
| M1 | GPT-6 Luna | 49 | 44 | 2 | 0 |
| M2 | GPT-6 Luna | 46 | 43 | 2 | 4 |
| M3 | GPT-6 Luna | 38 | – | 0 | – |

A hibák elemzése az 5. fejezetben leírt három javítást hozta. Az M2 a több adatlapos kérdéseknél
minden elem adatlapját külön lekérdezi, és a hatlépéses keret a 30 lapos üzemen a 24 ilyen
válaszból 10-et, az 50 lapos üzemen 8-at üresen hagyott; ezért nőtt a keret 16 lépésre, és került
be a kötelező végső válasz. Az M1 hibáinak nagy része hiányos feltételű részválasz volt, ezért
bővültek a lekérdezési szabályai, és egy sok adatlap-hívást igénylő kérdés miatt nőtt a kaszkád
időkorlátja. A javítást az 50 lapos üzem több adatlapos kérdésein ellenőriztük: az M2 üres válaszai modellenként 4-ről 2-re
csökkentek, a teljesen helyes válaszok száma az M2-nél GLM-mel 5-ről 6-ra nőtt, Lunával 4 maradt,
az M1-nél GLM-mel 3 maradt, Lunával 0-ról 2-re nőtt. Ezután a módszereket
befagyasztottuk.

## A gráf nélküli módszer az 1000 lapos üzemen

Az M3 a teljes rajzot szövegként kapja meg a promptban. Ez a szöveg a
100 lapos üzemen 474 716, az 1000 lapos üzemen 4 793 987 karakter. Egy korábbi, 98 lapos próbaüzemen végzett mérésben
egy ekkora rajz kérdésenként átlagosan kb. 194 ezer prompttokent jelentett, ezzel az aránnyal az
1000 lapos rajz kérdésenként kb. 1,96 millió token lenne. Ez meghaladja mindkét modell kontextusát
(GLM: 1 048 576, Luna: 1 050 000 token az OpenRouter modellistája szerint), ezért az M3-at az 1000
lapos üzemen nem lehetett lefuttatni; ott csak a két gráfos módszert mértük. A teljes rajz promptba tétele
tehát egy valódi méretű üzemnél nem csak drága, hanem
kivitelezhetetlen, a gráfos módszerek viszont ugyanúgy működnek.

## Eredmény a két tesztüzemen

A hangolt, befagyasztott módszereket mindkét tesztüzem 60 kérdésén (családonként 15) mindegyik
párosításon egyszer futtattuk. Az eredményt az alábbi
táblázat és ábra mutatja. A táblázat utolsó négy oszlopa a 3. fejezetben leírt négy
kérdéscsalád helyes válaszainak száma: (a) csak a rajzról kérdez, (b) csak egy adatlapról, (c) a
kettőt köti össze, (d) pedig olyan kérdés, amelyre a dokumentumok nem adnak választ.

Táblázat: Eredmény a két tesztüzemen párosításonként és családonként (60-60 kérdés; az 1000 lapos üzemen az M3 nem futtatható)
| Módszer | Modell | Lap | Helyes | Részben | Rossz | Halluc. | Pontosság [95% CI] | (a) | (b) | (c) | (d) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | GLM-5.3 Flash | 100 | 50 | 4 | 6 | 0 | 0,833 [0,733–0,917] | 13 | 13 | 9 | 15 |
| M1 | GLM-5.3 Flash | 1000 | 43 | 6 | 10 | 1 | 0,717 [0,600–0,833] | 12 | 12 | 5 | 14 |
| M2 | GLM-5.3 Flash | 100 | 51 | 5 | 4 | 0 | 0,850 [0,750–0,933] | 13 | 12 | 11 | 15 |
| M2 | GLM-5.3 Flash | 1000 | 48 | 4 | 8 | 0 | 0,800 [0,700–0,900] | 12 | 10 | 11 | 15 |
| M3 | GLM-5.3 Flash | 100 | 44 | 2 | 14 | 0 | 0,733 [0,617–0,833] | 11 | 8 | 10 | 15 |
| M1 | GPT-6 Luna | 100 | 46 | 10 | 4 | 0 | 0,767 [0,650–0,867] | 14 | 9 | 8 | 15 |
| M1 | GPT-6 Luna | 1000 | 41 | 14 | 5 | 0 | 0,683 [0,567–0,800] | 14 | 6 | 6 | 15 |
| M2 | GPT-6 Luna | 100 | 43 | 10 | 7 | 0 | 0,717 [0,600–0,833] | 10 | 8 | 10 | 15 |
| M2 | GPT-6 Luna | 1000 | 46 | 9 | 5 | 0 | 0,767 [0,650–0,867] | 12 | 10 | 9 | 15 |
| M3 | GPT-6 Luna | 100 | 37 | 9 | 14 | 0 | 0,617 [0,483–0,733] | 13 | 3 | 9 | 12 |

![A pontosság a 100 lapos (halvány oszlop) és az 1000 lapos tesztüzemen (telt oszlop), párosításonként; az 1000 lapos üzemen az M3 nem futtatható (n. a.).](../../figures/scale_accuracy.png)

A 100 lapos tesztüzemen GLM-mel az M2 a legjobb párosítás (51 helyes a 60-ból), szorosan mögötte
az M1 (50; a különbség −0,017, 95% CI −0,083 és +0,050 között, nem szignifikáns). GLM-mel az M2
szignifikánsan jobb a gráf nélküli M3-nál (+0,117, +0,033 és +0,217 között), az M1 a határon
(+0,100, 0,000 és +0,217 között); Lunával az M1 szignifikánsan jobb az M3-nál (+0,150, +0,033 és
+0,267 között), az M2 nem (+0,100, −0,033 és +0,233 között).

Az 1000 lapos tesztüzemen is az M2 GLM-mel a legjobb párosítás (48 helyes), utána az M2 Lunával
(46), az M1 GLM-mel 43, Lunával 41 helyes választ adott; az M1 és az M2 különbsége egyik modellel
sem szignifikáns (GLM-mel −0,083, 95% CI −0,217 és +0,033 között, Lunával −0,083, −0,183 és +0,017
között). A tízszer nagyobb rajzon az M2 GLM-mel 3 kérdéssel, az M1 GLM-mel 7, Lunával 5
kérdéssel kevesebbet oldott meg, mint a 100 lapos üzemen, az M2 Lunával 3-mal többet; a
visszaesés főleg az összetett (c) családból jön (az M1 GLM-mel 9 helyett 5 helyes).

A hangolás hatása a tesztüzemen kicsi: a 100 lapos üzemen a hangolás előtti módszerekkel is
lefutott ugyanez a mérés, és a helyes válaszok száma párosításonként legfeljebb hárommal
tért el (az M2 GLM-mel 54 és 51, Lunával 42 és 43; az M1 GLM-mel 50 és 50, Lunával 45 és 46). A
hangolás tehát a fejlesztési üzemeken látott üres válaszokat csökkentette, a pontosságot a
tesztüzemen mérhetően nem változtatta; ez a kis mintán belüli ingadozás nagyságrendje.

## Költség

Táblázat: Kérdésenkénti költség a két tesztüzemen (USD)
| Módszer | Modell | 100 lap | 1000 lap |
|---|---|---|---|
| M1 | GLM-5.3 Flash | 0,00416 | 0,00592 |
| M2 | GLM-5.3 Flash | 0,00451 | 0,00866 |
| M3 | GLM-5.3 Flash | 0,00757 | – |
| M1 | GPT-6 Luna | 0,01089 | 0,01272 |
| M2 | GPT-6 Luna | 0,00248 | 0,00385 |
| M3 | GPT-6 Luna | 0,02501 | – |

A gráfos módszereknél a modellhez csak a lekérdezés eredménye jut el, ezért a kérdésenkénti
költségük sokkal lassabban nő, mint a rajz: a 100 és az 1000 lapos üzem között az M2 GLM-mel
0,00451-ről 0,00866 USD-re, Lunával 0,00248-ról 0,00385 USD-re, az M1 GLM-mel 0,00416-ról 0,00592
USD-re, Lunával 0,01089-ről 0,01272 USD-re nőtt, vagyis a tízszer nagyobb rajzon legfeljebb a
kétszeresére; ennek okát részletesen nem vizsgáltuk. Az M3 a 100 lapos üzemen GLM-mel
0,00757, Lunával 0,02501 USD-be került kérdésenként, Lunával tízszer annyiba, mint az M2 (0,00248
USD), kevesebb helyes válasszal; a fejlesztési üzemek közül a 30 lapos üzemen még 0,00206, illetve
0,00731 USD volt, az 1000 lapos rajz pedig már nem fér a modellek kontextusába. A
késleltetést a tesztüzemeken nem hasonlítjuk össze, mert a válaszok egy része (az M3 válaszai és az
M2 rajzi hívásainak egy része) a korábbi futások eltárolt válaszaiból jött.

## Több adatlapos kérdések

Mindkét tesztüzemen lefuttattuk a 12 kérdéses (e) családot is, amelyben a rajzon egy utat, egy
elemhalmazt vagy két topológiai lépést kell bejárni, és kettő–hat különböző adatlapot kell
összevetni (például: „Along the process flow path from P-2-1 to E-38-1, which item has the lowest
maximum allowable pressure according to its datasheet?”, a 100 lapos üzemen). A referenciát
program rakta össze a generátor hibátlan gráfjából és a PDF-ekből gyűjtött tényekből.

Táblázat: A több adatlapos kérdések eredménye a két tesztüzemen (12-12 kérdés)
| Módszer | Modell | Helyes, 100 lap | Részben, 100 lap | Helyes, 1000 lap | Részben, 1000 lap |
|---|---|---|---|---|---|
| M1 | GLM-5.3 Flash | 5 | 2 | 1 | 3 |
| M2 | GLM-5.3 Flash | 4 | 4 | 3 | 5 |
| M3 | GLM-5.3 Flash | 0 | 3 | – | – |
| M1 | GPT-6 Luna | 0 | 4 | 0 | 5 |
| M2 | GPT-6 Luna | 0 | 7 | 1 | 8 |
| M3 | GPT-6 Luna | 0 | 3 | – | – |

A gráf nélküli M3 a 100 lapos üzemen egyik kérdésre sem adott teljesen helyes választ. GLM-mel a
gráfos módszerek 4–5 kérdést oldottak meg teljesen (az M1 és az M3 különbsége +0,417, 95% CI
+0,167 és +0,667 között, az M2-é +0,333, +0,083 és +0,583 között), Lunával egyet sem, csak
részben (4, illetve 7 kérdés). Az 1000 lapos üzemen ezek a kérdések még nehezebbek lettek: teljesen helyes választ az M2
GLM-mel 3, Lunával 1, az M1 GLM-mel 1, Lunával egy kérdésre sem adott. Az M2 üres válaszai a hangolás után is
megmaradtak, de ritkábbak: a 100 lapos üzemen modellenként 2 (a hangolás előtt 3), az 1000 lapos üzemen
GLM-mel egy sem, Lunával 1.

## Hibaelemzés

**Téves „nincs benne” válaszok.** A gráf nélküli módszer jellemző hibája a hamis lemondás, főleg a
több adatlapos kérdéseken: az M3 GLM-mel a 30 lapos fejlesztési üzemen 7, a 100 lapos tesztüzemen 5
esetben állította, hogy a dokumentum nem tartalmazza a választ. Ez veszélyesebb, mint amilyennek látszik, mert a „nincs benne” a
megválaszolhatatlan kérdéseken helyes, így a (d) családon az M3 jól szerepel, miközben a
megválaszolható kérdéseken elbukik.

**Az M1 egyetlen lekérdezése.** Az M1 hibáinak nagy része „részben helyes” válasz: a kaszkád első
szintje egy szűk lekérdezéssel talál egy releváns adatpontot, a kaszkád elfogadja a nem üres eredményt,
és a válaszból kimarad egy feltétel vagy egy második érték (példa a Függelék G-ben). Az elfogadási
szabály a rajzi kérdésekre készült, ahol a nem üres sorhalmaz jó jelzés; adatlapi kérdésnél a
hiányos sor is nem üres.

**Az M2 eszközhívásai.** Az M2 a rajzeszköznek szabad szöveges kérdést ad, ezért a válasz alakja
elcsúszhat (a kis üzemen például a szabályozókör helyett a szelepét adta meg, Függelék G), és a
több adatlapos kérdéseknél többször üres választ adott, mielőtt minden elem adatlapját
lekérdezte volna (lépéskorlát vagy feldolgozási hiba). A hangolás után ezek ritkábbak lettek (a 100 lapos tesztüzemen modellenként 2).

**A referencia korlátja.** Az (e) család referenciája óvatos: ha valamelyik elemnek van olyan
változata, amelyhez az adatlap nem ad számot, a „legkisebb” elem nem dönthető el, és a bíráló
ilyenkor a konkrét elemet megnevező választ is rossznak ítéli. A referenciák általános korlátait a
8. fejezet foglalja össze.
