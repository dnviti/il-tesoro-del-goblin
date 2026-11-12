#!/usr/bin/env python3
"""Ritaglia e ricampiona le illustrazioni grezze (WebP) in PNG a 260 ppi della misura impaginata (PhotoCraft).

Uso: python3 prep_images.py spec.json  — {nome: [larghezza pt, altezza pt, fuoco x, fuoco y, scontorno]}"""
import json, math, os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'immagini')
RAW, OUT = ROOT + '/grezze', ROOT + '/png'
PPI = 260
# name: (placed width pt, placed height pt, focus x 0..1, focus y 0..1, cutout)
SPEC = json.load(open(sys.argv[1]))

def run(name, w, h, fx, fy, cut):
    src = f'{RAW}/{name}.webp'
    info = json.loads(subprocess.check_output(['photocraft-cli', 'info', src]))
    sw, sh = info['width'], info['height']
    a = w / h
    if sw / sh > a:
        cw, ch = round(sh * a), sh
    else:
        cw, ch = sw, round(sw / a)
    x = round((sw - cw) * fx); y = round((sh - ch) * fy)
    tw = math.ceil(w * PPI / 72); th = math.ceil(h * PPI / 72)
    args = ['photocraft-cli', 'run', src]
    if cut:
        args += ['--cmd', 'layer.removeBackground', '--params', '{}']
    args += ['--cmd', 'image.crop', '--params', json.dumps({"x": x, "y": y, "width": cw, "height": ch, "targetWidth": tw, "targetHeight": th,
                                                              "resample": "lanczos", "resolution": PPI}),
             '--out', f'{OUT}/{name}.png']
    r = subprocess.run(args, capture_output=True, text=True)
    print(name, (sw, sh), '->', (tw, th), 'crop', (x, y, cw, ch), 'upscale %.2f' % (tw / cw), r.returncode, r.stderr[-300:])

for n, v in SPEC.items():
    run(n, *v)
