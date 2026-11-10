"""Plancia della Mappa TM-02 Città Avanzata (Spec_v7.md R 8.12, §17), stessi campi di mappa.py.
Carattere: quartieri: tre isolati di case e una fila di officine (rocce E1-F3) nel mezzo;
i vicoli C2-D3 e G8-H9 sono i tappi (+13 passi).
Terra: 6 bosco, 14 case, 8 rocce. Parti fisse come la plancia base."""

_STRADA = """A1 B1 C1 H1 I1 A2 C2 G2 I2 J2 A3 D3 E3 G3 H3 J3 A4 B4 C4 D4 E4 F4 G4 H4 I4 J4 G5 H5 I5 J5 A6 B6 C6 D6 A7 B7 C7
D7 E7 F7 G7 H7 I7 J7 A8 C8 D8 F8 G8 J8 A9 B9 D9 H9 J9 B10 C10 H10 I10 J10"""
_GUADI = "D5 F5 E6 G6"

PARTENZE = {1: 'C1', 2: 'H1', 3: 'J5', 4: 'H10', 5: 'C10', 6: 'A6'}
CRIPTE = {1: 'D4', 2: 'G4', 3: 'D7', 4: 'G7'}
DOMANDE = tuple("A1 A9 B6 B9 B10 C2 C7 D3 D6 E3 F8 G5 G8 H4 H9 I1 I2 I5 J2 J10".split())

_MURI = """D3|D4 D4|E3 G4|H3 G4|H4 G4|H5 C6|D7 C7|D7 C8|D7 F8|G7 G7|G8
A6|B7 C6|D6 D8|D9 G2|G3 G5|H5 I4|J5"""

BOSCO = "J1 H2 I3 B8 C9 A10"
CASE = "D1 F1 G1 B2 D2 B3 C3 H8 I8 G9 I9 D10 E10 G10"
ROCCE = "E1 E2 F2 F3 E8 E9 F9 F10"
ACQUA = "A5 B5 C5 E5 F6 H6 I6 J6"
