"""Plancia della Mappa TM-07 Yuma – Pozzo di Luce (Spec_v7.md R 8.12, §17), stessi campi di mappa.py.
Carattere: il lago è il cuore: contano tutte e tre le traversate (guadi +15 passi, ponte +6; nella base +2).
Terra: 14 bosco, 6 case, 8 rocce. Parti fisse come la plancia base."""

_STRADA = """A1 B1 C1 D1 H1 I1 J1 A2 C2 H2 I2 J2 B3 D3 E3 G3 H3 J3 B4 C4 D4 E4 F4 G4 H4 J4 G5 H5 I5 J5 A6 B6 C6 D6 A7 C7 D7
E7 F7 G7 H7 I7 A8 C8 D8 F8 G8 I8 A9 B9 C9 H9 J9 A10 B10 C10 G10 H10 I10 J10"""
_GUADI = "D5 F5 E6 G6"

PARTENZE = {1: 'C1', 2: 'H1', 3: 'J5', 4: 'H10', 5: 'C10', 6: 'A6'}
CRIPTE = {1: 'D4', 2: 'G4', 3: 'D7', 4: 'G7'}
DOMANDE = tuple("A1 A9 B6 B9 B10 C2 C7 D3 D6 E3 F8 G5 G8 H4 H9 I1 I2 I5 J2 J10".split())

_MURI = """D3|D4 D4|E3 G4|H3 G4|H4 G4|H5 C6|D7 C7|D7 C8|D7 F8|G7 G7|G8
B6|C7 C6|D6 D6|E7 F4|G5 G5|H5 H4|I5"""

BOSCO = "G1 F2 G2 A3 I3 A4 I4 B7 J7 B8 J8 D9 E9 D10"
CASE = "E1 F1 D2 G9 E10 F10"
ROCCE = "B2 E2 C3 F3 E8 H8 F9 I9"
ACQUA = "A5 B5 C5 E5 F6 H6 I6 J6"
