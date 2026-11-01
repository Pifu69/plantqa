# Összefoglalás

Két egyéni munkát kötöttünk össze: a P&ID-rajzokból épített üzemi gráfot és a gyártói
adatlapokból épített, eszközönkénti ISO 15926 gráfokat. Egyetlen Neo4j-adatbázisba töltöttük a két
réteget, és egy tagalapú kapcsolattal kötöttük össze őket. Három kérdés-válaszoló módszert
építettünk fel egy négylapos prototípus-üzemen, a közös rendszert egy 30 és egy 50 lapos
fejlesztési üzemen hangoltuk, majd befagyasztva két modellel megmértük egy 100 és egy 1000 lapos,
a hangolás során nem használt tesztüzemen, üzemenként 60 kérdésen és 12, több adatlapot összevető
kérdésen.

## Válaszok a kutatási kérdésekre

**RQ1.** A rajzot és az adatlapot összekötő kérdések megválaszolhatók az összevont gráfon: az M1
GLM-mel 50 és 43, Lunával 46 és 41 helyes választ adott a 60-ból a 100 és az 1000
lapos tesztüzemen (EXP-096, EXP-098). A két rész meglévő rendszerét külön hívó irányító (M2)
GLM-mel mindkét tesztüzemen a legjobb párosítás volt (51 és 48 helyes), de az M1-től való különbsége nem szignifikáns. A gráf nélküli M3-mal szemben a
100 lapos üzemen GLM-mel az M2, Lunával az M1 előnye szignifikáns.

**RQ2.** A gráfos módszerek kérdésenkénti költsége a tízszer nagyobb rajzon legfeljebb a
kétszeresére nőtt (az M2 GLM-mel 0,00451 és 0,00866 USD a 100 és az 1000 lapos üzemen), a gráf nélküli M3 költsége viszont a 30
lapos fejlesztési üzem és a 100 lapos tesztüzem között a GLM modellel 0,00206-ról 0,00757 USD-re,
a Luna modellel 0,00731-ről 0,02501 USD-re nőtt, és az 1000 lapos rajz már nem fér a modellek
kontextusába, így ott az M3 nem futtatható. A gráfos módszerek pontossága a 100 és az 1000 lap között legfeljebb 7
kérdéssel csökkent (az M2 GLM-mel 51-ről 48-ra, az M1 GLM-mel 50-ről 43-ra, az M2 Lunával viszont 43-ról 46-ra nőtt;
EXP-096, EXP-098). A gráf tehát nemcsak olcsóbbá, hanem nagy
üzemen egyáltalán lehetővé teszi a kérdés-válaszolást; ez egybevág Benedek mérésével, amely
szerint a teljes rajz promptba tétele a lapszámmal romlik és drágul. A hangolás a fejlesztési
üzemeken látott üres válaszokat csökkentette, a tesztüzem pontosságát mérhetően nem változtatta.

**RQ3.** A rajzi (a) és a megválaszolhatatlan (d) kérdéseken minden módszer erős, a különbség az
adatlapi (b), az összetett (c) és a több adatlapos (e) kérdéseken jön ki. A több adatlapos
kérdések közül a gráf nélküli módszer a 100 lapos üzemen egyiket sem oldotta meg teljesen, a
gráfos módszerek GLM-mel 4–5-öt, az 1000 lapos üzemen 1–3-at (EXP-097, EXP-099). Az M1 jellemző hibája a hiányos egylekérdezéses
válasz, az M2-é a több adatlapos kérdéseken a lépéskorlát miatti üres válasz, a gráf nélküli
módszeré a téves „nincs benne” jelzés.

## Korlátok

- **Szintetikus üzemek.** Az eredmény öt szintetikus üzemre érvényes (4, 30, 50, 100 és 1000 lap),
  amelyeket Benedek generátora állított elő szabályok szerint (egységek, berendezések,
  csővezetékek, szabályozókörök, lapközi csatlakozók); a rajz nem valódi üzem rajza, és a hét
  adatlap sok tag-et ír le.
- **Modellkészítésű referenciák.** A (b)–(d) család referenciáit egy modell írta a PDF-ből, ember
  nem ellenőrizte őket; a bíráló is modell (vak, de nem ember), és ugyanazt a választ két
  bírálat egyszer eltérően ítélte meg (EXP-086, EXP-096).
- **Kis minta.** Üzemenként és családonként 15 kérdés, egyetlen futás; a konfidenciaintervallumok
  szélesek, és a pontosság üzemenként néhány kérdéssel ingadozik.
- **Hiányzó szókészlet-ellenőrzés.** A POSC Caesar régi SPARQL-végpontja a mérés idején nem volt
  elérhető, ezért az új adatlapgráfokban csak az rds- és CFIHOS-illesztések szerepelnek.
- **A rajzgenerátor egyszerűbb változata.** A kaszkádot Benedek a generátor valósághűbb, későbbi
  változatának üzemeire hangolta; mi az első változatot használtuk, mert csak az szűkíthető az
  adatlappal rendelkező elemosztályokra.

## Továbblépés

A legközvetlenebb javítás az M1 elfogadási szabályának adatlapi kérdésekre szabott változata
(például a feltétel és az oldalszám meglétének ellenőrzése), és egy olyan Cypher-szint, amely a
rajzi lépés után az adatlapi részt az adatlapoldali rendszerre bízza. Hosszabb távon a mérést
valódi rajzokon, szélesebb adatlapkészlettel és emberileg ellenőrzött referenciákkal kell
megismételni.
