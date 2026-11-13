#!/usr/bin/env python3
"""Render 3D con le texture vere della carta (13/11, Daniele: «fai le texture nei render 3D»). Solo SolidCraft.

Uso (dalla radice del repo, dopo genera_3d_solidcraft.py e la build del kit A4):
    python3 v7/stampa/3d_solidcraft/render_3d.py
Scrive in out/: render_montata.png, render_esplosa.png, render_plancia.png, render_segnalini.png, piatto_segnalini.png.

Come funziona: costruisce la scena con i pezzi del generatore (stesse classi e stessi parametri di
genera_3d_solidcraft.py), poi dà a ogni corpo una texture «base color» proiettata dall'alto (render.surface.import, frame in
mm del mondo) e fa il render CPU (solidcraft-cli render). La texture di un corpo è un'immagine grande quanto il suo
ingombro: colore del filamento, con sopra l'arte della carta esattamente dove sta la carta:
- adesivi di segnalini, tessere, Stati, Cripta e rotelle: ritagliati da playtest_v7/segnalini_3d.pdf (300 dpi) sulla loro
  linea di taglio (letta dal PDF, come --verifica-adesivi), centrati sulla faccia di sopra (liscia);
- facce dei fiori: out/carta_fiori_3d.pdf ritagliata sulla linea di taglio, sopra il fiore, girata come nel preset;
- cornice della base: playtest_v7/carta_base_3d.pdf, foglio del quarto, posata con la traslazione di carta_base_3d.py;
- plancia eroe: playtest_v7/plance_eroe.pdf, foglio 1.
La carta si posa a faccia in su: in alto nell'immagine = +y nel mondo, nessuno specchio. Proiezione dall'alto: sui fianchi
dei pezzi resta il colore del filamento.
"""
import ast
import hashlib
import json
import math
import csv
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Polygon

QUI = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(QUI, '..', 'playtest_v7')
GEN = os.path.join(QUI, '..', 'sorgenti', 'componenti_gen')
sys.dont_write_bytecode = True
sys.path.insert(0, QUI)
sys.path.insert(0, GEN)
import genera_3d_solidcraft as G  # noqa: E402
import carta_base_3d as CB  # noqa: E402
import carta_fiori_3d as CF  # noqa: E402
import fiori12 as F12  # noqa: E402

P, OUT = G.P, G.OUT
DPI = 300
PX = DPI / 25.4                                  # px per mm
BUDGET_PX = 6.0e6                               # pixel di texture per scena (tetto di memoria del ray tracing)
PLA = (214, 204, 186)                            # filamento dei segnalini (crema)
PLA_VASSOIO = (92, 72, 52)                       # vassoio
PLA_FIORE = (120, 104, 84)                       # fiori
PRESET = 'Strettoie'                             # come la guida di montaggio


# ---- raster e ritagli --------------------------------------------------------------------------------------------
_RASTER = {}


def raster(pdf, n, dpi, tmp):
    k = (pdf, n, dpi)
    if k not in _RASTER:
        base = os.path.join(tmp, f'r{len(_RASTER)}')
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(n), '-l', str(n), '-png', '-singlefile', pdf, base], check=True)
        _RASTER[k] = Image.open(base + '.png').convert('RGB')
    return _RASTER[k]


def maschera(size, anelli_px):
    """maschera (L, 4× sovracampionata) del primo anello pieno meno gli altri (fori)."""
    s = 4
    m = Image.new('L', (size[0] * s, size[1] * s), 0)
    d = ImageDraw.Draw(m)
    for i, a in enumerate(anelli_px):
        d.polygon([(x * s, y * s) for x, y in a], fill=255 if i == 0 else 0)
    return m.resize(size, Image.LANCZOS)


def ritaglio(img, dpi, anelli_mm, centro_mm, lato_mm):
    """RGBA quadrato di lato_mm centrato in centro_mm (mm di pagina, y in giù), opaco solo dentro gli anelli."""
    k = dpi / 25.4
    x0, y0 = centro_mm[0] - lato_mm / 2, centro_mm[1] - lato_mm / 2
    n = int(round(lato_mm * k))
    box = (int(round(x0 * k)), int(round(y0 * k)))
    c = Image.new('RGB', (n, n), (255, 255, 255))
    c.paste(img.crop((box[0], box[1], box[0] + n, box[1] + n)))
    m = maschera((n, n), [[((x - x0) * k, (y - y0) * k) for x, y in a] for a in anelli_mm])
    c.putalpha(m)
    return c


def adesivi(tmp):
    """{tipo: [(RGBA, lato_mm)]} dagli adesivi di segnalini_3d.pdf, in ordine di disegno (= ordine dei CSV)."""
    pdf = os.path.join(KIT, 'segnalini_3d.pdf')
    out = {}

    def prendi(n):
        img = raster(pdf, n, DPI, tmp)
        res = []
        for anelli in G.anelli_pdf(pdf, n, tmp):
            pol = sorted((Polygon(a) for a in anelli), key=lambda p: -p.area)
            if len(pol) > 1:                        # rotella: centro sul foro del mozzo, lato = corona
                c = pol[1].centroid
                lato = 2 * max(math.dist((c.x, c.y), q) for q in pol[0].exterior.coords) + 0.4
            else:
                b = pol[0].bounds
                c = Polygon(pol[0]).envelope.centroid
                lato = max(b[2] - b[0], b[3] - b[1]) + 0.4
            res.append((ritaglio(img, DPI, [list(pol[0].exterior.coords)] + [list(p.exterior.coords) for p in pol[1:]], (c.x, c.y), lato), lato,
                        len(pol[0].exterior.coords)))
        return res
    # segnalini_3d.pdf a 9 fogli, doppia faccia: 1 fronti 36 + Cripta · 2 dorsi 36 + Cripta (fondo) · 3 Stati sopra · 4 Stati fondo ·
    # 5 segnalini sopra · 6 segnalini fondo · 7-9 rotelle. Le texture si incollano sulla faccia di sopra: fogli «sopra».
    p1, p2 = prendi(1), prendi(2)
    out['fronte'], out['cripta'] = p1[:36], p1[36:]
    out['dorso'] = p2[:36]
    out['stato'], out['tondo'] = prendi(3), prendi(5)
    out['rotella'] = prendi(7) + prendi(8) + prendi(9)
    assert [len(out[k]) for k in ('fronte', 'cripta', 'dorso', 'stato', 'tondo', 'rotella')] == [36, 1, 36, 31, 40, 27], \
        {k: len(v) for k, v in out.items()}
    return out


# ---- texture di un corpo -----------------------------------------------------------------------------------------
class Tex:
    """texture di un corpo: immagine di lato_mm × lato_mm centrata in (cx, cy) a quota z, girata di ang gradi (antiorario,
    mondo); fondo del colore del filamento, arte incollata al centro (o in pezzi con offset in mm)."""

    def __init__(self, cx, cy, z, lato, fondo, ang=0.0, alto=None):
        self.cx, self.cy, self.z, self.w, self.h, self.ang = cx, cy, z, lato, alto or lato, ang
        self.img = Image.new('RGB', (int(round(self.w * PX)), int(round(self.h * PX))), fondo)

    def incolla(self, rgba, lato_mm, dx=0.0, dy=0.0):
        n = int(round(lato_mm * PX))
        a = rgba.resize((n, n), Image.LANCZOS) if rgba.size != (n, n) else rgba
        x = int(round((self.w / 2 + dx - lato_mm / 2) * PX))
        y = int(round((self.h / 2 - dy - lato_mm / 2) * PX))
        self.img.paste(a, (x, y), a)

    def frame(self):
        c, s = math.cos(math.radians(self.ang)), math.sin(math.radians(self.ang))
        u = (self.w * c, self.w * s, 0.0)
        v = (self.h * s, -self.h * c, 0.0)                  # verso il basso dell'immagine = -y girato
        o = (self.cx - u[0] / 2 - v[0] / 2, self.cy - u[1] / 2 - v[1] / 2, self.z)
        return {'origin': list(o), 'u': list(u), 'v': list(v)}


# ---- scena ------------------------------------------------------------------------------------------------------------
class Scena:
    def __init__(self, tmp):
        self.tmp, self.cmd, self.tex, self.colori, self.fatti = tmp, G.params_cmds(), {}, {}, set()

    def modello(self, pz, base):
        """crea (una volta) il corpo `base` del pezzo pz, fuori scena (z = -500)."""
        if base not in self.fatti:
            self.cmd += pz.commands(base) + [{'command': 'solid.move', 'params': {'bodies': [base], 'translate': [0, 0, -500]}}]
            self.fatti.add(base)

    def metti(self, pz, base, nome, x, y, z=0.0, ang=0.0, capovolto=False):
        """copia del corpo base in (x, y, z), girata di ang gradi; capovolto: fondo in su (tessera coperta)."""
        self.modello(pz, base)
        self.cmd.append({'command': 'solid.move', 'params': {'bodies': [base], 'copy': True, 'translate': [0, 0, 0]}})
        tmpn = f'{base} (2)'
        if capovolto:
            self.cmd.append({'command': 'solid.move', 'params': {'bodies': [tmpn], 'axis': [1, 0, 0], 'angle': '180 deg',
                                                                  'origin': [0, 0, -500]}})
            self.cmd.append({'command': 'solid.move', 'params': {'bodies': [tmpn], 'translate': [0, 0, 500 + G.ev(pz.spessore)]}})
        else:
            self.cmd.append({'command': 'solid.move', 'params': {'bodies': [tmpn], 'translate': [0, 0, 500]}})
        if ang:
            self.cmd.append({'command': 'solid.move', 'params': {'bodies': [tmpn], 'axis': [0, 0, 1], 'angle': f'{ang} deg'}})
        self.cmd += [{'command': 'solid.move', 'params': {'bodies': [tmpn], 'translate': [x, y, z]}},
                     {'command': 'body.rename', 'params': {'body': tmpn, 'name': nome}}]

    def comandi(self, cmds):
        self.cmd += cmds

    def via_modelli(self):
        """toglie i corpi modello (una volta sola: la stessa scena si può rendere da più punti di vista)."""
        if self.fatti:
            self.cmd += [{'command': 'solid.remove', 'params': {'bodies': sorted(self.fatti)}}]
            self.fatti = set()

    def render(self, png, camera, w=1600, h=1200):
        self.via_modelli()
        sc = os.path.join(self.tmp, 'scena.solidcraft')
        jo = os.path.join(self.tmp, 'scena.out.json')
        sp = os.path.join(self.tmp, 'scena.json')
        json.dump({'commands': self.cmd + [{'command': 'render.scene', 'params': {}}]}, open(sp, 'w'))
        r = subprocess.run(['solidcraft-cli', 'run', sp, '--save', sc, '--results', '--quiet', '--json-out', jo], capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-2000:] + r.stderr[-2000:])
        corpi = {b['name']: b['ordinal'] for b in json.load(open(jo))[-1]['bodies']}
        # limiti di SolidCraft: al massimo 32 immagini diverse, 1024 × 1024 l'una, e un tetto di memoria del ray tracing
        # (con 24 texture da ~1024² il render della mappa viene rifiutato): stessi byte = stesso file, lato <= 1024 px, in
        # tutto al massimo BUDGET_PX pixel (si riducono tutte in proporzione; il frame in mm non cambia)
        imp, uniche, per_hash = [], {}, {}
        cart = tempfile.mkdtemp(prefix='tex', dir=self.tmp)
        for nome, t in self.tex.items():
            dig = hashlib.sha1(repr(t.img.size).encode() + t.img.tobytes()).digest()
            per_hash.setdefault(dig, (os.path.join(cart, f'texture{len(per_hash) + 1}.png'), t.img))
            uniche[nome] = per_hash[dig][0]
        assert len(per_hash) <= 32, f'{len(per_hash)} texture diverse (massimo 32)'
        fatt = [min(1.0, 1024 / max(img.size)) for _, img in per_hash.values()]
        tot = sum(img.size[0] * img.size[1] * f * f for (_, img), f in zip(per_hash.values(), fatt))
        g = min(1.0, math.sqrt(BUDGET_PX / tot))
        for (p, img), f in zip(per_hash.values(), fatt):
            f *= g
            (img.resize((max(1, int(img.size[0] * f)), max(1, int(img.size[1] * f))), Image.LANCZOS) if f < 1 else img).save(p)
        for nome, t in self.tex.items():
            p = uniche[nome]
            imp.append({'command': 'render.surface.import', 'params': {
                'name': 'foto', 'body_index': corpi[nome], 'body_name': nome, 'frame': t.frame(), 'maps': {'base_color_srgb': {'path': p}},
                'provenance': {'author': 'Il Tesoro del Goblin', 'source': 'kit playtest v7', 'license': 'progetto'}}})
        imp[0]['params']['set'] = {'job': {'method': 'cpu_raytrace'}, 'width': w, 'height': h, 'camera': camera, 'background': [236, 240, 245]}
        col = [{'command': 'appearance.assign', 'params': {'bodies': [n], 'color': '#%02x%02x%02x' % c}} for n, c in self.colori.items()]
        sp2 = os.path.join(self.tmp, 'tex.json')
        sc2 = os.path.join(self.tmp, 'scena_tex.solidcraft')
        json.dump({'commands': col + imp}, open(sp2, 'w'))
        r = subprocess.run(['solidcraft-cli', 'run', sp2, '--in', sc, '--save', sc2, '--quiet'], capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-2000:] + r.stderr[-2000:])
        r = subprocess.run(['solidcraft-cli', 'render', sc2, '--out', png, '--setup', 'foto', '--overwrite', '--timeout', '1200', '--exposure', '0.6',
                            '--legacy-memory-admission'],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-2000:] + r.stderr[-2000:])
        print('RENDER', os.path.basename(png), len(imp), 'texture')


# ---- pezzi con la loro arte ---------------------------------------------------------------------------------------
TESSERA, TONDO, STATO = G.Tondo('tessera_esplorazione', 'tessera_d'), G.Tondo('segnalino_tondo', 'gettone_d'), G.Stato()
CRIPTA = G.Cripta()
H_SEG = P['segnalino_spessore']


def segnalino(sc, pz, base, nome, art, x, y, z=0.0, ang=0.0, capovolto=False):
    """pezzo piatto con l'adesivo `art` (RGBA, lato) sopra (o sul fondo, se capovolto)."""
    sc.metti(pz, base, nome, x, y, z, ang, capovolto)
    b = pz.forma(0.0).bounds
    lato = max(b[2] - b[0], b[3] - b[1]) + 1.0
    t = Tex(x, y, z + H_SEG, lato, PLA, ang)
    t.incolla(art[0], art[1])
    sc.tex[nome] = t


def cripta(sc, art, x, y, z=0.0):
    segnalino(sc, CRIPTA, 'm_cripta', 'cripta', art, x, y, z)


ROT_NOMI = ['PV', 'Danni', 'ATT', 'MOV', 'AR', 'PL']
FIN = dict((n, f) for n, f, _ in G.ROTELLE_3D)


def rotella(sc, nome_rot, nome, art, x, y, z, ang=0.0, rivetto=True):
    """rotella 3D sulla plancia (z = sopra della plancia) con l'adesivo; rivetto: maschio sotto la plancia, femmina girata
    con la manica sulla plancia e la testa sopra la rotella (neri come in Unmatched)."""
    pz = G.Rotella(FIN['rotella_' + nome_rot])
    sc.metti(pz, 'm_' + pz.nome, nome, x, y, z, ang)
    t = Tex(x, y, z + P['rotella_spessore'], P['rotella_d'] + 1.0, PLA, ang)
    t.incolla(art[0], art[1])
    sc.tex[nome] = t
    if rivetto:
        sc.metti(G.RivettoMaschio(), 'm_rivetto_maschio', nome + '_maschio', x, y, z - P['carta_plancia'] - P['testa_h'])
        sc.metti(G.RivettoFemmina(), 'm_rivetto_femmina', nome + '_femmina', x, y, z, capovolto=True)
        sc.colori[nome + '_maschio'] = sc.colori[nome + '_femmina'] = (38, 38, 40)


# ---- mappa: vassoio con la carta della base e fiori del preset ---------------------------------------------------
def mappa(sc, tmp, apri=0.0, alza=0.0):
    """vassoio (4 quarti, spostati di apri mm dal centro) con la cornice di carta e i 14 fiori del preset (alzati di alza)."""
    metr = G.text_metrics(tmp, [str(i) for i in range(1, len(G.M.SPAZI) + 1)])
    pdf = os.path.join(KIT, 'carta_base_3d.pdf')
    L, A = F12.LARGO, F12.ALTO
    k = 200 / 25.4
    for n, q in enumerate(G.QUARTI, 1):
        qt = G.Quarto(q, metr)
        dx = apri * (1 if 'E' in q else -1)
        dy = apri * (1 if 'N' in q else -1)
        sc.comandi(qt.commands(solo_solido=True) + [{'command': 'solid.move', 'params': {'bodies': [qt.nome], 'translate': [dx, dy, 0]}}])
        _, _, (tx, ty) = CB.pagina(q, tmp)
        x0, y0, x1, y1 = G.quarter_shape(q, P).buffer(6).bounds
        img = raster(pdf, n, 200, tmp)
        crop = img.crop(tuple(int(round(v * k)) for v in (x0 + L / 2 + tx, A / 2 - y1 + ty, x1 + L / 2 + tx, A / 2 - y0 + ty)))
        pk = G.paper_pocket(q, P)
        anelli = [[((x - x0) * k, (y1 - y) * k) for x, y in pk.exterior.coords]] + [[((x - x0) * k, (y1 - y) * k) for x, y in r.coords] for r in pk.interiors]
        m = maschera(crop.size, anelli)
        t = Tex((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, G.ev('fondo + alloggio_prof'), x1 - x0, PLA_VASSOIO, alto=y1 - y0)
        t.img = t.img.resize(crop.size)
        t.img.paste(crop, (0, 0), m)
        sc.tex[qt.nome] = t
    # fiori del preset
    fiori, _, _, _, preset = F12.leggi(CB.DATI)
    facce = sorted(fiori, key=lambda f: (f[0], f[1]))
    pdf = os.path.join(OUT, 'carta_fiori_3d.pdf')
    rientro = P['gioco_fiore'] + P['margine_adesivo']
    fi = G.Fiore()
    for s, (i, lato, fr) in sorted(preset[PRESET]['righe'].items()):
        j = facce.index((i, lato))
        pag, slot = j // len(CF.POSTI) + 1, j % len(CF.POSTI)
        px, py = CF.POSTI[slot]
        taglio = CF.linea_taglio(px, py, rientro)
        lato_mm = 2 * max(math.dist((px, py), c) for c in taglio.exterior.coords) + 0.4
        art = ritaglio(raster(pdf, pag, DPI, tmp), DPI, [list(taglio.exterior.coords)], (px, py), lato_mm)
        x, y = G.xy(G.centre_u(G.M.SPAZI[s]), P)
        q = G.quarter_of(G.M.SPAZI[s])
        x += apri * (1 if 'E' in q else -1)
        y += apri * (1 if 'N' in q else -1)
        z = P['fondo'] + alza
        nome = f'fiore_{s}'
        sc.metti(fi, 'm_fiore', nome, x, y, z)
        t = Tex(x, y, z + P['fiore_spessore'], lato_mm + 2, PLA_FIORE, 60 * (fr - 1))
        t.incolla(art, lato_mm)
        sc.tex[nome] = t
    return preset[PRESET]['righe']


def centro(s, apri=0.0):
    x, y = G.xy(G.centre_u(s), P)
    q = G.quarter_of(s)
    return x + apri * (1 if 'E' in q else -1), y + apri * (1 if 'N' in q else -1)


def render_mappa(ad, tmp):
    # montata: vassoio, fiori, 4 tessere coperte (dorso in su), 1 tessera scoperta e la Cripta sui fiori
    sc = Scena(tmp)
    mappa(sc, tmp)
    zf = P['fondo'] + P['fiore_spessore']
    celle = [G.M.anello(3, 2), G.M.anello(6, 4), G.M.anello(9, 0), G.M.anello(12, 3), G.M.anello(5, 5)]
    for k, h in enumerate(celle[:4]):
        segnalino(sc, TESSERA, 'm_tessera', f'tessera_{k}', ad['dorso'][k], *centro(h), zf, capovolto=True)
    segnalino(sc, TESSERA, 'm_tessera', 'tessera_su', ad['fronte'][0], *centro(celle[4]), zf)
    cripta(sc, ad['cripta'][0], *centro(G.M.anello(8, 1)), zf)
    cam = {'target': [0, -10, 0], 'yaw': -0.7853981633974483, 'pitch': 0.75, 'distance': 470, 'fov': 0.0}
    sc.render(os.path.join(OUT, 'render_montata.png'), cam)
    # dall'alto (nord in alto, come la guida di montaggio): per controllare preset, rotazioni e allineamento della carta
    sc.render(os.path.join(OUT, 'render_montata_alto.png'), {'target': [0, 0, 0], 'yaw': 0.0, 'pitch': 1.5707, 'distance': 360, 'fov': 0.0},
              1400, 1240)
    # esplosa: quarti aperti di 25 mm, fiori alzati di 30 mm
    sc = Scena(tmp)
    mappa(sc, tmp, apri=25.0, alza=30.0)
    sc.render(os.path.join(OUT, 'render_esplosa.png'), dict(cam, target=[0, -10, 10], distance=540))


def celle_plancia():
    """CELLE della plancia eroe da gen.py (centro della rotella = cella + (40, 29), mm della plancia, y in giù)."""
    src = open(os.path.join(GEN, 'gen.py'), encoding='utf-8').read()
    nodo = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'CELLE')
    return ast.literal_eval(nodo.value)


def render_plancia(ad, tmp):
    """plancia eroe 1 (carta da carta_plancia, foro Ø 4) con le 6 rotelle 3D e i rivetti (maschio sotto, femmina sopra); valori di partenza
    (PV 5, Danni 0, ATT 1, MOV 1, AR 9, PL 0: solo MOV non è in alto, indice 2 di 10)."""
    sc = Scena(tmp)
    W, H, z0 = 280.0, 194.0, P['testa_h']
    k = 300 / 25.4
    img = raster(os.path.join(KIT, 'plance_eroe.pdf'), 1, 300, tmp)
    for i in range(2):                   # la plancia in 2 × 2 pezzi: ogni texture al massimo 1024 px (limite di SolidCraft)
        for j in range(2):
            x0, y0 = -W / 2 + i * W / 2, H / 2 - j * H / 2           # angolo in alto a sinistra del pezzo (mondo)
            nome = f'plancia_{i}{j}'
            sc.comandi([{'command': 'sketch.create', 'params': {'plane': 'XY', 'offset': 'testa_h', 'name': nome}},
                        {'command': 'sketch.rectangle.two_point', 'params': {'p0': [f'{x0} + 0*testa_h', f'{y0 - H / 2} + 0*testa_h'],
                                                                             'p1': [f'{x0 + W / 2} + 0*testa_h', f'{y0} + 0*testa_h']}},
                        {'command': 'sketch.finish', 'params': {}},
                        {'command': 'solid.extrude', 'params': {'distance': 'carta_plancia', 'operation': 'new', 'name': nome, 'body_name': nome}}])
            t = Tex(x0 + W / 4, y0 - H / 4, z0 + P['carta_plancia'], W / 2, (255, 255, 255), alto=H / 2)
            px, py = 8.5 + i * W / 2, 8.0 + j * H / 2                 # stesso angolo sul foglio (plancia a translate(8.5, 8))
            t.img = img.crop(tuple(int(round(v * k)) for v in (px, py, px + W / 2, py + H / 2)))
            sc.tex[nome] = t
    celle = celle_plancia()
    chiavi = ['PV', 'DANNI', 'ATT', 'MOV', 'AR', 'PL']
    partenza = {'MOV': -2 * 360 / 10}             # MOV 1 = valore 3 di 10 (da -1): tacca girata in senso orario
    for i, (ch, nm) in enumerate(zip(chiavi, ROT_NOMI)):
        cx, cy = celle[ch][0] + 40, celle[ch][1] + 29
        rotella(sc, nm, f'rotella_{nm}', ad['rotella'][i], cx - W / 2, H / 2 - cy, z0 + P['carta_plancia'], partenza.get(ch, 0.0))
    sc.render(os.path.join(OUT, 'render_plancia.png'), {'target': [0, -5, 0], 'yaw': -0.35, 'pitch': 0.95, 'distance': 340, 'fov': 0.0})


def render_segnalini(ad, tmp):
    """il set dei segnalini 3D: tessere (rosse, blu, una coperta), Stati (uno orizzontale), Indizio, Forte Volontà,
    Usato, Cripta e una rotella dello scontro col rivetto."""
    sc = Scena(tmp)
    for k, i in enumerate([0, 1, 25, 26]):
        segnalino(sc, TESSERA, 'm_tessera', f'tessera_{k}', ad['fronte'][i], -60 + 30 * k, 40)
    segnalino(sc, TESSERA, 'm_tessera', 'tessera_coperta', ad['dorso'][0], 60, 40, capovolto=True)
    stati = [0, 4, 9, 13, 17, 23]                   # tipi diversi (ordine di stati.csv)
    for k, i in enumerate(stati):
        ang = 90.0 if k == 1 else 0.0
        segnalino(sc, STATO, 'm_stato', f'stato_{k}', ad['stato'][i], -66 + 30 * k, 6, ang=ang)
    for k, i in enumerate([0, 16, 20]):              # Indizio, Forte Volontà, Usato
        segnalino(sc, TONDO, 'm_tondo', f'tondo_{k}', ad['tondo'][i], -66 + 26 * k, -26)
    cripta(sc, ad['cripta'][0], 16, -26)
    rotella(sc, 'scontro', 'rotella_scontro', ad['rotella'][24], 70, -36, P['testa_h'] + P['carta_plancia'])
    sc.render(os.path.join(OUT, 'render_segnalini.png'), {'target': [5, 2, 0], 'yaw': -0.5, 'pitch': 0.8, 'distance': 200, 'fov': 0.0})


def render_piatto(ad, tmp):
    """piatto 1 di segnalini.3mf (disposizione di genera_3d_solidcraft.disponi), ogni pezzo col suo adesivo (una sola
    immagine per tipo: le copie dello stesso Stato hanno la stessa arte, e SolidCraft tiene al massimo 32 texture)."""
    ogg = [t for t in G.oggetti_3mf() if G.file_3mf(t[0]) == 'segnalini.3mf']
    mesh = {s: G.leggi_mesh(s) for s in dict.fromkeys(s for _, s, _ in ogg)}
    piatto = G.disponi(ogg, mesh, 5.0)[0]
    stati, i = [], 0
    for r in csv.DictReader(open(os.path.join(G.DATI, 'stati.csv'), encoding='utf-8')):
        stati += [ad['stato'][i]] * int(r['copie'])
        i += int(r['copie'])
    pz = {'tessera_stato': (STATO, 'm_stato', stati), 'segnalino_indizio': (TONDO, 'm_tondo', [ad['tondo'][0]] * 16),
          'segnalino_forte_volonta': (TONDO, 'm_tondo', [ad['tondo'][16]] * 4), 'segnalino_usato': (TONDO, 'm_tondo', [ad['tondo'][20]] * 20)}
    sc = Scena(tmp)
    n = {}
    for o, x, y in piatto:
        k = n[o] = n.get(o, -1) + 1
        if o == 'segnalino_cripta':
            cripta(sc, ad['cripta'][0], x, y)
            continue
        p, base, arte = pz[o]
        segnalino(sc, p, base, f'{o}_{k}', arte[k], x, y)
    sc.render(os.path.join(OUT, 'piatto_segnalini.png'), {'target': [0, 0, 0], 'yaw': 0.0, 'pitch': 1.15, 'distance': 330, 'fov': 0.0}, 1400, 1100)


def main():
    tmp = tempfile.mkdtemp(prefix='render3d-')
    try:
        ad = adesivi(tmp)
        quali = sys.argv[1:] or ['segnalini', 'piatto', 'plancia', 'mappa']
        for q in quali:
            {'segnalini': render_segnalini, 'piatto': render_piatto, 'plancia': render_plancia, 'mappa': render_mappa}[q](ad, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('RENDER OK')


if __name__ == '__main__':
    main()
