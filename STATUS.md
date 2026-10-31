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
