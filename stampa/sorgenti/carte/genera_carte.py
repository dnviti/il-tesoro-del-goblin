#!/usr/bin/env python3
"""Carte del playtest «Il Tesoro del Goblin»: unione dati CSV -> DesignCraft.

Equivale a un Data Merge: legge i CSV in ../dati, scrive per ogni PDF uno script
di comandi DesignCraft (carte_*.dcs), lo esegue con `designcraft-cli script`,
salva il progetto modificabile (carte_*.designcraft) e il PDF in ../../playtest_v5.

Formato: carta 63 x 88 mm rifilata, OGNI carta con la sua abbondanza (bleed) su tutti e 4 i lati: fondo/cornice colorati
si estendono oltre il rifilo di 2,5 mm (A4, cella 68 x 93 mm) o 3 mm (A3, cella 69 x 94 mm). Le celle si toccano ma non si
sovrappongono. A4: 3 x 3 = 9 carte, blocco 204 x 279 mm centrato (rifilo esterno a >= 5,5 mm dal bordo); l'abbondanza
esterna può cadere nella zona non stampabile (è solo colore in più). Segni di taglio: tacche d'angolo sul margine esterno
del foglio dove c'è posto, più un filetto bianco sottilissimo a ogni angolo di rifilo dentro l'abbondanza (si ritaglia
sul bordo dell'abbondanza e poi si centra la carta nella dima 63 x 88 mm).
Ordine delle pagine per il fronte-retro automatico: F1, R1, F2, R2, ...; i retro sono specchiati sul lato lungo
(rilegatura sul lato lungo): la carta in colonna c sul fronte ha il retro in colonna NC - 1 - c.

Formato A3 (`--formato A3`): 16 carte per foglio A3 verticale (4 x 4), blocco 276 x 376 mm centrato, abbondanza 3 mm,
stesse regole; PDF in ../../playtest_v5_A3 e progetti in ./A3. Senza opzione: A4.

Uso: python3 genera_carte.py [--solo NOME] [--formato A4|A3]   (richiede designcraft-cli)
"""
import csv
import json
import pathlib
import subprocess
import sys
import tempfile

QUI = pathlib.Path(__file__).resolve().parent
DATI = QUI.parent / "dati"
FORMATO = sys.argv[sys.argv.index("--formato") + 1].upper() if "--formato" in sys.argv else "A4"
if FORMATO not in ("A4", "A3"):
    sys.exit("--formato: A4 o A3")
PDF_DIR = QUI.parent.parent / ("playtest_v5" if FORMATO == "A4" else "playtest_v5_A3")
DC_DIR = QUI if FORMATO == "A4" else QUI / "A3"

MM = 72 / 25.4
CW, CH = 63 * MM, 88 * MM                     # carta (pt)
if FORMATO == "A4":
    PW, PH = 595.276, 841.89                   # A4
    NC, NR = 3, 3
else:
    PW, PH = 841.89, 1190.551                  # A3 (297 x 420 mm)
    NC, NR = 4, 4
PER_FOGLIO = NC * NR
B = (2.5 if FORMATO == "A4" else 3.0) * MM     # abbondanza per lato (pt)
CELLA_W, CELLA_H = CW + 2 * B, CH + 2 * B      # cella = carta + abbondanza; le celle vicine si toccano
# Griglia NC x NR di celle: A4 3 x 3 = 204 x 279 mm (margini 3 / 9 mm), A3 4 x 4 = 276 x 376 mm (margini 10,5 / 22 mm).
X0, Y0 = (PW - NC * CELLA_W) / 2, (PH - NR * CELLA_H) / 2   # angolo del blocco (bordo esterno dell'abbondanza)
SAFE = 9.0                                     # bordo colorato: tutto il testo sta oltre 3 mm (8,5 pt) dal rifilo
TACCA, TACCA_GAP = 3.0 * MM, 0.5 * MM          # tacche esterne: lunghezza e distanza dal blocco
TACCA_MIN = 5.0 * MM                           # tacche solo dove il margine esterno e' >= 5 mm
FILETTO_GAP = 0.3 * MM                         # i filetti interni finiscono 0,3 mm prima del rifilo

SWATCH = {
    "Inchiostro": "#2a2118", "Marrone": "#6b4a2b", "Rosso": "#9c2f24", "Oro": "#b8862b",
    "Blu": "#2f5d7c", "Carta": "#fbf8ef", "Pergamena": "#f1dcae", "OroChiaro": "#f6d68b",
    # tipi (legenda dell'autore: Mappa rossa, Incanto blu, Equipaggiamento verde, Classe viola)
    "Mappa": "#9c2f24", "Incanto": "#2f5d7c", "Equipaggiamento": "#3d6f45", "Classe": "#7a4f86",
    # nemici (Carte_Nemico_v2.pptx)
    "Notte": "#0b1530", "Medaglione": "#2a1259", "Lettera": "#c9a6ff", "OroNemico": "#d9a93c",
    "PV": "#c62b2b", "Scudo": "#e0a43a",
    # imprevisti (tessera blu e colori di Locanda/Fonte/Fabbro; Trappola = tessera rossa)
    "Imprevisto": "#2f5d9c", "Trappola": "#a8352a", "Locanda": "#c0662b", "Fonte": "#2f7a8a",
    "Fabbro": "#4a5568",
    "Retro": "#3b2a1c",
    # dorsi dei mazzi di classe (concordati con le pedine eroe)
    "Assaltatore": "#9c2f24", "Ricercatore": "#3b7d4f", "Stregone": "#5b4a9c", "Oracolo": "#b8862b",
}
TIPO_COLORE = {"TM": "Mappa", "TI": "Incanto", "TE": "Equipaggiamento", "TC": "Classe", "NE": "Notte"}

SERIF, SANS = "Noto Serif", "IBM Plex Sans Condensed"


def lead(v):
    return {"kind": "points", "value": v}


PARA = [
    ("Titolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    ("Etichetta", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaDx", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaCentro", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("Testo", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Valore", "pattern": "\\([+\u2011\u2212-]?\\d+\\)"}]},
     {"fontFamily": SERIF, "fontStyle": "Regular", "size": 9.5, "leading": lead(12), "fill": "Inchiostro"}),
    ("TestoCentro", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Regular", "size": 10.5, "leading": lead(13.5), "fill": "Inchiostro"}),
    ("Classi", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 7, "leading": lead(8), "fill": "Marrone"}),
    ("Piede", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 6, "leading": lead(7), "fill": "Marrone"}),
    ("Codice", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 20}),
    ("CodiceChiaro", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Carta", "tracking": 20}),
    ("Provvisorio", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6, "leading": lead(7), "fill": "Rosso", "tracking": 60}),
    ("Segnaposto", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 26, "leading": lead(28), "fill": "Carta"}),
    # nemici
    ("NomeNemico", {"align": "left"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    ("LetteraMed", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(16), "fill": "Lettera"}),
    ("StatNome", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 40}),
    ("StatValore", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(15), "fill": "Inchiostro"}),
    ("Danno", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.5, "leading": lead(9), "fill": "Inchiostro"}),
    ("Sezione", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6.5, "leading": lead(7.5), "fill": "Notte", "tracking": 60}),
    ("TestoNemico", {"align": "left", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Regular", "size": 8.8, "leading": lead(10.6), "fill": "Inchiostro"}),
    ("Ricompensa", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Grassetto", "pattern": "^[^:]+:"}]},
     {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.6, "leading": lead(9), "fill": "Inchiostro"}),
    # imprevisti
    ("TitoloChiaro", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 12, "leading": lead(14), "fill": "Carta"}),
    # aiuto
    ("PassoNum", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 9, "leading": lead(10), "fill": "Carta"}),
    ("PassoNome", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 8.5, "leading": lead(9.5), "fill": "Rosso"}),
    ("PassoTesto", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 8.3, "leading": lead(9.6), "fill": "Inchiostro"}),
    ("RiepTitolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 8.5, "leading": lead(9.5), "fill": "Inchiostro"}),
    ("RiepSez", {"align": "left", "spaceBefore": 1.6}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6.4, "leading": lead(7), "fill": "Rosso", "tracking": 40}),
    ("RiepRiga", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 6.1, "leading": lead(6.8), "fill": "Inchiostro"}),
    # divisori e dorsi
    ("DivCodice", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 40, "leading": lead(42), "fill": "Carta"}),
    ("DivTitolo", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 12.5, "leading": lead(14), "fill": "Carta", "tracking": 20}),
    ("DivSotto", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 8.5, "leading": lead(10), "fill": "Carta"}),
    ("DorsoMarchio", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(8), "fill": "OroChiaro", "tracking": 120}),
    ("DorsoTitolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 18, "leading": lead(20), "fill": "OroChiaro"}),
    ("DorsoGrande", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 54, "leading": lead(56), "fill": "OroChiaro"}),
    ("DorsoSotto", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 8, "leading": lead(9.5), "fill": "OroChiaro", "tracking": 80}),
]
# varianti scure dei dorsi, per i fondi chiari (oro dell'Oracolo)
PARA += [(n + "Scuro", p, {**c, "fill": "Retro"}) for n, p, c in PARA if n.startswith("Dorso")]
DORSO_CHIARO = {"Oracolo"}

CHAR = [
    ("Valore", {"fontFamily": SERIF, "fontStyle": "Bold"}),
    ("Grassetto", {"fontFamily": SANS, "fontStyle": "SemiBold"}),
]


def leggi(nome):
    with open(DATI / nome, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def tipografico(s):
    """Apostrofo tipografico (il motore lo farebbe comunque; così gli offset restano stabili)
    e trattino unificatore in «(-1)», per non spezzare il valore a fine riga."""
    return s.replace("'", "\u2019").replace("(-", "(\u2011")


_CMYK = {}


def cmyk(nome):
    """Colori dell'identità visiva (hex) convertiti in CMYK con gli spazi di lavoro di DesignCraft,
    così il PDF/X-4 non contiene RGB senza profilo. Una sola chiamata al motore per tutti."""
    if not _CMYK:
        args = ["designcraft-cli", "run", "--sample"]
        for hexa in SWATCH.values():
            h = hexa.lstrip("#")
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            args += ["--cmd", "color.convert=" + json.dumps({"color": {"model": "rgb", "r": r, "g": g, "b": b}, "to": "cmyk"})]
        out = subprocess.run(args, capture_output=True, text=True, check=True).stdout
        dec, pos = json.JSONDecoder(), 0
        for n in SWATCH:
            while out[pos].isspace():
                pos += 1
            v, pos = dec.raw_decode(out, pos)
            _CMYK[n] = {k: round(v[k] * 100, 2) for k in "cmyk"}
    return _CMYK[nome]


class Doc:
    def __init__(self, titolo, pagine):
        self.righe = []
        self.cmd("file.new", preset=FORMATO, pages=pagine, facingPages=False, bleed=0, margins=0, title=titolo, intent="print")
        for nome in SWATCH:
            self.cmd("swatch.create", name=nome, color=cmyk(nome))
        for nome, chars in CHAR:
            self.cmd("style.character.create", name=nome, chars=chars)
        for nome, para, chars in PARA:
            self.cmd("style.paragraph.create", name=nome, para=para, chars=chars)

    def cmd(self, cid, **p):
        self.righe.append(f"{cid} {json.dumps(p, ensure_ascii=False)}")
        return len(self.righe) - 1

    # primitive in coordinate della carta (ox, oy = angolo del rifilo)
    def rett(self, sp, r, fill=None, tint=None, stroke=None, peso=0.0, raggio=0.0, forma="rectangle"):
        i = self.cmd("frame.create", spread=sp, rect=[round(v, 3) for v in r], shape=forma, content="graphic")
        if fill:
            p = {"swatch": fill}
            if tint is not None:
                p["tint"] = tint
            self.cmd("object.fill", **p)
        else:
            self.cmd("object.fill", swatch="[None]")
        if stroke:
            self.cmd("object.stroke", swatch=stroke, weight=peso, align="inside")
        else:
            self.cmd("object.stroke", swatch="[None]", weight=0)
        if raggio:
            self.cmd("object.cornerOptions", shape="rounded", size=raggio)
        return i

    def testo(self, sp, r, txt, stile, vj=None, paragrafi=None):
        """paragrafi: lista di (testo, stile) per storie con più stili."""
        if paragrafi:
            txt = "\n".join(t for t, _ in paragrafi)
        i = self.cmd("frame.create", spread=sp, rect=[round(v, 3) for v in r], content="text", text=txt)
        self.cmd("selection.set", ids=[f"${i}.id"])
        self.cmd("style.paragraph.apply", name=stile)
        if vj:
            self.cmd("object.textFrameOptions", verticalJustification=vj)
        if paragrafi:
            pos = 0
            for t, st in paragrafi:
                n = len(t.encode("utf-8"))
                if st != stile:
                    self.cmd("text.select", story=f"${i}.story", anchor=pos, focus=pos + n)
                    self.cmd("style.paragraph.apply", name=st)
                pos += n + 1
        self.cmd("object.label", label=f"testo:{stile}", ids=[f"${i}.id"])
        return i

    def linea(self, sp, a, b, swatch, peso):
        self.cmd("path.create", spread=sp, anchors=[{"p": [round(a[0], 3), round(a[1], 3)]}, {"p": [round(b[0], 3), round(b[1], 3)]}])
        self.cmd("object.stroke", swatch=swatch, weight=peso)

    def script(self):
        return "\n".join(self.righe) + "\n"


def origine(pos, retro):
    """Angolo di rifilo (ox, oy) della carta in posizione pos; il retro e' specchiato sul lato lungo."""
    r, c = divmod(pos, NC)
    if retro:
        c = NC - 1 - c
    return X0 + c * CELLA_W + B, Y0 + r * CELLA_H + B


def sangue(ox, oy):
    """Rettangolo del fondo colorato: il rifilo piu' l'abbondanza B su tutti e 4 i lati (le celle vicine si toccano)."""
    return [ox - B, oy - B, ox + CW + B, oy + CH + B]


def segni_taglio(d, sp, nome, foglio, fogli, retro, pagina, pagine, occupate):
    """Tacche d'angolo sul margine esterno (solo dove ci sono >= 5 mm), filetti bianchi dentro l'abbondanza di ogni carta
    presente (occupate = angoli di rifilo) ed etichette del foglio, nelle fasce di margine tra le tacche."""
    xs = [X0 + c * CELLA_W + B + dx for c in range(NC) for dx in (0, CW)]       # linee verticali di rifilo
    ys = [Y0 + r * CELLA_H + B + dy for r in range(NR) for dy in (0, CH)]      # linee orizzontali di rifilo
    bx0, by0, bx1, by1 = X0, Y0, X0 + NC * CELLA_W, Y0 + NR * CELLA_H
    if by0 >= TACCA_MIN:
        for x in xs:
            d.linea(sp, (x, by0 - TACCA_GAP - TACCA), (x, by0 - TACCA_GAP), "[Registration]", 0.5)
            d.linea(sp, (x, by1 + TACCA_GAP), (x, by1 + TACCA_GAP + TACCA), "[Registration]", 0.5)
    if bx0 >= TACCA_MIN:
        for y in ys:
            d.linea(sp, (bx0 - TACCA_GAP - TACCA, y), (bx0 - TACCA_GAP, y), "[Registration]", 0.5)
            d.linea(sp, (bx1 + TACCA_GAP, y), (bx1 + TACCA_GAP + TACCA, y), "[Registration]", 0.5)
    # filetti bianchi: a ogni angolo di rifilo, sul prolungamento dei lati, dentro l'abbondanza (si ritagliano via)
    for ox, oy in occupate:
        for x, sx in ((ox, -1), (ox + CW, 1)):
            for y, sy in ((oy, -1), (oy + CH, 1)):
                a = x + sx * FILETTO_GAP
                d.linea(sp, (a, y), (x + sx * B, y), "[Paper]", 0.25)
                b = y + sy * FILETTO_GAP
                d.linea(sp, (x, b), (x, y + sy * B), "[Paper]", 0.25)
    # etichette: sopra (fronte/retro) e sotto (file e pagina) il blocco. A4 (3 colonne): nella fascia delle tacche, tra
    # quelle della colonna centrale (dove non ci sono tacche). Con piu' colonne le tacche attraversano la fascia, quindi
    # l'etichetta va oltre le tacche (sul margine esterno c'e' posto: sull'A3 22 mm sopra e sotto).
    lato = "RETRO · girare sul lato lungo" if retro else "FRONTE"
    if NC <= 3:
        xa, xb, su = X0 + CELLA_W + B + 2, X0 + (NC - 2) * CELLA_W + B + CW - 2, 0.0
    else:
        xa, xb, su = X0 + B, X0 + NC * CELLA_W - B, TACCA + 1.0 * MM
    d.testo(sp, [xa, by0 - TACCA_GAP - TACCA - su, xb, by0 - TACCA_GAP - su], f"{lato} · foglio {foglio} di {fogli}", "EtichettaCentro", vj="bottom")
    d.testo(sp, [xa, by1 + TACCA_GAP + su, xb, by1 + TACCA_GAP + TACCA + su], f"{nome}.pdf · pag. {pagina}/{pagine}", "EtichettaCentro", vj="top")


def cornice(d, sp, ox, oy, colore, fondo="Carta"):
    d.rett(sp, sangue(ox, oy), fill=colore)
    d.rett(sp, [ox + SAFE, oy + SAFE, ox + CW - SAFE, oy + CH - SAFE], fill=fondo, raggio=4)


def L(ox, oy, x0, y0, x1, y1):
    return [ox + x0, oy + y0, ox + x1, oy + y1]


# ---------------------------------------------------------------- fronti

def carta_trama(d, sp, ox, oy, r, mazzo=None):
    tipo = r["tipo"]
    col = TIPO_COLORE[tipo]
    cornice(d, sp, ox, oy, col)
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 31), tipografico(r["nome"]), "Titolo", vj="center")
    sx = r["tipo_nome"].upper() + (" · " + r["slot"].upper() if r.get("slot") else "")
    d.testo(sp, L(ox, oy, 14, 32, CW - 14, 40), sx, "Etichetta")
    d.linea(sp, (ox + 14, oy + 42), (ox + CW - 14, oy + 42), col, 0.6)
    d.rett(sp, L(ox, oy, 14, 46, CW - 14, 96), fill=col, tint=0.14, raggio=2)
    d.testo(sp, L(ox, oy, 14, 57, CW - 14, 87), tipo, "Segnaposto", vj="center")
    if r.get("provvisorio"):
        d.testo(sp, L(ox, oy, 17, 48, CW - 17, 56), "PROVVISORIO", "Provvisorio")
    if mazzo:
        d.testo(sp, L(ox, oy, 60, 48, CW - 17, 56), "MAZZO " + mazzo.upper(), "EtichettaDx")
    d.testo(sp, L(ox, oy, 15, 101, CW - 15, CH - 33), tipografico(r["testo"]), "Testo")
    d.linea(sp, (ox + 14, oy + CH - 31), (ox + CW - 14, oy + CH - 31), col, 0.6)
    d.testo(sp, L(ox, oy, 14, CH - 29, CW - 14, CH - 20), r["classe_riga"], "Classi")
    piede = " · ".join(v for v in (r.get("rarita", ""), r.get("copia", "") if r.get("copia", "") not in ("", "1 di 1") else "") if v)
    if piede:
        d.testo(sp, L(ox, oy, 14, CH - 19, 110, CH - 11.5), piede, "Piede")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


def carta_ritratto(d, sp, ox, oy, r):
    rr = {"tipo": "TC", "tipo_nome": "Carta Classe", "nome": r["nome"], "slot": "", "testo": r["testo"],
          "classe_riga": r["classe"], "id": r["id"], "provvisorio": bool(r["corretto_dalla_bozza"].strip())}
    carta_trama(d, sp, ox, oy, rr)


def carta_mostro(d, sp, ox, oy, r):
    cornice(d, sp, ox, oy, "Notte", fondo="Pergamena")
    boss = r["mazzetto"].startswith("3")
    d.rett(sp, L(ox, oy, 13, 13, 39, 39), fill="Medaglione", stroke="OroNemico", peso=1.2, forma="ellipse")
    d.testo(sp, L(ox, oy, 13, 13, 39, 39), r["lettera"], "LetteraMed", vj="center")
    d.testo(sp, L(ox, oy, 43, 13, CW - 13, 31), tipografico(r["nome"]), "NomeNemico", vj="center")
    mz = "MAZZETTO " + r["mazzetto"].upper().replace(" / ", " · ")
    d.testo(sp, L(ox, oy, 43, 31, CW - 13, 39), f"LV {r['lv']} · {mz}", "Etichetta")
    d.testo(sp, L(ox, oy, 100, 41, CW - 14, 48), r["id"], "Codice")
    d.rett(sp, L(ox, oy, 14, 49, CW - 14, 86), fill="Notte", tint=0.12, raggio=2)
    if boss:
        d.testo(sp, L(ox, oy, 14, 52, CW - 14, 84), "BOSS", "Segnaposto", vj="center")
    stats = [("PV", r["pv"], "PV"), ("ATT", r["att"], "Inchiostro"), ("AR", r["ar"], "Scudo"), ("DIFESA", r["difesa"], "Blu")]
    w = (CW - 28 - 3 * 4) / 4
    for k, (nome, val, colore) in enumerate(stats):
        x0 = 14 + k * (w + 4)
        d.rett(sp, L(ox, oy, x0, 90, x0 + w, 122), fill="Carta", stroke=colore, peso=1.2, raggio=2)
        d.testo(sp, L(ox, oy, x0, 92, x0 + w, 99), nome, "StatNome")
        d.testo(sp, L(ox, oy, x0, 100, x0 + w, 120), val, "StatValore", vj="center")
    d.testo(sp, L(ox, oy, 14, 124, CW - 14, 134), "Danno: " + r["danno"], "Danno", vj="center")
    d.testo(sp, L(ox, oy, 15, 137, CW - 15, 145), "ABILITÀ SPECIALI", "Sezione")
    if boss:
        y_ric = CH - 13 - 9 - 2 * 9 - 2
    else:
        y_ric = CH - 13 - 9 - 9 - 2
    d.testo(sp, L(ox, oy, 15, 146, CW - 15, y_ric - 2), tipografico(r["abilita"]), "TestoNemico")
    d.linea(sp, (ox + 14, oy + y_ric - 1), (ox + CW - 14, oy + y_ric - 1), "OroNemico", 0.6)
    d.testo(sp, L(ox, oy, 15, y_ric + 1, CW - 15, y_ric + 9), "RICOMPENSE", "Sezione")
    if boss:
        ric = [("Custode: " + r["ricompense"], "Ricompensa"), ("Mazzetto 3: " + r["ricompensa_se_mazzetto_3"], "Ricompensa")]
        d.testo(sp, L(ox, oy, 15, y_ric + 9, CW - 15, CH - 12), "", "Ricompensa", paragrafi=ric)
    else:
        d.testo(sp, L(ox, oy, 15, y_ric + 9, CW - 15, CH - 12), r["ricompense"], "Ricompensa")


def carta_imprevisto(d, sp, ox, oy, r):
    cornice(d, sp, ox, oy, "Imprevisto")
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, 40), fill=r["nome"], raggio=4)
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 36), r["nome"], "TitoloChiaro", vj="center")
    d.testo(sp, L(ox, oy, 14, 43, CW - 14, 51), "IMPREVISTO", "Etichetta")
    d.rett(sp, L(ox, oy, 14, 54, CW - 14, 110), fill=r["nome"], tint=0.14, raggio=2)
    d.testo(sp, L(ox, oy, 14, 64, CW - 14, 100), "?", "Segnaposto", vj="center")
    testo = r["testo_bozza"].strip() or r["testo"]
    d.testo(sp, L(ox, oy, 16, 118, CW - 16, CH - 30), tipografico(testo), "TestoCentro", vj="center")
    d.linea(sp, (ox + 14, oy + CH - 27), (ox + CW - 14, oy + CH - 27), "Imprevisto", 0.6)
    d.testo(sp, L(ox, oy, 14, CH - 19, 110, CH - 11.5), r["copia"], "Piede")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


def carta_aiuto_fronte(d, sp, ox, oy, r):
    cornice(d, sp, ox, oy, "Oro")
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 31), r["fronte_titolo"], "Titolo", vj="center")
    d.linea(sp, (ox + 14, oy + 33), (ox + CW - 14, oy + 33), "Oro", 0.6)
    passo = 37.5
    for k in range(5):
        y = 37 + k * passo
        d.rett(sp, L(ox, oy, 14, y + 1, 30, y + 17), fill="Oro", forma="ellipse")
        d.testo(sp, L(ox, oy, 14, y + 1, 30, y + 17), str(k + 1), "PassoNum", vj="center")
        d.testo(sp, L(ox, oy, 34, y + 1, CW - 14, y + 11), r[f"passo{k + 1}_nome"], "PassoNome")
        d.testo(sp, L(ox, oy, 34, y + 11, CW - 14, y + passo - 1), tipografico(r[f"passo{k + 1}_testo"]), "PassoTesto")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


RIEPILOGO = [("Scontro", "retro_scontro"), ("Ricompense", "retro_ricompense"),
             ("Tessere «?»", "retro_tessere"), ("Sconfitta", "retro_sconfitta"), ("Vittoria", "retro_vittoria")]


def carta_aiuto_retro(d, sp, ox, oy, r):
    cornice(d, sp, ox, oy, "Oro")
    par = [(r["retro_titolo"], "RiepTitolo")]
    for sez, campo in RIEPILOGO:
        par.append((sez.upper(), "RiepSez"))
        par += [(tipografico(riga), "RiepRiga") for riga in r[campo].split("\n")]
    d.testo(sp, L(ox, oy, 11.5, 11, CW - 11.5, CH - 10), "", "RiepRiga", paragrafi=par)


def divisore(d, sp, ox, oy, r):
    col = TIPO_COLORE[r["codice"]]
    d.rett(sp, sangue(ox, oy), fill=col)
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, CH - SAFE), stroke="Carta", peso=0.8, raggio=4)
    d.testo(sp, L(ox, oy, 13, 18, CW - 13, 30), "DIVISORE", "DorsoSotto")
    d.testo(sp, L(ox, oy, 13, 60, CW - 13, 110), r["codice"], "DivCodice", vj="center")
    d.testo(sp, L(ox, oy, 13, 118, CW - 13, 138), r["titolo"], "DivTitolo", vj="center")
    d.testo(sp, L(ox, oy, 13, 142, CW - 13, 168), f"{r['contenuto_playtest']} · {r['carte_del_tipo']} carte", "DivSotto", vj="center")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "CodiceChiaro")


# ---------------------------------------------------------------- dorsi

def dorso(d, sp, ox, oy, colore, titolo, sotto="", grande=""):
    scuro = colore in DORSO_CHIARO
    inch, suf = ("Retro", "Scuro") if scuro else ("OroChiaro", "")
    d.rett(sp, sangue(ox, oy), fill=colore)
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, CH - SAFE), stroke=inch, peso=1.0, raggio=4)
    d.rett(sp, L(ox, oy, SAFE + 4, SAFE + 4, CW - SAFE - 4, CH - SAFE - 4), stroke=inch, peso=0.4, raggio=2)
    d.testo(sp, L(ox, oy, 16, 24, CW - 16, 34), "IL TESORO DEL GOBLIN", "DorsoMarchio" + suf)
    if grande:
        d.testo(sp, L(ox, oy, 16, 70, CW - 16, 140), grande, "DorsoGrande" + suf, vj="center")
        d.testo(sp, L(ox, oy, 16, 146, CW - 16, 186), titolo, "DorsoTitolo" + suf, vj="center")
    else:
        d.testo(sp, L(ox, oy, 16, 95, CW - 16, 155), titolo, "DorsoTitolo" + suf, vj="center")
    if sotto:
        d.testo(sp, L(ox, oy, 16, CH - 40, CW - 16, CH - 26), sotto, "DorsoSotto" + suf, vj="center")


def costruisci(nome, titolo, carte):
    """carte: lista di (funzione_fronte, funzione_retro); PER_FOGLIO per foglio. Pagine in ordine F1, R1, F2, R2..."""
    n = len(carte)
    fogli = (n + PER_FOGLIO - 1) // PER_FOGLIO
    d = Doc(titolo, 2 * fogli)
    occupate = [([], []) for _ in range(fogli)]          # per foglio: angoli di rifilo (fronte, retro)
    for k, (fr, rt) in enumerate(carte):
        ox, oy = origine(k % PER_FOGLIO, False)
        fr(d, 2 * (k // PER_FOGLIO), ox, oy)
        occupate[k // PER_FOGLIO][0].append((ox, oy))
        ox, oy = origine(k % PER_FOGLIO, True)
        rt(d, 2 * (k // PER_FOGLIO) + 1, ox, oy)
        occupate[k // PER_FOGLIO][1].append((ox, oy))
    d.cmd("layer.new", name="Segni di taglio")
    for sp in range(2 * fogli):
        segni_taglio(d, sp, nome, sp // 2 + 1, fogli, sp % 2 == 1, sp + 1, 2 * fogli, occupate[sp // 2][sp % 2])
    d.cmd("file.exportPdf", path=str(PDF_DIR / f"{nome}.pdf"), standard="x4", title=titolo, bleed=False, marks=False)
    with tempfile.TemporaryDirectory(prefix="goblin_carte_") as tmp:
        src = pathlib.Path(tmp) / f"{nome}.dcs"
        src.write_text(d.script(), encoding="utf-8")
        out = subprocess.run(["designcraft-cli", "script", str(src), "--save", str(DC_DIR / f"{nome}.designcraft")],
                             capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"{nome}: designcraft-cli ha fallito\n{out.stdout[-2000:]}\n{out.stderr[-2000:]}")
    res = json.loads(out.stdout)
    print(f"{nome}: {n} carte, {fogli} fogli fronte + {fogli} retro, {res['completed']} comandi")


def mazzi():
    def f(fn, *a):
        return lambda d, sp, ox, oy: fn(d, sp, ox, oy, *a)

    comune_retro = f(dorso, "Retro", "Carta comune", "", "")
    comuni = []
    for r in leggi("carte_comuni.csv"):
        r["provvisorio"] = bool(r["corretto_dalla_bozza"].strip())
        comuni.append((f(carta_trama, r), comune_retro))

    classe = []
    for r in leggi("carte_classe.csv"):
        classe.append((f(carta_trama, r, r["mazzo"]), f(dorso, r["mazzo"], r["mazzo"], "MAZZO DI CLASSE")))
    for r in leggi("carte_classe_ritratto.csv"):
        classe.append((f(carta_ritratto, r), f(dorso, "Classe", "Carta Classe", "")))

    mostri = []
    for r in leggi("carte_mostro.csv"):
        num = r["mazzetto"][0]
        retro = f(dorso, "Notte", "Mostro", "MAZZETTO · BOSS" if num == "3" else "MAZZETTO", num)
        mostri.append((f(carta_mostro, r), retro))

    impr = [(f(carta_imprevisto, r), f(dorso, "Imprevisto", "Imprevisto", "")) for r in leggi("carte_imprevisto.csv")]

    aiuto = [(f(carta_aiuto_fronte, r), f(carta_aiuto_retro, r)) for r in leggi("carte_aiuto.csv")]
    aiuto += [(f(divisore, r), f(divisore, r)) for r in leggi("divisori.csv")]

    return {
        "carte_comuni": ("Il Tesoro del Goblin – carte comuni (playtest)", comuni),
        "carte_classe": ("Il Tesoro del Goblin – carte di classe (playtest)", classe),
        "carte_mostro": ("Il Tesoro del Goblin – carte Mostro (playtest)", mostri),
        "carte_imprevisto": ("Il Tesoro del Goblin – carte Imprevisto (playtest)", impr),
        "carte_aiuto_divisori": ("Il Tesoro del Goblin – Carte Aiuto e Divisori (playtest)", aiuto),
    }


if __name__ == "__main__":
    solo = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    DC_DIR.mkdir(parents=True, exist_ok=True)
    totale = 0
    for nome, (titolo, carte) in mazzi().items():
        if solo and nome != solo:
            continue
        costruisci(nome, titolo, carte)
        totale += len(carte)
    print("totale carte:", totale)
