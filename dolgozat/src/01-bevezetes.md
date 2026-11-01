# Bevezetés

Egy ipari üzemet több ezer oldalnyi, sokféle dokumentáció ír le. A csővezeték- és műszerezési
rajzok (angol rövidítéssel P&ID-k) azt mutatják meg, hogyan kapcsolódnak egymáshoz a berendezések,
szelepek és műszerek; a gyártói adatlapok pedig az egyes eszközök műszaki jellemzőit adják meg. A
rajzon minden elemnek egyedi azonosítója, tag-je van (például P-101 egy szivattyú), és ez köti
össze a rajzot az eszköz adatlapjával. Az üzemeltető és a tervező mérnökök kérdései gyakran
mindkét dokumentumfajtát érintik: „Mekkora a megengedett legnagyobb nyomás azon a szelepen, amely
a P-101 szivattyú nyomóoldalát elzárja?” A válaszhoz előbb a rajzon kell megtalálni a szelepet
(a vezeték akár egy másik rajzlapon is folytatódhat), majd a tag-je alapján az adatlapját, és
abban a megfelelő feltételhez tartozó értéket. Ma ezt kézzel végzik.

A nagy nyelvi modellek (angol rövidítéssel LLM-ek) kézenfekvő segítségnek tűnnek, az üzemi
dokumentáció azonban nehéz terep számukra. A lényeges információ jelentős része nem egyetlen
elemben van, hanem a kontextusban: egy táblázat fejlécében, egy értéket korlátozó lábjegyzetben
vagy egy lapközi csatlakozóban, amely egy csővezetéket egy másik rajzlapon folytat. Ezt a
szerkezetet egy tudásgráf teheti explicitté. A tudásgráf olyan adatbázis, amelyben a dolgok
csúcsok, a köztük lévő kapcsolatok élek; a gráfalapú, visszakereséssel kiegészített generálás
(GraphRAG) során a modell a kérdéshez tartozó részt visszakeresi a gráfból, és ebből fogalmazza
meg a választ. Ez azonban csak akkor működik, ha a gráf megőrzi a kontextust.

Közös munkánk ugyanennek a dokumentációnak két, egymást kiegészítő oldalát vizsgálja. A
rajzoldali rész, Kiszely Benedek László egyéni munkája (a továbbiakban **plantgraph**), egy egész
üzem rajzlapjaiból épít tudásgráfot: a berendezések és műszerek csúcsok, a csövek és jelvezetékek
élek, és a lapok határán megszakadó vezetékek újra összekapcsolódnak. Erre a gráfra építve egy
kétlépcsős rendszer, a **kaszkád** válaszol a kérdésekre: először egyetlen adatbázis-lekérdezéssel
próbálkozik, és ha ez nem elég, egy gráfbejáró eszközöket hívó nyelvi modell, egy úgynevezett
ágens veszi át a kérdést. Az adatlapoldali rész, Szabó Zsombor István egyéni munkája (a
továbbiakban **plantdocs**), egy-egy eszköz PDF-adatlapjából épít tudásgráfot, amelyben minden
érték mellett megmarad a mértékegysége, az érvényességi feltétele (például „csak 100 °F alatt”) és
a forrásoldala, vagyis az adatlapnak az az oldala, ahol az érték nyomtatva szerepel. A feltételt
azért kell megőrizni, mert egy feltétel nélküli érték nem hiányos, hanem hibás. A plantdocs a gráf
lekérdezésére két módszert hasonlított össze; ebben a munkában a jobbat, az **A2**-t használjuk,
amely a gráfra egy nyelvi modell által írt adatbázis-lekérdezéssel és jelentés szerinti
(vektoros) kereséssel válaszol.

A két munka együtt ugyanazt a kérdést járja körül: hogyan őrizhető meg a szerkezet és a kontextus,
amikor az ipari dokumentációt gráffá alakítjuk. Mindkettő egyetlen dokumentumfajtára szorítkozik,
így természetes továbblépés, hogy az eszközönkénti adatlapgráfokat a rajzokon szereplő
berendezésekhez kössük, és az egész üzemről egyetlen lekérdezhető modell jöjjön létre. Ez a
dolgozat ezt a lépést teszi meg, és megméri, mennyire jól válaszolnak az így kapott rendszerek a
két dokumentumfajtát együtt igénylő kérdésekre.

## Kutatási kérdések és hozzájárulások

A dolgozat három kérdésre keres választ. Először arra, hogy a rajzokból és az adatlapokból külön
épített tudás összeköthető-e egyetlen lekérdezhető tudásgráfban úgy, hogy közben a rajz
kapcsolatai és az adatlapi értékek feltételei is megmaradjanak (RQ1). Másodszor arra, hogy egy
ilyen gráf fölött működő kérdés-válaszoló rendszer megbízhatóan megválaszolja-e a mindkét
dokumentumfajtát igénylő kérdéseket, és hogyan viszonyul két kézenfekvő alternatívához: a két
meglévő rendszer külön hívásához és a gráf nélküli megoldáshoz, amely a teljes rajzot a modell elé
teszi (RQ2). Harmadszor arra, hogy hogyan változik a pontosság és a költség, ha az üzem mérete egy
nagyságrenddel nő (RQ3).

A válaszokhoz négy lépésben jutottunk el, és ezek adják a dolgozat hozzájárulásait. Először
áttekintettük a mérnöki tervezési dokumentumok, elsősorban a P&ID-k és a gyártói adatlapok gépi
feldolgozásáról és a rajtuk működő kérdés-válaszolásról szóló szakirodalmat; ebben nem találtunk
olyan munkát, amely a kettőt összekötné (2. fejezet). Másodszor megvizsgáltuk, hogy a P&ID-kból
és a hozzájuk tartozó adatlapokból építhető-e integrált tudásgráf: a rajzi üzemi réteget és hét
eszköz adatlapgráfját egy adatbázisba töltöttük, és a tag-ek alapján összekötöttük, a két
forrásrendszer módosítása nélkül (4. fejezet). Harmadszor erre a gráfra kérdés-válaszoló
rendszert, vagyis chatbotot építettünk három változatban, és egy webes demóban mindegyiket
kipróbálhatóvá tettük a válasz útvonalával és forrásoldalaival együtt (5. és 7. fejezet).
Negyedszer a rendszert működőképességre és skálázhatóságra teszteltük öt, ugyanazzal a
generátorral készült üzemen, a 4 lapostól az 1000 laposig, üzemenként 60 kérdésen és 12, több
adatlapot összevető kérdésen, két nyelvi modellel; a hangoláshoz és a teszthez külön üzemeket
használtunk (3. és 6. fejezet).

## Munkamegosztás

A rajzoldali rendszert (az üzemgenerátort, a lapokra bontást és a visszaépítést, az üzemi gráfot
és a kaszkádot) Kiszely Benedek László, az adatlapoldali rendszert (a feldolgozó folyamatot, az
ISO 15926 szerinti adatlapgráfot és az A2-lekérdezést) Szabó Zsombor István készítette egyéni
munkaként. Ebben a dolgozatban mindkét rendszert változtatás nélkül használjuk. Az összevonást, a
kérdéssort, a három kérdés-válaszoló módszert, a méréseket és a demót közösen készítettük. A
továbbiakban a két rendszerre a nevükkel (plantgraph, plantdocs) hivatkozunk.

## A dolgozat felépítése

A 2. fejezet a hátteret és a kapcsolódó munkákat foglalja össze. A 3. fejezet a mérés tárgyát
mutatja be: a példaüzemeket, az adatlapokat, a kérdéssort és a pontozást. A 4. fejezet leírja,
hogyan épül fel az összevont tudásgráf, az 5. fejezet pedig a rá épülő három kérdés-válaszoló
módszert. A 6. fejezet a mért eredményeket, a 7. fejezet a demót mutatja be két végigkövetett
kérdéssel, a 8. fejezet pedig összefoglalja a kutatási kérdésekre adott válaszokat és a munka
korlátait. A függelékek a példakérdéseket (A), az M2 és az M1 promptjainak részleteit (B, C), a
két forrásfolyamat részletes leírását (D), a módszerek lépéseinek részleteit (E), további
demó-képernyőképeket (F) és az első, négylapos prototípus méréseit (G) tartalmazzák.
