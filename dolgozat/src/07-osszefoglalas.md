# Összefoglalás

Két egyéni munkát kötöttünk össze: a P&ID-rajzokból épített üzemi gráfot és a gyártói
adatlapokból épített, eszközönkénti ISO 15926 gráfokat. Egyetlen Neo4j-adatbázisba töltöttük a két
réteget, és egy tagalapú kapcsolattal kötöttük össze őket. Három kérdés-válaszoló módszert
fejlesztettünk egy négylapos kis üzemen, majd változtatás nélkül megmértük őket két modellel egy
27 lapos és egy 98 lapos üzemen, üzemenként 60 kérdésen és 12 több adatlapos kérdésen.

## Válaszok a kutatási kérdésekre

**RQ1.** A rajzot és az adatlapot összekötő kérdések megválaszolhatók az összevont gráfon: az M1
a 27 lapos üzemen GLM-mel 42, Lunával 43, a 98 lapos üzemen 38, illetve 43 helyes választ adott a
60-ból (EXP-060, EXP-070). A két rész meglévő rendszerét külön hívó irányító (M2) azonban
pontosabb volt: GLM-mel mindkét méretnél ez lett a legjobb párosítás (51, illetve 49 helyes), és
mindkét méretnél szignifikánsan megelőzte az M1-et. A gráf nélküli M3-mal szemben az M2 előnye a
27 lapos üzemen GLM-mel, mindkét gráfos módszeré a 98 lapos üzemen Lunával szignifikáns.

**RQ2.** A gráfos módszerek kérdésenkénti költsége a 27 és a 98 lap között nem nőtt (az M2
GLM-mel 0,00344 és 0,00355 USD), a pontosságuk kevéssé változott, a gráf nélküli M3 költsége viszont a rajz
méretével nőtt (Lunával 0,00680-ról 0,02409 USD-re), a pontossága pedig modellenként ellentétes
irányba mozdult (GLM-mel 35-ről 42-re nőtt, Lunával 39-ről 30-ra esett; EXP-060, EXP-070). A kis
üzemen versenyképes gráf nélküli módszer tehát a nagy rajzon drágább és kiszámíthatatlanabb lett;
ez egybevág Benedek mérésével, amely szerint a teljes rajz promptba tétele a lapszámmal romlik és
drágul.

**RQ3.** A rajzi (a) és a megválaszolhatatlan (d) kérdéseken a gráfos módszerek erősek, a
különbség az adatlapi (b), az összetett (c) és a több adatlapos (e) kérdéseken jön ki. A több
adatlapos kérdések közel felét (5–6-ot a 12-ből) a 27 lapos üzemen a két gráfos módszer teljesen
megoldotta, a gráf
nélküli egyet sem; a 98 lapos üzemen ezek a kérdések minden párosításnak nehezebbek lettek, ott
csak az M2 GLM-mel oldott meg hatot (EXP-061, EXP-071). Az M1 jellemző hibája a hiányos
egylekérdezéses válasz, a gráf nélküli módszeré a téves „nincs benne” jelzés. A 60 kérdéses
sorok 720 válaszából három volt hallucinált.

## Korlátok

- **Szintetikus üzemek.** Az eredmény három szintetikus üzemre érvényes (4, 27 és 98 lap),
  amelyeket Benedek v1 generátora állított elő; a rajz nem valódi rajz, és a hét adatlap sok tagot
  ír le.
- **Modellkészítésű referenciák.** A (b)–(d) család referenciáit egy modell írta a PDF-ből, ember
  nem ellenőrizte őket; a bíráló is modell (vak, de nem ember), és a bírálók között egy
  következetlenséget is láttunk.
- **Kis minta.** Üzemenként és családonként 15 kérdés; a konfidenciaintervallumok szélesek.
- **Hiányzó szókészlet-ellenőrzés.** A POSC Caesar régi SPARQL-végpontja a mérés idején nem volt
  elérhető, ezért az új adatlapgráfokban csak az rds- és CFIHOS-illesztések szerepelnek.
- **A rajzot nem változtattuk.** A kaszkádot Benedek a valósághűbb v2 üzemekre hangolta; mi a v1
  generátort használtuk, mert csak az szűkíthető az adatlappal rendelkező elemosztályokra.

## Továbblépés

A legközvetlenebb javítás az M1 elfogadási szabályának adatlapi kérdésekre szabott változata
(például a feltétel és az oldalszám meglétének ellenőrzése), és egy olyan Cypher-szint, amely a
rajzi lépés után az adatlapi részt a plantdocs A2-re bízza. Hosszabb távon a mérést valódi rajzokon,
szélesebb adatlapkészlettel és emberileg ellenőrzött referenciákkal kell megismételni.
