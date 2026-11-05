function eqBonus(p) {
  const b = { att: 0, mov: 0, ar: 0, pv: 0, adv: 0, dis: 0 };
  for (const id of equipped(p)) {
    switch (baseId(id)) {
      case 'TE-01': b.ar += 1; break;
      case 'TE-04': b.ar += 1; break;
      case 'TE-05': b.ar += 2; b.mov -= 1; break;
      case 'TE-06': case 'TE-07': case 'TE-08': case 'TE-09': b.ar += 1; break;
      case 'TE-10': case 'TE-11': case 'TE-12': b.att += 1; break;
      case 'TE-16': b.ar += 1; break;
      case 'TE-17': b.ar += 2; b.mov -= 1; break;
      case 'TE-18': b.mov += 1; break;
      case 'TE-19': case 'TE-20': b.ar += 1; break;
      case 'CA-04': b.ar += 1; if (isC(p, 'Oracolo')) b.att++; break;
    }
  }
  return b;
}
// Mappe v2: il tabellone cambia (una sola Mappa attiva); Miraggio del Tesoro sposta solo il tesoro
function mapBonus(p, mapId = G.map && G.map.id) {
  const b = { att: 0, mov: 0, ar: 0, pv: 0, adv: 0, dis: 0 };
  switch (mapId) {
    case 'TM-02': b.mov += 2; break;
    case 'TM-03': b.mov -= 1; if (isR(p, 'Elfo')) b.adv++; break;
    case 'TM-04': b.mov -= 1; break;
    case 'TM-05': b.mov -= 1; if (isR(p, 'Sanguar')) b.adv++; break;
  }
  return b;
}
