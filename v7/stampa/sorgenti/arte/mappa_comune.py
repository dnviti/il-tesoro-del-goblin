"""Mappa 12×12: geometria, palette e quadri comuni a guide (mappa_guide/), compositore e verifica (mappa_compone.py).

Una sola fonte per: dove sta ogni esagono in ogni guida, la palette dei terreni, la misura dei PNG di stampa.
La geometria in mm viene da componenti_gen/fiori12.py (W = 25,2 mm da lato a lato, esagoni a punta in alto, origine
della base nell'angolo in alto a sinistra della griglia), i dati da dati/*.csv.

FIORI (28 guide, MF-<NN><A|B>.png, 1024 × 1024 px)
  scala FIORE_PX_MM = 12 px/mm (304,8 ppi); centro del fiore (esagono 0) in (512, 512) px; freccia verso l'esagono 1
  a EST (rotazione 0, come stampato). Il fiore misura 75,6 × 72,75 mm = 907 × 873 px: margine 58 px a sinistra/destra
  (5,7 %) e 75 px sopra/sotto (7,3 %).
BASE (4 guide, MB-NO|NE|SO|SE.png, 1536 × 1024 px)
  scala BASE_PX_MM = 7 px/mm (177,8 ppi); la finestra copre 219,43 × 146,29 mm della griglia 315 × 269,16 mm e supera
  il bordo della griglia di BASE_MARGINE_MM = 4 mm sul lato esterno. Origini (mm, nell'angolo in alto a sinistra della
  finestra): NO (-4, -4), NE (L+4-219,43, -4), SO (-4, A+4-146,29), SE (L+4-219,43, A+4-146,29). Le finestre si
  sovrappongono (orizzontalmente 115,9 mm, verticalmente 15,4 mm): nel compositore ogni esagono si prende dal solo quarto
  che lo possiede (colonna <= 6 -> ovest, riga <= 6 -> nord), il taglio segue i lati degli esagoni.
STAMPA: PPM = 300/25,4 px/mm (300 ppi esatti).
"""
import json
import math
import pathlib
import sys

QUI = pathlib.Path(__file__).resolve().parent
GUIDE = QUI / "mappa_guide"
GREZZE = QUI / "grezze"
PNG = QUI / "png"
DATI = QUI.parent / "dati"
sys.dont_write_bytecode = True
sys.path.insert(0, str(QUI.parent / "componenti_gen"))
import fiori12 as F12  # noqa: E402

W, R, N = F12.W, F12.R, F12.N
LARGO, ALTO = F12.LARGO, F12.ALTO          # 315 × 269,16 mm: la griglia 12 × 12
PPM = 300 / 25.4                            # px/mm dei PNG di stampa (300 ppi)
ABB = 2.0                                   # abbondanza dei fiori (mm), come ABB12 di gen.py

FIORE_PX, FIORE_PX_MM = 1024, 12.0
FIORE_C = (FIORE_PX / 2, FIORE_PX / 2)
BASE_PX_MM, BASE_W, BASE_H, BASE_MARGINE_MM = 7.0, 1536, 1024, 4.0

# palette delle guide (flat): nome terreno -> colore. 'sfondo' = pergamena fuori dal fiore e negli spazi della base.
PALETTE = {
    "prato": "#a8e063", "sentiero": "#c9954a", "mattonato": "#e0763c", "pavimento": "#b7b0d6",
    "guado": "#5fd3d0", "ponte": "#7b4a21", "acqua": "#2a62c9",
    "bosco": "#1b5e2f", "rocce": "#6b6b6b", "case": "#b8322a",
    "partenza": "#f4d21f", "sfondo": "#f1dcae",
}
LINEA_GUIDA = "#1a1a1a"                     # 1 px sui lati degli esagoni
EN = {"prato": "meadow", "sentiero": "dirt path", "mattonato": "brick paving", "pavimento": "stone pavers",
      "guado": "ford (stepping stones across water)", "ponte": "wooden bridge over water", "acqua": "water",
      "bosco": "forest", "rocce": "boulders", "case": "village houses", "partenza": "start hex"}
DIREZIONI = ["E", "NE", "NW", "W", "SW", "SE"]   # anello 1-6 antiorario da est

OSTACOLI = ("bosco", "rocce", "case")
ACQUATICI = ("acqua", "guado", "ponte")
CATEGORIA = {t: ("ostacolo-" + t if t in OSTACOLI else "acqua" if t in ACQUATICI else "libero") for t in
             ("prato", "sentiero", "mattonato", "pavimento", "guado", "ponte", "acqua", "bosco", "rocce", "case", "partenza")}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dati():
    """(fiori, base, spazi, partenze) come F12.leggi; fiori[(n, 'A')] = {'nome', 'celle': {pos: terreno}, 'id': '01A'}."""
    fiori, base, spazi, partenze, _ = F12.leggi(str(DATI))
    return fiori, base, spazi, partenze


def id_fiore(n, faccia):
    return f"MF-{n:02d}{faccia}"


def tutti_id_fiori():
    return [id_fiore(n, f) for n in range(1, 15) for f in "AB"]


# ------------------------------------------------------------------ fiori
def celle_fiore(f):
    """[(pos, terreno, cx_px, cy_px)] del fiore nella guida 1024 × 1024."""
    return [(p, t, FIORE_C[0] + F12.centro_locale(p, 0)[0] * FIORE_PX_MM, FIORE_C[1] + F12.centro_locale(p, 0)[1] * FIORE_PX_MM)
            for p, t in sorted(f["celle"].items())]


def vertici_px(cx, cy, raggio_mm, px_mm):
    return [(cx + raggio_mm * px_mm * math.cos(math.radians(a)), cy + raggio_mm * px_mm * math.sin(math.radians(a)))
            for a in (-90, -30, 30, 90, 150, 210)]


def fiore_bbox_mm(abb=ABB):
    """semilarghezza e semialtezza (mm) del fiore con abbondanza abb (esagoni di raggio R + abb/cos30, fatti a mitra)."""
    ra = R + abb / math.cos(math.radians(30))
    return 1.5 * W + abb, 1.5 * R + ra


def fiore_png_px(abb=ABB):
    """dimensione (px, a 300 ppi) del PNG di stampa del fiore e dimensione in mm con cui va posato, centrato sul fiore."""
    hw, hh = fiore_bbox_mm(abb)
    w, h = math.ceil(2 * hw * PPM), math.ceil(2 * hh * PPM)
    return w, h, w / PPM, h / PPM


# ------------------------------------------------------------------ base
def origine_quarto(q):
    """(x0, y0) in mm della finestra del quarto q (NO|NE|SO|SE), nelle coordinate della griglia."""
    m, ww, hh = BASE_MARGINE_MM, BASE_W / BASE_PX_MM, BASE_H / BASE_PX_MM
    return (-m if q[1] == "O" else LARGO + m - ww), (-m if q[0] == "N" else ALTO + m - hh)


QUARTI = ("NO", "NE", "SO", "SE")


def quarto_di(h):
    """quarto che possiede l'esagono (x, y)."""
    return ("N" if h[1] <= 6 else "S") + ("O" if h[0] <= 6 else "E")


def terreno_base(base, partenze):
    """{(x, y): terreno} dei 144 esagoni della base: 'partenza' sulle Partenze, None sugli spazi dei fiori."""
    t = {}
    for y in range(1, 13):
        for x in range(1, 13):
            t[(x, y)] = ("partenza" if (x, y) in partenze else base[(x, y)]) if (x, y) in base else None
    return t


def base_png_px():
    """dimensione (px a 300 ppi) del PNG di stampa della base intera (griglia 315 × 269,16 mm) e in mm."""
    w, h = math.ceil(LARGO * PPM), math.ceil(ALTO * PPM)
    return w, h, w / PPM, h / PPM


def geometria_json():
    """geometria documentata per mappa_guide/geometria.json."""
    ww, hh = BASE_W / BASE_PX_MM, BASE_H / BASE_PX_MM
    w, h, wmm, hmm = fiore_png_px()
    bw, bh, bwmm, bhmm = base_png_px()
    return {
        "fiore_guida": {"px": [FIORE_PX, FIORE_PX], "px_per_mm": FIORE_PX_MM, "centro_px": list(FIORE_C),
                        "ingombro_mm": [3 * W, 5 * R], "ingombro_px": [round(3 * W * FIORE_PX_MM), round(5 * R * FIORE_PX_MM)],
                        "esagono_lato_a_lato_mm": W, "esagono_punta_punta_mm": round(2 * R, 3),
                        "orientamento": "esagoni a punta in alto; esagono 0 al centro; anello 1-6 antiorario da EST (1 = E, 2 = NE, 3 = NW, 4 = W, 5 = SW, 6 = SE)"},
        "fiore_stampa": {"px": [w, h], "mm": [round(wmm, 4), round(hmm, 4)], "ppi": 300, "abbondanza_mm": ABB,
                         "nota": "PNG centrato sul centro del fiore; fuori dal contorno + abbondanza l'immagine e' solo estesa (il clip lo taglia)"},
        "base_guida": {"px": [BASE_W, BASE_H], "px_per_mm": BASE_PX_MM, "finestra_mm": [round(ww, 3), round(hh, 3)],
                       "griglia_mm": [LARGO, round(ALTO, 3)], "margine_oltre_bordo_mm": BASE_MARGINE_MM,
                       "origini_mm": {q: [round(v, 4) for v in origine_quarto(q)] for q in QUARTI},
                       "pixel": "px = (x_mm - x0) * 7, py = (y_mm - y0) * 7, con x_mm,y_mm nelle coordinate della griglia (0,0 = angolo in alto a sinistra)",
                       "centro_esagono_mm": "x = 25,2 * (c - 0,5 + (0,5 se r pari)), y = R * (1 + 1,5 * (r - 1)), R = 14,549",
                       "sovrapposizione_mm": {"orizzontale": round(2 * ww - LARGO - 2 * BASE_MARGINE_MM, 2), "verticale": round(2 * hh - ALTO - 2 * BASE_MARGINE_MM, 2)},
                       "possesso": "colonna <= 6 -> ovest, riga <= 6 -> nord (taglio lungo i lati degli esagoni)"},
        "base_stampa": {"px": [bw, bh], "mm": [round(bwmm, 4), round(bhmm, 4)], "ppi": 300, "origine_mm": [0, 0]},
        "palette_file": "palette.json",
    }


def scrivi_json(path, obj):
    pathlib.Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
