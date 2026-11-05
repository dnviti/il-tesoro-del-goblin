#!/bin/bash
# Rigenera i 6 PDF dei componenti non-carta: gen.py (SVG in mm) -> VectorCraft (.vectorcraft + PDF) -> PdfCraft (combine).
# uso: build.sh <cartella_sorgenti> <cartella_pdf>
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$1"; PDF="$2"; TMP="$(mktemp -d)"
mkdir -p "$PDF"
python3 "$HERE/gen.py" "$SRC" >/dev/null
for c in plancia schede_eroe tessere_esplorazione tessere_specie segnalini pedine; do
  d="$SRC/$c/"
  pages=()
  for f in "$d"pagina_*.svg; do
    n=$(basename "$f" .svg)
    vectorcraft-cli convert "$f" "$d$n.vectorcraft" >/dev/null
    vectorcraft-cli convert "$d$n.vectorcraft" "$TMP/$c-$n.pdf" >/dev/null
    pages+=("$TMP/$c-$n.pdf")
  done
  if [ ${#pages[@]} -eq 1 ]; then cp "${pages[0]}" "$PDF/$c.pdf"; else pdfcraft-cli combine "${pages[@]}" --out "$PDF/$c.pdf" >/dev/null; fi
done
rm -rf "$TMP"
