#!/bin/bash
# uso: ./mkpdf.sh file.html out.pdf larghezza altezza  (poi TrimBox a 3 mm)
cd "$(dirname "$0")"; export NODE_PATH=${NODE_PATH:-$(npm root -g)}
node render.js "$PWD/$1" "$2.tmp.pdf" "$3" "$4" && python3 -c "
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
r=PdfReader(sys.argv[1]); w=PdfWriter(); m=3*72/25.4
for p in r.pages:
    b=p.mediabox; p.trimbox=RectangleObject([m,m,float(b.width)-m,float(b.height)-m]); p.bleedbox=RectangleObject([0,0,float(b.width),float(b.height)]); w.add_page(p)
w.write(sys.argv[2])" "$2.tmp.pdf" "$2" && rm "$2.tmp.pdf"
