#!/usr/bin/env python3
"""Rifinitura delle illustrazioni v7 con PhotoCraft: grezze/<id>.png -> pcraft/<id>.pcraft + png/<id>.png.

Per ogni illustrazione (tutto con `photocraft-cli`, nessun pixel ritoccato a mano):
  1. `convert` della grezza in un progetto .pcraft (livello «Immagine grezza»);
  2. un solo `run`: ritaglio centrato al rapporto del riquadro + misura in px a 300 ppi (image.crop con targetWidth/Height,
     bicubico), poi due livelli di regolazione uguali per tutte le immagini («Curve tono e calore», «Tonalita e saturazione»);
  3. `convert` del progetto in png/<id>.png (300 ppi, sRGB, SENZA profilo ICC incorporato: DesignCraft lo scarta nel PDF/X-4
     e la validazione fallisce; il chunk iCCP viene tolto dal png, i pixel restano invariati);
I due file sono scritti in una cartella temporanea e spostati solo a lavoro finito: un errore non lascia mezzi file.

Uso (da qualsiasi cartella):
  python3 elabora.py <id> --tipo <tipo>      un'illustrazione; --tipo si puo' omettere se il prefisso dell'id lo dice
  python3 elabora.py <id> [<id> ...]          piu' illustrazioni
  python3 elabora.py --tutti [--forza]        ogni grezze/*.png il cui tipo e' noto; salta quelle gia' fatte (pcraft e png
                                              presenti) salvo --forza; quelle senza tipo sono elencate e saltate
  python3 elabora.py --elenco-tipi            tipi e misure da formati.csv
  python3 elabora.py --pulisci-png            toglie l'ICC dai png/*.png gia' esportati (senza rifare i progetti)

Ritaglio verticale/orizzontale: di norma centrato. Per un id solo: --alto / --basso / --sinistra / --destra (o
--posizione-x/--posizione-y con un numero 0..1; 0 = bordo alto/sinistro, 1 = basso/destro). Per tutti gli id:
ritagli.csv (colonne `id,tipo,orizzontale,verticale`; i valori sono sinistra|centro|destra, alto|centro|basso o un numero
0..1; `tipo` forza il tipo di un id senza prefisso noto; colonne vuote = centrato). Priorita': riga di comando, ritagli.csv, centro.

Tipo dall'id (prefisso): TM TI TE CA CG CO CR CS TC -> carta; TS -> specie; NE -> mostro; IM -> imprevisto;
PD -> pedina_boss o pedina_eroe secondo dati/pedine.csv (tipo «boss…»); PB -> plancia_eroe; PG -> plancia; PT -> terreno;
PS -> sala.
Misure: formati.csv. Richiede photocraft-cli (0.22).
"""
import argparse
import csv
import json
import pathlib
import shutil
import subprocess
import sys
import struct
import tempfile
import time

QUI = pathlib.Path(__file__).resolve().parent
GREZZE, PCRAFT, PNG = QUI / "grezze", QUI / "pcraft", QUI / "png"
FORMATI, RITAGLI = QUI / "formati.csv", QUI / "ritagli.csv"
PEDINE = QUI.parent / "dati" / "pedine.csv"
PPI = 300

PREFISSI = {"TM": "carta", "TI": "carta", "TE": "carta", "CA": "carta", "CG": "carta", "CO": "carta", "CR": "carta",
            "CS": "carta", "TC": "carta", "TS": "specie", "NE": "mostro", "IM": "imprevisto", "PB": "plancia_eroe",
            "PG": "plancia", "PT": "terreno", "PS": "sala"}

# Look condiviso, identico per tutte le immagini: lieve, solo per uniformare tono e calore (carta/pergamena).
# Curve: nero appena alzato, mezzitoni piu' netti di un soffio; rosso +3 e blu -3 sui mezzitoni = calore costante.
CURVE = {"points": [[0, 3], [64, 60], [192, 196], [255, 253]],
         "red": [[0, 0], [128, 131], [255, 255]], "blue": [[0, 0], [128, 125], [255, 255]],
         "name": "Curve tono e calore"}
TONALITA = {"saturation": -3, "name": "Tonalita e saturazione"}


def leggi(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def formati():
    return {r["tipo"]: r for r in leggi(FORMATI)}


def posizione(valore, parole):
    """sinistra|centro|destra (o alto|centro|basso) o numero 0..1 -> frazione; vuoto -> None."""
    v = (valore or "").strip().lower()
    if not v:
        return None
    if v in parole:
        return parole[v]
    try:
        f = float(v.replace(",", "."))
    except ValueError:
        sys.exit(f"posizione «{valore}» non valida (attese: {', '.join(parole)} o un numero 0..1)")
    if not 0 <= f <= 1:
        sys.exit(f"posizione {f} fuori da 0..1")
    return f


X_PAROLE = {"sinistra": 0.0, "centro": 0.5, "destra": 1.0}
Y_PAROLE = {"alto": 0.0, "centro": 0.5, "basso": 1.0}


def tipo_da_id(i):
    pref = i.split("-")[0].upper()
    if pref == "PD":
        for r in leggi(PEDINE):
            if r["id"] == i:
                return "pedina_boss" if r["tipo"].startswith("boss") else "pedina_eroe"
        return None
    return PREFISSI.get(pref)


def senza_icc(path):
    """Toglie il chunk iCCP dal PNG (pixel e altri chunk invariati). Le immagini sono sRGB; DesignCraft scarta il profilo
    nel PDF/X-4 e la validazione fallisce se il PNG ne porta uno incorporato. Ritorna 1 se l'ha tolto, 0 se non c'era."""
    dati = pathlib.Path(path).read_bytes()
    if dati[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"{path}: non e' un PNG")
    out, i, tolto = [dati[:8]], 8, 0
    while i < len(dati):
        n, tipo = struct.unpack(">I4s", dati[i:i + 8])
        if tipo == b"iCCP":
            tolto = 1
        else:
            out.append(dati[i:i + 12 + n])
        i += 12 + n
    if tolto:
        pathlib.Path(path).write_bytes(b"".join(out))
    return tolto


def photocraft(*args):
    p = subprocess.run(["photocraft-cli", *map(str, args)], capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"photocraft-cli {' '.join(map(str, args[:2]))} ha fallito:\n{p.stdout}{p.stderr}")
    return p.stdout


def elabora(i, fmt, fx, fy):
    """Una illustrazione. Ritorna (ingrandimento, dimensioni pcraft, dimensioni png)."""
    grezza = GREZZE / f"{i}.png"
    if not grezza.is_file():
        sys.exit(f"{i}: manca {grezza}")
    W, H = int(fmt["larghezza_px"]), int(fmt["altezza_px"])
    with tempfile.TemporaryDirectory(prefix="goblin_arte_") as tmp:
        tmp = pathlib.Path(tmp)
        pc, png = tmp / f"{i}.pcraft", tmp / f"{i}.png"
        photocraft("convert", grezza, pc)
        info = json.loads(photocraft("info", pc))
        sw, sh = info["width"], info["height"]
        # ritaglio al rapporto del riquadro, il piu' grande possibile, posizionato da fx/fy (0..1)
        if sw * H >= sh * W:
            ch, cw = sh, round(sh * W / H)
        else:
            cw, ch = sw, round(sw * H / W)
        x, y = round((sw - cw) * fx), round((sh - ch) * fy)
        ingrandimento = W / cw
        photocraft(
            "run", pc,
            "--cmd", "layer.renameLayer", "--params", json.dumps({"name": "Immagine grezza"}),
            "--cmd", "image.crop", "--params", json.dumps({
                "x": x, "y": y, "width": cw, "height": ch, "targetWidth": W, "targetHeight": H,
                "resolution": PPI, "resample": "bicubic"}),
            "--cmd", "layer.newAdjustmentLayer.curves", "--params", json.dumps(CURVE),
            "--cmd", "layer.newAdjustmentLayer.hueSaturation", "--params", json.dumps(TONALITA),
            "--out", pc, "--in-place")
        photocraft("convert", pc, png)
        senza_icc(png)
        PCRAFT.mkdir(exist_ok=True)
        PNG.mkdir(exist_ok=True)
        shutil.move(str(pc), PCRAFT / f"{i}.pcraft")
        shutil.move(str(png), PNG / f"{i}.png")
    return ingrandimento, (PCRAFT / f"{i}.pcraft").stat().st_size, (PNG / f"{i}.png").stat().st_size


def main():
    ap = argparse.ArgumentParser(description="grezze/<id>.png -> pcraft/<id>.pcraft + png/<id>.png (PhotoCraft)")
    ap.add_argument("id", nargs="*", help="id delle illustrazioni (nome del file in grezze/ senza .png)")
    ap.add_argument("--tipo", help="tipo di formati.csv (vale per tutti gli id dati)")
    ap.add_argument("--tutti", action="store_true", help="ogni grezze/*.png con tipo noto, salta le gia' fatte")
    ap.add_argument("--forza", action="store_true", help="con --tutti: rifa' anche le gia' fatte")
    ap.add_argument("--elenco-tipi", action="store_true", help="stampa i tipi e le misure")
    ap.add_argument("--pulisci-png", action="store_true", help="toglie il profilo ICC dai png/*.png gia' esportati")
    ap.add_argument("--alto", action="store_true")
    ap.add_argument("--basso", action="store_true")
    ap.add_argument("--sinistra", action="store_true")
    ap.add_argument("--destra", action="store_true")
    ap.add_argument("--posizione-x", help="0..1 (0 sinistra, 1 destra)")
    ap.add_argument("--posizione-y", help="0..1 (0 alto, 1 basso)")
    a = ap.parse_args()

    fm = formati()
    if a.pulisci_png:
        n = sum(senza_icc(p) for p in sorted(PNG.glob("*.png")))
        print(f"profilo ICC tolto da {n} png")
        return
    if a.elenco_tipi:
        for t, r in fm.items():
            print(f"{t:14s} {r['larghezza_mm']} x {r['altezza_mm']} mm = {r['larghezza_px']} x {r['altezza_px']} px")
        return
    if bool(a.id) == a.tutti:
        ap.error("dare uno o piu' id oppure --tutti")
    if a.tipo and a.tipo not in fm:
        sys.exit(f"tipo «{a.tipo}» sconosciuto (formati.csv: {', '.join(fm)})")
    if a.alto and a.basso or a.sinistra and a.destra:
        ap.error("--alto/--basso e --sinistra/--destra si escludono a vicenda")
    cli_x = posizione(a.posizione_x, X_PAROLE) if a.posizione_x else (0.0 if a.sinistra else 1.0 if a.destra else None)
    cli_y = posizione(a.posizione_y, Y_PAROLE) if a.posizione_y else (0.0 if a.alto else 1.0 if a.basso else None)

    ritagli = {r["id"]: r for r in leggi(RITAGLI)} if RITAGLI.is_file() else {}
    ids = sorted(p.stem for p in GREZZE.glob("*.png")) if a.tutti else a.id
    fatte = saltate = 0
    senza_tipo = []
    for i in ids:
        r = ritagli.get(i, {})
        tipo = a.tipo or (r.get("tipo") or "").strip() or tipo_da_id(i)
        if not tipo:
            senza_tipo.append(i)
            continue
        if tipo not in fm:
            sys.exit(f"{i}: tipo «{tipo}» sconosciuto (formati.csv: {', '.join(fm)})")
        if a.tutti and not a.forza and (PCRAFT / f"{i}.pcraft").is_file() and (PNG / f"{i}.png").is_file():
            saltate += 1
            continue
        fx = cli_x if cli_x is not None else posizione(r.get("orizzontale"), X_PAROLE)
        fy = cli_y if cli_y is not None else posizione(r.get("verticale"), Y_PAROLE)
        t0 = time.monotonic()
        ingr, sp, sg = elabora(i, fm[tipo], 0.5 if fx is None else fx, 0.5 if fy is None else fy)
        avviso = f"  ATTENZIONE: ingrandita x{ingr:.2f}" if ingr > 1.0 else ""
        print(f"{i} [{tipo}] {fm[tipo]['larghezza_px']}x{fm[tipo]['altezza_px']} px  pcraft {sp / 1024:.0f} KB  "
              f"png {sg / 1024:.0f} KB  {time.monotonic() - t0:.2f} s{avviso}")
        fatte += 1
    if a.tutti:
        print(f"fatte {fatte}, gia' fatte (saltate) {saltate}, senza tipo {len(senza_tipo)}")
    if senza_tipo:
        print("senza tipo (dare --tipo o una riga con `tipo` in ritagli.csv):", ", ".join(senza_tipo), file=sys.stderr)
        if not a.tutti:
            sys.exit(1)


if __name__ == "__main__":
    main()
