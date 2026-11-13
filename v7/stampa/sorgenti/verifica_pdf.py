#!/usr/bin/env python3
"""Controlli di stampa sui PDF di playtest_v7 e playtest_v7_A3 (richiede poppler: pdfinfo, pdftoppm, pdffonts, pdftotext).

Per ogni PDF: dimensione pagine (A4, o A3 con --formato A3; verticale o orizzontale), numero pagine, font non incorporati
e distanza minima dal bordo del foglio (rasterizzazione a 150 dpi).
- PDF normali: tutto l'inchiostro a >= 6 mm dal bordo (le stampanti domestiche non stampano il bordo esterno).
- carte_*.pdf (ogni carta ha la sua abbondanza, 2,5 mm su A4, 3 mm su A3): le linee di RIFILO stanno a >= 5 mm dal bordo
  (--margine-rifilo). Il blocco colorato delle abbondanze arriva piu' vicino al bordo (3 mm su A4): puo' cadere nella zona
  non stampabile, e' solo colore in piu'. Il bordo del blocco si trova con le righe/colonne quasi interamente colorate
  (le tacche e le etichette nel margine sono sottili e non contano) e si aggiunge l'abbondanza.

Stampa solo fronte (v6-bis): nessun PDF puo' essere un fronte-retro interlacciato. ERRORE se una pagina porta la scritta
«RETRO» (etichetta delle pagine retro dei vecchi PDF fronte-retro). Unica eccezione voluta, mappa_fiori.pdf (D24: fiori a
due facce, fronte/retro manuale sul lato lungo): pagine dispari «fronte», pari «retro»; ogni fiore n ha l'id «nA» sul
fronte e «nB» sul retro, e il retro sta esattamente dietro il fronte girando il foglio sul lato lungo (la x del retro è
specchiata: x del bordo destro dell'id sul fronte + quella sul retro uguale per tutti i fiori, stessa y, entro 0,6 mm). Per ogni carte_<nome>_retri.pdf:
- deve esistere carte_<nome>.pdf; ogni pagina dei retri dice «RETRI … coi fronti del foglio k» (k crescente, al massimo le
  pagine dei fronti: un foglio di fronti senza dorsi non ha la sua pagina dei retri) e porta almeno un dorso;
- niente specchio: il dorso nella cella p della pagina dei retri del foglio k porta nell'abbondanza l'ID della carta che
  sta nella cella p del foglio k dei fronti (si confrontano le posizioni degli ID letti con pdftotext -bbox).

Per mappa_base.pdf e mappa_fiori.pdf (A4) anche il contorno dell'arte generata: a 300 dpi, per ogni lato di ogni esagono, né vuoti
(pergamena/carta) appena dentro la linea né arte appena fuori (vedi mappa_compone.py --verifica-pdf).

Scala reale: su mappa_base.pdf e carta_base_3d.pdf si misura a 600 dpi il segmento di controllo di 100 mm (errore oltre lo 0,05 %).

Uso: python3 v7/stampa/sorgenti/verifica_pdf.py [cartella_pdf] [--margine MM] [--margine-rifilo MM] [--formato A4|A3]
Senza cartella: v7/stampa/playtest_v7 (A4) o v7/stampa/playtest_v7_A3 (--formato A3).
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
ID_CARTA = re.compile(r"^(TM|TI|TE|CA|CR|CS|CO|CG|TC|TS|NE|IM|AI|DV)-\d{2,3}$")   # CA…CG: carte di classe v7 (Spec v7 §14.1)


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


ID_FIORE = re.compile(r"^(\d{1,2})([AB])$")


def verifica_contorno_arte(pdf):
    """Contorno dell'arte generata contro la linea vettoriale (a 300 dpi): vuoti dentro, arte fuori. Lo fa
    arte/mappa_compone.py --verifica-pdf (stessa geometria di gen.py); qui si riportano i suoi ERRORE."""
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve().parent / "arte" / "mappa_compone.py"), "--verifica-pdf", str(pdf)],
                       capture_output=True, text=True)
    errori = [l[len("ERRORE "):] for l in r.stdout.splitlines() if l.startswith("ERRORE ") and "problemi di contorno" not in l]
    if r.returncode not in (0, 1):
        errori.append("verifica del contorno dell'arte non riuscita: " + r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "verifica del contorno dell'arte non riuscita")
    return errori


TACCA = 0.25             # mm: larghezza delle tacche alle estremità del segmento (gen.py, carta_base_3d.py)
SCALA_TOL = 0.0005        # 0,05 %
SCALA_MIN, SCALA_MAX = 2300, 2430   # px a 600 dpi (97-103 mm): lunghezza dei tratti candidati al segmento di 100 mm


def lunghezza_segmento(png):
    """lunghezza in mm del segmento di controllo da 100 mm nel PNG a 600 dpi: tratto nero orizzontale o verticale lungo 97-103 mm
    (con le tacche d'estremità, larghe TACCA mm, che lo allungano di TACCA), bordi a mezza intensità interpolati (~0,01 mm).
    None se non c'è."""
    im = np.asarray(Image.open(png).convert("L")).astype(float)
    for a in (im, im.T):                          # orizzontale, poi verticale
        buio = a < 110
        for y in np.nonzero(buio.sum(axis=1) >= SCALA_MIN)[0]:
            riga = buio[y].astype(np.int8)
            d = np.diff(np.concatenate(([0], riga, [0])))
            for s, e in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
                if SCALA_MIN <= e - s <= SCALA_MAX:
                    r = a[y]
                    fl = (255 - r[s - 1]) / 255.0 if s > 0 else 0.0
                    fr = (255 - r[e]) / 255.0 if e < len(r) else 0.0
                    return (e - s + fl + fr) / 600 * 25.4 - TACCA
    return None


def verifica_scala(pdf, pagine):
    """Scala reale (100 mm di controllo misurati a 600 dpi) di mappa_base.pdf e carta_base_3d.pdf: errore oltre lo 0,05 %."""
    errori = []
    with tempfile.TemporaryDirectory(prefix="goblin_scala_") as tmp:
        for n in range(1, pagine + 1):
            subprocess.run(["pdftoppm", "-r", "600", "-gray", "-f", str(n), "-l", str(n), "-png", str(pdf), f"{tmp}/s{n}"], check=True)
            f = next(pathlib.Path(tmp).glob(f"s{n}-*.png"))
            mm = lunghezza_segmento(f)
            f.unlink()
            if mm is None:
                errori.append(f"pag. {n}: segmento di controllo di 100 mm non trovato")
            elif abs(mm / 100 - 1) > SCALA_TOL:
                errori.append(f"pag. {n}: scala {mm:.3f} mm per 100 mm ({(mm / 100 - 1) * 100:+.3f} %, limite 0,05 %)")
    return errori


def verifica_fiori(pdf, pagine, testi):
    """Errori di mappa_fiori.pdf: pagine alterne fronte/retro e retri allineati ai fronti (vedi docstring del modulo)."""
    errori = [] if pagine % 2 == 0 else [f"{pagine} pagine: servono coppie fronte/retro"]
    for k, t in enumerate(testi, 1):
        atteso = "fronte" if k % 2 else "retro"
        if f"· {atteso}" not in t:
            errori.append(f"pag. {k} senza «{atteso}»")
    out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True).stdout
    ids, pagina = {}, 0
    for riga in out.splitlines():
        if "<page " in riga:
            pagina += 1
            continue
        m = re.search(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>', riga)
        if m and ID_FIORE.match(m[5]):
            n, lato = ID_FIORE.match(m[5]).groups()
            ids[(pagina, int(n), lato)] = (float(m[3]) / PT, (float(m[2]) + float(m[4])) / 2 / PT)   # id allineato a destra
    somme = []
    for p in range(1, pagine, 2):
        fr = {n: xy for (pg, n, l), xy in ids.items() if pg == p and l == "A"}
        re_ = {n: xy for (pg, n, l), xy in ids.items() if pg == p + 1 and l == "B"}
        if not fr or set(fr) != set(re_):
            errori.append(f"fogli {p}-{p + 1}: fiori del fronte {sorted(fr)} e del retro {sorted(re_)} diversi")
            continue
        for n in fr:
            somme.append(fr[n][0] + re_[n][0])
            if abs(fr[n][1] - re_[n][1]) > 0.6:
                errori.append(f"fiore {n}: y fronte {fr[n][1]:.1f} mm, y retro {re_[n][1]:.1f} mm")
    if somme and max(somme) - min(somme) > 0.6:
        errori.append(f"retri non specchiati: x fronte + x retro da {min(somme):.1f} a {max(somme):.1f} mm")
    return errori


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
    """Errori di un carte_<nome>_retri.pdf rispetto ai fronti carte_<nome>.pdf: ogni pagina dei retri va col foglio dei fronti
    scritto nell'etichetta («coi fronti del foglio k»), ha almeno un dorso e ogni dorso sta nella cella del suo fronte."""
    fronti = pdf.with_name(pdf.name.replace("_retri.pdf", ".pdf"))
    if not fronti.exists():
        return [f"manca {fronti.name}"]
    info = subprocess.run(["pdfinfo", str(fronti)], capture_output=True, text=True).stdout
    pf = int(next(r.split()[-1] for r in info.splitlines() if r.startswith("Pages:")))
    errori = [] if pagine <= pf else [f"{pagine} pagine contro {pf} dei fronti"]
    errori += [f"pag. {k} senza «RETRI»" for k, t in enumerate(testi, 1) if "RETRI" not in t]
    fogli = []                                            # pagina dei retri (da 1) -> foglio dei fronti
    for k, t in enumerate(testi, 1):
        m = re.search(r"coi fronti del foglio (\d+)", t)
        if not m:
            errori.append(f"pag. {k} senza «coi fronti del foglio»")
        fogli.append(int(m[1]) if m else k)
    if fogli != sorted(set(fogli)) or not all(1 <= f <= pf for f in fogli):
        errori.append(f"fogli dei fronti non validi: {fogli}")
    idf, idr = id_per_cella(fronti, formato), id_per_cella(pdf, formato)
    errori += [f"pag. {k} senza dorsi" for k in range(1, pagine + 1) if not any(p == k for p, _ in idr)]
    errori += [f"pag. {p} cella {c + 1}: dorso {i}, fronte del foglio {fogli[p - 1]} {idf.get((fogli[p - 1], c), 'vuoto')}"
               for (p, c), i in sorted(idr.items()) if idf.get((fogli[p - 1], c)) != i]
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
    predefinita = "playtest_v7" if formato == "A4" else "playtest_v7_A3"
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
        if pdf.name == "mappa_fiori.pdf":
            errori += verifica_fiori(pdf, pagine, testi)
        if pdf.name in ("mappa_base.pdf", "mappa_fiori.pdf") and formato == "A4":
            errori += verifica_contorno_arte(pdf)
        if pdf.name in ("mappa_base.pdf", "carta_base_3d.pdf") and formato == "A4":
            errori += verifica_scala(pdf, pagine)
            if pdf.name == "carta_base_3d.pdf" and pagine != 4:
                errori.append(f"{pagine} pagine: servono 4 fogli (NO, NE, SO, SE)")
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
