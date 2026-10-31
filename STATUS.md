# STATUS

## 2026-10-31 09:20 — 0. és 1. fázis kész, 2. fázis részben

- **Kész:** felmérés (`docs/felmeres.md`); projektváz (uv path-függőségek, tesztek, ruff, mypy
  zöld); közös költségnapló és keret (`plantqa.costlog`); példa P&ID (seed 6, 26 tagelt elem,
  4 lap) és tag → adatlap hozzárendelés (`data/plant/`); rajzexport PDF; összevont gráf
  betöltője (`python -m plantqa.graph.load`), egyelőre a 3 kész Opus-eszközgráffal.
- **Folyamatban:** 4 adatlap Opus-feldolgozása al-sessionökben (Rosemount 3051, Worcester
  F51/F52, Swagelok MS-01-176, Alfa Laval M3).
- **Következő:** kérdéssor (3. fázis), M1/M2/M3 (4. fázis); a betöltés újrafuttatása, amint az
  Opus-gráfok elkészülnek.
- **Költés eddig:** 0,30 USD (Azure, listaár) / 20 USD.

## 2026-10-31 10:05 — 2. és 3. fázis kész, 4. fázis: módszerek kész, első dev-mérés fut

- **Kész:** összevont gráf 6 eszközgráffal (a Rosemount Opus-feldolgozása még fut) + vektorok;
  kérdéssor (60 kérdés, teszt befagyasztva, hash az `eredmenyek.md`-ben); közös LLM-réteg
  (pinek, mérő, cache, költségnapló); M1 (kiegészített cascade), M2 (router), M3 (baseline);
  futtató, pontozó, összesítő, ábramodul; demó-váz (`python -m plantqa.app`).
- **Fut:** EXP-010 (dev, GLM, mindhárom módszer); minta-elemzés (subagent).
- **Következő:** bírálat → EXP-010 sor; Rosemount-gráf betöltése; további dev iterációk.
- **Költés eddig:** ~0,33 USD / 20 USD.

## 2026-10-31 10:48 — 4. fázis kész (dev iterációk), 5. fázis: végső teszt fut

- **Kész:** mind a 7 adatlap Opus-gráfja; összevont gráf (EXP-005); dev iterációk: EXP-010
  (kiindulás), EXP-011 (M1 A2-szabályok, M2/M3 válaszszabály), EXP-012 (+ Rosemount) GLM-mel,
  EXP-013 Lunával (bírálat fut); módszerek befagyasztva; dolgozat 1–5. fejezet és függelék
  vázlata; minta-elemzés; irodalomjegyzék-alap; demó működik.
- **Fut:** EXP-020 (befagyasztott teszt, 6 párosítás); EXP-013 bírálata.
- **Következő:** bírálat → végső táblázat és ábrák; demó-képernyőképek; 6–7. fejezet, kivonat;
  előadás.
- **Költés eddig:** spent 0.7411 USD / 20 USD.
