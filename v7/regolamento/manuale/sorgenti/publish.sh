#!/bin/bash
# Ricostruisce il .designcraft, fa il preflight, esporta i PDF e i render delle pagine.
set -euo pipefail
SRC=$(cd "$(dirname "$0")" && pwd); M=$(dirname "$SRC")
DOC="$M/Manuale_Il_Tesoro_del_Goblin.designcraft"
TITLE="Il Tesoro del Goblin – Regolamento"
export WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
python3 "$SRC/genera.py" final > "$WORK/script.txt"
designcraft-cli script "$WORK/script.txt" --save "$DOC" > "$WORK/out.json" || { tail -3 "$WORK/out.json"; exit 1; }
designcraft-cli run --in "$DOC" --cmd 'preflight.run={"minPpi":250}' \
  | jq -c '{errors, warnings, altro: [.issues[] | select(.kind != "rgbColor") | .message]}'
designcraft-cli run --in "$DOC" \
  --cmd "file.exportPdf={\"path\":\"$M/Manuale_Il_Tesoro_del_Goblin_PDFX1a.pdf\",\"standard\":\"x1a\",\"flatten\":\"high\",\"bleed\":true,\"marks\":true,\"title\":\"$TITLE\"}" \
  --cmd "file.exportPdf={\"path\":\"$M/Manuale_Il_Tesoro_del_Goblin_stampa_A4.pdf\",\"standard\":\"none\",\"bleed\":false,\"marks\":false,\"title\":\"$TITLE\"}" \
  | jq -c '{path, pages, bytes}'
# PDF/X-1a (tutto CMYK): il PDF/X-4 non passa la validazione perché la grafica vettoriale
# importata (kit e schemi) è in RGB senza profilo ICC.
designcraft-cli validate-pdf "$M/Manuale_Il_Tesoro_del_Goblin_PDFX1a.pdf" --standard x1a
mkdir -p "$M/anteprime"
designcraft-cli run --in "$DOC" --scale 1.5 --all-pages "$WORK/r" > /dev/null
for i in 1 2 3 4 5; do cp "$WORK/r/page-00$i.png" "$M/anteprime/pagina-$i.png"; done
