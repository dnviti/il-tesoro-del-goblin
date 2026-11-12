#!/bin/bash
# Rigenera i PDF dei componenti non-carta e la pagina di prova: gen.py (SVG in mm) -> VectorCraft (.vectorcraft + PDF) -> PdfCraft (combine).
# uso: build.sh <cartella_sorgenti> <cartella_pdf> [A4|A3] [--dati CARTELLA]   (A4: build.sh v7/stampa/sorgenti v7/stampa/playtest_v7; A3: build.sh v7/stampa/sorgenti/A3 v7/stampa/playtest_v7_A3 A3)
# Le opzioni dopo il formato passano a gen.py (--dati: CSV da un'altra cartella, per provare dati nuovi).
# Solo fronte, tranne mappa_fiori (fronte/retro manuale: pagine dispari fronti, pari retri specchiati sul lato lungo).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$1"; PDF="$2"; FORMATO="${3:-A4}"; TMP="$(mktemp -d)"; shift $(( $# < 3 ? $# : 3 ))
mkdir -p "$PDF"
if [ "$FORMATO" = A3 ]; then
  python3 "$HERE/gen.py" "$SRC" --formato A3 "$@" >/dev/null
  COMPONENTI="sala_tesoro plance_eroe rotelle_eroe tessere_esplorazione componenti_misti prova_stampa"
else
  python3 "$HERE/gen.py" "$SRC" "$@" >/dev/null
  COMPONENTI="mappa_base carta_base_3d mappa_fiori mappa_preset guida_montaggio_mappa segnalini_3d sala_tesoro plance_eroe rotelle_eroe tessere_esplorazione segnalini pedine prova_stampa"
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
