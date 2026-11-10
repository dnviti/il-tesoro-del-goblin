#!/bin/bash
# Rigenera i PDF dei componenti non-carta e la pagina di prova (tutti solo fronte): gen.py (SVG in mm) -> VectorCraft (.vectorcraft + PDF) -> PdfCraft (combine).
# uso: build.sh <cartella_sorgenti> <cartella_pdf> [A4|A3]   (default A4; A3: es. build.sh v6_08-11/stampa/sorgenti/A3 v6_08-11/stampa/playtest_v6_A3 A3)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$1"; PDF="$2"; FORMATO="${3:-A4}"; TMP="$(mktemp -d)"
mkdir -p "$PDF"
if [ "$FORMATO" = A3 ]; then
  python3 "$HERE/gen.py" "$SRC" --formato A3 >/dev/null
  COMPONENTI="plancia plance_eroe rotelle_eroe tessere_esplorazione componenti_misti prova_stampa"
else
  python3 "$HERE/gen.py" "$SRC" >/dev/null
  COMPONENTI="plancia plance_eroe rotelle_eroe tessere_esplorazione segnalini pedine prova_stampa"
fi
for c in $COMPONENTI; do
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
