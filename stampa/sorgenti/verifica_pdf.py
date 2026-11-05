#!/usr/bin/env python3
"""Controlli di stampa sui PDF di playtest_v5 (richiede poppler: pdfinfo, pdftoppm, pdffonts).

Per ogni PDF: dimensione pagine (A4, o A3 con --formato A3), numero pagine, font non incorporati e distanza minima
tra qualunque inchiostro e il bordo del foglio (rasterizzazione a 150 dpi; la fascia dei 6 mm
deve essere bianca: le stampanti domestiche non stampano il bordo esterno).

Uso: python3 stampa/sorgenti/verifica_pdf.py [cartella_pdf] [--margine MM] [--formato A4|A3]
Esce con codice 1 se un PDF non è nel formato atteso, ha font non incorporati o ha inchiostro nella fascia.
"""
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

DPI = 150
MM_PX = DPI / 25.4


def main():
    argv = sys.argv[1:]
    margine = 6.0
    if "--margine" in argv:
        i = argv.index("--margine")
        margine = float(argv[i + 1])
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
                d = min(xs.min(), w - 1 - xs.max(), ys.min(), h - 1 - ys.max()) / MM_PX
                minimi.append(d)
        peggiore = min(minimi)
        stato = "OK" if (formato_ok and not non_inc and peggiore >= margine) else "ERRORE"
        ok &= stato == "OK"
        print(f"{stato:7} {pdf.name:28} {pagine:2} pag  {dim.split(':', 1)[1].strip():45} "
              f"min. inchiostro-bordo {peggiore:5.2f} mm  font non incorporati: {len(non_inc)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
