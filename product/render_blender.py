"""Blender headless render of the layered stack -> product photo.

Run:  blender -b -P render_blender.py -- <svg_dir> <out.png> [view] [elev_deg]

  view = hero    near-frontal, the main listing image
         angled  three-quarter, shows the layer edges

Imports each layer SVG as curves, extrudes to 3 mm, stacks them with the real
layer spacing, gives them a plywood-ish material and lights the scene so the
step shadows between layers read clearly. Those shadows are the whole point:
in a search-results grid full of flat black silhouettes, a rendered depth stack
is what makes the thumbnail different (wiki/findings/keyword-demand-sweep.md).
"""
import bpy, sys, math, pathlib

argv = sys.argv[sys.argv.index("--") + 1:]
SRC = pathlib.Path(argv[0])
OUT = argv[1]
VIEW = argv[2] if len(argv) > 2 else "hero"
PALETTE = argv[3] if len(argv) > 3 else "wood"
ELEV = float(argv[4]) if len(argv) > 4 else (74.0 if VIEW == "hero" else 34.0)
AZIM = 0.0 if VIEW == "hero" else 24.0
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


def wood(name, base, rough=0.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
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
    "knot":  [(0.045, 0.045, 0.05, 1), (0.55, 0.08, 0.08, 1), (0.30, 0.30, 0.33, 1),
              (0.62, 0.62, 0.65, 1), (0.82, 0.82, 0.84, 1), (0.95, 0.95, 0.96, 1)],
    # MaWood look: deep red field on the solid backer, near-black strands,
    # silver mid-weave, white frontmost over-strands
    "knot2": [(0.42, 0.05, 0.05, 1), (0.05, 0.05, 0.06, 1), (0.10, 0.10, 0.12, 1),
              (0.45, 0.45, 0.48, 1), (0.80, 0.80, 0.82, 1), (0.96, 0.96, 0.97, 1)],
}
TONES = PALETTES.get(PALETTE, PALETTES["wood"])

svgs = sorted(SRC.glob("layer_*_of_*.svg"))
print(f"[render] {len(svgs)} reteg")
APPLIED = []

for i, f in enumerate(svgs):
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=str(f))
    new = [o for o in bpy.data.objects if o not in before]
    mat = wood(f"wood_{i}", TONES[i % len(TONES)])
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
xs = [o.location.x for o in objs]; ys = [o.location.y for o in objs]
cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
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

# ------------------------------------------------------------------ backdrop
bpy.ops.mesh.primitive_plane_add(size=SIZE * 6, location=(0, 0, -0.0005))
bpy.context.object.data.materials.append(wood("wall", (0.80, 0.75, 0.68, 1), 0.7))

# ------------------------------------------------------------------ camera + light
# Distance from the framing we want, not a guessed multiplier: at focal length f
# on a 36 mm sensor, a camera d away sees d*36/f across. Solve for the piece plus
# a margin, then add back what the tilt foreshortens. The earlier fixed 1.75x
# multiplier cropped the piece.
LENS, MARGIN = 85.0, 1.22
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

key = bpy.data.lights.new("key", "AREA"); key.energy = SIZE * SIZE * 85; key.size = SIZE * 1.6
ko = bpy.data.objects.new("key", key); scene.collection.objects.link(ko)
ko.location = (-SIZE * 1.1, -SIZE * 1.1, SIZE * 1.5); ko.rotation_euler = (math.radians(38), 0, math.radians(-40))

fill = bpy.data.lights.new("fill", "AREA"); fill.energy = SIZE * SIZE * 22; fill.size = SIZE * 3
fo = bpy.data.objects.new("fill", fill); scene.collection.objects.link(fo)
fo.location = (SIZE * 1.6, -SIZE * 0.9, SIZE * 0.9); fo.rotation_euler = (math.radians(65), 0, math.radians(60))

world = bpy.data.worlds.new("w"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.52, 0.48, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.06

scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print(f"[render] kesz: {OUT}")
