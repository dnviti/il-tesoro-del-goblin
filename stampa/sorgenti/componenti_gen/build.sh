#!/bin/bash
# Rigenera i PDF dei componenti non-carta e la pagina di prova: gen.py (SVG in mm) -> VectorCraft (.vectorcraft + PDF) -> PdfCraft (combine).
# uso: build.sh <cartella_sorgenti> <cartella_pdf>
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$1"; PDF="$2"; TMP="$(mktemp -d)"
mkdir -p "$PDF"
python3 "$HERE/gen.py" "$SRC" >/dev/null
for c in plancia schede_eroe tessere_esplorazione tessere_specie segnalini pedine prova_stampa; do
  d="$SRC/$c/"
  out="$c"; [ "$c" = prova_stampa ] && out="00_prova_stampa"
  pages=()
  for f in "$d"pagina_*.svg; do
    n=$(basename "$f" .svg)
    vectorcraft-cli convert "$f" "$d$n.vectorcraft" >/dev/null
    vectorcraft-cli convert "$d$n.vectorcraft" "$TMP/$c-$n.pdf" >/dev/null
    pages+=("$TMP/$c-$n.pdf")
  done
  if [ ${#pages[@]} -eq 1 ]; then cp "${pages[0]}" "$PDF/$out.pdf"; else pdfcraft-cli combine "${pages[@]}" --out "$PDF/$out.pdf" >/dev/null; fi
done
rm -rf "$TMP"
