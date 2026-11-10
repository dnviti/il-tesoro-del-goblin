"""Plancia della Mappa TM-04 Tundra Invernale (Spec_v7.md R 8.12, §17), stessi campi di mappa.py.
Carattere: distesa aperta: due ghiacciai di rocce per metà e 109 collegamenti; uno sbarramento costa al massimo
+2 passi, vince chi corre.
Terra: 8 bosco, 4 case, 16 rocce. Parti fisse come la plancia base."""

_STRADA = """A1 B1 C1 H1 I1 J1 A2 B2 C2 G2 I2 J2 C3 D3 E3 G3 H3 J3 C4 D4 E4 F4 G4 H4 I4 J4 G5 H5 I5 J5 A6 B6 C6 D6 A7 B7 C7
D7 E7 F7 G7 H7 A8 C8 D8 F8 G8 H8 A9 B9 D9 H9 I9 J9 A10 B10 C10 H10 I10 J10"""
_GUADI = "D5 F5 E6 G6"

PARTENZE = {1: 'C1', 2: 'H1', 3: 'J5', 4: 'H10', 5: 'C10', 6: 'A6'}
CRIPTE = {1: 'D4', 2: 'G4', 3: 'D7', 4: 'G7'}
DOMANDE = tuple("A1 A9 B6 B9 B10 C2 C7 D3 D6 E3 F8 G5 G8 H4 H9 I1 I2 I5 J2 J10".split())

_MURI = """D3|D4 D4|E3 G4|H3 G4|H4 G4|H5 C6|D7 C7|D7 C8|D7 F8|G7 G7|G8
B2|C1 C6|D6 D8|D9 G2|G3 G5|H5 H10|I9"""

BOSCO = "D1 E1 D2 E2 F9 G9 F10 G10"
CASE = "H2 I3 B8 C9"
ROCCE = "F1 G1 F2 A3 B3 F3 A4 B4 I7 J7 E8 I8 J8 E9 D10 E10"
ACQUA = "A5 B5 C5 E5 F6 H6 I6 J6"
