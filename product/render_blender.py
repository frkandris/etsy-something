"""Blender headless render of the layered stack -> product photo.

Run:  blender -b -P render_blender.py -- <svg_dir> <out.png> [view] [palette] [elev_deg] [--grain]

  view = hero    near-frontal, the main listing image
         angled  three-quarter, shows the layer edges
         shelf   standing on a sideboard against a wall - the lifestyle shot
                 every high-review competitor uses

Imports each layer SVG as curves, extrudes to 3 mm, stacks them with the real
layer spacing, gives them a plywood-ish material and lights the scene so the
step shadows between layers read clearly. Those shadows are the whole point:
in a search-results grid full of flat black silhouettes, a rendered depth stack
is what makes the thumbnail different (wiki/findings/keyword-demand-sweep.md).
"""
import bpy, sys, math, pathlib

argv = sys.argv[sys.argv.index("--") + 1:]
GRAIN = "--grain" in argv
# --orbit N renders N frames on a short camera arc, for a listing video
ORBIT = 0
for i, a in enumerate(argv):
    if a == "--orbit":
        ORBIT = int(argv[i + 1])
FRAME = "--frame" in argv
ACCENT_ON = "--accent" in argv
skip = set()
for i, a in enumerate(argv):
    if a in ("--grain", "--orbit", "--frame", "--accent"):
        skip.add(i)
        if a == "--orbit":
            skip.add(i + 1)
argv = [a for i, a in enumerate(argv) if i not in skip]
SRC = pathlib.Path(argv[0])
OUT = argv[1]
VIEW = argv[2] if len(argv) > 2 else "hero"
PALETTE = argv[3] if len(argv) > 3 else "wood"
ELEV = float(argv[4]) if len(argv) > 4 else (80.0 if VIEW == "hero" else 34.0)
# a dead-on 0 deg yaw reads as a scan; the winning listings tilt 8-15 deg
AZIM = 10.0 if VIEW == "hero" else 24.0
THICK = 0.003          # 3 mm plywood, in metres (SVG imports in metres-ish)
GAP = 0.0002

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
scene.render.film_transparent = False
scene.view_settings.look = "AgX - Base Contrast"
scene.view_settings.exposure = -0.4
if "lifestyle" in sys.argv:
    # AgX desaturates hard; the reference look is flat saturated spot colour
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = 0.15


def wood(name, base, rough=0.45, grain=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    if GRAIN if grain is None else grain:
        # subtle plywood grain: elongated wave bands distorted by noise,
        # blending the base colour with a slightly darker/warmer sibling
        tex = nt.nodes.new("ShaderNodeTexWave")
        tex.wave_type = "BANDS"
        tex.inputs["Scale"].default_value = 3.2
        tex.inputs["Distortion"].default_value = 22.0
        tex.inputs["Detail"].default_value = 3.0
        tex.inputs["Detail Roughness"].default_value = 0.55
        map_ = nt.nodes.new("ShaderNodeMapping")
        map_.inputs["Scale"].default_value = (1.0, 7.0, 1.0)   # stretch the grain
        coord = nt.nodes.new("ShaderNodeTexCoord")
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        dark = tuple(c * 0.82 for c in base[:3]) + (1,)
        lite = tuple(min(1.0, c * 1.06) for c in base[:3]) + (1,)
        ramp.color_ramp.elements[0].color = dark
        ramp.color_ramp.elements[1].color = lite
        nt.links.new(coord.outputs["Object"], map_.inputs["Vector"])
        nt.links.new(map_.outputs["Vector"], tex.inputs["Vector"])
        nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


# back layer first. The competitor survey (wiki/findings/competitor-listing-images.md):
# high-volume sellers use bold colour layers and a DARK back field for contrast.
PALETTES = {
    "wood":  [(0.29, 0.19, 0.10, 1), (0.34, 0.23, 0.12, 1), (0.39, 0.27, 0.15, 1),
              (0.44, 0.31, 0.18, 1), (0.50, 0.36, 0.21, 1), (0.57, 0.42, 0.25, 1)],
    "doxie": [(0.055, 0.045, 0.042, 1), (0.28, 0.14, 0.06, 1), (0.48, 0.26, 0.10, 1),
              (0.72, 0.48, 0.22, 1), (0.87, 0.70, 0.45, 1), (0.93, 0.88, 0.80, 1),
              (0.97, 0.95, 0.91, 1)],
    # breed colours: colour is NOT depth - the dog (front levels) goes
    # black-and-tan like a real doxie, the ornament stays light wood
    "doxie2": [(0.07, 0.06, 0.055, 1), (0.90, 0.84, 0.72, 1), (0.66, 0.47, 0.26, 1),
               (0.84, 0.72, 0.55, 1), (0.13, 0.09, 0.07, 1), (0.55, 0.28, 0.10, 1),
               (0.16, 0.11, 0.08, 1)],
    # terrain: water/valley dark blue-green rising to sunlit rock and snow
    "terrain": [(0.09, 0.16, 0.20, 1), (0.16, 0.26, 0.20, 1), (0.30, 0.34, 0.20, 1),
                (0.48, 0.40, 0.24, 1), (0.68, 0.58, 0.42, 1), (0.92, 0.90, 0.86, 1),
                (0.97, 0.97, 0.96, 1)],
    # moonlit scene: deep night sky at the back, moon and mist in the middle,
    # white cat frontmost - the paper market's contrast anchor is a DARK back
    "moonlit": [(0.03, 0.05, 0.12, 1), (0.07, 0.11, 0.24, 1), (0.13, 0.20, 0.34, 1),
                (0.22, 0.32, 0.42, 1), (0.42, 0.52, 0.58, 1), (0.72, 0.78, 0.80, 1),
                (0.97, 0.97, 0.95, 1)],
    # thatSVGplace recipe (50 listing reviews): matt black back plate carries all
    # the contrast, cool petrol/teal/sage climb through the middle, pure white on
    # top, one warm accent. This is the palette that wins the category.
    # value ladder: each step is a clear jump in lightness. The first version
    # kept the top three layers within ~4 L* of each other and they merged.
    "catteal": [(0.006, 0.006, 0.008, 1), (0.02, 0.09, 0.12, 1), (0.04, 0.19, 0.22, 1),
                (0.09, 0.33, 0.33, 1), (0.22, 0.50, 0.46, 1), (0.50, 0.70, 0.66, 1),
                (0.90, 0.93, 0.92, 1)],
    # PaperCutMari recipe (49 listing reviews): white top, saturated rainbow mids,
    # contrast from complementary colours rather than a dark plate
    # saturated, not pastel: the first version sat near S=0.35 and read as
    # "easter". Dark anchor at the back, white on top, S 0.75-0.90 between.
    "catrainbow": [(0.006, 0.006, 0.009, 1), (0.60, 0.02, 0.32, 1), (0.26, 0.04, 0.55, 1),
                   (0.02, 0.10, 0.62, 1), (0.00, 0.42, 0.26, 1), (0.92, 0.58, 0.02, 1),
                   (0.90, 0.28, 0.03, 1), (0.98, 0.98, 0.97, 1)],
    # reference look: the field is WHITE paper, the motif is a scatter of
    # saturated flat colours - not a dark-to-light ramp
    "splatter": [(0.96, 0.96, 0.95, 1), (0.06, 0.13, 0.30, 1), (0.05, 0.42, 0.72, 1),
                 (0.78, 0.14, 0.10, 1), (0.03, 0.52, 0.30, 1), (0.94, 0.55, 0.05, 1),
                 (0.97, 0.78, 0.10, 1), (0.20, 0.62, 0.85, 1)],
    "knot":  [(0.045, 0.045, 0.05, 1), (0.55, 0.08, 0.08, 1), (0.30, 0.30, 0.33, 1),
              (0.62, 0.62, 0.65, 1), (0.82, 0.82, 0.84, 1), (0.95, 0.95, 0.96, 1)],
    # MaWood look: deep red field on the solid backer, near-black strands,
    # silver mid-weave, white frontmost over-strands
    "knot2": [(0.42, 0.05, 0.05, 1), (0.05, 0.05, 0.06, 1), (0.10, 0.10, 0.12, 1),
              (0.45, 0.45, 0.48, 1), (0.80, 0.80, 0.82, 1), (0.96, 0.96, 0.97, 1)],
}
if PALETTE not in PALETTES:
    print(f"[render] FIGYELEM: ismeretlen paletta '{PALETTE}', wood-ra esem vissza")
BASE = PALETTES.get(PALETTE, PALETTES["wood"])


def ramp(pal, n):
    """Fit a palette to n layers. If the palette already has enough entries take
    them as they are - blending them would turn a set of flat spot colours into
    muddy pastels, which is exactly what happened to the splatter palette."""
    if n <= 1:
        return [pal[-1]]
    if len(pal) >= n:
        return list(pal[:n])
    out = []
    for i in range(n):
        x = i * (len(pal) - 1) / (n - 1)
        lo, f = int(x), x - int(x)
        hi = min(lo + 1, len(pal) - 1)
        out.append(tuple(pal[lo][c] * (1 - f) + pal[hi][c] * f for c in range(4)))
    return out

# natural sort - lexicographic puts layer_10 before layer_2
svgs = sorted(SRC.glob("layer_*_of_*.svg"),
              key=lambda p: int(p.stem.split("_")[1]))
TONES = ramp(BASE, len(svgs))
print(f"[render] {len(svgs)} reteg")
APPLIED = []

FRONT = []
ACCENT = wood("accent_eye", (0.30, 0.62, 0.20, 1), 0.4, grain=False)
ACCENT2 = wood("accent_nose", (0.94, 0.55, 0.62, 1), 0.4, grain=False)

for i, f in enumerate(svgs):
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=str(f))
    new = [o for o in bpy.data.objects if o not in before]
    mat = wood(f"wood_{i}", TONES[i])
    for o in new:
        if o.type != "CURVE":
            continue
        o.data.extrude = THICK / 2
        o.data.dimensions = "2D"
        o.data.fill_mode = "BOTH"
        o.data.materials.clear()
        o.data.materials.append(mat)
        for sl in o.material_slots:
            sl.material = mat
        FRONT.append((i, o))
        APPLIED.append(o.data.materials[0].name if o.data.materials else "NINCS")
        o.location.z = i * (THICK + GAP)

print(f"[render] anyagok: {sorted(set(APPLIED))}")

# centre everything on the origin
objs = [o for o in bpy.data.objects if o.type == "CURVE"]
bpy.ops.object.select_all(action="DESELECT")
for o in objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
# centre on the real bounding box, not the mean of object origins - the mean
# drifts toward whichever layer has more pieces and left the panel off-centre
import mathutils as _mu
_p = [o.matrix_world @ _mu.Vector(c) for o in objs for c in o.bound_box]
cx = (min(q.x for q in _p) + max(q.x for q in _p)) / 2
cy = (min(q.y for q in _p) + max(q.y for q in _p)) / 2
for o in objs:
    o.location.x -= cx
    o.location.y -= cy

# ---- fit the camera to the actual bounding box ---------------------------
import mathutils
pts = [o.matrix_world @ mathutils.Vector(c) for o in objs for c in o.bound_box]
minv = mathutils.Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
maxv = mathutils.Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
SIZE = max(maxv.x - minv.x, maxv.y - minv.y)
print(f"[render] darab merete: {SIZE:.4f} egyseg")

if ACCENT_ON:
    # The trace writes ONE <path> per layer, so a whole layer arrives as a single
    # multi-spline curve - assigning material per OBJECT painted every piece at
    # once, which is why the eyes AND the nose came out the same colour. Curve
    # splines carry their own material_index, so colour them individually.
    top = max(i for i, _ in FRONT)
    n = 0
    for i, o in FRONT:
        if i < top - 2 or o.type != "CURVE":
            continue
        base = o.data.materials[0] if o.data.materials else None
        o.data.materials.clear()
        for m in (base, ACCENT, ACCENT2):
            o.data.materials.append(m)
        for sp in o.data.splines:
            pts = [p.co for p in (sp.bezier_points if sp.type == "BEZIER" else sp.points)]
            if not pts:
                continue
            d = max(max(q[0] for q in pts) - min(q[0] for q in pts),
                    max(q[1] for q in pts) - min(q[1] for q in pts)) * max(o.scale)
            if d < 0.10 * SIZE:              # eye-or-nose scale on a 300 mm piece
                sp.material_index = 1 if d > 0.055 * SIZE else 2
                n += 1
    print(f"[render] akcentus {n} spline-on")

# ------------------------------------------------------------------ backdrop
if VIEW == "shelf":
    STACK = max(p.z for p in pts) - min(p.z for p in pts)
    for o in objs:
        # +90 about X keeps the artwork upright with its front toward the
        # camera; a few degrees SHORT of 90 leans the top toward the wall
        o.rotation_euler = (math.radians(84), 0, 0)
        ox, oy, oz = o.location.x, o.location.y, o.location.z
        o.location = (ox, -oz, oy + SIZE / 2)
    # sideboard top
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -SIZE * 0.25, -SIZE * 0.016))
    top = bpy.context.object
    top.scale = (SIZE * 2.6, SIZE * 0.9, SIZE * 0.03)
    top.data.materials.append(wood("board", (0.42, 0.30, 0.19, 1), 0.35, grain=True))
    # wall behind
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 8, location=(0, SIZE * 0.09, 0),
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(wood("wall", (0.84, 0.80, 0.74, 1), 0.8,
                                                  grain=False))
else:
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 6, location=(0, 0, -0.0005))
    # whitewashed board, not a 60% grey sweep - the grey read as CGI
    bpy.context.object.data.materials.append(
        wood("wall", (0.885, 0.870, 0.845, 1), 0.72, grain=GRAIN))

FRAME_OBJS = []
if FRAME:
    fw = SIZE * 0.115
    fd = SIZE * 0.14
    inner, outer = SIZE / 2 * 1.06, SIZE / 2 * 1.06 + fw
    _fm = wood("frame", (0.955, 0.95, 0.94, 1), 0.55, grain=False)
    for sx, sy, cx_, cy_ in ((outer, fw / 2, 0, outer - fw / 2),
                             (outer, fw / 2, 0, -(outer - fw / 2)),
                             (fw / 2, inner, outer - fw / 2, 0),
                             (fw / 2, inner, -(outer - fw / 2), 0)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx_, cy_, fd / 2 - 0.0006))
        b = bpy.context.object
        b.scale = (sx * 2, sy * 2, fd)
        b.data.materials.append(_fm)
        FRAME_OBJS.append(b)

if VIEW == "lifestyle":
    # A warm styled shelf with out-of-focus props. The winning listings put the
    # frame in a room, not on a sweep; the bokeh is what makes it read as a
    # photograph instead of a render.
    for o in objs + FRAME_OBJS:
        # the frame must stand up WITH the artwork. Rotating +90 deg about X maps
        # (x,y,z) -> (x,-z,y); the earlier version pinned z to a constant, which
        # was harmless for the flat art (y~0) but collapsed the frame bars onto
        # the centre line.
        o.rotation_euler = (math.radians(90), 0, 0)
        ox, oy, oz = o.location.x, o.location.y, o.location.z
        o.location = (ox, -oz, oy + SIZE * 0.60)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, SIZE * 0.1, -SIZE * 0.02))
    tb = bpy.context.object
    tb.scale = (SIZE * 6, SIZE * 3, SIZE * 0.05)
    tb.data.materials.append(wood("table", (0.40, 0.26, 0.15, 1), 0.35, grain=True))
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 10, location=(0, SIZE * 1.5, 0),
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(
        wood("backwall", (0.52, 0.38, 0.24, 1), 0.85, grain=False))
    props = [(-SIZE * 0.95, SIZE * 0.75, 0.22, (0.45, 0.30, 0.18)),
             (-SIZE * 1.25, SIZE * 0.55, 0.15, (0.30, 0.42, 0.22)),
             (SIZE * 1.00, SIZE * 0.70, 0.26, (0.55, 0.36, 0.20)),
             (SIZE * 1.35, SIZE * 0.95, 0.34, (0.42, 0.28, 0.16)),
             (SIZE * 0.80, SIZE * 0.35, 0.10, (0.62, 0.48, 0.30))]
    for i, (px, py, r, col) in enumerate(props):
        bpy.ops.mesh.primitive_cylinder_add(radius=SIZE * r, depth=SIZE * r * 2.2,
                                            location=(px, py, SIZE * r * 1.1))
        bpy.context.object.data.materials.append(
            wood(f"prop{i}", (*col, 1), 0.6, grain=False))

# ------------------------------------------------------------------ camera + light
# Distance from the framing we want, not a guessed multiplier: at focal length f
# on a 36 mm sensor, a camera d away sees d*36/f across. Solve for the piece plus
# a margin, then add back what the tilt foreshortens. The earlier fixed 1.75x
# multiplier cropped the piece.
LENS, MARGIN = 85.0, 1.22
if FRAME:
    # the frame is built after the bounding box, so the camera must be told the
    # object is bigger - otherwise it fits the art and crops the frame away
    MARGIN *= 1.34
if VIEW == "lifestyle":
    D = SIZE * MARGIN * LENS / 36.0 * 1.02
    bpy.ops.object.camera_add(location=(0, -D, SIZE * 0.62),
                              rotation=(math.radians(90), 0, 0))
    cam = bpy.context.object
    cam.data.lens = LENS
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = D
    cam.data.dof.aperture_fstop = 2.2
    scene.camera = cam
    print(f"[render] nezet=lifestyle tavolsag={D:.3f}")
elif VIEW == "shelf":
    D = SIZE * MARGIN * LENS / 36.0 * 1.06
    az = math.radians(14)
    bpy.ops.object.camera_add(
        location=(D * math.sin(az), -D * math.cos(az), SIZE * 0.52),
        rotation=(math.radians(88), 0, az))
elif True:
    D = SIZE * MARGIN * LENS / 36.0 / max(0.55, math.sin(math.radians(ELEV)) ** 0.35)
    el, az = math.radians(ELEV), math.radians(AZIM)
    bpy.ops.object.camera_add(
        location=(D * math.sin(az) * math.cos(el),
                  -D * math.cos(az) * math.cos(el),
                  D * math.sin(el)),
        rotation=(math.radians(90 - ELEV), 0, az))
cam = bpy.context.object
cam.data.lens = LENS
scene.camera = cam
print(f"[render] nezet={VIEW} emelkedes={ELEV:.0f} tavolsag={D:.3f}")

# tighter key = sharper layer-edge shadows, which is what sells the depth
key = bpy.data.lights.new("key", "AREA"); key.energy = SIZE * SIZE * 110; key.size = SIZE * 0.85
ko = bpy.data.objects.new("key", key); scene.collection.objects.link(ko)
ko.location = (-SIZE * 1.1, -SIZE * 1.1, SIZE * 1.5); ko.rotation_euler = (math.radians(38), 0, math.radians(-40))

fill = bpy.data.lights.new("fill", "AREA"); fill.energy = SIZE * SIZE * 22; fill.size = SIZE * 3
fo = bpy.data.objects.new("fill", fill); scene.collection.objects.link(fo)
fo.location = (SIZE * 1.6, -SIZE * 0.9, SIZE * 0.9); fo.rotation_euler = (math.radians(65), 0, math.radians(60))

world = bpy.data.worlds.new("w"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.52, 0.48, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.06

if ORBIT:
    # a short left-right arc reads as "turning it in your hand" and shows the
    # layer edges - a static hero cannot show depth, which is the whole product
    import os
    base = OUT[:-4] if OUT.endswith(".png") else OUT
    scene.cycles.samples = 64
    scene.render.resolution_x = scene.render.resolution_y = 1000
    for f in range(ORBIT):
        t = f / (ORBIT - 1) if ORBIT > 1 else 0.5
        sway = math.radians(-16 + 32 * (0.5 - 0.5 * math.cos(2 * math.pi * t)))
        el2 = math.radians(ELEV) - math.radians(6) * math.sin(2 * math.pi * t)
        cam.location = (D * math.sin(sway) * math.cos(el2),
                        -D * math.cos(sway) * math.cos(el2),
                        D * math.sin(el2))
        cam.rotation_euler = (math.pi / 2 - el2, 0, sway)
        scene.render.filepath = f"{base}_f{f:03d}"
        bpy.ops.render.render(write_still=True)
    print(f"[render] orbit kesz: {ORBIT} kocka -> {base}_fNNN.png")
else:
    scene.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print(f"[render] kesz: {OUT}")
