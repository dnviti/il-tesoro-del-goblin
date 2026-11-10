#!/usr/bin/env python3
"""Carte del playtest v7 «Il Tesoro del Goblin»: unione dati CSV -> DesignCraft.

Equivale a un Data Merge: legge i CSV in ../dati, scrive per ogni PDF uno script
di comandi DesignCraft (carte_*.dcs), lo esegue con `designcraft-cli script`,
salva il progetto modificabile (carte_*.designcraft) e il PDF in ../../playtest_v7.

Schema v7 delle carte comuni (dati/carte_comuni.csv) e di classe (dati/classi/<classe>.csv, un file per classe, uniti
nell'ordine di CLASSI e poi della direzione A/B): id, tipo (TE/TI/TM o Equipaggiamento/Incanto/Mappa), nome, classe
(nome della classe o «Tutte le classi»), direzione (solo carte di classe: A o B), pl (Equipaggiamenti: Comune 1, Rara 2,
Leggendaria 3; vuoto per Incanti e Mappe), rarita, slot, testo, testo_situazionale (la riga «Se…», stampata sotto il
testo), nota (non stampata; se contiene «segnaposto» la carta porta la scritta SEGNAPOSTO). Direzione e PL stanno in
basso nel riquadro dell'illustrazione. Il testo che non entra nel suo riquadro ferma lo script (preflight di DesignCraft).

Stampa SOLO FRONTE (v6-bis, 8/11): nessun PDF va stampato sui due lati. Ogni mazzo coperto ha due PDF: <nome>.pdf con i fronti e
<nome>_retri.pdf con i dorsi. I dorsi NON sono specchiati: il dorso nella posizione p della pagina dei retri che dice «coi
fronti del foglio k» va con il fronte nella posizione p del foglio k (stessa griglia, stesse celle). Un foglio di fronti
senza nessun dorso (le Carte Classe in fondo al mazzo di classe) non ha la sua pagina dei retri: niente pagine di dorsi
vuote (fogli_dorsi). Ogni fronte e ogni dorso si fustella da solo con la dima e poi si
uniscono (colla stick dorso contro dorso, o bustina). Nell'abbondanza in basso di ogni dorso c'e' un'etichetta minuscola
(mazzo e ID del fronte) che sparisce col taglio. Carte Classe, Carte Specie, Carte Aiuto e Divisori hanno un solo lato.

Formato: carta 63 x 88 mm rifilata, OGNI carta con la sua abbondanza (bleed) su tutti e 4 i lati: fondo/cornice colorati
si estendono oltre il rifilo di 2,5 mm (A4, cella 68 x 93 mm) o 3 mm (A3, cella 69 x 94 mm). Le celle si toccano ma non si
sovrappongono. A4: 3 x 3 = 9 carte, blocco 204 x 279 mm centrato (rifilo esterno a >= 5,5 mm dal bordo); l'abbondanza
esterna può cadere nella zona non stampabile (è solo colore in più). Segni di taglio: tacche d'angolo sul margine esterno
del foglio dove c'è posto, più un filetto bianco sottilissimo a ogni angolo di rifilo dentro l'abbondanza (si ritaglia
sul bordo dell'abbondanza e poi si centra la carta nella dima 63 x 88 mm).

Formato A3 (`--formato A3`): 16 carte per foglio A3 verticale (4 x 4), blocco 276 x 376 mm centrato, abbondanza 3 mm,
stesse regole; PDF in ../../playtest_v7_A3 e progetti in ./A3. Senza opzione: A4.

Uso: python3 genera_carte.py [--solo NOME] [--formato A4|A3] [--dati CARTELLA] [--uscita CARTELLA]   (richiede designcraft-cli)
--dati legge i CSV da un'altra cartella (per provare dati nuovi); --uscita scrive PDF e progetti .designcraft in un'altra
cartella, senza toccare playtest_v7*.

Colonna facoltativa `battuta` (ultima colonna di ogni CSV di carte): una riga di colore, al massimo 70 caratteri e 2 righe,
in corsivo piccolo nel riquadro dell'illustrazione (al posto del codice segnaposto). Vuota o assente: non si stampa niente.
"""
import csv
import json
import pathlib
import subprocess
import sys
import tempfile

QUI = pathlib.Path(__file__).resolve().parent


def opzione(nome, predefinita):
    return pathlib.Path(sys.argv[sys.argv.index(nome) + 1]).resolve() if nome in sys.argv else predefinita


DATI = opzione("--dati", QUI.parent / "dati")
FORMATO = sys.argv[sys.argv.index("--formato") + 1].upper() if "--formato" in sys.argv else "A4"
if FORMATO not in ("A4", "A3"):
    sys.exit("--formato: A4 o A3")
PDF_DIR = opzione("--uscita", QUI.parent.parent / ("playtest_v7" if FORMATO == "A4" else "playtest_v7_A3"))
DC_DIR = PDF_DIR / "designcraft" if "--uscita" in sys.argv else (QUI if FORMATO == "A4" else QUI / "A3")

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
    "Assaltatore": "#9c2f24", "Ricercatore": "#3b7d4f", "Stregone": "#5b4a9c", "Oracolo": "#b8862b", "Giullare": "#a8407e",
    # Carte Specie (spec v6-bis §4.2)
    "Umano": "#4a5568", "Elfo": "#2f7a8a", "Sanguar": "#7a2f4f", "Yumaniano": "#8a6a1c",
}
TIPO_COLORE = {"TM": "Mappa", "TI": "Incanto", "TE": "Equipaggiamento", "TC": "Classe", "NE": "Notte"}
TIPO_CODICE = {"MAPPA": "TM", "INCANTO": "TI", "EQUIPAGGIAMENTO": "TE"}   # colonna tipo: codice o nome del tipo
TIPO_NOME = {"TM": "Mappa", "TI": "Incanto", "TE": "Equipaggiamento"}
# le 5 classi v7 nell'ordine di stampa; direzioni A/B col loro nome goliardico (tono v7, 10/11; meccaniche nel piano v7 §6.2-6.6)
CLASSI = ["Assaltatore", "Ricercatore", "Stregone", "Oracolo", "Giullare"]
DIREZIONI = {
    "Assaltatore": {"A": "Spaccatutto", "B": "Armadio a due ante"}, "Ricercatore": {"A": "Ficcanaso", "B": "Mani lunghe"},
    "Stregone": {"A": "Fumo e fiamme", "B": "So tutto io"}, "Oracolo": {"A": "Ci ho preso!", "B": "Malocchio"},
    "Giullare": {"A": "Gioco di mano", "B": "Carta nella manica"},
}

SERIF, SANS = "Noto Serif", "IBM Plex Sans Condensed"


def lead(v):
    return {"kind": "points", "value": v}


PARA = [
    ("Titolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    ("Etichetta", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    # v7: riga del tipo lunga (direzione · tipo · slot): corpo più piccolo, senza spaziatura
    ("EtichettaStretta", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 5.2, "leading": lead(7.5), "fill": "Marrone"}),
    ("EtichettaDx", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaCentro", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaFoglio", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone"}),
    ("Testo", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Valore", "pattern": "\\([+\u2011\u2212-]?\\d+\\)"}]},
     {"fontFamily": SERIF, "fontStyle": "Regular", "size": 9.5, "leading": lead(12), "fill": "Inchiostro"}),
    # v7: la riga «Se…» (testo_situazionale) sotto l'effetto base
    ("TestoSituazionale", {"align": "left", "hyphenate": False, "spaceBefore": 2, "grepStyles": [{"style": "Valore", "pattern": "\\([+\u2011\u2212-]?\\d+\\)"}]},
     {"fontFamily": SERIF, "fontStyle": "Italic", "size": 9.5, "leading": lead(12), "fill": "Inchiostro"}),
    ("TestoCentro", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Regular", "size": 10.5, "leading": lead(13.5), "fill": "Inchiostro"}),
    ("Classi", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 7, "leading": lead(8), "fill": "Marrone"}),
    # v7: riga in fondo alla Carta Classe «Mazzetto: 6 delle 10 carte di classe · Mano: 3 + 3» (Spec R 13.1)
    ("ClassiPiccolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 6.5, "leading": lead(8), "fill": "Marrone"}),
    ("Piede", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 6, "leading": lead(7), "fill": "Marrone"}),
    ("Nota", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.6, "leading": lead(9), "fill": "Marrone"}),
    ("Codice", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 20}),
    ("CodiceChiaro", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Carta", "tracking": 20}),
    ("Provvisorio", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6, "leading": lead(7), "fill": "Rosso", "tracking": 60}),
    ("Segnaposto", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 26, "leading": lead(28), "fill": "Carta"}),
    # v7: battuta (colonna facoltativa `battuta`) nel riquadro dell'illustrazione, al massimo 2 righe
    ("Battuta", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 7.2, "leading": lead(8.6), "fill": "Inchiostro"}),
    # v7: lettera della direzione nel tondo della riga del tipo e PL nel riquadro dell'illustrazione
    ("DirLettera", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 6.5, "leading": lead(7.5), "fill": "Carta"}),
    ("PL", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 7.5, "leading": lead(8.5), "fill": "Carta", "tracking": 40}),
    # nemici
    ("NomeNemico", {"align": "left"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    ("LetteraMed", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(16), "fill": "Lettera"}),
    ("StatNome", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 40}),
    ("StatValore", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(15), "fill": "Inchiostro"}),
    ("Danno", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.5, "leading": lead(9), "fill": "Inchiostro"}),
    ("Sezione", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6.5, "leading": lead(7.5), "fill": "Notte", "tracking": 60}),
    ("TestoNemico", {"align": "left", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Regular", "size": 8.5, "leading": lead(10.2), "fill": "Inchiostro"}),
    # v7: nomi lunghi (fino a 26 caratteri, tono goliardico) su una riga sola
    ("NomeNemicoStretto", {"align": "left"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 9, "leading": lead(10.5), "fill": "Inchiostro", "tracking": -10}),
    ("Ricompensa", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Grassetto", "pattern": "^[^:]+:"}]},
     {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.6, "leading": lead(9), "fill": "Inchiostro"}),
    # imprevisti
    ("TitoloChiaro", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 12, "leading": lead(14), "fill": "Carta"}),
    # aiuto
    ("PassoNum", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 9, "leading": lead(10), "fill": "Carta"}),
    ("PassoNome", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 8.5, "leading": lead(9.5), "fill": "Rosso"}),
    ("PassoTesto", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 8.3, "leading": lead(9.6), "fill": "Inchiostro"}),
    ("PassoRiquadro", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Grassetto", "pattern": "(Carte|Equipaggiamenti|Mano):"}]},
     {"fontFamily": SANS, "fontStyle": "Regular", "size": 8.3, "leading": lead(9.6), "fill": "Inchiostro"}),
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
    # etichetta nell'abbondanza in basso dei dorsi (sparisce col taglio): mazzo e ID del fronte
    ("DorsoAbbondanza", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 4.2, "leading": lead(4.6), "fill": "OroChiaro", "tracking": 20}),
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
        self.testi = {}            # indice del comando frame.create -> (foglio, inizio del testo): per i messaggi di overset
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
        self.testi[i] = (sp, txt[:60])
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


def origine(pos):
    """Angolo di rifilo (ox, oy) della carta in posizione pos. Fronti e dorsi usano la stessa posizione (niente specchio)."""
    r, c = divmod(pos, NC)
    return X0 + c * CELLA_W + B, Y0 + r * CELLA_H + B


def sangue(ox, oy):
    """Rettangolo del fondo colorato: il rifilo piu' l'abbondanza B su tutti e 4 i lati (le celle vicine si toccano)."""
    return [ox - B, oy - B, ox + CW + B, oy + CH + B]


def segni_taglio(d, sp, sopra, sotto, occupate):
    """Tacche d'angolo sul margine esterno (solo dove ci sono >= 5 mm), filetti bianchi dentro l'abbondanza di ogni carta
    presente (occupate = angoli di rifilo) ed etichette del foglio (sopra/sotto), nelle fasce di margine tra le tacche."""
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
    # etichette: sopra (fronti/retri e foglio) e sotto (file e pagina) il blocco. A4 (3 colonne): nella fascia delle tacche,
    # tra quelle della colonna centrale (dove non ci sono tacche). Con piu' colonne le tacche attraversano la fascia, quindi
    # l'etichetta va oltre le tacche (sul margine esterno c'e' posto: sull'A3 22 mm sopra e sotto).
    if NC <= 3:
        xa, xb, su = X0 + CELLA_W + B + 1, X0 + (NC - 2) * CELLA_W + B + CW - 1, 0.0
    else:
        xa, xb, su = X0 + B, X0 + NC * CELLA_W - B, TACCA + 1.0 * MM
    d.testo(sp, [xa, by0 - TACCA_GAP - TACCA - su, xb, by0 - TACCA_GAP - su], sopra, "EtichettaFoglio", vj="bottom")
    d.testo(sp, [xa, by1 + TACCA_GAP + su, xb, by1 + TACCA_GAP + TACCA + su], sotto, "EtichettaFoglio", vj="top")


def cornice(d, sp, ox, oy, colore, fondo="Carta"):
    d.rett(sp, sangue(ox, oy), fill=colore)
    d.rett(sp, [ox + SAFE, oy + SAFE, ox + CW - SAFE, oy + CH - SAFE], fill=fondo, raggio=4)


def L(ox, oy, x0, y0, x1, y1):
    return [ox + x0, oy + y0, ox + x1, oy + y1]


# ---------------------------------------------------------------- fronti

BATTUTA_MAX = 70   # caratteri (local v7_tono.md); le 2 righe le controlla il preflight


def battuta(d, sp, ox, oy, r, y0, y1):
    """Stampa la battuta della carta (colonna facoltativa `battuta`) centrata tra y0 e y1 nel riquadro dell'illustrazione.
    Il riquadro alto ~21 pt regge 2 righe: una terza va in overset e ferma lo script. Ritorna True se c'era una battuta."""
    t = (r.get("battuta") or "").strip()
    if not t:
        return False
    if len(t) > BATTUTA_MAX:
        sys.exit(f"{r['id']}: battuta di {len(t)} caratteri (massimo {BATTUTA_MAX}): «{t}»")
    d.testo(sp, L(ox, oy, 17, y0, CW - 17, y1), tipografico(t), "Battuta", vj="center")
    return True


def carta_trama(d, sp, ox, oy, r, mazzo=None):
    """Fronte di Mappe, Incanti, Equipaggiamenti e Carte Classe. r: dizionario di carta_v7() o carta_ritratto().
    Riga del tipo (Spec v7 §14.1): per le carte di classe comincia con la direzione, lettera nel tondo del colore della
    classe e nome, poi tipo e slot. Riquadro dell'illustrazione: in alto l'etichetta rossa (SEGNAPOSTO/PLAYTEST) e il
    mazzo, in basso a destra il PL. Testo: effetto base e riga «Se…» (corsivo), ~9 righe."""
    tipo = r["tipo"]
    col = TIPO_COLORE[tipo]
    cornice(d, sp, ox, oy, col)
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 31), tipografico(r["nome"]), "Titolo", vj="center")
    sx = r["tipo_nome"].upper() + (" · " + r["slot"].upper() if r.get("slot") else "")
    x_tipo = 14
    if r.get("direzione"):
        d.rett(sp, L(ox, oy, 14, 31.5, 23, 40.5), fill=r["classe"], forma="ellipse")
        d.testo(sp, L(ox, oy, 14, 31.5, 23, 40.5), r["direzione"], "DirLettera", vj="center")
        sx = r["dir_nome"].upper() + " · " + sx
        x_tipo = 26
        if len(sx) > 49:   # es. «ARMADIO A DUE ANTE · EQUIPAGGIAMENTO · ARMA DX / SCUDO»: il tipo si abbrevia
            sx = sx.replace("EQUIPAGGIAMENTO", "EQUIP.")
    d.testo(sp, L(ox, oy, x_tipo, 32, CW - 14, 40), sx, "Etichetta" if len(sx) <= 34 else "EtichettaStretta", vj="center")
    d.linea(sp, (ox + 14, oy + 42), (ox + CW - 14, oy + 42), col, 0.6)
    d.rett(sp, L(ox, oy, 14, 46, CW - 14, 96), fill=col, tint=0.14, raggio=2)
    if not battuta(d, sp, ox, oy, r, 57, 79):
        d.testo(sp, L(ox, oy, 14, 52, CW - 14, 80), tipo, "Segnaposto", vj="center")
    if r.get("etichetta"):
        d.testo(sp, L(ox, oy, 17, 48, CW - 17, 56), r["etichetta"], "Provvisorio")
    if mazzo:
        d.testo(sp, L(ox, oy, 60, 48, CW - 17, 56), "MAZZO " + mazzo.upper(), "EtichettaDx")
    if r.get("pl"):
        d.rett(sp, L(ox, oy, CW - 47, 81, CW - 17, 93), fill="Oro", raggio=2)
        d.testo(sp, L(ox, oy, CW - 47, 81, CW - 17, 93), f"PL {r['pl']}", "PL", vj="center")
    par = [(tipografico(r["testo"]), "Testo")]
    if r.get("testo_situazionale"):
        par.append((tipografico(r["testo_situazionale"]), "TestoSituazionale"))
    d.testo(sp, L(ox, oy, 15, 101, CW - 15, CH - 33), "", "Testo", paragrafi=par)
    d.linea(sp, (ox + 14, oy + CH - 31), (ox + CW - 14, oy + CH - 31), col, 0.6)
    d.testo(sp, L(ox, oy, 12, CH - 29, CW - 12, CH - 20), r["classe_riga"], r.get("stile_classi", "Classi"))
    if r.get("rarita"):
        d.testo(sp, L(ox, oy, 14, CH - 19, 110, CH - 11.5), r["rarita"], "Piede")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


def carta_v7(r, classe_mazzo=None):
    """Riga del CSV v7 (carte_comuni.csv o classi/<classe>.csv) -> dizionario per carta_trama, con i controlli dello schema."""
    tipo = r["tipo"].strip()
    tipo = TIPO_CODICE.get(tipo.upper(), tipo.upper())
    if tipo not in TIPO_NOME:
        sys.exit(f"{r['id']}: tipo «{r['tipo']}» sconosciuto (TE/TI/TM o Equipaggiamento/Incanto/Mappa)")
    direzione = r["direzione"].strip().upper()
    classe = r["classe"].strip()
    if not classe_mazzo and classe not in ("Comune", "Tutte le classi"):
        sys.exit(f"{r['id']}: classe «{classe}» nel mazzo comune (Comune)")
    if classe_mazzo:
        if classe != classe_mazzo:
            sys.exit(f"{r['id']}: classe «{classe}» in un file del mazzo {classe_mazzo}")
        if direzione not in ("A", "B"):
            print(f"attenzione: {r['id']} ({classe}) senza direzione A/B", file=sys.stderr)
            direzione = ""
    elif direzione:
        sys.exit(f"{r['id']}: la direzione vale solo per le carte di classe")
    pl = r["pl"].strip()
    if tipo == "TE" and pl not in ("1", "2", "3"):
        sys.exit(f"{r['id']}: Equipaggiamento con PL «{pl}» (Comune 1, Rara 2, Leggendaria 3)")
    if tipo != "TE" and pl:
        sys.exit(f"{r['id']}: PL «{pl}» su un {TIPO_NOME[tipo]} (solo gli Equipaggiamenti hanno il PL)")
    return {"tipo": tipo, "tipo_nome": TIPO_NOME[tipo], "nome": r["nome"], "slot": r["slot"], "testo": r["testo"],
            "testo_situazionale": r["testo_situazionale"], "classe_riga": classe_mazzo or "Tutte le classi", "id": r["id"], "rarita": r["rarita"],
            "pl": pl, "classe": classe_mazzo, "direzione": direzione,
            "dir_nome": DIREZIONI[classe_mazzo][direzione] if direzione else "",
            "etichetta": "SEGNAPOSTO" if "segnaposto" in r["nota"].lower() else "", "battuta": r.get("battuta") or ""}


def carta_ritratto(d, sp, ox, oy, r):
    rr = {"tipo": "TC", "tipo_nome": "Carta Classe", "nome": r["nome"], "slot": "", "testo": r["testo"],
          "classe_riga": r["classe_riga"], "stile_classi": "ClassiPiccolo", "id": r["id"], "etichetta": r["provvisorio"].strip().upper(),
          "battuta": r.get("battuta") or ""}
    carta_trama(d, sp, ox, oy, rr)


def carta_specie(d, sp, ox, oy, r):
    """Carta Specie (spec v6-bis §4.2): impaginazione della Carta Classe, colore della specie, bonus grande e nota piccola."""
    col = r["specie"]
    cornice(d, sp, ox, oy, col)
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 31), r["nome"], "Titolo", vj="center")
    d.testo(sp, L(ox, oy, 14, 32, CW - 14, 40), "CARTA SPECIE", "Etichetta")
    d.linea(sp, (ox + 14, oy + 42), (ox + CW - 14, oy + 42), col, 0.6)
    d.rett(sp, L(ox, oy, 14, 46, CW - 14, 96), fill=col, tint=0.14, raggio=2)
    if not battuta(d, sp, ox, oy, r, 57, 79):
        d.testo(sp, L(ox, oy, 14, 57, CW - 14, 87), "TS", "Segnaposto", vj="center")
    if r["provvisorio"].strip():
        d.testo(sp, L(ox, oy, 17, 48, CW - 17, 56), "PROVVISORIO", "Provvisorio")
    d.testo(sp, L(ox, oy, 15, 101, CW - 15, 140), tipografico(r["bonus"]), "Testo")
    d.testo(sp, L(ox, oy, 15, 140, CW - 15, CH - 22), tipografico(r["nota"]), "Nota")
    d.testo(sp, L(ox, oy, 14, CH - 19, 110, CH - 11.5), r["copia"], "Piede")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


def carta_mostro(d, sp, ox, oy, r):
    """Carta Mostro. Riquadro dell'illustrazione 49-78 pt (battuta o «BOSS»), statistiche, danno, abilità (~200 caratteri:
    7 righe sui mostri, 6 sui boss, che hanno 3 righe di ricompense) e ricompense."""
    cornice(d, sp, ox, oy, "Notte", fondo="Pergamena")
    boss = r["mazzetto"].startswith("3")
    d.rett(sp, L(ox, oy, 13, 13, 39, 39), fill="Medaglione", stroke="OroNemico", peso=1.2, forma="ellipse")
    d.testo(sp, L(ox, oy, 13, 13, 39, 39), r["lettera"], "LetteraMed", vj="center")
    d.testo(sp, L(ox, oy, 43, 13, CW - 13, 31), tipografico(r["nome"]), "NomeNemico" if len(r["nome"]) <= 20 else "NomeNemicoStretto", vj="center")
    mz = "MAZZETTO " + r["mazzetto"].upper().replace(" / ", " · ")
    d.testo(sp, L(ox, oy, 43, 31, CW - 13, 39), f"LV {r['lv']} · {mz}", "Etichetta")
    d.testo(sp, L(ox, oy, 100, 41, CW - 14, 48), r["id"], "Codice")
    d.rett(sp, L(ox, oy, 14, 49, CW - 14, 78), fill="Notte", tint=0.12, raggio=2)
    con_battuta = battuta(d, sp, ox, oy, r, 57, 77)
    if boss and con_battuta:
        d.testo(sp, L(ox, oy, 17, 49.5, CW - 17, 57), "BOSS", "Provvisorio")
    elif boss:
        d.testo(sp, L(ox, oy, 14, 49, CW - 14, 78), "BOSS", "Segnaposto", vj="center")
    # dalla sera dell'8/11 niente Difesa: si colpisce con 2D6 + ATT ≥ AR del bersaglio (3 riquadri)
    stats = [("PV", r["pv"], "PV"), ("ATT", r["att"], "Inchiostro"), ("AR", r["ar"], "Scudo")]
    w = (CW - 28 - 2 * 6) / 3
    for k, (nome, val, colore) in enumerate(stats):
        x0 = 14 + k * (w + 6)
        d.rett(sp, L(ox, oy, x0, 81, x0 + w, 113), fill="Carta", stroke=colore, peso=1.2, raggio=2)
        d.testo(sp, L(ox, oy, x0, 83, x0 + w, 90), nome, "StatNome")
        d.testo(sp, L(ox, oy, x0, 91, x0 + w, 111), val, "StatValore", vj="center")
    d.testo(sp, L(ox, oy, 14, 115, CW - 14, 125), "Danno: " + r["danno"], "Danno", vj="center")
    d.testo(sp, L(ox, oy, 15, 128, CW - 15, 136), "ABILITÀ SPECIALI", "Sezione")
    if boss:
        # 3 righe: «Custode» + «Mazzetto 3», che dalla v6 (Indizio se D6 ≤ LV) va a capo
        y_ric = CH - 11 - 3 * 9 - 9
    else:
        y_ric = CH - 13 - 9 - 9 - 2
    d.testo(sp, L(ox, oy, 15, 137, CW - 15, y_ric - 2), tipografico(r["abilita"]), "TestoNemico")
    d.linea(sp, (ox + 14, oy + y_ric - 1), (ox + CW - 14, oy + y_ric - 1), "OroNemico", 0.6)
    d.testo(sp, L(ox, oy, 15, y_ric + 1, CW - 15, y_ric + 9), "RICOMPENSE", "Sezione")
    if boss:
        m3 = r["ricompensa_se_mazzetto_3"].replace("Forte Volontà", "Forte\u00a0Volontà")   # non spezzare il nome
        ric = [("Custode: " + r["ricompense"], "Ricompensa"), ("Mazzetto 3: " + m3, "Ricompensa")]
        d.testo(sp, L(ox, oy, 15, y_ric + 9, CW - 15, CH - 11), "", "Ricompensa", paragrafi=ric)
    else:
        d.testo(sp, L(ox, oy, 15, y_ric + 9, CW - 15, CH - 12), r["ricompense"], "Ricompensa")


# colore dell'Imprevisto dal suo id (i nomi possono cambiare col tono v7); id nuovi: colore generico
IMPREVISTO_COLORE = {"IM-01": "Trappola", "IM-02": "Locanda", "IM-03": "Fonte", "IM-04": "Fabbro"}


def carta_imprevisto(d, sp, ox, oy, r):
    cornice(d, sp, ox, oy, "Imprevisto")
    col = IMPREVISTO_COLORE.get(r["id"], "Imprevisto")
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, 40), fill=col, raggio=4)
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 36), r["nome"], "TitoloChiaro", vj="center")
    d.testo(sp, L(ox, oy, 14, 43, CW - 14, 51), "IMPREVISTO", "Etichetta")
    d.rett(sp, L(ox, oy, 14, 54, CW - 14, 110), fill=col, tint=0.14, raggio=2)
    if not battuta(d, sp, ox, oy, r, 71, 93):
        d.testo(sp, L(ox, oy, 14, 64, CW - 14, 100), "?", "Segnaposto", vj="center")
    testo = (r.get("testo_bozza") or "").strip() or r["testo"]
    d.testo(sp, L(ox, oy, 16, 118, CW - 16, CH - 30), tipografico(testo), "TestoCentro", vj="center")
    d.linea(sp, (ox + 14, oy + CH - 27), (ox + CW - 14, oy + CH - 27), "Imprevisto", 0.6)
    d.testo(sp, L(ox, oy, 14, CH - 19, 110, CH - 11.5), r["copia"], "Piede")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


def carta_aiuto_turno(d, sp, ox, oy, r):
    """Carta Aiuto «Il turno» (Spec v7 §4.0): Inizio (pesca), i 3 passi numerati e il riquadro senza numero su quando
    si giocano le carte. Altezza di ogni riga in pt: nome 10, poi 2 righe di testo (3 per la Fine)."""
    cornice(d, sp, ox, oy, "Oro")
    d.testo(sp, L(ox, oy, 13, 13, CW - 13, 31), r["fronte_titolo"], "Titolo", vj="center")
    d.linea(sp, (ox + 14, oy + 33), (ox + CW - 14, oy + 33), "Oro", 0.6)
    righe = [("•", "inizio", 31), ("1", "passo1", 31), ("2", "passo2", 31), ("3", "passo3", 41)]
    y = 36
    for num, campo, h in righe:
        d.rett(sp, L(ox, oy, 15, y + 1, 29, y + 15), fill="Oro", forma="ellipse")
        d.testo(sp, L(ox, oy, 15, y + 1, 29, y + 15), num, "PassoNum", vj="center")
        d.testo(sp, L(ox, oy, 34, y + 1, CW - 14, y + 11), r[f"{campo}_nome"], "PassoNome")
        d.testo(sp, L(ox, oy, 34, y + 10.5, CW - 14, y + h), tipografico(r[f"{campo}_testo"]), "PassoTesto")
        y += h
    # riquadro senza numero: quando si giocano le carte (non è un passo)
    d.rett(sp, L(ox, oy, 14, y + 1, CW - 14, CH - 21), fill="Oro", tint=0.14, raggio=2)
    d.testo(sp, L(ox, oy, 18, y + 3, CW - 18, CH - 23), tipografico(r["riquadro_carte"]), "PassoRiquadro", vj="center")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "Codice")


RIEPILOGO = [("Scontro", "retro_scontro"), ("Ricompense", "retro_ricompense"), ("Tessere «?»", "retro_tessere"),
             ("Sconfitta (0 PV)", "retro_sconfitta"), ("Mano", "retro_mano"), ("Vittoria", "retro_vittoria")]


def carta_aiuto_riepilogo(d, sp, ox, oy, r):
    """Carta Aiuto «Riepilogo» (carta a sé dalla v6-bis: era il retro della Carta Aiuto)."""
    cornice(d, sp, ox, oy, "Oro")
    par = [(r["retro_titolo"], "RiepTitolo")]
    for sez, campo in RIEPILOGO:
        par.append((sez.upper(), "RiepSez"))
        par += [(tipografico(riga), "RiepRiga") for riga in r[campo].split("\n")]
    d.testo(sp, L(ox, oy, 11.5, 11, CW - 11.5, CH - 10), "", "RiepRiga", paragrafi=par)


def divisore(d, sp, ox, oy, r, n):
    """n = carte del tipo nel kit, contate dai CSV in mazzi()."""
    col = TIPO_COLORE[r["codice"]]
    d.rett(sp, sangue(ox, oy), fill=col)
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, CH - SAFE), stroke="Carta", peso=0.8, raggio=4)
    d.testo(sp, L(ox, oy, 13, 18, CW - 13, 30), "DIVISORE", "DorsoSotto")
    d.testo(sp, L(ox, oy, 13, 60, CW - 13, 110), r["codice"], "DivCodice", vj="center")
    d.testo(sp, L(ox, oy, 13, 118, CW - 13, 138), r["titolo"], "DivTitolo", vj="center")
    d.testo(sp, L(ox, oy, 13, 142, CW - 13, 168), f"{r['contenuto_playtest']} · {n} carte", "DivSotto", vj="center")
    d.testo(sp, L(ox, oy, 110, CH - 19, CW - 14, CH - 11.5), r["id"], "CodiceChiaro")


# ---------------------------------------------------------------- dorsi

def dorso(d, sp, ox, oy, colore, titolo, sotto="", grande="", abb=""):
    """Dorso di un mazzo coperto; abb = etichetta minuscola nell'abbondanza in basso (sparisce col taglio)."""
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
    if abb:
        d.testo(sp, [ox + 14, oy + CH + 0.3 * MM, ox + CW - 14, oy + CH + B - 0.2 * MM], abb, "DorsoAbbondanza" + suf, vj="center")


def esegui(d, nome, titolo, descr):
    """Esporta il PDF e salva il progetto DesignCraft <nome>.designcraft. Si ferma se un testo non entra nel suo riquadro
    (overset nel preflight di DesignCraft): il PDF resta scritto per guardarlo, ma il kit non è valido."""
    d.cmd("file.exportPdf", path=str(PDF_DIR / f"{nome}.pdf"), standard="x4", title=titolo, bleed=False, marks=False)
    pf = d.cmd("preflight.run")
    with tempfile.TemporaryDirectory(prefix="goblin_carte_") as tmp:
        src = pathlib.Path(tmp) / f"{nome}.dcs"
        src.write_text(d.script(), encoding="utf-8")
        out = subprocess.run(["designcraft-cli", "script", str(src), "--save", str(DC_DIR / f"{nome}.designcraft")],
                             capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"{nome}: designcraft-cli ha fallito\n{out.stdout[-2000:]}\n{out.stderr[-2000:]}")
    res = json.loads(out.stdout)
    frame = {res["results"][i]["id"]: v for i, v in d.testi.items()}
    overset = [p["message"] + (f": foglio {frame[p['item']][0] + 1}, «{frame[p['item']][1]}…»" if p.get("item") in frame else "")
               for p in res["results"][pf]["issues"] if p["kind"] == "overset"]
    if overset:
        sys.exit(f"{nome}: testo che non entra nel riquadro (accorcialo nel CSV):\n  " + "\n  ".join(overset))
    print(f"{nome}.pdf: {descr}, {res['completed']} comandi")


def fogli_dorsi(carte):
    """Fogli dei fronti (da 0) con almeno un dorso: solo questi hanno una pagina in <nome>_retri.pdf, nello stesso ordine.
    Lo usa anche componenti_gen/gen.py per contare i fogli della prova di stampa."""
    return sorted({k // PER_FOGLIO for k, (_, rt) in enumerate(carte) if rt})


def costruisci(nome, titolo, carte):
    """carte: lista di (funzione_fronte, funzione_retro o None); PER_FOGLIO per foglio, un foglio per pagina, solo fronte.
    Scrive <nome>.pdf (fronti) e, se almeno una carta ha il dorso, <nome>_retri.pdf: il dorso della carta nella posizione p
    del foglio k sta nella posizione p della pagina dei retri «coi fronti del foglio k» (non specchiato); le carte senza
    dorso lasciano la cella vuota e i fogli di fronti senza nessun dorso non hanno la pagina dei retri (SOLO FRONTE)."""
    n = len(carte)
    fogli = (n + PER_FOGLIO - 1) // PER_FOGLIO
    fogli_r = fogli_dorsi(carte)
    pag_r = {sp: j for j, sp in enumerate(fogli_r)}       # foglio dei fronti -> pagina dei retri
    fronti = Doc(titolo, fogli)
    retri = Doc(titolo + " – retri", len(fogli_r)) if fogli_r else None
    occ_f = [[] for _ in range(fogli)]
    occ_r = [[] for _ in fogli_r]
    for k, (fr, rt) in enumerate(carte):
        sp = k // PER_FOGLIO
        ox, oy = origine(k % PER_FOGLIO)
        fr(fronti, sp, ox, oy)
        occ_f[sp].append((ox, oy))
        if rt:
            rt(retri, pag_r[sp], ox, oy)
            occ_r[pag_r[sp]].append((ox, oy))
    fronti.cmd("layer.new", name="Segni di taglio")
    for sp in range(fogli):
        lato = "FRONTI" if sp in pag_r else "SOLO FRONTE"
        segni_taglio(fronti, sp, f"{lato} · foglio {sp + 1} di {fogli}", f"{nome}.pdf · pag. {sp + 1}/{fogli}", occ_f[sp])
    esegui(fronti, nome, titolo, f"{n} carte, {fogli} fogli solo fronte")
    if fogli_r:
        nr = len(fogli_r)
        retri.cmd("layer.new", name="Segni di taglio")
        for j, sp in enumerate(fogli_r):
            segni_taglio(retri, j, f"RETRI · foglio {j + 1} di {nr} · coi fronti del foglio {sp + 1}",
                         f"{nome}_retri.pdf · pag. {j + 1}/{nr}", occ_r[j])
        esegui(retri, f"{nome}_retri", titolo + " – retri", f"{sum(map(len, occ_r))} dorsi, {nr} fogli solo fronte")


def mazzi():
    def f(fn, *a, **kw):
        return lambda d, sp, ox, oy: fn(d, sp, ox, oy, *a, **kw)

    righe_comuni = [carta_v7(r) for r in leggi("carte_comuni.csv")]
    comuni = [(f(carta_trama, r), f(dorso, "Retro", "Carta comune", abb=f"comune · {r['id']}")) for r in righe_comuni]

    # carte di classe: un CSV per classe in dati/classi/, unite nell'ordine di CLASSI, poi direzione A, B (sort stabile)
    per_classe = {}
    for p in sorted((DATI / "classi").glob("*.csv")):
        nome = next((c for c in CLASSI if c.lower() == p.stem.lower()), None)
        if nome is None:
            sys.exit(f"classi/{p.name}: classe sconosciuta (attese: {', '.join(CLASSI)})")
        per_classe[nome] = sorted((carta_v7(r, nome) for r in leggi(f"classi/{p.name}")),
                                  key=lambda r: r["direzione"] or "Z")
    classe = []
    for nome in CLASSI:
        for r in per_classe.get(nome, []):
            classe.append((f(carta_trama, r, nome),
                           f(dorso, nome, nome, "MAZZO DI CLASSE", abb=f"{nome} · {r['id']}")))
    ritratti = leggi("carte_classe_ritratto.csv")
    for r in ritratti:
        classe.append((f(carta_ritratto, r), None))          # un solo lato: sta scoperta sulla plancia eroe

    righe_specie = leggi("carte_specie.csv")
    specie = [(f(carta_specie, r), None) for r in righe_specie]

    righe_mostri = leggi("carte_mostro.csv")
    mostri = []
    for r in righe_mostri:
        num = r["mazzetto"][0]
        retro = f(dorso, "Notte", "Mostro", "MAZZETTO · BOSS" if num == "3" else "MAZZETTO", num,
                  abb=f"Mostro {num} · {r['id']}")
        mostri.append((f(carta_mostro, r), retro))

    impr = [(f(carta_imprevisto, r), f(dorso, "Imprevisto", "Imprevisto", abb=f"Imprevisto · {r['id']} · {r['copia']}"))
            for r in leggi("carte_imprevisto.csv")]

    aiuto = []
    for r in leggi("carte_aiuto.csv"):                      # ogni giocatore: «Il turno» e «Riepilogo», un lato ciascuna
        aiuto += [(f(carta_aiuto_turno, r), None), (f(carta_aiuto_riepilogo, r), None)]
    conta = {t: sum(r["tipo"] == t for r in righe_comuni) for t in TIPO_NOME}
    conta["TC"] = len(ritratti) + len(righe_specie)
    conta["NE"] = len(righe_mostri)
    aiuto += [(f(divisore, r, conta[r["codice"]]), None) for r in leggi("divisori.csv")]

    return {
        "carte_comuni": ("Il Tesoro del Goblin – carte comuni (playtest v7)", comuni),
        "carte_classe": ("Il Tesoro del Goblin – carte di classe (playtest v7)", classe),
        "carte_specie": ("Il Tesoro del Goblin – Carte Specie (playtest v7)", specie),
        "carte_mostro": ("Il Tesoro del Goblin – carte Mostro (playtest v7)", mostri),
        "carte_imprevisto": ("Il Tesoro del Goblin – carte Imprevisto (playtest v7)", impr),
        "carte_aiuto_divisori": ("Il Tesoro del Goblin – Carte Aiuto e Divisori (playtest v7)", aiuto),
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
