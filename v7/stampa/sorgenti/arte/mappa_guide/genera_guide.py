#!/usr/bin/env python3
"""Guide per il generatore di immagini della mappa 12×12: un'immagine piatta per ogni faccia di fiore (MF-<NN><A|B>.png,
1024 × 1024) e per ogni quarto di base (MB-NO|NE|SO|SE.png, 1536 × 1024), più palette.json, geometria.json e prompt.csv.

Ogni esagono è pieno del colore piatto del suo terreno (palette.json), lati degli esagoni a 1 px, nessun testo né
icona; fuori dal fiore e negli spazi dei fiori della base c'è la pergamena neutra #f1dcae. Geometria e misure in
../mappa_comune.py. Uso: python3 genera_guide.py   (riscrive tutto in questa cartella; ~2 s)
"""
import csv
import pathlib
import sys

from PIL import Image, ImageDraw

QUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QUI.parent))
import mappa_comune as M  # noqa: E402

SS = 3   # supersampling: bordi lisci, linee da 1 px nell'immagine finale


def disegna(dim, esagoni, px_mm):
    """esagoni: [(cx, cy, terreno | None, linea)] in px della guida; None = pergamena senza linee."""
    w, h = dim
    im = Image.new("RGB", (w * SS, h * SS), M.rgb(M.PALETTE["sfondo"]))
    d = ImageDraw.Draw(im)
    for cx, cy, t, _ in esagoni:
        if t:
            d.polygon([(x * SS, y * SS) for x, y in M.vertici_px(cx, cy, M.R, px_mm)], fill=M.rgb(M.PALETTE[t]))
    for cx, cy, t, linea in esagoni:
        if t and linea:
            v = [(x * SS, y * SS) for x, y in M.vertici_px(cx, cy, M.R, px_mm)]
            d.line(v + [v[0]], fill=M.rgb(M.LINEA_GUIDA), width=SS, joint="curve")
    return im.resize((w, h), Image.LANCZOS)


def descrizione_fiore(f):
    c = f["celle"]
    anello = {}
    for p in range(1, 7):
        anello.setdefault(c[p], []).append(p)
    parti = "; ".join(f"{M.EN[t]} at {','.join(map(str, ps))}" for t, ps in anello.items())
    return (f"flower '{f['nome']}': centre: {M.EN[c[0]]}; ring (1=E, 2=NE, 3=NW, 4=W, 5=SW, 6=SE; hex 1 is the east one): {parti}")


def descrizione_quarto(q, terr):
    """elenco per terreno degli esagoni di base del quarto (colonna,riga) + Partenze + spazi dei fiori."""
    ww, hh = M.BASE_W / M.BASE_PX_MM, M.BASE_H / M.BASE_PX_MM
    x0, y0 = M.origine_quarto(q)
    per = {}
    spazi = 0
    for h, t in terr.items():
        cx, cy = M.F12.centro_mappa(h)
        if not (x0 <= cx <= x0 + ww and y0 <= cy <= y0 + hh):
            continue
        if t is None:
            spazi += 1
        else:
            per.setdefault(t, []).append(h)
    parti = [f"{M.EN[t]} at " + " ".join(f"({x},{y})" for x, y in sorted(per[t], key=lambda h: (h[1], h[0])))
             for t in ("bosco", "rocce", "case", "partenza", "prato") if t in per and t != "prato"]
    nome = {"NO": "north-west", "NE": "north-east", "SO": "south-west", "SE": "south-east"}[q]
    return (f"{nome} quarter of the base (hexes are (column,row), column 1-12 left to right, row 1-12 top to bottom). "
            + "; ".join(parti) + f"; every other base hex is meadow; {spazi} hexes are neutral parchment = flower slots, covered later (paint plain parchment)")


def main():
    fiori, base, spazi, partenze = M.dati()
    righe = []
    for (n, faccia), f in sorted(fiori.items()):
        id_ = M.id_fiore(n, faccia)
        es = [(cx, cy, t, True) for _, t, cx, cy in M.celle_fiore(f)]
        disegna((M.FIORE_PX, M.FIORE_PX), es, M.FIORE_PX_MM).save(QUI / f"{id_}.png", optimize=True)
        righe.append({"id": id_, "file": f"{id_}.png", "size": f"{M.FIORE_PX}x{M.FIORE_PX}", "description": descrizione_fiore(f)})
    terr = M.terreno_base(base, partenze)
    for q in M.QUARTI:
        x0, y0 = M.origine_quarto(q)
        es = [(((cx := M.F12.centro_mappa(h))[0] - x0) * M.BASE_PX_MM, (cx[1] - y0) * M.BASE_PX_MM, t, True) for h, t in terr.items()]
        disegna((M.BASE_W, M.BASE_H), es, M.BASE_PX_MM).save(QUI / f"MB-{q}.png", optimize=True)
        righe.append({"id": f"MB-{q}", "file": f"MB-{q}.png", "size": f"{M.BASE_W}x{M.BASE_H}", "description": descrizione_quarto(q, terr)})
    with open(QUI / "prompt.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "file", "size", "description"])
        w.writeheader()
        w.writerows(righe)
    M.scrivi_json(QUI / "palette.json", {
        "nota": "colore piatto di ogni terreno nelle guide; 'sfondo' = pergamena fuori dal fiore e negli spazi dei fiori della base",
        "linee": f"{M.LINEA_GUIDA}, 1 px sui lati degli esagoni",
        "colori": {t: {"hex": c, "en": M.EN.get(t, "neutral parchment background / flower slot"), "categoria": M.CATEGORIA.get(t, "sfondo")}
                   for t, c in M.PALETTE.items()}})
    M.scrivi_json(QUI / "geometria.json", M.geometria_json())
    print(f"{len(righe)} guide in {QUI}")


if __name__ == "__main__":
    main()
