# Összefoglalás

Két egyéni munkát kötöttünk össze: a P&ID-rajzokból épített üzemi gráfot és a gyártói
adatlapokból épített, eszközönkénti ISO 15926 gráfokat. Egy seedelt, négylapos példaüzemen,
amelynek minden tagelt fizikai eleméhez gyártói adatlap tartozik, egyetlen Neo4j-adatbázisba
töltöttük a két réteget, és egy tagalapú kapcsolattal kötöttük össze őket. Három
kérdés-válaszoló módszert mértünk két modellel egy 60 kérdéses, négy családra bontott
kérdéssoron, befagyasztott teszthalmazzal.

## Válaszok a kutatási kérdésekre

**RQ1.** A rajzot és az adatlapot összekötő kérdések megválaszolhatók az összevont gráfon: az M1
a teszten GLM-mel 25, Lunával 27 helyes választ adott a 40-ből (EXP-020). A két meglévő rendszert
külön hívó router (M2) azonban pontosabb volt: GLM-mel 31 helyes válasszal ez lett a legjobb
párosítás, és GLM-mel az M1 elmaradása mind az M2-től, mind a gráf nélküli M3-tól statisztikailag
is kimutatható. Lunával a három módszer különbsége nem szignifikáns. A gráf nélküli baseline
ezen a kis üzemen versenyképes volt.

**RQ2.** Kérdésenként az M1 volt a legdrágább (GLM-mel 0,00453, Lunával 0,00539 USD), az M2 GLM-mel körülbelül fele, Lunával 0,4-szerese ennyi (0,00234, illetve 0,00213 USD), az M3 a legolcsóbb (GLM-mel 0,00029 USD); a medián késleltetés 4 és 18 s
között volt (EXP-020). A kis rajz miatt az M3 olcsó; Benedek mérései szerint a teljes rajzot
promptba tevő megközelítés költsége a lapszámmal meredeken nő.

**RQ3.** A rajzi (a) és a megválaszolhatatlan (d) kérdéseken mindhárom módszer erős, a
különbség az adatlapi (b) és az összetett (c) kérdéseken jön ki. Az M1 jellemző hibája a hiányos
egylekérdezéses válasz: a kaszkád elfogadási szabálya a rajzi kérdésekre készült, és egy nem üres,
de hiányos adatlapi sort is elfogad. Egyik módszer sem hallucinált a teszten. A kiegészítő, több
adatlapos kérdéseken (EXP-030) a különbség még nagyobb: teljesen helyes választ csak a router adott
(GLM-mel 3, Lunával 1 a 12-ből), legalább részben jót GLM-mel 9, Lunával 10 kérdésre, a gráf
nélküli baseline 2, illetve 0 kérdésre.

## Korlátok

- **Egy példaüzem, kis rajz.** Az eredmény egyetlen, 26 tagelt elemes, négylapos szintetikus
  üzemre érvényes; a rajzot Benedek v1 generátora állította elő, nem valódi rajz.
- **Modellkészítésű referenciák.** A (b)–(d) család referenciáit egy modell írta a PDF-ből, ember
  nem ellenőrizte őket; a bíráló is modell (vak, de nem ember).
- **Kis minta.** Családonként 10 tesztkérdés; a konfidenciaintervallumok szélesek.
- **Hiányzó szókészlet-ellenőrzés.** A POSC Caesar régi SPARQL-végpontja a mérés idején nem volt
  elérhető, ezért az új adatlapgráfokban csak az rds- és CFIHOS-illesztések szerepelnek.
- **A rajzot nem változtattuk.** A kaszkádot Benedek a valósághűbb v2 üzemekre hangolta; mi a v1
  generátort használtuk, mert csak az szűkíthető az adatlappal rendelkező elemosztályokra.

## Továbblépés

A legközvetlenebb javítás az M1 elfogadási szabályának adatlapi kérdésekre szabott változata
(például a feltétel és az oldalszám meglétének ellenőrzése), és egy olyan Cypher-szint, amely a
rajzi lépés után az adatlapi részt a plantdocs A2-re bízza. Hosszabb távon a mérést nagyobb,
valódi rajzokon és emberileg ellenőrzött referenciákkal kell megismételni.
