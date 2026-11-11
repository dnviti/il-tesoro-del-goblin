# Tessere della mappa in 3D (11/11, richiesta di Daniele)

Tessere esagonali incastrabili a misura vera per la stampa 3D, con muri a pioli. È la stessa mappa a tessere di `tessere_mappa.pdf` (Spec D23, R 8.1/8.2), solo per i playtest.

## File

- `tessera.stl` / `.3mf`: una tessera.
- `muro.stl` / `.3mf`: un muro, già capovolto per la stampa (cima sul piatto, pioli in alto).
- `prova_3x3.stl` / `.3mf`: 9 tessere già montate, girate di 0, 120 e 240°. Stampate così mostrano se il gioco viene pulito. Per provare l'incastro vero si stampano staccate.
- `piatto_20_tessere_8_muri.stl` / `.3mf`: 20 tessere e 8 muri staccati (168 × 117 mm), per un piatto da 220 × 220. Nel 3MF ogni pezzo è un oggetto a parte.
- `anteprima_tessera.png`, `anteprima_3x3_muro.png`, `anteprima_piatto.png`: viste di controllo.
- `genera_3d.py` (geometria e controlli) e `blender_3d.py` (solidi, controlli delle mesh, STL/3MF, anteprime).

Si rigenera tutto con `python3 v7/stampa/3d/genera_3d.py`. Servono shapely ≥ 2.1 e Blender ≥ 4.5, usato senza finestra. Le misure sono i parametri in cima a `genera_3d.py`: si cambiano lì e si rilancia.

## Misure

- **Tessera:** esagono a punta in su, passo **25,2 mm** (distanza tra i centri di due tessere vicine, come la plancia), spessa **3 mm**.
  - Il corpo misura 24,9 mm da lato a lato perché c'è il gioco. L'ingombro con i pomelli è 28,8 × 28,8 mm.
  - Pesa circa 1,6 g in PLA (1,26 cm³).
- **Incastro:** un pomello tondo da puzzle (collo 2,6 mm, pomello Ø 4, sporge 3,9 mm) a lati alterni: pomello, incavo, pomello, incavo, pomello, incavo.
  - Due lati opposti sono sempre uno pomello e uno incavo, quindi le tessere si incastrano sempre girate di 0, 120 o 240°.
  - Il pomello è alto 2 mm, sotto il fondo della tasca, così non alza la carta della tessera vicina.
  - Le tessere si montano dall'alto.
- **Gioco:** **0,15 mm per lato** su tutto il contorno (`GIOCO`), cioè 0,3 mm tra due tessere. Tirando, una tessera si sposta al massimo di 0,47 mm prima che il pomello faccia presa.
- **Tasca per la carta:** esagono di 23,2 mm da lato a lato, profonda 0,5 mm, con un bordino di 0,85 mm.
  - La carta da 25,2 mm non può entrare: è più larga della tessera stessa (24,9 mm).
  - Si stampa quindi **`tessere_mappa.pdf` in scala 90 %**: l'esagono di carta viene 22,7 mm (0,26 mm di gioco per lato) e non copre i fori dei muri.
- **Muro:** 3 mm di larghezza, 7 mm di altezza, 14,3 mm da punta a punta.
  - Le punte sono a 120°: due o tre muri si chiudono in un vertice con 0,2 mm di gioco.
  - Ha due pioli ad asola 3 × 1,8 mm, alti 2 mm, con un invito in punta.
  - Pesa circa 0,4 g.
- **Fori dei muri:** su ogni lato ci sono due mezzi fori (a ±4,5 mm dal centro del lato) che, con la tessera vicina, formano due asole 3,4 × 2,2 mm profonde 2,3 mm. Il gioco del piolo è 0,2 mm per lato.
  - Il muro si posa sui bordini delle due tessere, e i pioli entrano nelle asole.
  - Il materiale minimo intorno a un foro è 0,95 mm.

## Controlli (li fa lo script a ogni giro)

- Le celle ideali coprono il piano senza buchi né sovrapposizioni.
- Nella 3 × 3 ci sono 16 coppie di vicine. Il passo, misurato sui centri delle tasche, è 25,2 ± 0,0001 mm.
- L'intersezione tra vicine e tra muri e tessere è 0 mm³. Per controllo, spostando una tessera di 0,6 mm l'intersezione non è più zero.
- Le mesh sono chiuse (0 lati aperti, sia in Blender sia rileggendo gli STL), e il volume è uguale a quello calcolato (errore < 1e-7).
- Il 3MF è in millimetri, con un oggetto per pezzo.

## Stampa (FDM, ugello 0,4)

- PLA, strato 0,2 mm, 3 perimetri, 4 strati sopra e sotto, riempimento 20 % o più (di fatto la tessera è quasi piena). Non servono supporti.
- **Tessere:** col fondo sul piatto.
  - Attiva la compensazione del «piede d'elefante» (0,1-0,15 mm): i pomelli nascono sul primo strato.
- **Muri:** capovolti come nel file.
- **Prima prova:** 3 o 4 tessere staccate.
  - Se l'incastro è duro, porta `GIOCO` a 0,2.
  - Se balla, portalo a 0,1.
  - Poi rilancia lo script.
- **Carta:** incolla la carta nella tasca con colla stick, dopo aver ritagliato l'esagono.
