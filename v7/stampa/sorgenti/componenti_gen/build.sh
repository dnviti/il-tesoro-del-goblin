#!/bin/bash
# Rigenera i PDF dei componenti non-carta e la pagina di prova: gen.py (SVG in mm) -> VectorCraft (.vectorcraft + PDF) -> PdfCraft (combine).
# uso: build.sh <cartella_sorgenti> <cartella_pdf> [A4|A3] [--dati CARTELLA]   (A4: build.sh v7/stampa/sorgenti v7/stampa/playtest_v7; A3: build.sh v7/stampa/sorgenti/A3 v7/stampa/playtest_v7_A3 A3)
# Le opzioni dopo il formato passano a gen.py (--dati: CSV da un'altra cartella, per provare dati nuovi).
# A4: produce anche carta_base_3d.pdf (3d_solidcraft/carta_base_3d.py --verifica, scarto <= 0,2 mm o la build fallisce).
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
  COMPONENTI="mappa_base mappa_fiori mappa_preset guida_montaggio_mappa segnalini_3d sala_tesoro plance_eroe rotelle_eroe tessere_esplorazione segnalini pedine prova_stampa"
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
if [ "$FORMATO" != A3 ]; then
  # cornice 3D (4 fogli, uno per quarto del vassoio): sempre generata con la rigenerazione del kit; fallisce se manca o se il
  # percorso di taglio si scosta di piu' di 0,2 mm dalla tasca del generatore 3D (set -e ferma la build)
  python3 "$HERE/../../3d_solidcraft/carta_base_3d.py" --out "$PDF/carta_base_3d.pdf" --verifica >/dev/null
  [ -s "$PDF/carta_base_3d.pdf" ] || { echo "carta_base_3d.pdf mancante" >&2; exit 1; }
fi
rm -rf "$TMP"
