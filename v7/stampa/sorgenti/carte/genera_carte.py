#!/usr/bin/env python3
"""Carte del playtest v7 «Il Tesoro del Goblin»: unione dati CSV -> DesignCraft.

Equivale a un Data Merge: legge i CSV in ../dati, scrive per ogni PDF uno script
di comandi DesignCraft (carte_*.dcs), lo esegue con `designcraft-cli script`,
salva il progetto modificabile (carte_*.designcraft) e il PDF in ../../playtest_v7.

Schema v7 delle carte comuni (dati/carte_comuni.csv) e di classe (dati/classi/<classe>.csv, un file per classe, uniti
nell'ordine di CLASSI e poi della direzione A/B): id, tipo (TE/TI/TM o Equipaggiamento/Incanto/Mappa), nome, classe
(nome della classe o «Tutte le classi»), direzione (solo carte di classe: A o B), pl (Equipaggiamenti: Comune 1, Rara 2,
Leggendaria 3; vuoto per Incanti e Mappe), rarita, slot, testo, testo_situazionale (la riga «Se…», stampata sotto il
testo), nota (non stampata; se contiene «segnaposto» la carta porta la scritta SEGNAPOSTO). La direzione apre la riga
del tipo, il PL sta in basso a destra sull'illustrazione. Il testo che non entra nel suo riquadro ferma lo script
(preflight di DesignCraft); con --tutti-overset lo script non si ferma al primo PDF ed elenca in fondo tutti i testi che
non entrano (id della carta, stile e caratteri in più), poi esce con errore.

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

Uso: python3 genera_carte.py [--solo NOME] [--formato A4|A3] [--dati CARTELLA] [--uscita CARTELLA] [--arte CARTELLA] [--senza-arte]
[--tutti-overset]   (richiede designcraft-cli)
--dati legge i CSV da un'altra cartella (per provare dati nuovi); --uscita scrive PDF e progetti .designcraft in un'altra
cartella, senza toccare playtest_v7*.

Impaginazione «alla Magic» (11/11): barra del nome in alto; sotto la finestra grande dell'illustrazione (54,5 mm di
larghezza; 38,1 mm di altezza sulle carte, 36 sui Mostri, 29,6 sui Boss, 42,3 sugli Imprevisti: ARTE_H, arte/formati.csv)
con la cornice nel colore del tipo; la riga del tipo (sui Mostri PV, ATT, AR e danno); il testo; un filetto e la battuta
in corsivo in fondo al testo; il piede (rarità o copia, classe, id).

Illustrazioni: se esiste ../arte/png/<id>.png (--arte legge da un'altra cartella), l'immagine riempie la finestra
dell'illustrazione (proporzionale, centrata, ritagliata) al posto del riquadro tinto e del codice segnaposto; il PL resta
sopra, le etichette (SEGNAPOSTO/PLAYTEST/PROVVISORIO/BOSS, MAZZO) su un cartellino pergamena. Carte Aiuto, Divisori e
dorsi non hanno illustrazione. --senza-arte stampa sempre il riquadro tinto (come senza immagini).
Le carte con più copie (colonna `copia` «n di m»: Specie, Imprevisti) prendono prima <id>-<n>.png, poi <id>.png.

Colonna facoltativa `battuta` (ultima colonna di ogni CSV di carte): una riga di colore, al massimo 70 caratteri e 2 righe,
in corsivo in fondo al testo della carta sotto un filetto (sui Mostri in corpo 6), 1 riga se entra, se no 2. Vuota o
assente: niente filetto e niente battuta.

Kit dei motivi (Daniele, 11/11: «leggero flavour steampunk medieval high magic, minimale, bordo leggero che dà spazio ai
contenuti»; lo stesso dei componenti, descritto in stampa/LEGGIMI.md): cornice nel colore del tipo con un filetto doppio
d'ottone (filo sottile fuori dal pannello e bordo del pannello), un piccolo ingranaggio su ogni angolo, rivetti agli angoli
della cornice dell'illustrazione, losanghe d'ottone alle estremità delle barre, losanga di rame al centro del filetto
della battuta; dorsi con l'emblema grande (ingranaggio, anello di rivetti, stella a 8 punte o il segno del mazzo) e il
nome del mazzo. Tutto sta nel bordo colorato o sui bordi delle cornici: riquadri di testo e d'illustrazione invariati.
"""
import csv
import functools
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import ImageFont

QUI = pathlib.Path(__file__).resolve().parent


def opzione(nome, predefinita):
    return pathlib.Path(sys.argv[sys.argv.index(nome) + 1]).resolve() if nome in sys.argv else predefinita


DATI = opzione("--dati", QUI.parent / "dati")
FORMATO = sys.argv[sys.argv.index("--formato") + 1].upper() if "--formato" in sys.argv else "A4"
if FORMATO not in ("A4", "A3"):
    sys.exit("--formato: A4 o A3")
PDF_DIR = opzione("--uscita", QUI.parent.parent / ("playtest_v7" if FORMATO == "A4" else "playtest_v7_A3"))
DC_DIR = PDF_DIR / "designcraft" if "--uscita" in sys.argv else (QUI if FORMATO == "A4" else QUI / "A3")
ARTE_DIR = opzione("--arte", QUI.parent / "arte" / "png")
SENZA_ARTE = "--senza-arte" in sys.argv

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
    "Blu": "#2f5d7c", "Carta": "#f9f2e0", "Pergamena": "#f1dcae", "OroChiaro": "#f6d68b",
    # kit dei motivi (11/11): ottone scuro sui fondi chiari, ottone chiaro sui fondi colorati, rame per gli accenti
    "Ottone": "#a8823a", "OttoneChiaro": "#e8cd8f", "Rame": "#a65a32",
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


# testo delle regole: valori «(+1)» in grassetto; «≤»/«≥» (Noto Serif non li ha, es. «D6 ≤ LV + 2» di TM-09) col font sans
GREP_TESTO = [{"style": "Valore", "pattern": "\\([+\u2011\u2212-]?\\d+\\)"}, {"style": "Simbolo", "pattern": "[\u2264\u2265]"}]


PARA = [
    ("Titolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    # nomi lunghi delle carte (es. TE-22, 30 caratteri) su una riga sola, come NomeNemicoStretto dei Mostri
    ("TitoloStretto", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 9, "leading": lead(12), "fill": "Inchiostro", "tracking": -10}),
    ("Etichetta", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    # v7: riga del tipo lunga (direzione · tipo · slot): corpo più piccolo, senza spaziatura
    ("EtichettaStretta", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 5.2, "leading": lead(7.5), "fill": "Marrone"}),
    ("EtichettaDx", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaCentro", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone", "tracking": 40}),
    ("EtichettaFoglio", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6.5, "leading": lead(7.5), "fill": "Marrone"}),
    # corpo del testo delle regole «alla Magic» (Daniele, 11/11): 7,8 pt su 9,3 (7 righe), perché l'illustrazione resti grande
    ("Testo", {"align": "left", "hyphenate": False, "grepStyles": GREP_TESTO},
     {"fontFamily": SERIF, "fontStyle": "Regular", "size": 7.8, "leading": lead(9.3), "fill": "Inchiostro"}),
    # v7: la riga «Se…» (testo_situazionale) sotto l'effetto base
    ("TestoSituazionale", {"align": "left", "hyphenate": False, "spaceBefore": 1.5, "grepStyles": GREP_TESTO},
     {"fontFamily": SERIF, "fontStyle": "Italic", "size": 7.8, "leading": lead(9.3), "fill": "Inchiostro"}),
    ("TestoCentro", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Regular", "size": 10.5, "leading": lead(13.5), "fill": "Inchiostro"}),
    ("Classi", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 7, "leading": lead(8), "fill": "Marrone"}),
    # v7: riga in fondo alla Carta Classe «Mano: 5 delle 20 carte di classe · le altre: pila di classe» (D27, Spec R 13.1)
    ("ClassiPiccolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 6.5, "leading": lead(8), "fill": "Marrone"}),
    ("Piede", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 6, "leading": lead(7), "fill": "Marrone"}),
    ("Nota", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.6, "leading": lead(9), "fill": "Marrone"}),
    ("Codice", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 20}),
    ("CodiceChiaro", {"align": "right"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Carta", "tracking": 20}),
    ("Provvisorio", {"align": "left"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6, "leading": lead(7), "fill": "Rosso", "tracking": 60}),
    ("Segnaposto", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 26, "leading": lead(28), "fill": "Carta"}),
    # v7: battuta (colonna facoltativa `battuta`) in fondo al testo sotto un filetto, al massimo 2 righe
    ("Battuta", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 6.6, "leading": lead(7.8), "fill": "Inchiostro"}),
    # v7: battuta dei Mostri, in fondo alla carta sotto le ricompense: 1 riga, 2 se non entra
    ("BattutaPiccola", {"align": "center", "hyphenate": False}, {"fontFamily": SERIF, "fontStyle": "Italic", "size": 6, "leading": lead(7), "fill": "Inchiostro"}),
    # v7: lettera della direzione nel tondo della riga del tipo e PL sull'illustrazione
    ("DirLettera", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 6.5, "leading": lead(7.5), "fill": "Carta"}),
    ("PL", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 7.5, "leading": lead(8.5), "fill": "Carta", "tracking": 40}),
    # nemici
    ("NomeNemico", {"align": "left"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 10.5, "leading": lead(12), "fill": "Inchiostro", "tracking": -5}),
    ("LetteraMed", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(16), "fill": "Lettera"}),
    ("StatNome", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "SemiBold", "size": 6, "leading": lead(7), "fill": "Marrone", "tracking": 40}),
    ("StatValore", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 14, "leading": lead(15), "fill": "Inchiostro"}),
    ("Danno", {"align": "center"}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.5, "leading": lead(9), "fill": "Inchiostro"}),
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
    # testo dei passi e del riquadro: 7,4 pt (era 8,3 fino al 12/11) perché sotto entrino gli Stati (D27)
    ("PassoTesto", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.4, "leading": lead(8.6), "fill": "Inchiostro"}),
    ("PassoRiquadro", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Grassetto", "pattern": "(Carte|Equipaggiamenti|Mano|Primo giro):"}]},
     {"fontFamily": SANS, "fontStyle": "Regular", "size": 7.4, "leading": lead(8.6), "fill": "Inchiostro"}),
    ("RiepTitolo", {"align": "center"}, {"fontFamily": SERIF, "fontStyle": "Bold", "size": 8.5, "leading": lead(9.5), "fill": "Inchiostro"}),
    ("RiepSez", {"align": "left", "spaceBefore": 1.6}, {"fontFamily": SANS, "fontStyle": "Bold", "size": 6.4, "leading": lead(7), "fill": "Rosso", "tracking": 40}),
    ("RiepRiga", {"align": "left", "hyphenate": False}, {"fontFamily": SANS, "fontStyle": "Regular", "size": 6.1, "leading": lead(6.8), "fill": "Inchiostro"}),
    # Stati sulla carta «Il turno» (D27: le tessere portano solo nome, icona e segno): nome e segno in grassetto
    ("StatoRiga", {"align": "left", "hyphenate": False, "grepStyles": [{"style": "Grassetto", "pattern": "^\\S+ \\([+\u2212]\\)"}]},
     {"fontFamily": SANS, "fontStyle": "Regular", "size": 6.1, "leading": lead(6.8), "fill": "Inchiostro"}),
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


def _ombra(h):
    """Colore dell'ingranaggio grande dei dorsi: il colore del mazzo scurito del 20 % (schiarito del 14 % se è quasi nero)."""
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    chiaro = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.12
    return "#" + "".join(f"{round(v + (255 - v) * 0.14 if chiaro else v * 0.8):02x}" for v in (r, g, b))


# swatch Ombra<colore> dei colori dei dorsi (carte comuni, classi, mostri, imprevisti)
SWATCH.update({"Ombra" + n: _ombra(SWATCH[n]) for n in ["Retro", "Notte", "Imprevisto", *CLASSI]})

CHAR = [
    ("Valore", {"fontFamily": SERIF, "fontStyle": "Bold"}),
    ("Grassetto", {"fontFamily": SANS, "fontStyle": "SemiBold"}),
    ("Simbolo", {"fontFamily": SANS, "fontStyle": "Regular"}),
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
        self.testi = {}            # indice del comando frame.create -> [foglio, inizio del testo, stile, id della carta]
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
        self.testi[i] = [sp, txt[:60].replace("\n", " / "), stile, None]
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

    def immagine(self, sp, r, percorso, raggio=0.0):
        """Immagine raster nel riquadro r: riempie proporzionalmente, centrata, ritagliata dal riquadro (anche negli angoli
        arrotondati). Nel progetto .designcraft l'immagine resta collegata al file (pannello Collegamenti)."""
        i = self.rett(sp, r, raggio=raggio)
        self.cmd("object.fittingOptions", fitting="fillProportionally", align=4, ids=[f"${i}.id"])
        self.cmd("file.place", path=str(percorso), frame=f"${i}.id")
        self.cmd("object.fit", mode="fillProportionally", ids=[f"${i}.id"])
        return i

    def linea(self, sp, a, b, swatch, peso):
        self.cmd("path.create", spread=sp, anchors=[{"p": [round(a[0], 3), round(a[1], 3)]}, {"p": [round(b[0], 3), round(b[1], 3)]}])
        self.cmd("object.stroke", swatch=swatch, weight=peso)

    def poligono(self, sp, pts, fill=None, stroke=None, peso=0.0):
        """Tracciato chiuso dai punti pts (ingranaggi, losanghe e stelle del kit dei motivi)."""
        i = self.cmd("path.create", spread=sp, anchors=[{"p": [round(x, 3), round(y, 3)]} for x, y in pts], closed=True)
        self.cmd("object.fill", swatch=fill or "[None]")
        if stroke:
            self.cmd("object.stroke", swatch=stroke, weight=peso, join="miter")
        else:
            self.cmd("object.stroke", swatch="[None]", weight=0)
        return i

    def script(self):
        return "\n".join(self.righe) + "\n"

    def carta(self, primo):
        """Dà a tutti i testi creati dal comando `primo` in poi (una carta) l'id stampato nel suo riquadro Codice."""
        nuovi = [v for i, v in self.testi.items() if i >= primo]
        id_ = next((v[1] for v in nuovi if v[2].startswith("Codice")), None)
        for v in nuovi:
            v[3] = id_


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


# ---------------------------------------------------------------- kit dei motivi (11/11)
# Uguale a componenti_gen/svg.py (sezione «kit dei motivi») e descritto in stampa/LEGGIMI.md. Misure in pt.
FILO = 1.6             # filo sottile d'ottone della cornice: SAFE - FILO dal rifilo (fuori dal pannello)
INGR_R = 3.2           # raggio esterno degli ingranaggi agli angoli del filo sottile (8 denti)
RIVETTO_R = 1.3        # rivetti agli angoli della cornice dell'illustrazione
EMBLEMA_Y, EMBLEMA_R = 102.0, 50.0   # centro (dal rifilo in alto) e raggio esterno dell'emblema dei dorsi


def ingranaggio_punti(cx, cy, r, denti, prof=0.28):
    """Contorno chiuso di un ingranaggio di raggio esterno r: `denti` denti trapezi profondi prof * r, il primo in alto
    (come svg.cog_pts() dei componenti)."""
    ri, s, pts = r * (1 - prof), 2 * math.pi / denti, []
    for k in range(denti):
        a = k * s - math.pi / 2
        for da, rr in ((-0.27, ri), (-0.15, r), (0.15, r), (0.27, ri)):
            pts.append((cx + rr * math.cos(a + da * s), cy + rr * math.sin(a + da * s)))
    return pts


def stella_punti(cx, cy, r, punte, rapporto=0.4):
    """Stella a `punte` punte (raggio interno r * rapporto), la prima in alto: l'accento arcano del kit."""
    return [(cx + (r if k % 2 == 0 else r * rapporto) * math.cos(math.pi * k / punte - math.pi / 2),
             cy + (r if k % 2 == 0 else r * rapporto) * math.sin(math.pi * k / punte - math.pi / 2)) for k in range(2 * punte)]


def ingranaggio(d, sp, cx, cy, r, denti, colore, foro=None, prof=0.28):
    """Ingranaggio pieno; foro: colore del tondo al centro (quello del fondo), None senza foro."""
    d.poligono(sp, ingranaggio_punti(cx, cy, r, denti, prof), fill=colore)
    if foro:
        d.rett(sp, [cx - 0.3 * r, cy - 0.3 * r, cx + 0.3 * r, cy + 0.3 * r], fill=foro, forma="ellipse")


def rivetto(d, sp, cx, cy, r=RIVETTO_R, colore="OttoneChiaro", bordo="Ottone"):
    d.rett(sp, [cx - r, cy - r, cx + r, cy + r], fill=colore, stroke=bordo, peso=0.3 if bordo else 0, forma="ellipse")


def losanga(d, sp, cx, cy, w, h, colore, bordo=None):
    d.poligono(sp, [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill=colore, stroke=bordo, peso=0.3)


def filetto_ornato(d, sp, x0, x1, y, col, peso=0.5, centro="Rame"):
    """Filetto (coordinate del foglio) interrotto al centro da una losanga 4,4 x 1,8 pt nel colore centro."""
    cx = (x0 + x1) / 2
    d.linea(sp, (x0, y), (cx - 4, y), col, peso)
    d.linea(sp, (cx + 4, y), (x1, y), col, peso)
    losanga(d, sp, cx, y, 4.4, 1.8, centro)


def angoli(ox, oy, m):
    """I 4 angoli del rettangolo a m pt dentro il rifilo."""
    return [(ox + x, oy + y) for x in (m, CW - m) for y in (m, CH - m)]


def cornice(d, sp, ox, oy, colore, fondo="Carta"):
    """Fronte: fondo e abbondanza nel colore del tipo; filo sottile OttoneChiaro FILO pt fuori dal pannello con un
    ingranaggio su ogni angolo (foro nel colore del tipo); pannello chiaro (da SAFE, come prima) col bordo Ottone."""
    d.rett(sp, sangue(ox, oy), fill=colore)
    f = SAFE - FILO
    d.rett(sp, [ox + f, oy + f, ox + CW - f, oy + CH - f], stroke="OttoneChiaro", peso=0.35, raggio=1.5)
    d.rett(sp, [ox + SAFE, oy + SAFE, ox + CW - SAFE, oy + CH - SAFE], fill=fondo, stroke="Ottone", peso=0.6, raggio=4)
    for x, y in angoli(ox, oy, f):
        ingranaggio(d, sp, x, y, INGR_R, 8, "OttoneChiaro", colore)


def cornice_piena(d, sp, ox, oy, colore, linea):
    """Dorsi e divisori: tutto nel colore del mazzo, filetto doppio nel colore linea e un ingranaggio su ogni angolo."""
    d.rett(sp, sangue(ox, oy), fill=colore)
    d.rett(sp, L(ox, oy, SAFE, SAFE, CW - SAFE, CH - SAFE), stroke=linea, peso=1.0, raggio=4)
    d.rett(sp, L(ox, oy, SAFE + 4, SAFE + 4, CW - SAFE - 4, CH - SAFE - 4), stroke=linea, peso=0.4, raggio=2)
    for x, y in angoli(ox, oy, SAFE + 1.2):
        ingranaggio(d, sp, x, y, 3.8, 8, linea, colore)


def L(ox, oy, x0, y0, x1, y1):
    return [ox + x0, oy + y0, ox + x1, oy + y1]


# ---------------------------------------------------------------- fronti

BATTUTA_MAX = 70   # caratteri (local v7_tono.md); le 2 righe le controlla il preflight

# Impaginazione «alla Magic» (Daniele, 11/11): barra del nome in alto; sotto la finestra grande dell'illustrazione, con la
# sua cornice nel colore del tipo; la riga del tipo; il testo (con la riga «Se…»); in fondo al testo un filetto e la
# battuta in corsivo; il piede. Misure in pt dall'angolo di rifilo; le immagini (arte/formati.csv) sono ARTE_W x ARTE_H.
BX = 11                            # barre del nome e del tipo e cornice dell'illustrazione: x BX..CW-BX
CORNICE = 1.0                      # spessore della cornice dell'illustrazione (dentro c'e' l'immagine)
TX = 13                            # testi: x TX..CW-TX (152,6 pt)
ARTE_W = CW - 2 * (BX + CORNICE)   # larghezza dell'immagine: 154,58 pt = 54,53 mm
# altezza dell'immagine per tipo di formati.csv: carte 38,1 mm (Mappe, Incanti, Equipaggiamenti, carte di classe, Carte
# Classe, Specie), Mostri 36 mm, Boss 29,6 mm (3 righe di ricompense), Imprevisti 42,3 mm (testo corto)
ARTE_H = {"carta": 108, "specie": 108, "mostro": 102, "boss": 84, "imprevisto": 120}
NOME_Y = (10, 23.5)                # barra del nome
ARTE_Y0 = 25                       # bordo alto della cornice dell'illustrazione
TIPO_H, TIPO_GAP = 10, 1.2         # barra del tipo, TIPO_GAP sotto la cornice e sopra il testo
PIEDE_Y = (CH - 17.5, CH - 10.5)   # piede: rarità o copia a sinistra, classe al centro, id a destra


def testo_battuta(r):
    """Battuta della carta (colonna facoltativa `battuta`), tipografica; "" se manca. Si ferma oltre BATTUTA_MAX caratteri."""
    t = (r.get("battuta") or "").strip()
    if len(t) > BATTUTA_MAX:
        sys.exit(f"{r['id']}: battuta di {len(t)} caratteri (massimo {BATTUTA_MAX}): «{t}»")
    return tipografico(t)


def arte(r):
    """File dell'illustrazione della carta, o None se manca o con --senza-arte. Le carte con più copie (colonna `copia`
    «n di m»: Specie, Imprevisti) cercano prima ARTE_DIR/<id>-<n>.png, poi ARTE_DIR/<id>.png."""
    if SENZA_ARTE:
        return None
    n = (r.get("copia") or "").split(" ")[0]
    for nome in ([f"{r['id']}-{n}.png"] if n.isdigit() else []) + [f"{r['id']}.png"]:
        if (ARTE_DIR / nome).is_file():
            return ARTE_DIR / nome
    return None


@functools.lru_cache(maxsize=None)
def _font(famiglia, stile):
    file = subprocess.run(["fc-match", "-f", "%{file}", f"{famiglia}:{stile.lower()}"], capture_output=True, text=True, check=True).stdout
    return ImageFont.truetype(file, 100)


def stile_car(stile):
    return next(ch for nome, _, ch in PARA if nome == stile)


def in_una_riga(t, stile, larghezza):
    """True se il testo t nello stile di paragrafo `stile` entra in una riga larga `larghezza` pt. Misura con il file del
    font di fontconfig (stesse larghezze di DesignCraft) più la spaziatura dello stile, con l'1,5 % di margine: se
    sbaglia, la riga in più va in overset e il preflight ferma lo script."""
    c = stile_car(stile)
    w = _font(c["fontFamily"], c["fontStyle"]).getlength(t) * c["size"] / 100 + len(t) * c["size"] * c.get("tracking", 0) / 1000
    return w * 1.015 <= larghezza


def barra(d, sp, ox, oy, y0, y1, col, pieno=False):
    """Barra del nome o del tipo, larga quanto la cornice dell'illustrazione: colore del tipo al 16 % (pieno: al 100 %),
    con una losanga d'ottone su ogni estremità (tra il pannello e il testo, che comincia a TX)."""
    d.rett(sp, L(ox, oy, BX, y0, CW - BX, y1), fill=col, tint=None if pieno else 0.16, stroke=None if pieno else col,
           peso=0.6, raggio=2)
    for x in (BX, CW - BX):
        losanga(d, sp, ox + x, oy + (y0 + y1) / 2, 2.6, 4.4, "OttoneChiaro", "Ottone")


def finestra_arte(d, sp, ox, oy, r, y0, formato, col, segnaposto=None):
    """Finestra dell'illustrazione dal bordo alto y0: cornice piena nel colore del tipo (col) e, a CORNICE dentro,
    l'immagine (arte(), riempie la finestra centrata) alta ARTE_H[formato]; senza immagine il riquadro tinto (col al 14 %)
    col codice segnaposto in grande; un rivetto d'ottone su ogni angolo della cornice. Ritorna il riquadro dell'immagine
    (x0, y0, x1, y1) in coordinate della carta."""
    box = (BX + CORNICE, y0 + CORNICE, CW - BX - CORNICE, y0 + CORNICE + ARTE_H[formato])
    d.rett(sp, L(ox, oy, BX, y0, CW - BX, box[3] + CORNICE), fill=col, raggio=2)
    img = arte(r)
    if img is not None:
        d.immagine(sp, L(ox, oy, *box), img)
    else:
        d.rett(sp, L(ox, oy, *box), fill=col, tint=0.14)
        if segnaposto:
            d.testo(sp, L(ox, oy, *box), segnaposto, "Segnaposto", vj="center")
    for x in (BX + 1.8, CW - BX - 1.8):
        for y in (y0 + 1.8, box[3] + CORNICE - 1.8):
            rivetto(d, sp, ox + x, oy + y)
    return box


def etichetta(d, sp, ox, oy, r, box, txt, stile):
    """Etichetta nel riquadro dell'illustrazione (SEGNAPOSTO/PLAYTEST/PROVVISORIO/BOSS rosse, MAZZO). Sull'immagine sta su
    un cartellino Pergamena largo quanto il testo (autoSize del riquadro di testo), altrimenti si legge male."""
    if arte(r) is None:
        d.testo(sp, L(ox, oy, *box), txt, stile)
        return
    x0, y0, x1, y1 = box
    i = d.testo(sp, L(ox, oy, x0 - 1.5, y0 - 0.5, x1 + 1.5, y1), txt, stile)
    rif = "topRight" if stile == "EtichettaDx" else "topLeft"
    d.cmd("object.textFrameOptions", inset=[0.5, 1.5, 0.5, 1.5], autoSize="widthOnly", autoSizeReference=rif, ids=[f"${i}.id"])
    d.cmd("object.fill", swatch="Pergamena", ids=[f"${i}.id"])
    # niente angoli arrotondati: object.cornerOptions su un riquadro di testo con autoSize lo stringe a 3 pt (overset)


def battuta_in_fondo(d, sp, ox, oy, r, y1, col, stile="Battuta"):
    """Battuta della carta in corsivo in fondo al testo, che finisce a y1, sotto un filetto sottile nel colore col: 1 riga
    se entra, se no 2 (una terza va in overset e ferma lo script). Ritorna dove deve finire il testo sopra (y1 se la
    carta non ha battuta)."""
    t = testo_battuta(r)
    if not t:
        return y1
    righe = 1 if in_una_riga(t, stile, CW - 2 * TX) else 2
    y0 = y1 - righe * stile_car(stile)["leading"]["value"]
    d.testo(sp, L(ox, oy, TX, y0, CW - TX, y1), t, stile, vj="bottom")
    # filetto poco sopra la battuta: le discendenti dell'ultima riga del testo escono di ~1,3 pt dal fondo del suo riquadro
    filetto_ornato(d, sp, ox + TX + 8, ox + CW - TX - 8, oy + y0 - 0.5, col)
    return y0 - 3.0


def piede(d, sp, ox, oy, sinistra, id_, classe="", stile_classe="Classi", stile_id="Codice"):
    """Piede della carta: rarità o copia a sinistra, classe al centro, id a destra (PIEDE_Y). Una classe troppo lunga
    per stare tra le altre due (la riga del mazzetto delle Carte Classe) va su una riga sua sopra. Ritorna dove deve
    finire il contenuto sopra il piede."""
    y0, y1 = PIEDE_Y
    if sinistra:
        d.testo(sp, L(ox, oy, TX, y0, CW / 2, y1), sinistra, "Piede", vj="bottom")
    d.testo(sp, L(ox, oy, CW / 2, y0, CW - TX, y1), id_, stile_id, vj="bottom")
    if not classe:
        return y0 - 1
    if in_una_riga(classe, stile_classe, CW - 2 * TX - 2 * 34):
        d.testo(sp, L(ox, oy, TX + 34, y0 - 1.5, CW - TX - 34, y1), classe, stile_classe, vj="bottom")
        return y0 - 1
    d.testo(sp, L(ox, oy, TX - 2, y0 - 8.5, CW - TX + 2, y0 - 0.5), classe, stile_classe, vj="bottom")
    return y0 - 9.5


def riga_tipo(d, sp, ox, oy, y0, col, testo, direzione=None):
    """Barra del tipo sotto l'illustrazione (Spec v7 §14.1): per le carte di classe comincia con la direzione, lettera
    nel tondo del colore della classe. Ritorna il bordo basso della barra."""
    y1 = y0 + TIPO_H
    barra(d, sp, ox, oy, y0, y1, col)
    x = TX
    if direzione:
        lettera, classe = direzione
        d.rett(sp, L(ox, oy, BX + 2, y0 + 1, BX + 10.5, y1 - 1), fill=classe, forma="ellipse")
        d.testo(sp, L(ox, oy, BX + 2, y0 + 1, BX + 10.5, y1 - 1), lettera, "DirLettera", vj="center")
        x = BX + 13
    d.testo(sp, L(ox, oy, x, y0, CW - TX, y1), testo, "Etichetta" if len(testo) <= 34 else "EtichettaStretta", vj="center")
    return y1


def carta_trama(d, sp, ox, oy, r, mazzo=None):
    """Fronte di Mappe, Incanti, Equipaggiamenti e Carte Classe. r: dizionario di carta_v7() o carta_ritratto().
    Dall'alto: barra del nome; illustrazione (finestra_arte) con in alto l'etichetta rossa (SEGNAPOSTO/PLAYTEST) e il
    mazzo, in basso a destra il PL; riga del tipo (riga_tipo: direzione, tipo, slot); testo: effetto base e riga «Se…»
    (corsivo); filetto e battuta; piede (rarità, classe, id)."""
    tipo = r["tipo"]
    col = TIPO_COLORE[tipo]
    cornice(d, sp, ox, oy, col)
    barra(d, sp, ox, oy, *NOME_Y, col)
    nome = tipografico(r["nome"])
    d.testo(sp, L(ox, oy, TX, NOME_Y[0], CW - TX, NOME_Y[1]), nome, "Titolo" if in_una_riga(nome, "Titolo", CW - 2 * TX) else "TitoloStretto", vj="center")
    x0, y0, x1, y1 = finestra_arte(d, sp, ox, oy, r, ARTE_Y0, "carta", col, tipo)
    if r.get("etichetta"):
        etichetta(d, sp, ox, oy, r, (x0 + 3, y0 + 2.5, x1 - 3, y0 + 10.5), r["etichetta"], "Provvisorio")
    if mazzo:
        etichetta(d, sp, ox, oy, r, (x0 + 46, y0 + 2.5, x1 - 3, y0 + 10.5), "MAZZO " + mazzo.upper(), "EtichettaDx")
    if r.get("pl"):
        d.rett(sp, L(ox, oy, x1 - 32, y1 - 14.5, x1 - 2.5, y1 - 2.5), fill="Oro", raggio=2)
        d.testo(sp, L(ox, oy, x1 - 32, y1 - 14.5, x1 - 2.5, y1 - 2.5), f"PL {r['pl']}", "PL", vj="center")
    sx = r["tipo_nome"].upper() + (" · " + r["slot"].upper() if r.get("slot") else "")
    direzione = None
    if r.get("direzione"):
        sx = r["dir_nome"].upper() + " · " + sx
        direzione = (r["direzione"], r["classe"])
        if len(sx) > 49:   # es. «ARMADIO A DUE ANTE · EQUIPAGGIAMENTO · ARMA DX / SCUDO»: il tipo si abbrevia
            sx = sx.replace("EQUIPAGGIAMENTO", "EQUIP.")
    y_tipo = riga_tipo(d, sp, ox, oy, y1 + CORNICE + TIPO_GAP, col, sx, direzione)
    y_fondo = piede(d, sp, ox, oy, r.get("rarita"), r["id"], r["classe_riga"], r.get("stile_classi", "Classi"))
    y_testo = battuta_in_fondo(d, sp, ox, oy, r, y_fondo, col)
    par = [(tipografico(r["testo"]), "Testo")]
    if r.get("testo_situazionale"):
        par.append((tipografico(r["testo_situazionale"]), "TestoSituazionale"))
    d.testo(sp, L(ox, oy, TX, y_tipo + TIPO_GAP, CW - TX, y_testo), "", "Testo", paragrafi=par)


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
    """Carta Specie (spec v6-bis §4.2): impaginazione della Carta Classe, colore della specie; testo: il bonus (corpo del
    testo) e la nota piccola, poi filetto e battuta; piede: copia e id."""
    col = r["specie"]
    cornice(d, sp, ox, oy, col)
    barra(d, sp, ox, oy, *NOME_Y, col)
    d.testo(sp, L(ox, oy, TX, NOME_Y[0], CW - TX, NOME_Y[1]), r["nome"], "Titolo", vj="center")
    x0, y0, x1, y1 = finestra_arte(d, sp, ox, oy, r, ARTE_Y0, "specie", col, "TS")
    if r["provvisorio"].strip():
        etichetta(d, sp, ox, oy, r, (x0 + 3, y0 + 2.5, x1 - 3, y0 + 10.5), "PROVVISORIO", "Provvisorio")
    y_tipo = riga_tipo(d, sp, ox, oy, y1 + CORNICE + TIPO_GAP, col, "CARTA SPECIE")
    y_testo = battuta_in_fondo(d, sp, ox, oy, r, piede(d, sp, ox, oy, r["copia"], r["id"]), col)
    par = [(tipografico(r["bonus"]), "Testo"), (tipografico(r["nota"]), "Nota")]
    d.testo(sp, L(ox, oy, TX, y_tipo + TIPO_GAP, CW - TX, y_testo), "", "Testo", paragrafi=par)


MOSTRO_Y0 = 33.5   # bordo alto della cornice dell'illustrazione dei Mostri, sotto medaglione, nome e riga del LV


def carta_mostro(d, sp, ox, oy, r):
    """Carta Mostro. In alto il medaglione con la lettera, il nome e la riga del LV e del mazzetto con l'id; illustrazione
    (Mostri ARTE_H["mostro"], Boss ARTE_H["boss"]: hanno 3 righe di ricompense; senza immagine il riquadro tinto, sui boss
    con «BOSS» in grande, con l'immagine «BOSS» è l'etichetta rossa); sotto, al posto della riga del tipo, PV, ATT, AR e
    danno; abilità (~170 caratteri, 5 righe); filetto e ricompense («Ricompense:», sui boss «Custode:» e «Mazzetto 3:»);
    filetto e battuta in corpo 6."""
    cornice(d, sp, ox, oy, "Notte", fondo="Pergamena")
    boss = r["mazzetto"].startswith("3")
    # medaglione su un ingranaggio a 16 denti (kit dei motivi): i denti escono di 1 pt dal bordo d'oro
    ingranaggio(d, sp, ox + BX + 11, oy + 21, 12, 16, "OroNemico", prof=0.1)
    d.rett(sp, L(ox, oy, BX, 10, BX + 22, 32), fill="Medaglione", stroke="OroNemico", peso=1.2, forma="ellipse")
    d.testo(sp, L(ox, oy, BX, 10, BX + 22, 32), r["lettera"], "LetteraMed", vj="center")
    d.testo(sp, L(ox, oy, BX + 25, 10, CW - BX, 22.5), tipografico(r["nome"]),
            "NomeNemico" if len(r["nome"]) <= 20 else "NomeNemicoStretto", vj="center")
    lv = f"LV {r['lv']} · MAZZETTO " + r["mazzetto"].upper().replace(" / ", " · ")
    d.testo(sp, L(ox, oy, BX + 25, 23, CW - BX, 31), lv, "Etichetta" if in_una_riga(lv, "Etichetta", CW - 2 * BX - 25 - 22)
            else "EtichettaStretta", vj="center")
    d.testo(sp, L(ox, oy, CW / 2, 23, CW - BX, 31), r["id"], "Codice", vj="center")
    x0, y0, x1, y1 = finestra_arte(d, sp, ox, oy, r, MOSTRO_Y0, "boss" if boss else "mostro", "Notte", "BOSS" if boss else None)
    if boss and arte(r):
        etichetta(d, sp, ox, oy, r, (x0 + 3, y0 + 2.5, x1 - 3, y0 + 10.5), "BOSS", "Provvisorio")
    # dalla sera dell'8/11 niente Difesa: si colpisce con 2D6 + ATT ≥ AR del bersaglio. Riquadri: nome a sinistra, valore
    ys0, ys1 = y1 + CORNICE + 1.5, y1 + CORNICE + 17.5
    stats = [("PV", r["pv"], "PV", 30), ("ATT", r["att"], "Inchiostro", 30), ("AR", r["ar"], "Scudo", 30),
             ("DANNO", r["danno"], "Marrone", CW - 2 * BX - 90 - 3 * 2.5)]
    x = BX
    for nome, val, colore, w in stats:
        d.rett(sp, L(ox, oy, x, ys0, x + w, ys1), fill="Carta", stroke=colore, peso=1.0, raggio=2)
        grande = nome != "DANNO"
        wn = 14 if grande else 25
        # il nome sta alto e le cifre basse nel loro interlinea: 0,8 pt giù il nome, 1,6 pt su il valore (il danno, in
        # corpo piccolo, sulla riga del nome)
        dy = -1.6 if grande else 0.8
        d.testo(sp, L(ox, oy, x + 1.5, ys0 + 0.8, x + wn, ys1 + 0.8), nome, "StatNome", vj="center")
        d.testo(sp, L(ox, oy, x + wn - 1, ys0 + dy, x + w - 1, ys1 + dy), val, "StatValore" if grande else "Danno", vj="center")
        x += w + 2.5
    y_ric1 = battuta_in_fondo(d, sp, ox, oy, r, CH - 10.5, "OroNemico", "BattutaPiccola")
    if boss:
        m3 = r["ricompensa_se_mazzetto_3"].replace("Forte Volontà", "Forte\u00a0Volontà")   # non spezzare il nome
        ric = [("Custode: " + r["ricompense"], "Ricompensa"), ("Mazzetto 3: " + m3, "Ricompensa")]
    else:
        ric = [("Ricompense: " + r["ricompense"], "Ricompensa")]
    # righe delle ricompense: 1 per paragrafo se entra (4 pt di margine per il nome in grassetto), se no 2
    righe = sum(1 if in_una_riga(t, "Ricompensa", CW - 2 * TX - 4) else 2 for t, _ in ric)
    y_ric0 = y_ric1 - righe * stile_car("Ricompensa")["leading"]["value"] - 0.5
    d.testo(sp, L(ox, oy, TX, y_ric0, CW - TX, y_ric1), "", "Ricompensa", paragrafi=ric, vj="bottom")
    d.linea(sp, (ox + BX, oy + y_ric0 - 1.5), (ox + CW - BX, oy + y_ric0 - 1.5), "OroNemico", 0.6)
    for x in (BX, CW - BX):
        rivetto(d, sp, ox + x, oy + y_ric0 - 1.5, 0.9, "OroNemico", None)
    d.testo(sp, L(ox, oy, TX, ys1 + 2, CW - TX, y_ric0 - 3), tipografico(r["abilita"]), "TestoNemico")


# colore dell'Imprevisto dal suo id (i nomi possono cambiare col tono v7); id nuovi: colore generico
IMPREVISTO_COLORE = {"IM-01": "Trappola", "IM-02": "Locanda", "IM-03": "Fonte", "IM-04": "Fabbro"}


def carta_imprevisto(d, sp, ox, oy, r):
    """Carta Imprevisto: barra del nome piena nel colore dell'Imprevisto, illustrazione grande, riga del tipo, testo
    centrato, filetto e battuta, piede (copia e id)."""
    cornice(d, sp, ox, oy, "Imprevisto")
    col = IMPREVISTO_COLORE.get(r["id"], "Imprevisto")
    barra(d, sp, ox, oy, NOME_Y[0], 26, col, pieno=True)
    d.testo(sp, L(ox, oy, TX, NOME_Y[0], CW - TX, 26), r["nome"], "TitoloChiaro", vj="center")
    x0, y0, x1, y1 = finestra_arte(d, sp, ox, oy, r, 27.5, "imprevisto", col, "?")
    y_tipo = riga_tipo(d, sp, ox, oy, y1 + CORNICE + TIPO_GAP, col, "IMPREVISTO")
    y_testo = battuta_in_fondo(d, sp, ox, oy, r, piede(d, sp, ox, oy, r["copia"], r["id"]), col)
    testo = (r.get("testo_bozza") or "").strip() or r["testo"]
    d.testo(sp, L(ox, oy, TX + 1, y_tipo + TIPO_GAP, CW - TX - 1, y_testo), tipografico(testo), "TestoCentro", vj="center")


def righe_testo(t, stile, larghezza):
    """Righe che il testo t occupa nello stile di paragrafo `stile` in un riquadro largo `larghezza` pt: a capo tra le
    parole, con le misure (e il margine) di in_una_riga."""
    n, riga = 1, ""
    for parola in t.split():
        prova = f"{riga} {parola}" if riga else parola
        if riga and not in_una_riga(prova, stile, larghezza):
            n, riga = n + 1, parola
        else:
            riga = prova
    return n


def carta_aiuto_turno(d, sp, ox, oy, r):
    """Carta Aiuto «Il turno» (Spec v7 §4.0; D27: niente pesca, il turno comincia da Muovi): i 3 passi numerati, il
    riquadro senza numero su quando si giocano le carte e, in fondo, gli Stati (R 9.1): la regola del verso e l'effetto di
    ognuno da stati.csv, prima quelli che aiutano (+), perché le tessere Stato portano solo nome, icona e segno. Le altezze
    di passi e riquadro vengono dalle righe misurate (righe_testo); gli Stati prendono lo spazio che resta."""
    cornice(d, sp, ox, oy, "Oro")
    d.testo(sp, L(ox, oy, 13, 11, CW - 13, 25), r["fronte_titolo"], "Titolo", vj="center")
    filetto_ornato(d, sp, ox + 14, ox + CW - 14, oy + 27, "Oro", 0.6)
    passo = stile_car("PassoTesto")["leading"]["value"]
    y = 29
    for num in "123":
        testo = tipografico(r[f"passo{num}_testo"])
        h = 9.5 + righe_testo(testo, "PassoTesto", CW - 14 - 34) * passo
        d.rett(sp, L(ox, oy, 15, y + 1, 29, y + 15), fill="Oro", forma="ellipse")
        d.testo(sp, L(ox, oy, 15, y + 1, 29, y + 15), num, "PassoNum", vj="center")
        d.testo(sp, L(ox, oy, 34, y + 0.5, CW - 14, y + 10.5), r[f"passo{num}_nome"], "PassoNome")
        d.testo(sp, L(ox, oy, 34, y + 9.5, CW - 14, y + h + 1.5), testo, "PassoTesto")
        y += h + 1
    # riquadro senza numero: quando si giocano le carte (non è un passo)
    testo = tipografico(r["riquadro_carte"])
    h = righe_testo(testo, "PassoRiquadro", CW - 32) * stile_car("PassoRiquadro")["leading"]["value"] + 3.5
    d.rett(sp, L(ox, oy, 13, y + 1, CW - 13, y + 1 + h), fill="Oro", tint=0.14, raggio=2)
    d.testo(sp, L(ox, oy, 16, y + 1.5, CW - 16, y + h + 0.5), testo, "PassoRiquadro", vj="center")
    stati = sorted(leggi("stati.csv"), key=lambda s: s["segno"] != "+")
    par = [(r["stati_nome"].upper(), "RiepSez"), (tipografico(r["stati_testo"]), "RiepRiga")]
    par += [(f"{s['nome']} ({s['segno']}) {tipografico(s['testo'])}", "StatoRiga") for s in stati]
    d.testo(sp, L(ox, oy, 14, y + h + 1.5, CW - 14, CH - 17.5), "", "RiepRiga", paragrafi=par)
    d.testo(sp, L(ox, oy, 110, CH - 17.5, CW - 14, CH - 10.5), r["id"], "Codice")


RIEPILOGO = [("Scontro", "retro_scontro"), ("Ricompense", "retro_ricompense"), ("Tessere Esplorazione", "retro_tessere"),
             ("Sconfitta (Danni = PV)", "retro_sconfitta"), ("Mano", "retro_mano"), ("Vittoria", "retro_vittoria")]


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
    cornice_piena(d, sp, ox, oy, col, "OttoneChiaro")
    filetto_ornato(d, sp, ox + 40, ox + CW - 40, oy + 40, "OttoneChiaro", 0.4, "OttoneChiaro")
    filetto_ornato(d, sp, ox + 40, ox + CW - 40, oy + 178, "OttoneChiaro", 0.4, "OttoneChiaro")
    d.testo(sp, L(ox, oy, 13, 18, CW - 13, 30), "DIVISORE", "DorsoSotto")
    d.testo(sp, L(ox, oy, 13, 60, CW - 13, 110), r["codice"], "DivCodice", vj="center")
    d.testo(sp, L(ox, oy, 13, 118, CW - 13, 138), r["titolo"], "DivTitolo", vj="center")
    d.testo(sp, L(ox, oy, 13, 142, CW - 13, 168), f"{r['contenuto_playtest']} · {n} carte", "DivSotto", vj="center")
    # id dentro il filetto doppio della cornice (il filo interno sta a SAFE + 4)
    d.testo(sp, L(ox, oy, 110, CH - 24, CW - 17, CH - 16.5), r["id"], "CodiceChiaro")


# ---------------------------------------------------------------- dorsi

def emblema(d, sp, ox, oy, linea, ombra, stella=True):
    """Emblema dei dorsi, centrato a EMBLEMA_Y: ingranaggio a 14 denti (pieno nel colore ombra, bordo linea), anello
    interno, un rivetto sotto ogni dente e, con stella, la stella arcana a 8 punte con il tondo al centro (senza stella il
    centro resta libero per il segno grande del mazzo)."""
    cx, cy, R = ox + CW / 2, oy + EMBLEMA_Y, EMBLEMA_R
    d.poligono(sp, ingranaggio_punti(cx, cy, R, 14, 0.12), fill=ombra, stroke=linea, peso=0.9)
    ri = 0.76 * R
    d.rett(sp, [cx - ri, cy - ri, cx + ri, cy + ri], stroke=linea, peso=0.5, forma="ellipse")
    for k in range(14):
        a = 2 * math.pi * k / 14 - math.pi / 2
        rivetto(d, sp, cx + 0.82 * R * math.cos(a), cy + 0.82 * R * math.sin(a), 0.9, linea, None)
    if stella:
        d.poligono(sp, stella_punti(cx, cy, 0.6 * R, 8, 0.42), stroke=linea, peso=0.6)
        d.rett(sp, [cx - 4, cy - 4, cx + 4, cy + 4], fill=linea, forma="ellipse")


def dorso(d, sp, ox, oy, colore, titolo, sotto="", grande="", abb=""):
    """Dorso di un mazzo coperto (kit dei motivi, 11/11): cornice_piena, marchio e filetto in alto, emblema grande al
    centro con la stella o il segno grande del mazzo (numero del mazzetto, «?»), sotto il nome del mazzo e la riga
    piccola; abb = etichetta minuscola nell'abbondanza in basso (sparisce col taglio)."""
    scuro = colore in DORSO_CHIARO
    inch, suf = ("Retro", "Scuro") if scuro else ("OroChiaro", "")
    cornice_piena(d, sp, ox, oy, colore, inch)
    d.testo(sp, L(ox, oy, 16, 24, CW - 16, 34), "IL TESORO DEL GOBLIN", "DorsoMarchio" + suf)
    filetto_ornato(d, sp, ox + 44, ox + CW - 44, oy + 40, inch, 0.4, inch)
    emblema(d, sp, ox, oy, inch, "Ombra" + colore, stella=not grande)
    if grande:
        d.testo(sp, L(ox, oy, 16, EMBLEMA_Y - 35, CW - 16, EMBLEMA_Y + 35), grande, "DorsoGrande" + suf, vj="center")
    d.testo(sp, L(ox, oy, 16, 158, CW - 16, 198), titolo, "DorsoTitolo" + suf, vj="center")
    if sotto:
        d.testo(sp, L(ox, oy, 16, CH - 40, CW - 16, CH - 26), sotto, "DorsoSotto" + suf, vj="center")
    if abb:
        d.testo(sp, [ox + 14, oy + CH + 0.3 * MM, ox + CW - 14, oy + CH + B - 0.2 * MM], abb, "DorsoAbbondanza" + suf, vj="center")


TUTTI_OVERSET = "--tutti-overset" in sys.argv
OVERSET = []   # con --tutti-overset: i testi che non entrano di tutti i PDF, elencati in fondo


def esegui(d, nome, titolo, descr):
    """Esporta il PDF e salva il progetto DesignCraft <nome>.designcraft. Si ferma se un testo non entra nel suo riquadro
    (overset nel preflight di DesignCraft): il PDF resta scritto per guardarlo, ma il kit non è valido. Con
    --tutti-overset non si ferma: raccoglie i testi in OVERSET e va avanti col PDF dopo."""
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
    overset = []
    for p in res["results"][pf]["issues"]:
        if p["kind"] != "overset":
            continue
        n = re.search(r"(\d+) characters?", p["message"])
        msg = f"{n.group(1)} caratteri in più" if n else p["message"]
        if p.get("item") in frame:
            sp, inizio, stile, id_ = frame[p["item"]]
            msg = f"{id_ or '?'} [{stile}]: {msg}, foglio {sp + 1}, «{inizio}…»"
        overset.append(msg)
    if overset and not TUTTI_OVERSET:
        sys.exit(f"{nome}: testo che non entra nel riquadro (accorcialo nel CSV):\n  " + "\n  ".join(overset))
    OVERSET.extend(f"{nome}: {m}" for m in overset)
    print(f"{nome}.pdf: {descr}, {res['completed']} comandi" + (f", {len(overset)} testi che non entrano" if overset else ""))


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
        primo = len(fronti.righe)
        fr(fronti, sp, ox, oy)
        fronti.carta(primo)
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

    impr = [(f(carta_imprevisto, r), f(dorso, "Imprevisto", "Imprevisto", grande="?",
                                         abb=f"Imprevisto · {r['id']} · {r['copia']}"))
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
    if OVERSET:
        sys.exit(f"{len(OVERSET)} testi che non entrano nel riquadro (accorciali nel CSV):\n  " + "\n  ".join(OVERSET))
