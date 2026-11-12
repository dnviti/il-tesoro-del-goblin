#!/usr/bin/env python3
"""Mappa 12×12: compositore e verifica delle illustrazioni generate (grezze/MF-<NN><A|B>.webp, grezze/MB-<NO|NE|SO|SE>.webp).

Le grezze sono generate sulle guide di mappa_guide/ (stessa inquadratura, vedi mappa_comune.py). Il compositore:
  1. ALLINEA ogni grezza alla sua guida (solo scala e traslazione): correlazione normalizzata, grossolana poi fine, di
     cinque mappe di caratteristiche (bordi di colore, silhouette «non pergamena», Lab sfocato), vedi allinea(). Scala
     0,93-1,07, traslazione fino a ±80 px (±6,7 mm sui fiori, ±12 mm sulla base). Stampa scala, traslazione e punteggio;
     se il punteggio è basso (< PUNTEGGIO_MIN) o la stima tocca i limiti avvisa e NON corregge (identità: la guida è già
     la posizione giusta, e gpt-image-2 la rispetta);
  2. FIORI: ricampiona a 300 ppi, prende l'interno del contorno meno 1 mm (RIENTRO_MM, via il bordo scuro del modello), poi
     riflette l'immagine sul bordo per l'abbondanza di 2 mm (la texture continua, niente strisce) -> png/MF-<NN><A|B>.png,
     941 × 914 px (79,67 × 77,39 mm), centrato sul centro del fiore;
  3. BASE: i 4 quarti sono ricampionati a 300 ppi sulla griglia intera; ogni esagono si prende dal solo quarto che lo
     possiede (colonna <= 6 ovest, riga <= 6 nord): il taglio segue i lati degli esagoni -> png/MB-BASE.png (3721 × 3180 px,
     315,04 × 269,2 mm, origine nell'angolo in alto a sinistra della griglia). Servono tutti e 4 i quarti;
  4. RIFINITURA (riuso di elabora.py / PhotoCraft): stesso look condiviso (curve tono e calore + tonalità e saturazione) di
     tutte le illustrazioni; si salta con --senza-look. Il progetto va in pcraft/<id>.pcraft, il PNG in png/ senza profilo ICC.
  Perché non elabora.py direttamente: il suo `image.crop` fa solo ritagli centrati; qui servono allineamento e ritaglio sul
  contorno. L'unica parte riusata è il look finale (PhotoCraft) e la pulizia dell'ICC.

--verifica: per ogni esagono campiona l'interno (esagono al 62 % del raggio) dell'immagine riallineata alla guida e controlla
che somigli al terreno dei dati (vedi SOGLIE e verifica_esagono()). Non scrive nulla; esce con 1 se c'è un ERRORE.

Uso (da qualsiasi cartella):
  python3 mappa_compone.py                         compone tutto ciò che c'è in grezze/ (MF-* e MB-*)
  python3 mappa_compone.py MF-03A MB-NO ...        solo questi id (per la base servono tutti e 4 i quarti)
  SG-DOMANDA, SG-CRIPTA: segnalini «?» (cerchio Ø 20 mm) e Cripta (esagono 25,2 mm), grezze 1254², ritaglio + abbondanza di 2 mm
  riflessa -> png/SG-DOMANDA.png (284 x 284 px) e png/SG-CRIPTA.png (345 x 399 px); nessuna verifica dei terreni
  python3 mappa_compone.py --verifica [id ...]     controlla i terreni (senza comporre); --report FILE.csv scrive ogni esagono
  Opzioni: --grezze DIR, --uscita DIR (default png/), --guide DIR, --senza-look, --soglia nome=valore (vedi SOGLIE)
"""
import argparse
import csv
import json
import math
import pathlib
import shutil
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

QUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import mappa_comune as M  # noqa: E402

PUNTEGGIO_MIN = 1.5          # somma delle 5 correlazioni normalizzate (-5..5): sotto, l'allineamento è dubbio
SCALE = (0.93, 1.07)
MARGINE_PX = {"fiore": 40, "base": 28}          # a risoluzione dimezzata/terzo: ±80 / ±84 px sulla guida
FATTORE = {"fiore": 2, "base": 3}               # riduzione per la ricerca grossolana
RIENTRO_MM = 1.0                                 # dal contorno del fiore verso l'interno: da qui in fuori l'abbondanza è riflessa
PERGAMENA = np.array(M.rgb(M.PALETTE["sfondo"]), np.uint8)

# ------------------------------------------------------------------ soglie della verifica (frazioni dei pixel dell'esagono)
# Famiglie di colore per pixel (HSV di OpenCV: H 0-179 = gradi/2, S e V 0-255):
#   blu: H 85-135, S>=60, V>=50 | verde: H 30-85, S>=55, V>=35 (verde_scuro: V<150) | caldo: H<=20 o >=165, S>=100, V>=60
#   legno: H 8-28, S 60-230, V 30-210 | grigio: S<50, V>=50 (scuro V<165, chiaro >=165) | buio: V<50
SOGLIE = {
    "acqua_blu_min": 0.45,        # acqua: almeno questa quota di pixel blu
    "guado_blu_min": 0.25,        # guado: acqua con sassi
    "ponte_blu_min": 0.0,         # ponte: acqua con assi (0 = non richiesto: le assi possono coprire tutto l'esagono)
    "ponte_legno_min": 0.06,      # ponte: almeno questa quota di legno (le assi)
    "blu_max_asciutto": 0.20,     # su un terreno non acquatico: oltre questa quota di blu = acqua dove non c'è
    "bosco_scuro_min": 0.25,      # bosco: quota di verde scuro
    "verde_scuro_max": 0.45,      # su un terreno non bosco: oltre = bosco dove non c'è
    "rocce_grigio_min": 0.20,     # rocce: quota di grigio scuro
    "grigio_scuro_max": 0.35,     # terreno senza rocce né pavimento/guado/ponte: oltre = rocce dove non ci sono
    "rocce_pietra_min": 0.35,     # rocce: in alternativa al grigio, pietra calda (tono legno) senza verde scuro
    "case_caldo_min": 0.25,       # case: quota di rosso/arancio + legno (tetti e muri)
    "prato_verde_min": 0.30,      # prato: quota di verde
    "relativo_rapporto": 0.60,    # strato relativo: avviso se un altro terreno è più vicino di rapporto * distanza dal proprio
    "relativo_minimo": 0.25,      # ... e la distanza dal proprio supera questo
    "relativo_campioni": 4,       # ... e il prototipo dell'altro terreno ha almeno tanti campioni
    "liberi_verde_max": 0.60,     # sentiero/mattonato/pavimento: oltre questa quota di verde = prato dove non c'è (solo avviso)
    "raggio_campione": 0.62,      # raggio dell'area campionata / raggio dell'esagono
}
# coppie di terreni che il solo colore non distingue (tetti rossi e mattoni/sentiero ocra, Partenza gialla su terreno chiaro, pietra calda):
AMBIGUI = [{"case", "sentiero"}, {"case", "mattonato"}, {"case", "pavimento"}, {"partenza", "prato"}, {"partenza", "pavimento"},
           {"partenza", "sentiero"}, {"partenza", "mattonato"}, {"rocce", "pavimento"}, {"rocce", "partenza"}]
CARATTERISTICHE = ("blu", "verde", "verde_scuro", "caldo", "legno", "grigio_scuro", "grigio_chiaro", "buio")


# ------------------------------------------------------------------ immagini
def apri(path):
    return np.asarray(Image.open(path).convert("RGB"))


def trova_grezza(i, cartella):
    return next((p for p in (cartella / f"{i}.webp", cartella / f"{i}.png") if p.is_file()), None)


def carica_grezza(path, guida):
    """(grezza nativa, grezza ridotta alla misura della guida, fattori nativo/guida)."""
    nat = apri(path)
    gh, gw = guida.shape[:2]
    rh, rw = nat.shape[:2]
    if abs(rw / rh - gw / gh) > 0.03 * gw / gh:
        print(f"  ATTENZIONE {path.name}: proporzioni {rw}x{rh} diverse dalla guida {gw}x{gh}", file=sys.stderr)
    rid = nat if (rw, rh) == (gw, gh) else cv2.resize(nat, (gw, gh), interpolation=cv2.INTER_AREA)
    return nat, rid, (rw / gw, rh / gh)


# ------------------------------------------------------------------ allineamento
PESI = (1.0, 1.0, 1.0, 1.0, 1.0)      # bordi, silhouette «non pergamena», L, a, b (questi tre sfocati)


def mappe(img, sigma):
    """mappe di caratteristiche, sfocate di sigma, per la correlazione: bordi di colore, silhouette «non pergamena»,
    e i tre canali Lab sfocati (il modello tiene l'impronta di colore della guida anche quando ridipinge i dettagli)."""
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    s = cv2.GaussianBlur(lab, (0, 0), 1.2)
    g = np.sqrt(sum(cv2.Sobel(s[..., c], cv2.CV_32F, 1, 0) ** 2 + cv2.Sobel(s[..., c], cv2.CV_32F, 0, 1) ** 2 for c in range(3)))
    g = np.clip(g / (np.percentile(g, 99.5) + 1e-6), 0, 1)
    perg = cv2.cvtColor(PERGAMENA.reshape(1, 1, 3), cv2.COLOR_RGB2LAB).astype(np.float32)
    d = np.sqrt(((lab - perg) ** 2).sum(-1))
    sil = np.clip((d - 10) / 12, 0, 1)
    sf = sigma * 2.5
    return [cv2.GaussianBlur(g, (0, 0), sigma), cv2.GaussianBlur(sil, (0, 0), sigma)] + \
           [cv2.GaussianBlur(lab[..., c], (0, 0), sf) for c in range(3)]


def affine(s, tx, ty, c):
    """guida -> grezza: p' = c + s (p - c) + t."""
    return np.array([[s, 0, c[0] * (1 - s) + tx], [0, s, c[1] * (1 - s) + ty]], np.float64)


def migliore(guida_m, grezza_m, scale, margine, base=None, c=None):
    """prova le scale; per ognuna la guida scalata (e spostata di `base`) è cercata nella grezza con ±margine px. Ritorna
    (punteggio, scala, tx, ty) dove (tx, ty) include `base`."""
    h, w = guida_m[0].shape
    best = (-9, 1.0, 0, 0)
    for s in scale:
        A = affine(s, 0, 0, c)
        if base is not None:
            A[:, 2] += base
        gs = [cv2.warpAffine(m, A, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0) for m in guida_m]
        # la guida scalata è ancora nel riquadro della grezza: il modello ha tenuto la pergamena fuori, quindi il bordo e' 0
        r = sum(wt * np.nan_to_num(cv2.matchTemplate(g_m, t[margine:h - margine, margine:w - margine], cv2.TM_CCOEFF_NORMED))
                for wt, g_m, t in zip(PESI, grezza_m, gs))
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]:
            best = (mx, s, loc[0] - margine + (0 if base is None else base[0]), loc[1] - margine + (0 if base is None else base[1]))
    return best


def allinea(guida, grezza, tipo):
    """Stima scala e traslazione guida -> grezza (entrambe RGB della stessa misura). Ritorna (A 2x3, info)."""
    f = FATTORE[tipo]
    h, w = guida.shape[:2]
    c = (w / 2, h / 2)
    ridu = lambda im: cv2.resize(im, (w // f, h // f), interpolation=cv2.INTER_AREA)
    # grossolana (risoluzione 1/f): scale a passo 0,01
    gm, rm = mappe(ridu(guida), 3), mappe(ridu(grezza), 3)
    scale = [round(x, 4) for x in np.arange(SCALE[0], SCALE[1] + 1e-9, 0.01)]
    p, s, tx, ty = migliore(gm, rm, scale, MARGINE_PX[tipo], c=(c[0] / f, c[1] / f))
    tx, ty = tx * f, ty * f
    # fine (risoluzione piena): scala ±0,010 a passo 0,002, traslazione residua ±12 px attorno alla stima grossolana
    gm, rm = mappe(guida, 2), mappe(grezza, 2)
    scale = [round(s + d, 4) for d in np.arange(-0.010, 0.0101, 0.002)]
    p2, s2, tx2, ty2 = migliore(gm, rm, scale, 12, base=np.array([tx, ty]), c=c)
    limite = bool(abs(s2 - SCALE[0]) < 0.003 or abs(s2 - SCALE[1]) < 0.003
                  or abs(tx2) > MARGINE_PX[tipo] * f + 10 or abs(ty2) > MARGINE_PX[tipo] * f + 10)
    info = {"scala": s2, "tx": tx2, "ty": ty2, "punteggio": p2, "limite": limite, "identita": False}
    if p2 < PUNTEGGIO_MIN or limite:     # stima inattendibile: meglio nessuna correzione (la guida e' gia' la posizione giusta)
        info["identita"] = True
        return affine(1.0, 0, 0, c), info
    return affine(s2, tx2, ty2, c), info


def avvisa_allineamento(nome, info):
    t = f"{nome}: scala {info['scala']:.3f}  t=({info['tx']:+.1f}, {info['ty']:+.1f}) px  punteggio {info['punteggio']:.2f}"
    if info["punteggio"] < PUNTEGGIO_MIN or info["limite"]:
        t += "  ATTENZIONE: allineamento dubbio" + (" (stima al limite)" if info["limite"] else " (punteggio basso)") + ", nessuna correzione applicata"
    print("  " + t)
    return info["punteggio"] >= PUNTEGGIO_MIN and not info["limite"]


def riallinea(nat, A, fatt, dim):
    """grezza nativa -> riquadro della guida (dim = (w, h)), con la trasformazione A guida->grezza ridotta."""
    Mx = np.diag([fatt[0], fatt[1]]) @ A
    return cv2.warpAffine(nat, Mx, dim, flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)


# ------------------------------------------------------------------ geometria in px di uscita
def poligono(cx, cy, raggio_mm, px_mm):
    return np.round(np.array(M.vertici_px(cx, cy, raggio_mm, px_mm)) * 16).astype(np.int32)    # 4 bit frazionari per fillPoly


def riempi(maschera, poligoni):
    for p in poligoni:
        cv2.fillPoly(maschera, [p], 255, lineType=cv2.LINE_AA, shift=4)


# ------------------------------------------------------------------ composizione
def estendi_fuori(img, dentro):
    """i pixel fuori dalla maschera `dentro` si ricavano per riflessione sul bordo della maschera (la texture continua
    invece di strisciare come con il pixel più vicino); se il punto riflesso è fuori, vale il pixel di bordo."""
    _, idx = ndimage.distance_transform_edt(~dentro, return_indices=True)
    h, w = dentro.shape
    yy, xx = np.mgrid[0:h, 0:w]
    ry = np.clip(2 * idx[0] - yy, 0, h - 1)
    rx = np.clip(2 * idx[1] - xx, 0, w - 1)
    ok = dentro[ry, rx]
    sy, sx = np.where(ok, ry, idx[0]), np.where(ok, rx, idx[1])
    return img[sy, sx]


# ------------------------------------------------------------------ allineamento per esagono
# Il modello disegna ogni esagono vicino alla guida ma non esatto: bordi spostati fino a ~1,3 mm e scala diversa da un
# esagono all'altro (misurato sulla base: mediana 0,15 mm, 99° percentile 1,3 mm). Un'affine globale non basta: l'arte
# sbordava dalla linea vettoriale (doppio bordo, vuoti di pergamena). Ogni esagono ha quindi la sua affine (scala x/y e
# traslazione) che porta il suo bordo scuro sul contorno vero; poi si ritaglia ESATTAMENTE sul contorno.
FIT_RAGGIO_MM = 2.4                  # traslazione massima per esagono
FIT_SCALA = 0.06                     # scala massima ± per esagono
FIT_PUNTEGGIO_MIN = 0.12             # sotto, l'adattamento è inattendibile: si lascia l'identità e si avvisa
SOVRAPPOSIZIONE_MM = 0.10            # l'arte di un esagono arriva 0,1 mm oltre il contorno (sotto la linea), mai di più
CORDOLO_TOL = 30                     # distanza massima per canale dal colore pergamena per dire «cordolo»
CORDOLO_MAX_MM = 3.5                 # il cordolo si cerca entro questa distanza dal bordo
CORDOLO_DILATA_MM = 0.5              # ...e si allarga per portare via anche il filetto scuro che lo borda
FILETTO_CONTRASTO, FILETTO_MAX_MM, FILETTO_MIN_MM, FILETTO_STD_MM = 25, 2.6, 7.0, 0.4   # filetto scuro parallelo al bordo
RIENTRO_ESAGONO_MM = 1.0             # il bordo scuro del modello (~0,45 mm, fino a ~0,5 mm fuori posto per lato dopo l'adattamento) si scarta; la linea vettoriale lo sostituisce


def mappa_bordi(img, px_mm):
    """D in 0..1: dove c'è un bordo scuro sottile (cresta di scuro) o un bordo della silhouette «non pergamena»."""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    sig = 0.6 * px_mm
    cresta = np.clip(cv2.GaussianBlur(gray, (0, 0), sig) - gray, 0, None)
    cresta = cv2.GaussianBlur(cresta, (0, 0), 0.12 * px_mm)
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    perg = cv2.cvtColor(PERGAMENA.reshape(1, 1, 3), cv2.COLOR_RGB2LAB).astype(np.float32)
    sil = cv2.GaussianBlur(np.clip((np.sqrt(((lab - perg) ** 2).sum(-1)) - 10) / 12, 0, 1), (0, 0), 0.15 * px_mm)
    gs = np.hypot(cv2.Sobel(sil, cv2.CV_32F, 1, 0), cv2.Sobel(sil, cv2.CV_32F, 0, 1))
    return np.clip(cresta / (np.percentile(cresta, 99.5) + 1e-6), 0, 1) + 0.7 * np.clip(gs / (np.percentile(gs, 99.5) + 1e-6), 0, 1)


def adatta_esagoni(img, centri, px_mm):
    """Per ogni centro (px della guida) l'affine (sx, sy, tx, ty) che porta l'esagono della guida sull'esagono disegnato
    nella grezza `img` (già riportata nel riquadro della guida): p_grezza = c + (sx, sy) * (p - c) + (tx, ty). Ritorna
    [(sx, sy, tx, ty, punteggio)]; l'identità con punteggio basso se il bordo non si trova."""
    from scipy.optimize import minimize
    D = mappa_bordi(img, px_mm)
    t = np.linspace(0, 1, 25, endpoint=False)
    v = np.array(M.vertici_px(0, 0, M.R, px_mm))
    pts_ = np.concatenate([v[i] + (v[(i + 1) % 6] - v[i]) * t[:, None] for i in range(6)])      # perimetro, centrato su 0

    def valore(p, c):
        sx, sy, tx, ty = p
        x = c[0] + sx * pts_[:, 0] + tx
        y = c[1] + sy * pts_[:, 1] + ty
        return ndimage.map_coordinates(D, [y, x], order=1, mode="nearest").mean()

    out = []

    def cerca(c, r, scala):
        griglia = [(valore((1, 1, dx, dy), c), dx, dy) for dx in np.arange(-r, r + 1e-6, 0.2 * px_mm) for dy in np.arange(-r, r + 1e-6, 0.2 * px_mm)]
        v0, dx0, dy0 = max(griglia)
        # penalità piccola sullo spostamento e sulla scala (a parità di bordo preferisce l'identità)
        f = lambda p: -valore(p, c) + 0.004 * (abs(p[2]) + abs(p[3])) / px_mm + 0.025 * (abs(p[0] - 1) + abs(p[1] - 1))
        lim = [(1 - scala, 1 + scala)] * 2 + [(-r, r)] * 2
        best = minimize(f, [1, 1, float(np.clip(dx0, -r, r)), float(np.clip(dy0, -r, r))], method="Powell", bounds=lim, options={"xtol": 0.02, "ftol": 1e-5})
        return best.x, float(valore(best.x, c))

    for c in centri:
        # prima una rifinitura vicino alla guida; la correzione grande vale solo se il bordo trovato è MOLTO più netto:
        # un cordolo o un filetto dentro il bordo vero (alcuni esagoni di mattonato) attirerebbe l'adattamento
        pa, va = cerca(c, 0.6 * px_mm, 0.03)
        pb, vb = cerca(c, FIT_RAGGIO_MM * px_mm, FIT_SCALA)
        p, v = (pb, vb) if vb > 1.3 * va + 0.05 else (pa, va)
        out.append((float(p[0]), float(p[1]), float(p[2]), float(p[3]), v))
    return out


def adatta_o_identita(img, centri, px_mm, nome):
    """adatta_esagoni + avvisi; sotto FIT_PUNTEGGIO_MIN l'esagono resta com'è (identità)."""
    fit = adatta_esagoni(img, centri, px_mm)
    res, scarti = [], []
    for k, (sx, sy, tx, ty, pu) in enumerate(fit):
        if pu < FIT_PUNTEGGIO_MIN:
            print(f"  ATTENZIONE {nome} esagono {k}: bordo non trovato (punteggio {pu:.2f}), nessuna correzione", file=sys.stderr)
            res.append((1.0, 1.0, 0.0, 0.0))
        else:
            res.append((sx, sy, tx, ty))
            scarti.append(math.hypot(tx, ty) / px_mm)
    if scarti:
        print(f"  {nome}: adattamento per esagono, spostamento mediano {np.median(scarti):.2f} mm, massimo {max(scarti):.2f} mm")
    return res


def poligono_loc(cx, cy, raggio_mm, px_mm, ox, oy):
    return poligono(cx - ox, cy - oy, raggio_mm, px_mm)


GIALLO_PARTENZA = np.array(M.rgb(M.PALETTE["partenza"]), np.uint8)
GIALLO_TOL = 55


def bordo_pergamena(patch, dist, giallo=False):
    """maschera del «cordolo» color pergamena (con il suo filetto scuro) che il modello a volte disegna dentro il bordo di
    un esagono: pixel color pergamena, collegati al bordo (entro CORDOLO_MAX_MM) e dilatati di CORDOLO_DILATA_MM. Senza
    questo il cordolo diventa una striscia vuota sul contorno stampato. giallo: tratta come cordolo anche il giallo
    Partenza (esagoni di base che non sono Partenze)."""
    crema = (np.abs(patch.astype(int) - PERGAMENA.astype(int)).max(-1) < CORDOLO_TOL) & (dist > 0)
    if giallo:   # esagono che non è una Partenza: il giallo della Partenza vicina che il modello ha fatto sbordare
        crema |= (np.abs(patch.astype(int) - GIALLO_PARTENZA.astype(int)).max(-1) < GIALLO_TOL) & (dist > 0)
    vicino = dist < CORDOLO_MAX_MM * M.PPM
    cand = (crema & vicino).astype(np.uint8)
    n, lab = cv2.connectedComponents(cand, connectivity=8)
    if n <= 1:
        return np.zeros(dist.shape, bool)
    toccano = np.unique(lab[(dist < 1.0 * M.PPM) & (dist > 0) & (cand > 0)])
    sel = np.isin(lab, toccano[toccano > 0])
    r = int(round(CORDOLO_DILATA_MM * M.PPM))
    return cv2.dilate(sel.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0


def bordo_scuro_parallelo(patch, dist):
    """maschera di un filetto scuro (residuo del bordo del modello, rimasto dentro il contorno perché l'esagono disegnato
    non è un'affine esatta della guida): componente di pixel scuri e sottili, lunga almeno FILETTO_MIN_MM e parallela al
    bordo (distanza dal bordo quasi costante), entro FILETTO_MAX_MM. Ombre e foglie non sono lunghe e parallele."""
    gray = cv2.cvtColor(patch, cv2.COLOR_RGB2GRAY).astype(np.float32)
    cresta = (cv2.GaussianBlur(gray, (0, 0), 0.5 * M.PPM) - gray > FILETTO_CONTRASTO) & (gray < 120)
    banda = (dist > 0.2 * M.PPM) & (dist < FILETTO_MAX_MM * M.PPM)
    n, lab, st, _ = cv2.connectedComponentsWithStats((cresta & banda).astype(np.uint8), connectivity=8)
    out = np.zeros(dist.shape, bool)
    for k in range(1, n):
        if max(st[k, cv2.CC_STAT_WIDTH], st[k, cv2.CC_STAT_HEIGHT]) < FILETTO_MIN_MM * M.PPM:
            continue
        d = dist[lab == k] / M.PPM
        if d.std() < FILETTO_STD_MM:
            out |= lab == k
    if not out.any():
        return out
    r = int(round(0.35 * M.PPM))
    return cv2.dilate(out.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0


def compone_celle(nat, A, fatt, adat, centri_guida, px_guida_mm, centri_out, o2g, dim_out, bleed_mm=0.0, no_giallo=None):
    """Compone l'immagine di uscita esagono per esagono. centri_guida/centri_out: centro di ogni esagono in px della
    guida e in px di uscita; adat: affine per esagono (sx, sy, tx, ty); o2g: 3x3 uscita -> guida; dim_out = (w, h).
    Ogni esagono: warp locale (uscita -> guida -> affine dell'esagono -> grezza globale -> nativa), si tiene l'interno
    del contorno meno RIENTRO_ESAGONO_MM, si riflette fino al contorno + SOVRAPPOSIZIONE_MM (bleed_mm > 0: prima un giro
    con il raggio dell'abbondanza, per tutti, poi quello stretto sopra: il vero vince sul riflesso del vicino)."""
    w, h = dim_out
    out = np.empty((h, w, 3), np.uint8)
    out[:] = PERGAMENA
    A3 = np.vstack([A, [0, 0, 1]])
    F = np.diag([fatt[0], fatt[1], 1])
    metà = math.ceil((M.R + bleed_mm / math.cos(math.radians(30)) + 1.5) * M.PPM)
    giri = ([M.R + bleed_mm / math.cos(math.radians(30))] if bleed_mm else []) + [M.R + SOVRAPPOSIZIONE_MM]
    for ri, raggio in enumerate(giri):
        for (sx, sy, tx, ty), cg, co, ng in zip(adat, centri_guida, centri_out, no_giallo or [False] * len(adat)):
            ox, oy = int(round(co[0])) - metà, int(round(co[1])) - metà
            x0, y0, x1, y1 = max(ox, 0), max(oy, 0), min(ox + 2 * metà, w), min(oy + 2 * metà, h)
            if x1 <= x0 or y1 <= y0:
                continue
            T = np.array([[sx, 0, cg[0] * (1 - sx) + tx], [0, sy, cg[1] * (1 - sy) + ty], [0, 0, 1]])
            loc = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], float)
            Mx = F @ A3 @ T @ o2g @ loc
            ph, pw = y1 - y0, x1 - x0
            patch = cv2.warpAffine(nat, Mx[:2], (pw, ph), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
            cx, cy = co[0] - x0, co[1] - y0
            pieno = np.zeros((ph, pw), np.uint8)
            riempi(pieno, [poligono(cx, cy, M.R, M.PPM)])
            dist = ndimage.distance_transform_edt(pieno > 127)
            dentro = (dist > RIENTRO_ESAGONO_MM * M.PPM) & ~bordo_pergamena(patch, dist, ng) & ~bordo_scuro_parallelo(patch, dist)
            patch = estendi_fuori(patch, dentro)
            m = np.zeros((ph, pw), np.uint8)
            riempi(m, [poligono(cx, cy, raggio, M.PPM)])
            sel = m > 127
            out[y0:y1, x0:x1][sel] = patch[sel]
    return out


def compone_fiore(i, nat, A, fatt, fiore, adat, abb=M.ABB):
    w, h, _, _ = M.fiore_png_px(abb)
    k = M.FIORE_PX_MM / M.PPM
    O2G = np.array([[k, 0, M.FIORE_C[0] - (w - 1) / 2 * k], [0, k, M.FIORE_C[1] - (h - 1) / 2 * k], [0, 0, 1]])
    pos = sorted(fiore["celle"])
    cg = [(M.FIORE_C[0] + M.F12.centro_locale(p, 0)[0] * M.FIORE_PX_MM, M.FIORE_C[1] + M.F12.centro_locale(p, 0)[1] * M.FIORE_PX_MM) for p in pos]
    co = [((w - 1) / 2 + M.F12.centro_locale(p, 0)[0] * M.PPM, (h - 1) / 2 + M.F12.centro_locale(p, 0)[1] * M.PPM) for p in pos]
    return compone_celle(nat, A, fatt, adat, cg, M.FIORE_PX_MM, co, O2G, (w, h), bleed_mm=abb)


def centri_fiore_guida(fiore):
    return [(M.FIORE_C[0] + M.F12.centro_locale(p, 0)[0] * M.FIORE_PX_MM, M.FIORE_C[1] + M.F12.centro_locale(p, 0)[1] * M.FIORE_PX_MM)
            for p in sorted(fiore["celle"])]


def compone_base(quarti, terr):
    """quarti: {q: (nat, A, fatt, adat)}; ritorna l'immagine della base intera a 300 ppi. Ogni esagono viene dal solo
    quarto che lo possiede (colonna <= 6 ovest, riga <= 6 nord) e si ritaglia sul suo contorno."""
    w, h, _, _ = M.base_png_px()
    out = np.empty((h, w, 3), np.uint8)
    out[:] = PERGAMENA
    k = M.BASE_PX_MM / M.PPM
    for q, (nat, A, fatt, adat) in quarti.items():
        x0, y0 = M.origine_quarto(q)
        O2G = np.array([[k, 0, -x0 * M.BASE_PX_MM], [0, k, -y0 * M.BASE_PX_MM], [0, 0, 1]])
        mio = [hx for hx, t in terr.items() if t is not None and M.quarto_di(hx) == q]
        co = [tuple(c * M.PPM for c in M.F12.centro_mappa(hx)) for hx in mio]
        cg = [centri_base_guida(q, hx) for hx in mio]
        parziale = compone_celle(nat, A, fatt, [adat[hx] for hx in mio], cg, M.BASE_PX_MM, co, O2G, (w, h),
                                 no_giallo=[terr[hx] != "partenza" for hx in mio])
        # solo i pixel degli esagoni di questo quarto (il resto è pergamena)
        mask = np.zeros((h, w), np.uint8)
        riempi(mask, [poligono(c[0], c[1], M.R + SOVRAPPOSIZIONE_MM, M.PPM) for c in co])
        out[mask > 127] = parziale[mask > 127]
    return out


def centri_base_guida(q, hx):
    x0, y0 = M.origine_quarto(q)
    cx, cy = M.F12.centro_mappa(hx)
    return ((cx - x0) * M.BASE_PX_MM, (cy - y0) * M.BASE_PX_MM)


# ------------------------------------------------------------------ segnalini «?» (cerchio Ø 20 mm) e Cripta (esagono 25,2 mm)
# grezze/SG-DOMANDA.webp e SG-CRIPTA.webp (1254²): centro e px/mm misurati sul bordo dell'arte (bbox dei pixel non pergamena).
# Stati: quadrato 30 mm = tutta la grezza (l'illustrazione si vede intera, il kit la riduce a ~8 mm).
# Segnalini e tessere (grezze 1254²). forma: cerchio/esagono = arte che riempie la forma (bordo scuro scartato, abbondanza
# riflessa, `raggio` mm e `abb` mm); quadro = oggetto su pergamena: la grezza è ridimensionata a `lato_mm` e centrata su un
# rettangolo `out_mm` (w, h) con pergamena riflessa intorno (il kit la taglia sulla forma).
SEGNALI = {"SG-DOMANDA": {"forma": "cerchio", "centro": (625.0, 626.0), "px_mm": 1234 / 20.0, "raggio": 10.0, "abb": M.ABB},
           "SG-CRIPTA": {"forma": "esagono", "centro": (627.0, 628.5), "px_mm": 42.1, "abb": M.ABB},
           "TX-ROSSA": {"forma": "cerchio", "centro": (627.0, 627.0), "px_mm": 1205 / 24.0, "raggio": 12.0, "abb": 3.0},
           "TX-BLU": {"forma": "cerchio", "centro": (627.0, 627.0), "px_mm": 1205 / 24.0, "raggio": 12.0, "abb": 3.0},
           "TX-RETRO": {"forma": "cerchio", "centro": (624.5, 623.5), "px_mm": 1213 / 24.0, "raggio": 12.0, "abb": 3.0}}
for _i in ("SG-01", "SG-03", "SG-04"):     # Indizio, Forte Volontà, Usato: Ø 20 mm + abbondanza 3 mm
    SEGNALI[_i] = {"forma": "quadro", "centro": (627.0, 627.0), "px_mm": 1254 / 22.0, "out_mm": (26.0, 26.0)}
for _k in range(1, 10):                     # Stati 26 × 18 mm + abbondanza 3 mm
    SEGNALI[f"ST-{_k:02d}"] = {"forma": "quadro", "centro": (627.0, 627.0), "px_mm": 1254 / 30.0, "out_mm": (30.0, 30.0)}


def segnale_png_px(g):
    """(w, h) in px a 300 ppi del png, centrato sul centro del segnalino."""
    if g["forma"] == "quadro":
        return math.ceil(g["out_mm"][0] * M.PPM), math.ceil(g["out_mm"][1] * M.PPM)
    abb = g["abb"]
    if g["forma"] == "cerchio":
        d = math.ceil(2 * (g["raggio"] + abb) * M.PPM)
        return d, d
    ra = M.R + abb / math.cos(math.radians(30))
    return math.ceil(2 * (M.W / 2 + abb) * M.PPM), math.ceil(2 * ra * M.PPM)


def compone_segnale(i, nat, fatt):
    """segnalino da grezza (centro e scala fissi, vedi SEGNALI)."""
    g = SEGNALI[i]
    w, h = segnale_png_px(g)
    k = 1 / M.PPM * g["px_mm"]
    Mx = np.array([[k, 0, g["centro"][0] - (w - 1) / 2 * k], [0, k, g["centro"][1] - (h - 1) / 2 * k]])
    out = cv2.warpAffine(nat, Mx, (w, h), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    if g["forma"] == "quadro":
        return out
    abb = g["abb"]
    cx, cy = (w - 1) / 2, (h - 1) / 2
    pieno = np.zeros((h, w), np.uint8)
    if g["forma"] == "cerchio":
        cv2.circle(pieno, (round(cx * 16), round(cy * 16)), round(g["raggio"] * M.PPM * 16), 255, -1, cv2.LINE_AA, 4)
    else:
        riempi(pieno, [poligono(cx, cy, M.R, M.PPM)])
    dentro = ndimage.distance_transform_edt(pieno > 127) > RIENTRO_MM * M.PPM
    out = estendi_fuori(out, dentro)
    fuori = np.zeros((h, w), np.uint8)
    if g["forma"] == "cerchio":
        cv2.circle(fuori, (round(cx * 16), round(cy * 16)), round((g["raggio"] + abb) * M.PPM * 16), 255, -1, cv2.LINE_AA, 4)
    else:
        riempi(fuori, [poligono(cx, cy, M.R + abb / math.cos(math.radians(30)) + 0.1, M.PPM)])
    out[fuori <= 127] = PERGAMENA
    return out


def comanda_segnali(a, ids):
    for i in ids:
        g = trova_grezza(i, a.grezze)
        if g is None:
            sys.exit(f"{i}: manca {a.grezze / (i + '.webp')} (o .png)")
        nat = apri(g)
        if nat.shape[:2] != (1254, 1254):
            print(f"  ATTENZIONE {i}: misura {nat.shape[1]}x{nat.shape[0]}, la geometria di SEGNALI e' misurata su 1254x1254", file=sys.stderr)
        rgb = compone_segnale(i, nat, (1, 1))
        kb = rifinisci(rgb, i, a.uscita, not a.senza_look)
        print(f"{i} -> {a.uscita / (i + '.png')}  {rgb.shape[1]}x{rgb.shape[0]} px  {kb:.0f} KB")


# ------------------------------------------------------------------ rifinitura (PhotoCraft, come elabora.py)
def rifinisci(rgb, i, uscita, look=True):
    """scrive uscita/<i>.png (con il look condiviso di elabora.py se look) e ritorna la sua misura in KB."""
    uscita.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="goblin_mappa_") as tmp:
        tmp = pathlib.Path(tmp)
        grezzo, png = tmp / f"{i}_comp.png", tmp / f"{i}.png"
        Image.fromarray(rgb).save(grezzo, dpi=(300, 300))
        if look:
            import elabora as E
            pc = tmp / f"{i}.pcraft"
            E.photocraft("convert", grezzo, pc)
            E.photocraft("run", pc, "--cmd", "layer.renameLayer", "--params", '{"name": "Immagine composta"}',
                         "--cmd", "layer.newAdjustmentLayer.curves", "--params", json.dumps(E.CURVE),
                         "--cmd", "layer.newAdjustmentLayer.hueSaturation", "--params", json.dumps(E.TONALITA),
                         "--out", pc, "--in-place")
            E.photocraft("convert", pc, png)
            E.senza_icc(png)
            if uscita.resolve() == E.PNG.resolve():
                E.PCRAFT.mkdir(exist_ok=True)
                shutil.move(str(pc), E.PCRAFT / f"{i}.pcraft")
        else:
            shutil.move(str(grezzo), png)
        shutil.move(str(png), uscita / f"{i}.png")
    return (uscita / f"{i}.png").stat().st_size / 1024


# ------------------------------------------------------------------ verifica dei terreni
def caratteristiche(px):
    """frazioni di pixel per famiglia di colore; px = (N, 3) RGB uint8."""
    hsv = cv2.cvtColor(px.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3).astype(np.int32)
    H, S, V = hsv[:, 0], hsv[:, 1], hsv[:, 2]
    verde = (H >= 30) & (H < 85) & (S >= 55) & (V >= 35)
    grigio = (S < 50) & (V >= 50)
    f = {"blu": (H >= 85) & (H <= 135) & (S >= 60) & (V >= 50),
         "verde": verde, "verde_scuro": verde & (V < 150),
         "caldo": ((H <= 20) | (H >= 165)) & (S >= 100) & (V >= 60),
         "legno": (H >= 8) & (H <= 28) & (S >= 60) & (S <= 230) & (V >= 30) & (V <= 210),
         "grigio_scuro": grigio & (V < 165), "grigio_chiaro": grigio & (V >= 165), "buio": V < 50}
    return {k: float(v.mean()) for k, v in f.items()}


def verifica_esagono(t, f, so):
    """(errori, avvisi) del terreno t date le frazioni f; so = soglie. Vedi SOGLIE per il significato."""
    e, av = [], []
    acquatico = t in M.ACQUATICI
    if t == "acqua" and f["blu"] < so["acqua_blu_min"]:
        e.append(f"acqua attesa ma blu solo {f['blu']:.2f} (min {so['acqua_blu_min']})")
    if t == "guado" and f["blu"] < so["guado_blu_min"]:
        e.append(f"guado (acqua con sassi) atteso ma blu solo {f['blu']:.2f} (min {so['guado_blu_min']})")
    if t == "ponte":
        if f["blu"] < so["ponte_blu_min"]:
            e.append(f"ponte (acqua con assi) atteso ma blu solo {f['blu']:.2f} (min {so['ponte_blu_min']})")
        if f["legno"] < so["ponte_legno_min"]:
            e.append(f"ponte atteso ma legno solo {f['legno']:.2f} (min {so['ponte_legno_min']})")
    if not acquatico and f["blu"] > so["blu_max_asciutto"]:
        e.append(f"acqua dipinta dove il dato dice {t} (blu {f['blu']:.2f} > {so['blu_max_asciutto']})")
    if t == "bosco" and f["verde_scuro"] < so["bosco_scuro_min"]:
        e.append(f"bosco atteso ma verde scuro solo {f['verde_scuro']:.2f} (min {so['bosco_scuro_min']})")
    if t != "bosco" and f["verde_scuro"] > so["verde_scuro_max"]:
        e.append(f"bosco dipinto dove il dato dice {t} (verde scuro {f['verde_scuro']:.2f} > {so['verde_scuro_max']})")
    if t == "rocce" and f["grigio_scuro"] < so["rocce_grigio_min"] and not (f["legno"] >= so["rocce_pietra_min"] and f["verde_scuro"] < 0.1):
        e.append(f"rocce attese ma grigio scuro solo {f['grigio_scuro']:.2f} (min {so['rocce_grigio_min']})")
    if t in ("prato", "sentiero", "mattonato", "partenza", "case") and f["grigio_scuro"] > so["grigio_scuro_max"]:
        e.append(f"rocce dipinte dove il dato dice {t} (grigio scuro {f['grigio_scuro']:.2f} > {so['grigio_scuro_max']})")
    if t == "case" and f["caldo"] + f["legno"] < so["case_caldo_min"]:
        e.append(f"case attese ma rosso/legno solo {f['caldo'] + f['legno']:.2f} (min {so['case_caldo_min']})")
    if t == "prato" and f["verde"] < so["prato_verde_min"]:
        e.append(f"prato atteso ma verde solo {f['verde']:.2f} (min {so['prato_verde_min']})")
    if t in ("sentiero", "mattonato", "pavimento") and f["verde"] > so["liberi_verde_max"]:
        av.append(f"prato dipinto dove il dato dice {t} (verde {f['verde']:.2f} > {so['liberi_verde_max']})")
    return e, av


def strato_relativo(righe, so):
    """Aggiunge a ogni riga avvisi/errori «assomiglia a un altro terreno»: prototipo = mediana delle caratteristiche di
    ogni terreno atteso nel lotto controllato; se un altro terreno è più vicino (L1) del proprio di un fattore
    relativo_rapporto, avviso (stessa categoria) o errore (categoria diversa: ostacolo/acqua/libero)."""
    gruppi = {}
    for r in righe:
        gruppi.setdefault(r["terreno"], []).append([r["f"][k] for k in CARATTERISTICHE])
    proto = {t: np.median(v, axis=0) for t, v in gruppi.items() if len(v) >= so["relativo_campioni"]}
    for r in righe:
        v = np.array([r["f"][k] for k in CARATTERISTICHE])
        if r["terreno"] not in proto:
            continue
        d_own = np.abs(v - proto[r["terreno"]]).sum()
        if d_own <= so["relativo_minimo"]:
            continue
        alt = min(((np.abs(v - p).sum(), t) for t, p in proto.items() if t != r["terreno"]), default=None)
        if alt and alt[0] < so["relativo_rapporto"] * d_own:
            msg = f"assomiglia a «{alt[1]}» (distanza {alt[0]:.2f}) più che al terreno atteso (distanza {d_own:.2f})"
            ambiguo = {r["terreno"], alt[1]} in AMBIGUI      # il colore da solo non li separa: solo avviso
            if M.CATEGORIA[alt[1]] != M.CATEGORIA[r["terreno"]] and not ambiguo:
                r["errori"].append(msg)
            else:
                r["avvisi"].append(msg)


def campiona(img, centri_px, px_mm, so):
    """caratteristiche dell'interno (esagono al raggio_campione) di ogni centro (px) dell'immagine."""
    out = []
    for cx, cy in centri_px:
        m = np.zeros(img.shape[:2], np.uint8)
        riempi(m, [poligono(cx, cy, M.R * so["raggio_campione"], px_mm)])
        out.append(caratteristiche(img[m > 127]))
    return out


# ------------------------------------------------------------------ verifica geometrica sul PDF (arte vs contorno vettoriale)
# Rende le pagine a 300 dpi e confronta con la geometria vera: per ogni lato di ogni esagono, una striscia appena DENTRO il
# contorno (0,3-1,0 mm) non deve essere vuota (pergamena o carta: arte che non arriva al contorno), e una striscia appena
# FUORI (0,5-1,2 mm; sui fiori oltre l'abbondanza) non deve contenere arte (arte che sbordava). Nata dal difetto della
# base (12/11): esagoni disegnati dal modello fino a 1,3 mm fuori posto -> doppio bordo, vuoti, spicchi nei vicini.
GAP_COLORI = ((241, 220, 174), (255, 255, 255))       # pergamena dell'arte, carta
GAP_TOL = 14                                          # distanza massima per canale (0-255) per dirsi «vuoto»
GAP_FRAZIONE = 0.40                                   # oltre questa quota di vuoto nella striscia -> ERRORE
SBORDO_FRAZIONE = 0.20                                # oltre questa quota di pixel «non vuoti» fuori -> ERRORE
SLOT_FONDO, FASCIA_FONDO = (239, 230, 207), (217, 207, 168)    # fondo degli spazi / delle fasce (gen.py base12_svg)
POS_FIORI = [(63.0, 58.0), (147.0, 58.0), (63.0, 140.0), (147.0, 140.0), (63.0, 222.0), (147.0, 222.0)]   # gen.py FIORI_POS
FASCIA12 = 5.5
PLATE_FONDO = (247, 238, 219)                         # fondo del riquadro delle istruzioni (svg.PLATE)


def render_pagine(pdf, tmp, pagine):
    import subprocess
    for n in pagine:
        subprocess.run(["pdftoppm", "-r", "300", "-png", "-f", str(n), "-l", str(n), str(pdf), str(tmp / f"p{n}")], check=True)
    out = {}
    for n in pagine:
        f = next(tmp.glob(f"p{n}-*.png"))
        out[n] = np.asarray(Image.open(f).convert("RGB"))
    return out


def striscia(img, cx, cy, ang, d0, d1, mm=None):
    """pixel (N, 3) della striscia a distanze d0..d1 mm dal centro (cx, cy) in mm di pagina lungo la normale `ang` (gradi),
    larghezza ±0,35 R lungo il lato (evita gli spigoli). Ritorna (pixel, punti mm)."""
    a = math.radians(ang)
    nx, ny = math.cos(a), math.sin(a)
    tx, ty = -ny, nx
    pts_ = [(cx + nx * d + tx * u, cy + ny * d + ty * u) for d in np.arange(d0, d1 + 1e-9, 0.1) for u in np.linspace(-0.35 * M.R, 0.35 * M.R, 9)]
    h, w = img.shape[:2]
    px = np.array([(int(round(x * PPM300)), int(round(y * PPM300))) for x, y in pts_])
    ok = (px[:, 0] >= 0) & (px[:, 0] < w) & (px[:, 1] >= 0) & (px[:, 1] < h)
    return img[px[ok, 1], px[ok, 0]], [p for p, o in zip(pts_, ok) if o]


PPM300 = 300 / 25.4


def vicino(img_px, colori, tol):
    ok = np.zeros(len(img_px), bool)
    for c in colori:
        ok |= (np.abs(img_px.astype(int) - np.array(c)).max(-1) < tol)
    return ok


def controlla_esagono(img, cx, cy, vicino_vuoto, nome, errori, abb=0.0, sbordo_colori=None, salta=lambda x, y: False):
    """vicino_vuoto(angolo) -> True se il lato confina con «vuoto» (spazio, fascia, carta) e va controllato lo sbordo;
    sbordo_colori: colori leciti fuori (spazio/fascia/carta)."""
    ap = M.W / 2
    for k in range(6):
        ang = k * 60
        px, pts_ = striscia(img, cx, cy, ang, ap - 1.0, ap - 0.3)
        keep = [not salta(x, y) for x, y in pts_]
        px = px[keep]
        if len(px):
            f = vicino(px, GAP_COLORI, GAP_TOL).mean()
            if f > GAP_FRAZIONE:
                errori.append(f"{nome} lato {k}: {f:.0%} di vuoto dentro il contorno (l'arte non arriva alla linea)")
        if vicino_vuoto(ang):
            px, pts_ = striscia(img, cx, cy, ang, ap + abb + 0.5, ap + abb + 1.2)
            keep = [not salta(x, y) for x, y in pts_]
            px = px[keep]
            if len(px):
                f = 1 - vicino(px, sbordo_colori, GAP_TOL).mean()
                if f > SBORDO_FRAZIONE:
                    errori.append(f"{nome} lato {k}: {f:.0%} di arte fuori dal contorno")


def controlla_cerchio(img, cx, cy, r, nome, errori, abb=M.ABB):
    """segnalino tondo: anello 0,3-1,0 mm dentro il bordo senza vuoti, anello oltre l'abbondanza senza arte."""
    h, w = img.shape[:2]

    def anello(d0, d1):
        pts_ = [(int(round((cx + d * math.cos(a)) * PPM300)), int(round((cy + d * math.sin(a)) * PPM300)))
                for d in np.arange(d0, d1, 0.1) for a in np.radians(np.arange(0, 360, 4))]
        pts_ = [p for p in pts_ if 0 <= p[0] < w and 0 <= p[1] < h]
        return np.array([img[y, x] for x, y in pts_])
    f = vicino(anello(r - 1.0, r - 0.3), GAP_COLORI, GAP_TOL).mean()
    if f > GAP_FRAZIONE:
        errori.append(f"{nome}: {f:.0%} di vuoto dentro il bordo")
    f = 1 - vicino(anello(r + abb + 0.5, r + abb + 1.2), ((255, 255, 255),), GAP_TOL).mean()
    if f > SBORDO_FRAZIONE:
        errori.append(f"{nome}: {f:.0%} di arte fuori dal bordo")


def verifica_pdf_mappa(pdf, fiori, terr):
    """controlla mappa_base.pdf, mappa_fiori.pdf o carta_fiori_3d.pdf; ritorna la lista degli errori."""
    import tempfile
    pdf = pathlib.Path(pdf)
    errori = []
    with tempfile.TemporaryDirectory(prefix="goblin_vpdf_") as tmp:
        tmp = pathlib.Path(tmp)
        if pdf.name == "mappa_base.pdf":
            f, L, A = FASCIA12, M.LARGO, M.ALTO
            m, ABB = L / 2, M.ABB
            larg = f + m + 2 * ABB
            ty = (297 - (A + 2 * f + 2 * ABB)) / 2 + f + ABB
            pagine = render_pagine(pdf, tmp, (1, 2))
            for n in (1, 2):
                x0 = -f - ABB if n == 1 else m - ABB
                tx = (210 - larg) / 2 - x0
                lo, hi = (-f - ABB, m + ABB) if n == 1 else (m - ABB, L + f + ABB)
                for hx, t in terr.items():
                    if t is None:
                        continue
                    gx, gy = M.F12.centro_mappa(hx)
                    if not (lo - 5 < gx < hi + 5):
                        continue

                    def vuoto(ang, hx=hx, gx=gx, gy=gy):
                        nc = (gx + M.W * math.cos(math.radians(ang)), gy + M.W * math.sin(math.radians(ang)))
                        for h2, t2 in terr.items():
                            c2 = M.F12.centro_mappa(h2)
                            if abs(c2[0] - nc[0]) < 1 and abs(c2[1] - nc[1]) < 1:
                                return t2 is None
                        return True            # fuori dalla griglia: fascia

                    salta = lambda x, y, tx=tx, lo=lo, hi=hi: not (lo + 0.5 < x - tx < hi - 0.5) or abs(x - tx - m) < 4.5
                    controlla_esagono(pagine[n], gx + tx, gy + ty, vuoto, f"base pag.{n} esagono ({hx[0]},{hx[1]})", errori,
                                      sbordo_colori=(SLOT_FONDO, FASCIA_FONDO), salta=salta)
                    # il riquadro delle istruzioni (fondo PLATE) non deve coprire l'arte dell'esagono
                    pl = np.array([(int(round((gx + tx + r * math.cos(a)) * PPM300)), int(round((gy + ty + r * math.sin(a)) * PPM300)))
                                   for r in np.arange(0, M.R - 0.8, 0.4) for a in np.radians(np.arange(0, 360, 10))])
                    ok_ = (pl[:, 0] >= 0) & (pl[:, 0] < pagine[n].shape[1]) & (pl[:, 1] >= 0) & (pl[:, 1] < pagine[n].shape[0])
                    quanti = vicino(pagine[n][pl[ok_, 1], pl[ok_, 0]], (PLATE_FONDO,), 2).sum()
                    if quanti > 6:
                        errori.append(f"base pag.{n} esagono ({hx[0]},{hx[1]}): il riquadro delle istruzioni copre l'arte ({quanti} campioni)")
        else:
            tre_d = pdf.name == "carta_fiori_3d.pdf"
            facce = sorted(fiori, key=lambda k: (k[0], k[1]))
            if tre_d:
                blocchi = [facce[i:i + 6] for i in range(0, len(facce), 6)]
                pag = {n: [(i, lato, POS_FIORI[j], False) for j, (i, lato) in enumerate(b)] for n, b in enumerate(blocchi, 1)}
            else:
                bl = [list(range(1, 7)), list(range(7, 13)), [13, 14]]
                pag = {}
                for k, b in enumerate(bl, 1):
                    for lato, n in (("A", 2 * k - 1), ("B", 2 * k)):
                        pag[n] = [(i, lato, POS_FIORI[j], lato == "B") for j, i in enumerate(b)]
            pagine = render_pagine(pdf, tmp, sorted(pag))
            for n, lista in pag.items():
                for i, lato, (x, y), speculare in lista:
                    cx = 210 - x if speculare else x
                    centri = [(cx + M.F12.centro_locale(p, 0)[0], y + M.F12.centro_locale(p, 0)[1]) for p in sorted(fiori[(i, lato)]["celle"])]
                    for p, (hx_, hy_) in zip(sorted(fiori[(i, lato)]["celle"]), centri):
                        def vuoto(ang, hx_=hx_, hy_=hy_):
                            nc = (hx_ + M.W * math.cos(math.radians(ang)), hy_ + M.W * math.sin(math.radians(ang)))
                            return not any(abs(c[0] - nc[0]) < 1 and abs(c[1] - nc[1]) < 1 for c in centri)
                        controlla_esagono(pagine[n], hx_, hy_, vuoto, f"{pdf.name} pag.{n} fiore {i}{lato} pos {p}", errori,
                                          abb=0.0 if tre_d else M.ABB, sbordo_colori=((255, 255, 255),))
            if not tre_d:       # segnalini «?» e Cripta (foglio 3, pagine 5 e 6)
                for n in (5, 6):
                    sx = (lambda x: x) if n == 5 else (lambda x: 210 - x)
                    for j in range(24):
                        controlla_cerchio(pagine[n], sx(19.5 + 28.5 * (j % 7)), 116.0 + 26.0 * (j // 7), 10.0, f"{pdf.name} pag.{n} segnaposto «?» {j + 1}", errori)
                    controlla_esagono(pagine[n], sx(147.0), 194.0, lambda ang: True, f"{pdf.name} pag.{n} Cripta", errori,
                                      abb=M.ABB, sbordo_colori=((255, 255, 255),))
    return errori


def comanda_verifica_pdf(a, fiori, terr):
    pdfs = [pathlib.Path(p) for p in a.verifica_pdf] or [QUI.parent.parent / "playtest_v7" / "mappa_base.pdf",
                                                     QUI.parent.parent / "playtest_v7" / "mappa_fiori.pdf",
                                                     QUI.parent.parent / "3d_solidcraft" / "out" / "carta_fiori_3d.pdf"]
    tot = 0
    for pdf in pdfs:
        err = verifica_pdf_mappa(pdf, fiori, terr)
        for e in err:
            print(f"ERRORE {e}")
        print(f"{'OK    ' if not err else 'ERRORE'} {pdf.name}: {len(err)} problemi di contorno")
        tot += len(err)
    return 1 if tot else 0


# ------------------------------------------------------------------ comandi
def lista_id(a, fiori):
    tutti = M.tutti_id_fiori() + [f"MB-{q}" for q in M.QUARTI] + list(SEGNALI)
    if a.id:
        ids = list(dict.fromkeys(a.id))
        for i in ids:
            if i not in tutti:
                sys.exit(f"id «{i}» sconosciuto (MF-<NN><A|B>, MB-NO|NE|SO|SE)")
        return ids
    return [i for i in tutti if trova_grezza(i, a.grezze)]


def allinea_id(i, a):
    guida = apri(a.guide / f"{i}.png")
    g = trova_grezza(i, a.grezze)
    if g is None:
        sys.exit(f"{i}: manca {a.grezze / (i + '.webp')} (o .png)")
    nat, rid, fatt = carica_grezza(g, guida)
    A, info = allinea(guida, rid, "fiore" if i.startswith("MF") else "base")
    ok = avvisa_allineamento(i, info)
    return guida, nat, rid, fatt, A, ok


def comanda_compone(a, ids, fiori, terr):
    quarti, fatti = {}, []
    for i in ids:
        print(i)
        guida, nat, rid, fatt, A, ok = allinea_id(i, a)
        img = riallinea(nat, A, fatt, (guida.shape[1], guida.shape[0]))
        if i.startswith("MB-"):
            q = i[3:]
            mio = [hx for hx, t in terr.items() if t is not None and M.quarto_di(hx) == q]
            fit = adatta_o_identita(img, [centri_base_guida(q, hx) for hx in mio], M.BASE_PX_MM, i)
            quarti[q] = (nat, A, fatt, dict(zip(mio, fit)))
            continue
        n, faccia = int(i[3:5]), i[5]
        fit = adatta_o_identita(img, centri_fiore_guida(fiori[(n, faccia)]), M.FIORE_PX_MM, i)
        rgb = compone_fiore(i, nat, A, fatt, fiori[(n, faccia)], fit)
        kb = rifinisci(rgb, i, a.uscita, not a.senza_look)
        print(f"  -> {a.uscita / (i + '.png')}  {rgb.shape[1]}x{rgb.shape[0]} px  {kb:.0f} KB")
        fatti.append(i)
    if quarti:
        mancano = [q for q in M.QUARTI if q not in quarti]
        if mancano:
            print(f"base NON composta: mancano i quarti {', '.join(mancano)}", file=sys.stderr)
        else:
            rgb = compone_base(quarti, terr)
            kb = rifinisci(rgb, "MB-BASE", a.uscita, not a.senza_look)
            print(f"MB-BASE -> {a.uscita / 'MB-BASE.png'}  {rgb.shape[1]}x{rgb.shape[0]} px  {kb:.0f} KB")
            fatti.append("MB-BASE")
    print(f"composte: {len(fatti)}")


def comanda_verifica(a, ids, fiori, terr):
    so = dict(SOGLIE)
    for s in a.soglia or []:
        k, _, v = s.partition("=")
        if k not in so:
            sys.exit(f"soglia «{k}» sconosciuta ({', '.join(so)})")
        so[k] = float(v)
    righe = []
    for i in ids:
        print(i)
        guida, nat, rid, fatt, A, ok = allinea_id(i, a)
        img = riallinea(nat, A, fatt, (guida.shape[1], guida.shape[0]))
        if i.startswith("MF-"):
            f = fiori[(int(i[3:5]), i[5])]
            celle = M.celle_fiore(f)
            sel = [(f"pos {p}", t, cx, cy) for p, t, cx, cy in celle]
            px_mm = M.FIORE_PX_MM
        else:
            q = i[3:]
            x0, y0 = M.origine_quarto(q)
            sel = []
            for h, t in sorted(terr.items(), key=lambda kv: (kv[0][1], kv[0][0])):
                if t and M.quarto_di(h) == q:
                    cx, cy = M.F12.centro_mappa(h)
                    sel.append((f"({h[0]},{h[1]})", t, (cx - x0) * M.BASE_PX_MM, (cy - y0) * M.BASE_PX_MM))
            px_mm = M.BASE_PX_MM
        car = campiona(img, [(cx, cy) for _, _, cx, cy in sel], px_mm, so)
        for (nome, t, _, _), f in zip(sel, car):
            e, av = verifica_esagono(t, f, so)
            righe.append({"id": i, "esagono": nome, "terreno": t, "f": f, "errori": e, "avvisi": av, "allineato": ok})
    strato_relativo(righe, so)
    ne = na = 0
    for r in righe:
        for m in r["errori"]:
            print(f"ERRORE {r['id']} {r['esagono']} [{r['terreno']}]: {m}")
        for m in r["avvisi"]:
            print(f"ATTENZIONE {r['id']} {r['esagono']} [{r['terreno']}]: {m}")
        ne += bool(r["errori"])
        na += bool(r["avvisi"]) and not r["errori"]
    print(f"verifica: {len(righe)} esagoni in {len(ids)} immagini, {ne} con errore, {na} con avviso, "
          f"{sum(not r['allineato'] for r in righe)} in immagini con allineamento dubbio")
    if a.report:
        with open(a.report, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["id", "esagono", "terreno", *CARATTERISTICHE, "errori", "avvisi"])
            for r in righe:
                w.writerow([r["id"], r["esagono"], r["terreno"], *(f"{r['f'][k]:.3f}" for k in CARATTERISTICHE),
                            " | ".join(r["errori"]), " | ".join(r["avvisi"])])
        print(f"report: {a.report}")
    return 1 if ne else 0


def main():
    ap = argparse.ArgumentParser(description="grezze/MF-*/MB-* -> allineamento, composizione a 300 ppi, verifica dei terreni")
    ap.add_argument("id", nargs="*", help="MF-<NN><A|B>, MB-NO|NE|SO|SE (default: tutto ciò che c'è in grezze/)")
    ap.add_argument("--verifica", action="store_true", help="controlla i terreni invece di comporre")
    ap.add_argument("--verifica-pdf", nargs="*", metavar="PDF", help="controlla il contorno dell'arte sui PDF (default: mappa_base, mappa_fiori, "
                    "carta_fiori_3d): vuoti dentro e arte fuori dalla linea vettoriale, a 300 dpi")
    ap.add_argument("--report", help="con --verifica: CSV con le caratteristiche di ogni esagono")
    ap.add_argument("--soglia", action="append", metavar="NOME=VALORE", help="cambia una soglia (vedi SOGLIE)")
    ap.add_argument("--grezze", type=pathlib.Path, default=M.GREZZE)
    ap.add_argument("--guide", type=pathlib.Path, default=M.GUIDE)
    ap.add_argument("--uscita", type=pathlib.Path, default=M.PNG)
    ap.add_argument("--senza-look", action="store_true", help="salta le curve di elabora.py (PhotoCraft)")
    a = ap.parse_args()
    fiori, base, _, partenze = M.dati()
    terr = M.terreno_base(base, partenze)
    if a.verifica_pdf is not None:
        sys.exit(comanda_verifica_pdf(a, fiori, terr))
    ids = lista_id(a, fiori)
    if not ids:
        sys.exit(f"nessuna grezza MF-*/MB-*/SG-* in {a.grezze}")
    segnali = [i for i in ids if i in SEGNALI]
    ids = [i for i in ids if i not in SEGNALI]
    if segnali and not a.verifica:
        comanda_segnali(a, segnali)
        if not ids:
            return
    if not ids:
        return
    sys.exit(comanda_verifica(a, ids, fiori, terr) if a.verifica else comanda_compone(a, ids, fiori, terr))


if __name__ == "__main__":
    main()
