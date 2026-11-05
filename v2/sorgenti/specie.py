import re, sys
M = {'razza': 'specie', 'razze': 'specie', 'Razza': 'Specie', 'Razze': 'Specie', 'RAZZA': 'SPECIE', 'RAZZE': 'SPECIE'}
def fix(s): return re.sub(r'\b(razz[ae]|Razz[ae]|RAZZ[AE])\b', lambda m: M[m.group(1)], s)
if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p).read(); t = fix(s)
        if s != t: open(p, 'w').write(t); print(p, len(re.findall(r'\b(razz[ae]|Razz[ae]|RAZZ[AE])\b', s)))
