# Összefoglalás

Két egyéni munkát kötöttünk össze: a P&ID-rajzokból épített üzemi gráfot és a gyártói
adatlapokból épített, eszközönkénti ISO 15926 gráfokat. Egyetlen Neo4j-adatbázisba töltöttük a két
réteget, és egy tagalapú kapcsolattal kötöttük össze őket. Három kérdés-válaszoló módszert
fejlesztettünk egy négylapos kis üzemen, majd változtatás nélkül megmértük őket két modellel egy
27 lapos, 190 tagelt elemes nagy üzemen, 60 kérdésen és 12 több adatlapos kérdésen.

## Válaszok a kutatási kérdésekre

**RQ1.** A rajzot és az adatlapot összekötő kérdések megválaszolhatók az összevont gráfon: a nagy
üzemen az M1 GLM-mel 42, Lunával 43 helyes választ adott a 60-ból (EXP-060). A két rész meglévő
rendszerét külön hívó irányító (M2) azonban pontosabb volt: GLM-mel 51 helyes válasszal ez lett a
legjobb párosítás, és szignifikánsan megelőzte mind az M1-et, mind a gráf nélküli M3-at (35
helyes). Lunával a három módszer különbsége nem szignifikáns. A több adatlapos kérdéseken a két
gráfos módszer a 12 kérdés felét teljesen megoldotta, a gráf nélküli M3 egyet sem (EXP-061).

**RQ2.** A kis üzemen a gráf nélküli M3 versenyképes volt (30 helyes a 40-ből, EXP-020), a 27
lapos üzemen viszont GLM-mel a rajzi kérdések közül csak 6-ot oldott meg a 15-ből, és a hibái
nagy része téves „nincs benne” válasz volt (EXP-062). Az M3 kérdésenkénti költsége GLM-mel
0,00029-ről 0,00133, Lunával 0,00182-ről 0,00680 USD-re nőtt, a gráfos módszereké a centes
nagyságrendben maradt (EXP-020, EXP-060). Ez egybevág Benedek mérésével: a teljes rajz promptba
tétele a lapszámmal romlik és drágul, a gráfon lekérdező módszer nem.

**RQ3.** A rajzi (a) és a megválaszolhatatlan (d) kérdéseken a gráfos módszerek erősek, a
különbség az adatlapi (b), az összetett (c) és a több adatlapos (e) kérdéseken jön ki. Az M1
jellemző hibája a hiányos egylekérdezéses válasz: a kaszkád elfogadási szabálya a rajzi
kérdésekre készült, és egy nem üres, de hiányos adatlapi sort is elfogad. A gráf nélküli módszer
jellemző hibája a nagy rajzon a hamis lemondás. A 360 válaszból kettő volt hallucinált.

## Korlátok

- **Szintetikus üzemek.** Az eredmény két szintetikus üzemre érvényes (4 és 27 lap), amelyeket
  Benedek v1 generátora állított elő; a rajz nem valódi rajz, és a hét adatlap sok tagot ír le.
- **Modellkészítésű referenciák.** A (b)–(d) család referenciáit egy modell írta a PDF-ből, ember
  nem ellenőrizte őket; a bíráló is modell (vak, de nem ember), és a bírálók között egy
  következetlenséget is láttunk.
- **Kis minta.** Családonként 15 kérdés; a konfidenciaintervallumok szélesek.
- **Hiányzó szókészlet-ellenőrzés.** A POSC Caesar régi SPARQL-végpontja a mérés idején nem volt
  elérhető, ezért az új adatlapgráfokban csak az rds- és CFIHOS-illesztések szerepelnek.
- **A rajzot nem változtattuk.** A kaszkádot Benedek a valósághűbb v2 üzemekre hangolta; mi a v1
  generátort használtuk, mert csak az szűkíthető az adatlappal rendelkező elemosztályokra.

## Továbblépés

A legközvetlenebb javítás az M1 elfogadási szabályának adatlapi kérdésekre szabott változata
(például a feltétel és az oldalszám meglétének ellenőrzése), és egy olyan Cypher-szint, amely a
rajzi lépés után az adatlapi részt a plantdocs A2-re bízza. Hosszabb távon a mérést valódi rajzokon,
szélesebb adatlapkészlettel és emberileg ellenőrzött referenciákkal kell megismételni.
