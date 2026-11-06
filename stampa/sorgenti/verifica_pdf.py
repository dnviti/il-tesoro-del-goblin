#!/usr/bin/env python3
"""Controlli di stampa sui PDF di playtest_v5 (richiede poppler: pdfinfo, pdftoppm, pdffonts).

Per ogni PDF: dimensione pagine (A4, o A3 con --formato A3), numero pagine, font non incorporati e distanza minima
dal bordo del foglio (rasterizzazione a 150 dpi).
- PDF normali: tutto l'inchiostro a >= 6 mm dal bordo (le stampanti domestiche non stampano il bordo esterno).
- carte_*.pdf (ogni carta ha la sua abbondanza, 2,5 mm su A4, 3 mm su A3): le linee di RIFILO stanno a >= 5 mm dal bordo
  (--margine-rifilo). Il blocco colorato delle abbondanze arriva piu' vicino al bordo (3 mm su A4): puo' cadere nella zona
  non stampabile, e' solo colore in piu'. Il bordo del blocco si trova con le righe/colonne quasi interamente colorate
  (le tacche e le etichette nel margine sono sottili e non contano) e si aggiunge l'abbondanza.

Uso: python3 stampa/sorgenti/verifica_pdf.py [cartella_pdf] [--margine MM] [--margine-rifilo MM] [--formato A4|A3]
Esce con codice 1 se un PDF non è nel formato atteso, ha font non incorporati o ha inchiostro nella fascia
(per le carte: rifilo troppo vicino al bordo).
"""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

DPI = 150
MM_PX = DPI / 25.4
ABBONDANZA = {"A4": 2.5, "A3": 3.0}   # mm per lato, come in carte/genera_carte.py


def distanza_rifilo(inchiostro, abbondanza):
    """Distanza minima (mm) tra una linea di rifilo delle carte e il bordo del foglio: bordo del blocco di abbondanze
    (righe con >= 60 mm di inchiostro, colonne con >= 80 mm) piu' l'abbondanza."""
    h, w = inchiostro.shape
    righe = np.nonzero(inchiostro.sum(axis=1) >= 60 * MM_PX)[0]
    colonne = np.nonzero(inchiostro.sum(axis=0) >= 80 * MM_PX)[0]
    if len(righe) == 0 or len(colonne) == 0:
        return 99.0
    blocco = min(colonne.min(), w - 1 - colonne.max(), righe.min(), h - 1 - righe.max()) / MM_PX
    return blocco + abbondanza


def main():
    argv = sys.argv[1:]
    margine = 6.0
    if "--margine" in argv:
        i = argv.index("--margine")
        margine = float(argv[i + 1])
        del argv[i:i + 2]
    margine_rifilo = 5.0
    if "--margine-rifilo" in argv:
        i = argv.index("--margine-rifilo")
        margine_rifilo = float(argv[i + 1])
        del argv[i:i + 2]

    formato = "A4"
    if "--formato" in argv:
        i = argv.index("--formato")
        formato = argv[i + 1].upper()
        del argv[i:i + 2]
    args = argv
    predefinita = "playtest_v5" if formato == "A4" else "playtest_v5_A3"
    cartella = pathlib.Path(args[0]) if args else pathlib.Path(__file__).resolve().parent.parent / predefinita
    ok = True
    for pdf in sorted(cartella.glob("*.pdf")):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        pagine = int(next(r.split()[-1] for r in info.splitlines() if r.startswith("Pages:")))
        dim = next(r for r in info.splitlines() if r.startswith("Page size:"))
        formato_ok = f"({formato})" in dim
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
        non_inc = [r.split()[0] for r in fonts if r.strip() and r.split()[-5] == "no"]
        with tempfile.TemporaryDirectory(prefix="goblin_verifica_") as tmp:
            subprocess.run(["pdftoppm", "-r", str(DPI), "-png", str(pdf), f"{tmp}/p"], check=True)
            minimi = []
            for png in sorted(pathlib.Path(tmp).glob("p-*.png")):
                im = np.asarray(Image.open(png).convert("RGB")).astype(int)
                inchiostro = (im < 245).any(axis=2)
                h, w = inchiostro.shape
                ys, xs = np.nonzero(inchiostro)
                if len(xs) == 0:
                    minimi.append(99.0)
                    continue
                if pdf.name.startswith("carte_"):
                    minimi.append(distanza_rifilo(inchiostro, ABBONDANZA[formato]))
                    continue
                d = min(xs.min(), w - 1 - xs.max(), ys.min(), h - 1 - ys.max()) / MM_PX
                minimi.append(d)
        peggiore = min(minimi)
        soglia = margine_rifilo if pdf.name.startswith("carte_") else margine
        cosa = "min. rifilo-bordo" if pdf.name.startswith("carte_") else "min. inchiostro-bordo"
        stato = "OK" if (formato_ok and not non_inc and peggiore >= soglia) else "ERRORE"
        ok &= stato == "OK"
        print(f"{stato:7} {pdf.name:28} {pagine:2} pag  {dim.split(':', 1)[1].strip():45} "
              f"{cosa} {peggiore:5.2f} mm  font non incorporati: {len(non_inc)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
