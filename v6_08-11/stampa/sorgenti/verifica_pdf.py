#!/usr/bin/env python3
"""Controlli di stampa sui PDF di playtest_v6 (richiede poppler: pdfinfo, pdftoppm, pdffonts, pdftotext).

Per ogni PDF: dimensione pagine (A4, o A3 con --formato A3; verticale o orizzontale), numero pagine, font non incorporati
e distanza minima dal bordo del foglio (rasterizzazione a 150 dpi).
- PDF normali: tutto l'inchiostro a >= 6 mm dal bordo (le stampanti domestiche non stampano il bordo esterno).
- carte_*.pdf (ogni carta ha la sua abbondanza, 2,5 mm su A4, 3 mm su A3): le linee di RIFILO stanno a >= 5 mm dal bordo
  (--margine-rifilo). Il blocco colorato delle abbondanze arriva piu' vicino al bordo (3 mm su A4): puo' cadere nella zona
  non stampabile, e' solo colore in piu'. Il bordo del blocco si trova con le righe/colonne quasi interamente colorate
  (le tacche e le etichette nel margine sono sottili e non contano) e si aggiunge l'abbondanza.

Stampa solo fronte (v6-bis): nessun PDF puo' essere un fronte-retro interlacciato. ERRORE se una pagina porta la scritta
«RETRO» (etichetta delle pagine retro dei vecchi PDF fronte-retro). Per ogni carte_<nome>_retri.pdf:
- deve esistere carte_<nome>.pdf con lo stesso numero di pagine, e ogni pagina dei retri dice «RETRI»;
- niente specchio: il dorso nella cella p del foglio k porta nell'abbondanza l'ID della carta che sta nella cella p del
  foglio k dei fronti (si confrontano le posizioni degli ID letti con pdftotext -bbox).

Uso: python3 v6_08-11/stampa/sorgenti/verifica_pdf.py [cartella_pdf] [--margine MM] [--margine-rifilo MM] [--formato A4|A3]
Esce con codice 1 se un PDF non è nel formato atteso, ha font non incorporati, ha inchiostro nella fascia
(per le carte: rifilo troppo vicino al bordo), è interlacciato o ha i dorsi non allineati ai fronti.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

DPI = 150
MM_PX = DPI / 25.4
PT = 72 / 25.4
ABBONDANZA = {"A4": 2.5, "A3": 3.0}   # mm per lato, come in carte/genera_carte.py
GRIGLIA = {"A4": (3, 3), "A3": (4, 4)}  # colonne, righe di carte per foglio, come in carte/genera_carte.py
ID_CARTA = re.compile(r"^(TM|TI|TE|TC|TS|NE|IM|AI|DV)-\d\d$")


def testi_pagine(pdf, pagine):
    return [subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"], capture_output=True, text=True).stdout
            for p in range(1, pagine + 1)]


def id_per_cella(pdf, formato):
    """{(pagina, cella): ID} dalle parole che sono ID di carta, con la cella della griglia in cui cade il loro centro."""
    nc, nr = GRIGLIA[formato]
    out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True).stdout
    celle, pagina, pw, ph = {}, 0, 0.0, 0.0
    for riga in out.splitlines():
        m = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', riga)
        if m:
            pagina, pw, ph = pagina + 1, float(m[1]), float(m[2])
            cw, ch = (63 + 2 * ABBONDANZA[formato]) * PT, (88 + 2 * ABBONDANZA[formato]) * PT
            x0, y0 = (pw - nc * cw) / 2, (ph - nr * ch) / 2
            continue
        m = re.search(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>', riga)
        if m and ID_CARTA.match(m[5]):
            cx, cy = (float(m[1]) + float(m[3])) / 2, (float(m[2]) + float(m[4])) / 2
            c, r = int((cx - x0) // cw), int((cy - y0) // ch)
            if 0 <= c < nc and 0 <= r < nr:
                celle.setdefault((pagina, r * nc + c), m[5])
    return celle


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


def verifica_retri(pdf, pagine, testi, formato):
    """Errori di un carte_<nome>_retri.pdf rispetto ai fronti carte_<nome>.pdf (stesse pagine, stesse celle, niente specchio)."""
    fronti = pdf.with_name(pdf.name.replace("_retri.pdf", ".pdf"))
    if not fronti.exists():
        return [f"manca {fronti.name}"]
    info = subprocess.run(["pdfinfo", str(fronti)], capture_output=True, text=True).stdout
    pf = int(next(r.split()[-1] for r in info.splitlines() if r.startswith("Pages:")))
    errori = [] if pf == pagine else [f"{pagine} pagine contro {pf} dei fronti"]
    errori += [f"pag. {k} senza «RETRI»" for k, t in enumerate(testi, 1) if "RETRI" not in t]
    idf, idr = id_per_cella(fronti, formato), id_per_cella(pdf, formato)
    if not idr:
        errori.append("nessun ID nell'abbondanza dei dorsi")
    errori += [f"pag. {p} cella {c + 1}: dorso {i}, fronte {idf.get((p, c), 'vuoto')}"
               for (p, c), i in sorted(idr.items()) if idf.get((p, c)) != i]
    return errori


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
    predefinita = "playtest_v6" if formato == "A4" else "playtest_v6_A3"
    cartella = pathlib.Path(args[0]) if args else pathlib.Path(__file__).resolve().parent.parent / predefinita
    ok = True
    for pdf in sorted(cartella.glob("*.pdf")):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        pagine = int(next(r.split()[-1] for r in info.splitlines() if r.startswith("Pages:")))
        dim = next(r for r in info.splitlines() if r.startswith("Page size:"))
        formato_ok = f"({formato})" in dim
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
        non_inc = [r.split()[0] for r in fonts if r.strip() and r.split()[-5] == "no"]
        testi = testi_pagine(pdf, pagine)
        errori = [f"pag. {k} è un RETRO (fronte-retro interlacciato)" for k, t in enumerate(testi, 1) if re.search(r"\bRETRO\b", t)]
        if pdf.name.endswith("_retri.pdf"):
            errori += verifica_retri(pdf, pagine, testi, formato)
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
        stato = "OK" if (formato_ok and not non_inc and peggiore >= soglia and not errori) else "ERRORE"
        ok &= stato == "OK"
        print(f"{stato:7} {pdf.name:30} {pagine:2} pag  {dim.split(':', 1)[1].strip():45} "
              f"{cosa} {peggiore:5.2f} mm  font non incorporati: {len(non_inc)}"
              + ("" if not errori else "  ← " + "; ".join(errori[:4]) + (" …" if len(errori) > 4 else "")))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
