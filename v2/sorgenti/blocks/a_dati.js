// Scatola base v2 (Carte Trama v2 di Alessandro De Simone, 27/10/2026): 4 classi, Oracolo al posto del Chierico
const CLASSES = ['Guerriero', 'Ladro', 'Mago', 'Oracolo'];
const CLASS_CARD = { Guerriero: 'TC-01', Ladro: 'TC-02', Mago: 'TC-03', Oracolo: 'TC-04' };
// 4 slot della scheda: Elmo, Arma DX / Scudo, Arma SX, Armatura
const SLOT = {};
['TE-01', 'TE-02', 'TE-03', 'TE-04'].forEach(i => SLOT[i] = 'elmo');
['TE-05', 'TE-06', 'TE-07', 'TE-08', 'TE-09', 'TE-10', 'TE-11', 'TE-12'].forEach(i => SLOT[i] = 'dx');
['TE-13', 'TE-14', 'TE-15'].forEach(i => SLOT[i] = 'sx');
['TE-16', 'TE-17', 'TE-18', 'TE-19', 'TE-20'].forEach(i => SLOT[i] = 'armatura');
SLOT['CA-04'] = 'elmo';
const SHIELDS = ['TE-05', 'TE-06', 'TE-07', 'TE-08', 'TE-09'];
const POTIONS = [];
const SLOTN_5 = { elmo: 'Elmo', dx: 'Arma DX / Scudo', sx: 'Arma SX', armatura: 'Armatura' };
const SLOTN_3 = SLOTN_5;
let SLOTN = SLOTN_5;
const SLOT_LABEL = { elmo: 'Elmo', dx: 'Arma DX / Scudo', sx: 'Arma SX', armatura: 'Armatura' };

// Carte Nemico a livelli (Daniele, 27/10): mazzetto I = LV 1-2, mazzetto II = LV 3-4 (+ mini-boss LV 4,5 facoltativi), boss LV 5.
// Danno dal livello (LV 1 → D6 − 1, LV 2 → D6, LV 3 e oltre → D6 + 1); tiro per colpire D20 + ATT ≥ Difesa = 14 + AR (Daniele 27/10: colpire è il 20% più difficile, +4); ogni nemico ha un effetto (fx)
const HIT_DIE = () => BAL.hitDie || 20;
const DIFESA = x => (BAL.defBase ?? 14) + x;
const DMG_LV = lv => BAL.dmgLv[Math.min(Math.ceil(lv), BAL.dmgLv.length) - 1];
const NEMICI = (typeof NEMICI_JSON !== 'undefined' ? NEMICI_JSON : []).map(n => ({ id: n.id, name: n.nome, lv: n.lv, pv: n.pv, att: n.att, ar: n.ar, tipo: n.tipo, fx: n.fx, abil: n.abilita, nonMorto: /Non morto/.test(n.abilita), agguato: n.fx === 'agguato', borseggio: n.fx === 'borseggio' }));
const BESTIARIO = NEMICI.filter(n => n.tipo === 'Nemico I');
const MAZZO_II = NEMICI.filter(n => n.tipo === 'Nemico II');
const MINIBOSS = NEMICI.filter(n => n.tipo === 'Mini-boss');
const BOSSES = NEMICI.filter(n => n.tipo === 'Boss');
const BOSS = BOSSES[0] || { name: 'Guardiano di MIMI', lv: 5, pv: 14, att: 4, ar: 3 };
const BEHOLDER = { name: 'Beholder', lv: 4, pv: 15, att: 3, ar: 2, beholder: true };
