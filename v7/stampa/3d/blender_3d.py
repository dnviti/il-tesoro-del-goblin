"""Parte Blender di genera_3d.py (non si lancia da sola): blender -b --factory-startup --python blender_3d.py -- spec.json

Estrude i profili calcolati da genera_3d.py, fa le booleane esatte, controlla le mesh, scrive STL, 3MF e anteprime.
"""
import json, math, os, struct, sys, zipfile

import bmesh
import bpy
from mathutils import Matrix, Vector

SPEC = json.load(open(sys.argv[sys.argv.index('--') + 1]))
OUT = SPEC['out']
P = SPEC['params']
FAIL = []
SOLVER = 'MANIFOLD'   # booleane di costruzione: libreria Manifold (uscita sempre chiusa, robusta sulle facce complanari)


def say(tag, **kw):
    print(tag, json.dumps(kw, ensure_ascii=False), flush=True)


bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
SC.unit_settings.scale_length = 0.001
SC.unit_settings.length_unit = 'MILLIMETERS'


def prism(name, poly, z0, z1):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    f = bm.faces.new([bm.verts.new((x, y, z0)) for x, y in poly])
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in r['geom']:
        if isinstance(v, bmesh.types.BMVert):
            v.co.z = z1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    SC.collection.objects.link(ob)
    return ob


def bake(ob):
    """applica i modificatori (booleane) e restituisce la mesh nuova."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def boolean(target, tools, op):
    for t in tools:
        m = target.modifiers.new('b', 'BOOLEAN')
        m.operation, m.solver, m.object = op, SOLVER, t
    bake(target)
    for t in tools:
        bpy.data.objects.remove(t)


def build(name, s):
    ops = s['ops']
    base = prism(name, ops[0]['poly'], ops[0]['z0'], ops[0]['z1'])
    for o in ops[1:]:
        if o['op'] == 'union':
            boolean(base, [prism('t', o['poly'], o['z0'], o['z1'])], 'UNION')
        else:
            boolean(base, [prism('t', p, z0, o['z1']) for p, z0 in zip(o['polys'], o['z0s'])], 'DIFFERENCE')
    bm = bmesh.new()
    bm.from_mesh(base.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bm.to_mesh(base.data)
    bm.free()
    return base


def stats(ob, world=False):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    if world:
        bm.transform(ob.matrix_world)
    bad = [e for e in bm.edges if not e.is_manifold]
    dove = [[round(x, 3) for x in (e.verts[0].co + e.verts[1].co) / 2] + [len(e.link_faces), round(e.calc_length(), 5)] for e in bad[:8]]
    vol = bm.calc_volume(signed=True)
    lo = Vector([min(v.co[i] for v in bm.verts) for i in range(3)]) if bm.verts else Vector()
    hi = Vector([max(v.co[i] for v in bm.verts) for i in range(3)]) if bm.verts else Vector()
    bm.free()
    return {'bordi_non_manifold': len(bad), 'volume_mm3': round(vol, 4), 'min': [round(x, 3) for x in lo], 'max': [round(x, 3) for x in hi],
            'ingombro_mm': [round(x, 3) for x in (hi - lo)], **({'non_manifold_dove': dove} if dove else {})}


# ---- solidi base ---------------------------------------------------------------------------------------------
solids = {}
for name, s in SPEC['solids'].items():
    ob = build(name, s)
    st = stats(ob)
    st['volume_atteso_mm3'] = round(s['volume'], 4)
    st['errore_volume_rel'] = abs(st['volume_mm3'] - s['volume']) / s['volume']
    say('RESULT solido ' + name, **st)
    if st['bordi_non_manifold'] or st['errore_volume_rel'] > 1e-4:
        FAIL.append(name)
    solids[name] = ob
    ob.hide_render = True
    ob.hide_set(True)

# muro in posizione di stampa: capovolto (cima sul piatto, pioli in alto), base a z = 0
ms = solids['muro'].data.copy()
ms.transform(Matrix.Translation((0, 0, P['muro_h'])) @ Matrix.Rotation(math.pi, 4, 'X'))
solids['muro_stampa'] = bpy.data.objects.new('muro_stampa', ms)


def place(items, prefix):
    out = []
    for k, it in enumerate(items):
        ob = bpy.data.objects.new(f'{prefix}_{k + 1:02d}_{it["obj"]}', solids[it['obj']].data)
        ob.matrix_world = Matrix.Translation((it['x'], it['y'], it['z'])) @ Matrix.Rotation(math.radians(it['rot']), 4, 'Z')
        SC.collection.objects.link(ob)
        out.append(ob)
    return out


def world_tris(obs):
    res = []
    for ob in obs:
        me = ob.data
        me.calc_loop_triangles()
        M = ob.matrix_world
        res.append((ob.name, [tuple(M @ v.co) for v in me.vertices], [tuple(t.vertices) for t in me.loop_triangles]))
    return res


def write_stl(path, obs):
    data = world_tris(obs)
    n = sum(len(f) for _, _, f in data)
    with open(path, 'wb') as fh:
        fh.write(b'Il Tesoro del Goblin - tessere 3D'.ljust(80, b' '))
        fh.write(struct.pack('<I', n))
        for _, vs, fs in data:
            for a, b, c in fs:
                va, vb, vc = Vector(vs[a]), Vector(vs[b]), Vector(vs[c])
                nn = (vb - va).cross(vc - va).normalized()
                fh.write(struct.pack('<12fH', *nn, *va, *vb, *vc, 0))
    return n


def write_3mf(path, obs):
    data = world_tris(obs)
    res, build_items = [], []
    for i, (name, vs, fs) in enumerate(data, 1):
        v = ''.join(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x, y, z in vs)
        t = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in fs)
        res.append(f'<object id="{i}" type="model" name="{name}"><mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>')
        build_items.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="it-IT" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<metadata name="Title">Il Tesoro del Goblin - tessere 3D</metadata>'
             f'<resources>{"".join(res)}</resources><build>{"".join(build_items)}</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
            '</Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', model)


def export(name, obs):
    n = write_stl(os.path.join(OUT, name + '.stl'), obs)
    write_3mf(os.path.join(OUT, name + '.3mf'), obs)
    say('SAVED ' + name, stl=name + '.stl', mf3=name + '.3mf', oggetti=len(obs), triangoli=n)


def world_copy(ob, name):
    me = ob.data.copy()
    me.transform(ob.matrix_world)
    c = bpy.data.objects.new(name, me)
    SC.collection.objects.link(c)
    return c


def inter_volume(a, b, shift=(0, 0, 0)):
    t = world_copy(a, 'tmp_a')
    t.location = shift
    m = t.modifiers.new('i', 'BOOLEAN')
    m.operation, m.solver, m.object = 'INTERSECT', 'EXACT', b
    bake(t)
    v = stats(t)['volume_mm3'] if len(t.data.vertices) else 0.0
    me = t.data
    bpy.data.objects.remove(t)
    bpy.data.meshes.remove(me)
    return v


# ---- pezzi singoli -------------------------------------------------------------------------------------------
t1 = place([{'obj': 'tessera', 'x': 0, 'y': 0, 'z': 0, 'rot': 0}], 'tessera')
export('tessera', t1)
w1 = place([{'obj': 'muro_stampa', 'x': 0, 'y': 0, 'z': 0, 'rot': 0}], 'muro')
say('RESULT muro_stampa', **stats(w1[0], world=True))
export('muro', w1)
for o in t1 + w1:
    bpy.data.objects.remove(o)

# ---- prova 3x3 montata: passo, intersezioni tra vicini, muri sui pioli ---------------------------------------
patch = place(SPEC['patch'], 'prova')
walls = place(SPEC['walls'], 'muro_prova')
wpatch = [world_copy(o, 'w_' + o.name) for o in patch]
wwalls = [world_copy(o, 'w_' + o.name) for o in walls]


def pocket_centre(ob):
    """baricentro del fondo della tasca (facce in su a z = fondo): simmetrico a 120°, cade nel centro della tessera."""
    me = ob.data
    acc, area = Vector(), 0.0
    for p in me.polygons:
        if p.normal.z > 0.999 and abs(p.center.z - P['z_pocket']) < 1e-4:
            acc += p.center * p.area
            area += p.area
    return acc / area


cent = [pocket_centre(o) for o in wpatch]
pitches = [(cent[a] - cent[b]).length for a, b in SPEC['pairs']]
iv = [inter_volume(wpatch[a], wpatch[b]) for a, b in SPEC['pairs']]
a0, b0 = SPEC['pairs'][0]
d = (cent[b0] - cent[a0]).normalized() * 0.6
control = inter_volume(wpatch[a0], wpatch[b0], shift=tuple(d))
wv = [inter_volume(w, t) for w in wwalls for t in wpatch]
ww = inter_volume(wwalls[0], wwalls[1])
res = {'coppie': len(pitches), 'passo_min_mm': round(min(pitches), 5), 'passo_max_mm': round(max(pitches), 5),
       'centri_xy_errore_max_mm': round(max(math.hypot(c.x - it['x'], c.y - it['y']) for c, it in zip(cent, SPEC['patch'])), 6),
       'intersezione_vicini_max_mm3': max(iv), 'controllo_spostata_0_6mm_mm3': round(control, 3),
       'intersezione_muri_tessere_max_mm3': max(wv), 'intersezione_muro_muro_mm3': ww,
       'manifold_tessere_montate': sum(stats(o)['bordi_non_manifold'] for o in wpatch)}
say('RESULT prova_3x3', **res)
if (abs(res['passo_min_mm'] - P['passo']) > 1e-3 or abs(res['passo_max_mm'] - P['passo']) > 1e-3 or max(iv) > 1e-6
        or control <= 0.1 or max(wv) > 1e-6 or ww > 1e-6 or res['manifold_tessere_montate']):
    FAIL.append('prova_3x3')
for o in wpatch + wwalls:
    me = o.data
    bpy.data.objects.remove(o)
    bpy.data.meshes.remove(me)
export('prova_3x3', patch)

# ---- piatto 20 tessere + 8 muri ------------------------------------------------------------------------------
plate = place(SPEC['plate'], 'piatto')
lo = Vector((1e9, 1e9, 1e9)); hi = -lo
for o in plate:
    s = stats(o, world=True)
    lo = Vector(map(min, lo, s['min'])); hi = Vector(map(max, hi, s['max']))
say('RESULT piatto', min=[round(x, 2) for x in lo], max=[round(x, 2) for x in hi], pezzi=len(plate))
if lo.x < 0 or lo.y < 0 or hi.x > 220 or hi.y > 220 or abs(lo.z) > 1e-6:
    FAIL.append('piatto')
export('piatto_20_tessere_8_muri', plate)

# ---- anteprime -----------------------------------------------------------------------------------------------
SC.render.engine = 'BLENDER_WORKBENCH'
sh = SC.display.shading
sh.light, sh.color_type = 'STUDIO', 'OBJECT'
sh.show_cavity, sh.cavity_type = True, 'BOTH'
sh.show_object_outline = True
sh.show_shadows = True
SC.render.resolution_x = SC.render.resolution_y = 900
SC.render.film_transparent = False
SC.world = bpy.data.worlds.new('w')
SC.world.color = (0.93, 0.91, 0.86)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
SC.collection.objects.link(cam)
SC.camera = cam
cam.data.type = 'ORTHO'
TONI = [(0.85, 0.72, 0.46, 1), (0.62, 0.70, 0.48, 1), (0.74, 0.62, 0.74, 1)]   # un tono per rotazione (0, 120, 240°)


def shot(path, obs, target, direction, scale):
    for o in SC.objects:
        if o.type == 'MESH':
            o.hide_render = o not in obs
    d = Vector(direction).normalized()
    cam.location = Vector(target) + d * 300
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    cam.data.ortho_scale = scale
    cam.data.clip_end = 1000
    SC.render.filepath = path
    bpy.ops.render.render(write_still=True)
    say('SAVED ' + os.path.basename(path))


for k, o in enumerate(patch):
    o.color = TONI[(SPEC['patch'][k]['rot'] // 120) % 3]
for o in walls:
    o.color = (0.30, 0.19, 0.11, 1)
for o in plate:
    o.color = TONI[0] if 'tessera' in o.name else (0.30, 0.19, 0.11, 1)
single = place([{'obj': 'tessera', 'x': 0, 'y': 0, 'z': 0, 'rot': 0}], 'vista')
single[0].color = TONI[0]
shot(os.path.join(OUT, 'anteprima_tessera.png'), single, (0, 0, 1.0), (0.9, -1.4, 1.3), 40)
pc = Vector((sum(i['x'] for i in SPEC['patch']) / 9, sum(i['y'] for i in SPEC['patch']) / 9, 2))
shot(os.path.join(OUT, 'anteprima_3x3_muro.png'), patch + walls, pc, (0.8, -1.5, 1.6), 92)
shot(os.path.join(OUT, 'anteprima_piatto.png'), plate, (110, 110, 0), (0, 0, 1), 225)

if FAIL:
    say('ERRORE', falliti=FAIL)
