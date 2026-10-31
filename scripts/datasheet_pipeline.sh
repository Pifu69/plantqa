#!/usr/bin/env bash
# Egy adatlap teljes plantdocs-folyamata (01–10), a plantdocs EXP-0038 futtatas.sh lépéseivel.
# Különbség: az LLM-lépéseket NEM az API (GLM) végzi, hanem egy Claude Code al-session (Opus)
# írja meg a kimenetfájlt (docs/dontesek.md, 2026-10-31). Ha egy LLM-kimenet hiányzik, a szkript
# kiírja, melyik kell, és 3-as kóddal kilép; a kimenet elkészülte után újraindítható.
# A plantdocs repó csak olvasható: a munkakönyvtár ott van (relatív útvonalai miatt), de minden
# kimenet a plantqa/data/datasheets/<id>/ alá kerül.
# Használat: bash scripts/datasheet_pipeline.sh <document_id> <prefix> "<cím>"
set -euo pipefail
export PYTHONIOENCODING=utf-8
Q=C:/Users/Zsombi/plantqa
P=C:/Users/Zsombi/plantdocs
D=$1; PREFIX=$2; TITLE=$3
E=$Q/data/datasheets/$D
PDF=$Q/data/raw/$D/$D.pdf
cd "$P"
py() { uv run --project "$Q" python -m "$@"; }
need() { [ -f "$E/$1" ] || { echo "LLM-LEPES-KELL: $2 -> $E/$1"; exit 3; }; py plantdocs.contracts "$3" "$E/$1" ${4:-}; }

mkdir -p $E/01-azure $E/02-rekordok $E/03-abrak $E/04-diagramok $E/05-ellenorzes $E/06-celformatum $E/07-labjegyzetek $E/08-forrasleirasok $E/09-szokeszlet $E/10-rdf
if [ ! -f $E/01-azure/raw-all.json ]; then
  uv run --project "$Q" --env-file "$P/.env" python -m plantdocs.extract.azure_di analyze "$PDF" --out-dir $E/01-azure --note "plantqa"
  py plantqa.costlog azure --pdf "$PDF" --tag "azure-di:$D"
fi
[ -f $E/01-azure/azure-pages.md ] || py plantdocs.extract.azure_di pages-md $E/01-azure/raw-all.json --out $E/01-azure/azure-pages.md
echo '{"figures": []}' > $E/06-celformatum/no-envelope-charts.json
[ -f $E/03-abrak/figures.json ] || py plantdocs.extract.figures $E/01-azure/raw-all.json --pdf "$PDF" --document-id $D --out $E/03-abrak/figures.json --crops-dir $E/03-abrak/kivagasok
need 02-rekordok/output.json records records
need 03-abrak/claude-labels.json figure-labels figure-labels
py plantdocs.extract.chart_pages "$PDF" --figures $E/03-abrak/figures.json --labels $E/03-abrak/claude-labels.json --render-dir $E/04-diagramok/renders --out $E/04-diagramok/chart-pages.json
py plantdocs.extract.figure_checks $E/03-abrak/figures.json --raw $E/01-azure/raw-all.json --labels $E/03-abrak/claude-labels.json --out $E/03-abrak/figure-checks.json
need 04-diagramok/image-readoff.json chart-readoff chart-readoff
py plantdocs.extract.chart_ocr "$PDF" --azure $E/01-azure/raw-all.json --readoff $E/04-diagramok/image-readoff.json --document-id $D --out $E/04-diagramok/chart-analysis.json
py plantdocs.extract.record_checks $E/02-rekordok/output.json --pdf "$PDF" --raw $E/01-azure/raw-all.json --out $E/05-ellenorzes/record-checks.json
need 06-celformatum/table-schemas.json table-schema table-schema
py plantdocs.target.build --exp0010 $E/02-rekordok/output.json --schemas $E/06-celformatum/table-schemas.json --figures $E/03-abrak/figures.json --labels $E/03-abrak/claude-labels.json --figure-checks $E/03-abrak/figure-checks.json --azure $E/01-azure/raw-all.json --charts $E/06-celformatum/no-envelope-charts.json --pdf "$PDF" --document $D --prefix $PREFIX --out $E/06-celformatum/target-records-a-build.json > $E/06-celformatum/build-summary.txt
py plantdocs.target.curve_charts --readoff $E/04-diagramok/image-readoff.json --analysis $E/04-diagramok/chart-analysis.json --figures $E/03-abrak/figures.json --target $E/06-celformatum/target-records-a-build.json --out $E/06-celformatum/target-records-b-charts.json
py plantdocs.target.figure_notes --target $E/06-celformatum/target-records-b-charts.json --azure $E/01-azure/raw-all.json --prefix $PREFIX --out $E/07-labjegyzetek/target-records-c-figure-notes.json --notes $E/07-labjegyzetek/figure-notes.json
py plantdocs.target.source_inventory --azure $E/01-azure/raw-all.json --figures $E/03-abrak/figures.json --labels $E/03-abrak/claude-labels.json --target $E/07-labjegyzetek/target-records-c-figure-notes.json --document $D --records $E/02-rekordok/output.json --schemas $E/06-celformatum/table-schemas.json --out $E/08-forrasleirasok/inventory.json
need 08-forrasleirasok/descriptions.json descriptions descriptions
py plantdocs.target.description_checks $E/08-forrasleirasok/inventory.json $E/08-forrasleirasok/descriptions.json --out $E/08-forrasleirasok/description-checks.json
py plantdocs.target.footnote_links --target $E/07-labjegyzetek/target-records-c-figure-notes.json --pdf "$PDF" --azure $E/01-azure/raw-all.json --inventory $E/08-forrasleirasok/inventory.json --descriptions $E/08-forrasleirasok/descriptions.json --schemas $E/06-celformatum/table-schemas.json --out $E/08-forrasleirasok/target-records.json --sources $E/08-forrasleirasok/source-descriptions.json --report $E/08-forrasleirasok/footnote-links.json
py plantdocs.rdf.vocab_items --target $E/08-forrasleirasok/target-records.json --out $E/09-szokeszlet/vocab-items.json
need 09-szokeszlet/vocabulary.json vocabulary vocabulary "--items $E/09-szokeszlet/vocab-items.json"
[ -f $E/09-szokeszlet/vocab-check.json ] || py plantdocs.rdf.vocab_check --vocabulary $E/09-szokeszlet/vocabulary.json --items $E/09-szokeszlet/vocab-items.json --cfihos data/vocab/cfihos-core-v2.0 --out $E/09-szokeszlet/vocab-check.json
py plantdocs.rdf.vocab_map --check $E/09-szokeszlet/vocab-check.json --document $D --schemas $E/06-celformatum/table-schemas.json --classes data/vocab/pca-classes.json --out $E/09-szokeszlet/vocab-map.json
py plantdocs.rdf.convert --target $E/08-forrasleirasok/target-records.json --inventory $E/08-forrasleirasok/inventory.json --descriptions $E/08-forrasleirasok/source-descriptions.json --schemas $E/06-celformatum/table-schemas.json --vocab-map $E/09-szokeszlet/vocab-map.json --vocab data/vocab --pdf-name $D.pdf --out $E/10-rdf/graph.ttl --report $E/10-rdf/report.json --azure $E/01-azure/raw-all.json
echo "KESZ: $E/10-rdf/graph.ttl"
