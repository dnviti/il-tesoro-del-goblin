import sys, json, math
sys.path.insert(0,'/mnt/project-files/tesoro-goblin/sorgenti/regolamento_stampa/book')
from svg import board, icon, INK, BROWN, RED, GOLD, BLUE, PAPER
W=26
svgb=board(W=W)
R=W/math.sqrt(3); step=1.5*R
mapw=W*10.5; maph=9*step+2*R; pad=W*1.8; top=W*4.5; bottom=W*4.3
bw=mapw+2*pad; bh=maph+top+bottom
yb=top+maph+W*0.9
gx=W*0.6; gy=yb+W*1.85; g0=bw/2-10*gx+W*0.6
bx=W*0.62; ty=W*3.25; x0=bw/2-7*bx+W*1.3
geom=dict(W=W,R=R,step=step,X0=pad,Y0=top,bw=bw,bh=bh,
  giro=dict(g0=g0,gy=gy,gx=gx), pvt=dict(x0=x0,ty=ty,bx=bx),
  sala=dict(cy=W*1.75, xs=[bw/2+(i-2.5)*W*2.3 for i in range(6)]))
icons={k:icon(k,12,12,1,c) for k,c in [('cuore',RED),('spade',INK),('scudo',BLUE),('stivale',BROWN),('stella',GOLD),('pergamena',INK),('clessidra',INK),('forziere',INK),('teschio',RED),('trappola',INK),('piedi',BROWN),('casa','#c0662b'),('goccia','#2f7a8a'),('martello','#4a5568'),('dado','#7a3e8e'),('carte',BROWN),('occhio',BROWN),('bandiera',BROWN),('elmo',BROWN),('cripta',GOLD)]}
html=open('page.html').read().replace('const MG=null;/*MG*/','const MG='+open('../suno/mg_mimi.json').read()+';/*MG*/').replace('/*GEOM*/', 'const GEOM='+json.dumps(geom)+';const ICONS='+json.dumps(icons)+';').replace('<!--BOARD-->', svgb.replace('<svg ', '<svg id="bsvg" ',1))
open('index.html','w').write(html)
print(json.dumps(geom))
