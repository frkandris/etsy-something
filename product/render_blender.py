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
# Every flag must be read BEFORE argv is filtered. Reading one afterwards
# silently yields False - that is why --white-top and --recessed did nothing.
GRAIN = "--grain" in argv
SCENE_HDRI = ""
PROP_SET = "warm"
PALETTE_FILE = ""
SCENE_ZOOM = 0.82   # matched to the references, where the frame fills ~85% of
                    # the picture. Wider than that and it reads as an interior
                    # photo the frame happens to appear in.
for _i, _a in enumerate(argv):
    if _a == "--scene" and _i + 1 < len(argv):
        SCENE_HDRI = argv[_i + 1]
    if _a == "--scene-zoom" and _i + 1 < len(argv):
        SCENE_ZOOM = float(argv[_i + 1])
    if _a == "--props" and _i + 1 < len(argv):
        PROP_SET = argv[_i + 1]
    if _a == "--palette-file" and _i + 1 < len(argv):
        PALETTE_FILE = argv[_i + 1]
DARK_FRAME = "--dark-frame" in argv
ENGRAVE = "--engrave" in argv
# --orbit N renders N frames on a short camera arc, for a listing video
ORBIT = 0
for i, a in enumerate(argv):
    if a == "--orbit":
        ORBIT = int(argv[i + 1])
FRAME = "--frame" in argv
ACCENT_ON = "--accent" in argv
PAPER = "--paper" in argv
RECESSED = "--recessed" in argv
WHITE_TOP = "--white-top" in argv
WOODFRAME = "--wood-frame" in argv
DOTS = "--dots" in argv
skip = set()
for i, a in enumerate(argv):
    if a in ("--grain", "--orbit", "--frame", "--accent", "--paper", "--white-top",
             "--dots", "--wood-frame", "--recessed", "--scene", "--scene-zoom",
             "--props", "--palette-file", "--dark-frame", "--engrave"):
        skip.add(i)
        if a in ("--orbit", "--scene", "--scene-zoom", "--props", "--palette-file"):
            skip.add(i + 1)
argv = [a for i, a in enumerate(argv) if i not in skip]
SRC = pathlib.Path(argv[0])
OUT = argv[1]
VIEW = argv[2] if len(argv) > 2 else "hero"
PALETTE = argv[3] if len(argv) > 3 else "wood"
ELEV = float(argv[4]) if len(argv) > 4 else (80.0 if VIEW == "hero" else 34.0)
# a dead-on 0 deg yaw reads as a scan; the winning listings tilt 8-15 deg
AZIM = 10.0 if VIEW == "hero" else 24.0
# 0.9 mm was physically honest for cardstock but read as a flat print; 2 mm
# still says "paper" and gives every edge its own visible contact shadow
# 2 mm is what cardstock actually measures, but at 300 mm the step shadow it
# throws is under a pixel and the stack renders flat. 3.2 mm keeps the paper
# read and gives every cut edge a visible shadow - the depth cue the reviewer
# kept scoring lowest.
# 3.2 mm threw a step shadow so deep that every recess read near-black, and
# the piece looked nothing like the light, airy illustration it came from.
# 2.2 mm still gives each cut edge its own shadow without burying the colour.
THICK = 0.0022 if PAPER else 0.003
GAP = 0.0002

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
# Eevee, not Cycles. Flat-shaded paper on flat sheets has nothing for path
# tracing to discover - no caustics, no glass, no subsurface - so 128 Cycles
# samples bought a couple of minutes per frame and no visible difference. The
# video work already ran on Eevee for exactly this reason; the stills were
# still quietly on Cycles.
scene.render.engine = "BLENDER_EEVEE"
# One try block around all four meant the first name Blender dropped silently
# skipped the rest - use_gtao is gone in 5.x, so the AO distance and the soft
# shadows were never being set at all.
for _k, _v in (("taa_render_samples", 96), ("use_gtao", True),
               ("gtao_distance", 0.008), ("use_soft_shadows", True),
               ("use_raytracing", True)):
    try:
        setattr(scene.eevee, _k, _v)
    except (AttributeError, TypeError):
        pass
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
if VIEW in ("styled", "exploded"):
    # a felhasznalo referencia-kepei fekvo formatumuak (~1,47:1)
    scene.render.resolution_y = 1360
# plate: kordbban atlatszo volt (kompozit-cel), de sotet nezegetoben feketenek
# renderelodott, es a reviewer render-szagunak jelolte - studio-hatter lett
scene.render.film_transparent = False
scene.view_settings.look = "AgX - Base Contrast"
scene.view_settings.exposure = -0.05
if VIEW == "plate":
    # Lit to match a photographed backdrop rather than a modelled one: warm key
    # from the upper left, gentle fill, neutral transform so the composite step
    # can grade it against the photo.
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = -0.75
if "lifestyle" in sys.argv:
    # AgX rolls saturated colour off toward pastel. The reference is flat
    # printed spot colour, so use the untouched Standard transform instead.
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    # Standard has no highlight roll-off, so the AgX-era light levels blew the
    # white frame and the paper out to pure white
    scene.view_settings.exposure = -0.55


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
    # rétegelt világtérkép: mély navy -> világoskék self, majd FA a szárazföldre.
    # A tetején szándékosan ugrik a szín: a víz és a part két külön anyag.
    # A referencia vilagosabb: a self majdnem feher, a mely palaszurke - a
    # navy-dominans elso valtozat tul sotet volt mellette.
    # A reviewer P1-e: a melyviz ne kozelitsen feketehez - vilagos-kek rampa,
    # a fa szarazfold adja a kontrasztot
    # 7 szin, mert a ripple-keszlet 5 sav + szarazfold + hatlap = 7 lap.
    # A referencia (VyvaStudio 22-es kep) szinei: telitett vilagoskek parti sav,
    # lefele melyulo kekek, a hatlap grafitsotet - az elozo halvany szurkes-
    # feher ramp "lapos palettat" kapott a reviewertol (2/5)
    # az EREDETI listing turkizes palettaja (a felhasznalo explicit kerese)
    "bathy": [(0.010, 0.016, 0.020, 1),   # hatlap: sotet pala-turkiz
              (0.040, 0.100, 0.140, 1),
              (0.100, 0.240, 0.330, 1),
              (0.220, 0.460, 0.590, 1),
              (0.420, 0.680, 0.790, 1),
              (0.650, 0.840, 0.900, 1),   # parti sav: halvany cian
              (0.430, 0.255, 0.110, 1)],  # szárazföld: dió (per-spline felulirva)
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
    # exact hexes the reviewer specified, converted sRGB -> linear (Blender base
    # colour is linear; feeding sRGB values straight in is what made everything
    # look washed out). Dark navy anchors, two cold blues break the warm cast.
    # 8 tones the reviewer specified: 3 warm, 3 cold, 2 green, orange dominant
    # and mustard cut back. Values converted sRGB -> linear.
    "splatter": [(0.155, 0.468, 0.731, 1),   # #6FB6DE  (layer 1, mostly hidden)
                 (0.008, 0.021, 0.069, 1),   # #17284A navy - big outer shape
                 (0.761, 0.133, 0.011, 1),   # #E2661C orange - dominant
                 (0.028, 0.212, 0.527, 1),   # #2F7FC0 cerulean
                 (0.871, 0.280, 0.042, 1),   # #F0913A light orange
                 (0.028, 0.342, 0.095, 1),   # #2F9E56 green
                 (0.577, 0.041, 0.027, 1),   # #C8392E red
                 (0.807, 0.451, 0.015, 1),   # #E8B321 mustard - now a small role
                 (0.202, 0.584, 0.258, 1)],  # #7CC98C light green
    # tuned for the 0022 portrait: neutral panel, warm cat, two cold accents,
    # and a near-white top so the whiskers read as whiskers rather than grass
    # 8 distinct hues, none repeating on adjacent layers (the reviewer counted
    # only 3 in the previous round). Values are sRGB converted to linear.
    "catref": [(0.60, 0.59, 0.57, 1),    # neutral panel, no warm tint
               (0.008, 0.021, 0.069, 1), # #17284A navy
               (0.761, 0.133, 0.011, 1), # #E2661C orange
               (0.011, 0.159, 0.462, 1), # #1B6FB5 cobalt
               (0.887, 0.445, 0.033, 1), # #F2B233 warm yellow
               (0.578, 0.037, 0.024, 1), # #C8362B deep red - the whisker layer;
                                         # leaf green here read as grass
               (0.049, 0.328, 0.087, 1), # #3F9C52 leaf green
               (0.080, 0.394, 0.731, 1)],# #4FA9DE sky
    # The seller's whole catalogue runs on one restrained earthy scheme: cream
    # field, sand, rust, warm brown, deep brown. Layer 1 being cream is what
    # gives the "white field" - no boolean top sheet needed, which is also far
    # more robust than cutting a plate with the motif outline.
    # The catalogue's portraits ALTERNATE light and dark rather than ramping:
    # that is what keeps every band readable. A cream layer 1 on a white backing
    # merged into it and the piece read as a blank field with a few brown chips.
    "earthy": [(0.30, 0.16, 0.08, 1),   # warm brown - outer silhouette
               (0.92, 0.87, 0.78, 1),   # cream
               (0.72, 0.26, 0.06, 1),   # rust
               (0.80, 0.68, 0.52, 1),   # sand
               (0.14, 0.07, 0.04, 1),   # deep brown
               (0.95, 0.92, 0.85, 1),   # bright cream
               (0.85, 0.42, 0.12, 1),   # bright rust
               (0.20, 0.11, 0.06, 1)],
    # recessed well: the top sheet is white and every sheet below is darker,
    # so depth reads as shadow falling into the opening
    # Recessed well. Layer 1 is the deepest sheet and layer N the white top
    # sheet, so the palette runs DARK to LIGHT - the opposite of a relief.
    # Strictly monotonic: brightness may only DECREASE with depth, no
    # exceptions. Layer 1 is the floor, the last is the top sheet. Values are
    # the reviewer's L*-spaced ramp, sRGB -> linear.
    # Five stops, L* 26/44/62/80/95, so the ladder reads as five steps rather
    # than collapsing to three. Layer 1 is the floor, the last the top sheet;
    # the mid stop is a saturated rust, not a greyish brown.
    # Every layer stays CHROMATIC (C* >= 22, hue 25-55 deg). The old ramp
    # bottomed out in neutral charcoal, and a neutral floor reads as a shadow
    # pit rather than as another sheet of coloured paper - the references have
    # no neutral anywhere. L* 38/52/64/76/90.
    # Chromatic everywhere (no neutral floor) but with the RANGE opened back
    # up: L* 38/52/64/76/90 was chromatic and monotonic, yet so compressed that
    # everything read as one mid-brown. L* 30-90 with higher chroma keeps the
    # warmth and gets the contrast back.
    # HUE variation, not a lightness ramp. Five stops that were merely lighter
    # versions of one brown read as a single string; the references alternate
    # three or four distinct hues. Adjacent layers differ by >=12 deg of hue.
    # Even L* ladder 20/36/51/63/74/84/92 - the previous set collapsed in the
    # dark half and the whole piece pressed flat. Deepest anchor #2A1B12.
    # The light end is COMPRESSED on purpose. The depth map's brightest tone is
    # only the small highlights, so a single bright stop landed there and the
    # big field - the actual top sheet - got the next one down and rendered
    # tan. The top two stops are both near-white so the field reads as the
    # white sheet and the highlights sit just above it.
    # Saturated warm midtones (terracotta, gold) so the three near-identical
    # browns separate, and NO pure white inside: the L*96 highlight slivers
    # round the eyes read as paint splatter, not paper. Interior ceiling L*90.
    # Even 12 L* steps from a WARM deep brown (not near-black - the reference's
    # darkest is a warm #4A3122, and true black read as a hole rather than a
    # sheet) up to a warm cream mat.
    "well":  [(0.068, 0.033, 0.015, 1),   # L*22  #4A3122
              (0.154, 0.068, 0.026, 1),   # L*34  #6E4A2E
              (0.305, 0.098, 0.033, 1),   # L*46  #9A5A34 terracotta
              (0.503, 0.195, 0.042, 1),   # L*58  #C07A3A
              (0.716, 0.389, 0.102, 1),   # L*70  #DDA85C gold
              (0.839, 0.638, 0.451, 1),   # L*82  #ECD3B4
              (0.888, 0.815, 0.731, 1)],  # L*92  #F2EADD warm cream mat
    "knot":  [(0.045, 0.045, 0.05, 1), (0.55, 0.08, 0.08, 1), (0.30, 0.30, 0.33, 1),
              (0.62, 0.62, 0.65, 1), (0.82, 0.82, 0.84, 1), (0.95, 0.95, 0.96, 1)],
    # MaWood look: deep red field on the solid backer, near-black strands,
    # silver mid-weave, white frontmost over-strands
    "knot2": [(0.42, 0.05, 0.05, 1), (0.05, 0.05, 0.06, 1), (0.10, 0.10, 0.12, 1),
              (0.45, 0.45, 0.48, 1), (0.80, 0.80, 0.82, 1), (0.96, 0.96, 0.97, 1)],
}
if PALETTE_FILE:
    # The sheets take the ILLUSTRATION's own colours, deepest first. sRGB has
    # to be linearised or every colour renders washed out and pale.
    import json as _json
    _srgb = _json.loads(pathlib.Path(PALETTE_FILE).read_text())

    def _lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    BASE = [tuple(_lin(v) for v in rgb) + (1,) for rgb in _srgb]
    PALETTES = dict(PALETTES, __file__=BASE)
    PALETTE = "__file__"
    print("[render] paletta a rajzbol: " + "  ".join(
        "#%02x%02x%02x" % tuple(c) for c in _srgb))
elif PALETTE not in PALETTES:
    print(f"[render] FIGYELEM: ismeretlen paletta '{PALETTE}', wood-ra esem vissza")
    BASE = PALETTES["wood"]
else:
    BASE = PALETTES[PALETTE]


# Spot palettes are a SET of flat colours: blending them makes mud, so they are
# truncated. Ramp palettes are a RANGE, and must always span end to end - taking
# the first n entries left the white end of "well" unused at 5 layers, so the
# top sheet came out cream instead of white.
SPOT = {"splatter", "catrainbow"}


def ramp(pal, n):
    """Fit a palette to n layers."""
    if n <= 1:
        return [pal[-1]]
    if PALETTE in SPOT and len(pal) >= n:
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
        # No z-inversion here. The depth map is already recessed at GENERATION
        # time (the field is the lightest level), so layer 1 is the deepest
        # sheet and the normal order is correct. Flipping z as well double-
        # inverted it and put the solid floor in front of everything.
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
import mathutils


def world_bbox(objects):
    """True world-space bounds. o.bound_box is the UNEVALUATED cage, es meg az
    evaluated masolate is hazudik az SVG-importalt gorbeknel: a 0.4 egyseges
    lapok ±1.2-es dobozt jelentettek, ami az exploded kamerat es a styled
    ultetest is elvitte. A tesszellalt to_mesh() csucsok az egyetlen igazsag."""
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in objects:
        oe = o.evaluated_get(dg)
        try:
            me = oe.to_mesh()
        except RuntimeError:
            me = None
        if me is not None and len(me.vertices):
            pts += [oe.matrix_world @ v.co for v in me.vertices]
            oe.to_mesh_clear()
        else:
            pts += [oe.matrix_world @ mathutils.Vector(c) for c in oe.bound_box]
    return pts


_p = world_bbox(objs)
cx = (min(q.x for q in _p) + max(q.x for q in _p)) / 2
cy = (min(q.y for q in _p) + max(q.y for q in _p)) / 2
for o in objs:
    o.location.x -= cx
    o.location.y -= cy

# ---- fit the camera to the actual bounding box ---------------------------
pts = world_bbox(objs)
minv = mathutils.Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
maxv = mathutils.Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
SIZE = max(maxv.x - minv.x, maxv.y - minv.y)
# A keret eddig mindig NEGYZET volt, mert csak a nagyobbik oldalt hasznaltuk.
# Egy 2:1-es vilagterkepnel ettol a mu a keret kozepen lebegett, korulotte
# ures savokkal. Az arany kell, nem csak a meret.
ASPECT = (maxv.x - minv.x) / max(1e-9, (maxv.y - minv.y))
# Tengelyenkénti szorzók. Az első javítás /max(1.0, 1/ASPECT)-tel osztott, ami
# sosem oszt (mindig 1.0 jön ki), ezért a keret négyzet maradt.
AX = (maxv.x - minv.x) / max(1e-9, SIZE)
AY = (maxv.y - minv.y) / max(1e-9, SIZE)
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

if PALETTE == "bathy" and FRONT:
    # A referencia orszagdarabjai TOBBFELE fabol vannak (vilagos tolgy, arany-
    # tolgy, dio) - az egyszinu tan "lapos palettat" kapott a reviewertol.
    # Per-spline determinisztikus tonus-valasztas a centroid hash-ebol.
    _woods = [wood("mixwood_light", (0.620, 0.470, 0.300, 1), 0.5, grain=True),
              wood("mixwood_gold", (0.360, 0.220, 0.115, 1), 0.5, grain=True),
              wood("mixwood_dark", (0.135, 0.068, 0.034, 1), 0.5, grain=True)]
    _top = max(i for i, _ in FRONT)
    for i, o in FRONT:
        if i != _top or o.type != "CURVE":
            continue
        o.data.materials.clear()
        for m in _woods:
            o.data.materials.append(m)
        for sp in o.data.splines:
            pts = [p.co for p in (sp.bezier_points if sp.type == "BEZIER" else sp.points)]
            if not pts:
                continue
            _cx = sum(q[0] for q in pts) / len(pts)
            _cy = sum(q[1] for q in pts) / len(pts)
            sp.material_index = int(abs(_cx * 7919.0 + _cy * 104729.0) * 997) % 3
    print("[render] vegyes fatonus a szarazfold-lapon")

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
elif VIEW != "plate":
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 6, location=(0, 0, -0.0005))
    # whitewashed board, not a 60% grey sweep - the grey read as CGI.
    # NEVER in plate view: the piece stands up there, and a horizontal plane
    # would slice straight through it.
    bpy.context.object.data.materials.append(
        wood("wall", (0.885, 0.870, 0.845, 1), 0.72, grain=GRAIN))

if FRAME and not RECESSED:
    # A relief motif needs breathing room inside the mat. A recessed panel IS
    # the mat and must fill the opening - this block still shrank it to 72%,
    # which is why the sheet kept reading as an inserted tile.
    for o in objs:
        o.scale = tuple(c * 0.72 for c in o.scale)
        o.location = (o.location.x * 0.72, o.location.y * 0.72, o.location.z)

if WHITE_TOP and objs:
    # The reference is not a motif sitting ON white - it is a WHITE TOP SHEET
    # with the motif's silhouette cut out of it, and the colour layers showing
    # through from underneath. That is why its white reads perfectly clean and
    # the colours look recessed.
    src = objs[0]                      # layer 1 = the full motif outline
    dup = src.copy(); dup.data = src.data.copy()
    scene.collection.objects.link(dup)
    bpy.ops.object.select_all(action="DESELECT")
    dup.select_set(True); bpy.context.view_layer.objects.active = dup
    bpy.ops.object.convert(target="MESH")
    sol = dup.modifiers.new("sol", "SOLIDIFY"); sol.thickness = SIZE * 0.5
    sol.offset = 0
    bpy.ops.object.modifier_apply(modifier="sol")
    ztop = max(o.location.z for o in objs) + THICK
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, ztop + THICK * 1.2))
    plate = bpy.context.object
    plate.scale = (SIZE * 1.14, SIZE * 1.14, THICK * 1.6)
    bl = plate.modifiers.new("cut", "BOOLEAN")
    bl.operation = "DIFFERENCE"; bl.object = dup
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier="cut")
    bpy.data.objects.remove(dup, do_unlink=True)
    plate.data.materials.append(wood("whitetop", (0.965, 0.965, 0.962, 1), 0.62,
                                     grain=False))
    objs.append(plate)
    print("[render] feher fedolap a motivum nyilasaval")

if DOTS and objs:
    # The generator kept dropping these, so place them here instead: 16 discs
    # scattered around the lower and side field, 60/40 right-heavy, sitting just
    # proud of the white sheet with their own soft shadow.
    _sc = [(-0.44, -0.30, .022), (-0.37, -0.42, .015), (-0.30, -0.50, .011),
           (-0.47, -0.10, .013), (-0.41,  0.12, .010), (-0.33, -0.20, .018),
           ( 0.36, -0.46, .020), ( 0.44, -0.33, .014), ( 0.30, -0.53, .012),
           ( 0.48, -0.14, .017), ( 0.42,  0.10, .011), ( 0.35,  0.24, .014),
           ( 0.28, -0.36, .010), ( 0.50,  0.30, .013), (-0.24, -0.55, .013),
           ( 0.20, -0.58, .016)]
    _dc = [BASE[i % len(BASE)] for i in (6, 5, 7, 1, 3, 2, 6, 7, 5, 1, 3, 8, 2, 6, 5, 7)]
    ztop_d = max(o.location.z for o in objs) + THICK * 2.6
    for k, (dx, dy, dr) in enumerate(_sc):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=SIZE * dr, depth=THICK * 0.8, vertices=48,
            location=(SIZE * dx, SIZE * dy, ztop_d))
        d = bpy.context.object
        c = _dc[k]
        d.data.materials.append(
            wood(f"dot{k}", (c[0] * .82, c[1] * .82, c[2] * .82, 1), 0.66, grain=False))
        objs.append(d)
    print(f"[render] {len(_sc)} potty elhelyezve")


# name, (x, y, z) in SIZE units, z-rotation, scale
PROP_SETS = {
    # Three, small, pushed to the edges. The references let a little greenery
    # and one ceramic thing peek in at a corner and nothing more; a full shelf
    # turns the listing into an interior photo the frame happens to be in.
    # Two behind and blurred, two in FRONT of the frame's plane and cut by the
    # picture edge - that front pair is what the reference uses to sell depth,
    # and a prop that is only ever behind cannot do it.
    # a vaza 0.94-nel pont a kepszelen vagodott le (reviewer P3) - beljebb;
    # a kosar elorebb es nagyobb, hogy legyen melysegi horgony az eloterben
    "warm": [("potted_plant_02",          (-0.92,  0.55, 0.0),  25, 0.62),
             ("antique_ceramic_vase_01",  ( 0.76,  0.50, 0.0), -15, 0.58),
             ("wicker_basket_01",         ( 0.72, -0.95, 0.0),  30, 0.58),
             ("wooden_candlestick",       (-0.84, -0.80, 0.0),   0, 0.55)],
}

FRAME_OBJS = []
if FRAME and not WHITE_TOP and not RECESSED:
    # White backing sheet - not needed when the panel IS the sheet. Leaving it
    # in put a visible mat ring around the recessed panel, which is exactly the
    # "floating tile" the reviewer marked down. in the
    # real product the cut layers are mounted on a plain sheet inside the frame.
    # tie the backing to THICK: a fixed -0.4 mm sat INSIDE the layer-1 extrusion
    # once paper thickness went to 2 mm, and the plane won the z-fight over the
    # largest, darkest layers - they vanished and the piece read as empty
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, -THICK * 1.6))
    _bk = bpy.context.object
    # pontosan a mu labnyoma: az 1.10-es tulmeret feher savkent logott ki a
    # keret mogul a nem-negyzetes tablanal
    _bk.scale = (SIZE * 0.998 * AX, SIZE * 0.998 * AY, 1.0)
    _bk.data.materials.append(wood("backing", (0.99, 0.988, 0.982, 1), 0.72,
                                   grain=False))
    FRAME_OBJS.append(_bk)
elif FRAME:
    # The recessed branch used to have NO backing at all - the oversized white
    # sheet above left a visible mat ring, so it was switched off entirely.
    # That left the stack open at the back, and with real geometry in the room
    # a plant leaf standing behind the frame showed THROUGH the deepest
    # openings. A backing matched to the panel's own footprint fixes both: no
    # ring, because it is not wider than the panel; nothing shows through,
    # because it is opaque. Colour is the deepest sheet, so an opening that
    # goes all the way down still reads as the bottom of the well.
    _pts = world_bbox([o for o in bpy.data.objects if o.type == "CURVE"])
    _xs = [p.x for p in _pts]; _ys = [p.y for p in _pts]
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(
        (min(_xs) + max(_xs)) / 2, (min(_ys) + max(_ys)) / 2, -THICK * 1.2))
    _bk = bpy.context.object
    _bk.scale = (max(_xs) - min(_xs), max(_ys) - min(_ys), 1.0)
    _bk.data.materials.append(wood("backing", PALETTES[PALETTE][0], 0.85, grain=False))
    FRAME_OBJS.append(_bk)

if FRAME:
    # ONE mitred body (outer box minus inner box), not four overlapping bars.
    # The bar version showed a detached left panel and a floating top rail from
    # any angle off dead-on. It was also nested in the "no white top" branch, so
    # with --white-top no frame was built at all and the white sheet's own edge
    # was standing in for it.
    # Measure the artwork HERE. SIZE was read from bound_box before the
    # depsgraph had re-evaluated the curves, and came out 39% too large - the
    # frame opening was then built to that stale figure and the panel filled
    # only 72% of it.
    _ab = world_bbox(objs)
    ART = max(max(q.x for q in _ab) - min(q.x for q in _ab),
              max(q.y for q in _ab) - min(q.y for q in _ab))
    fw = ART * 0.052
    # a recessed sheet sits right up against the rabbet; a deep empty well in
    # front of it reads as a floating tile
    if RECESSED:
        # Depth follows the STACK, not a fixed fraction. A frame deeper than the
        # paper left a wide unlit wall around the sheet, which read as the panel
        # floating in a dark well instead of sitting in the rabbet.
        _stack = len(svgs) * (THICK + GAP)
        fd = _stack + THICK * 1.6
    else:
        fd = ART * 0.17
    # overlap the sheet edge slightly: a 0.5% gap read as a scribed line 1.5%
    # inside the opening, which made the sheet look like an inserted plate
    inner = ART / 2 * (0.994 if RECESSED else 1.06)
    outer = inner + fw
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, fd / 2 - 0.0006))
    shell = bpy.context.object
    # x-ben az oldalarany szerint szeles, y-ban a magassag szerint - kulonben a
    # nem negyzetes mu a keret kozepen lebeg, korulotte ures savokkal
    shell.scale = (outer * 2 * AX, outer * 2 * AY + fw * 2 * (1 - AY), fd)
    # the opening must go ALL THE WAY THROUGH. Starting it at 0.28*depth left
    # the back of the shell solid, and that slab sat in front of the artwork:
    # only the two frontmost layers poked out and the piece looked empty.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, fd / 2))
    hole = bpy.context.object
    hole.scale = (inner * 2 * AX, inner * 2 * AY, fd * 3)
    bm = shell.modifiers.new("cut", "BOOLEAN")
    bm.operation = "DIFFERENCE"
    bm.object = hole
    bpy.context.view_layer.objects.active = shell
    bpy.ops.object.modifier_apply(modifier="cut")
    bpy.data.objects.remove(hole, do_unlink=True)
    # Light oak, not walnut. The reference frame is a pale, warm, visibly
    # grained oak; the near-black walnut swallowed the corner light and made
    # the whole listing read heavy.
    fc = ((0.115, 0.052, 0.022, 1) if DARK_FRAME else (0.318, 0.170, 0.068, 1)) \
        if WOODFRAME else (0.94, 0.933, 0.920, 1)
    # A flat matte plane reads as plastic. Real frame stock has grain running
    # one way, a slight sheen, and a bevel that catches a warm highlight.
    _fmat = wood("frame", fc, 0.34 if WOODFRAME else 0.42, grain=WOODFRAME)
    if WOODFRAME:
        _b = _fmat.node_tree.nodes["Principled BSDF"]
        _b.inputs["Specular IOR Level"].default_value = 0.42 \
            if "Specular IOR Level" in _b.inputs else None
    # inner bevel: a thin lighter lip around the opening.
    # FA keretnel NINCS: a referencian a dio kozvetlenul a legvilagosabb kek
    # laphoz simul; a vilagos lip 6 mm-es "paszpartu-savkent" logott a nyilasba
    if WOODFRAME:
        _lip = None
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, fd - fd * 0.06))
        _lip = bpy.context.object
        _lip.scale = ((inner * AX + fw * 0.16) * 2, (inner * AY + fw * 0.16) * 2,
                      fd * 0.12)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, fd))
        _lh = bpy.context.object
        _lh.scale = (inner * 2 * AX, inner * 2 * AY, fd)
        _bm2 = _lip.modifiers.new("cut", "BOOLEAN")
        _bm2.operation = "DIFFERENCE"; _bm2.object = _lh
        bpy.context.view_layer.objects.active = _lip
        bpy.ops.object.modifier_apply(modifier="cut")
        bpy.data.objects.remove(_lh, do_unlink=True)
        _lipmat = wood("framelip", tuple(min(1.0, c * 1.5) for c in fc[:3]) + (1,),
                       0.28, grain=False)
        _lip.data.materials.append(_lipmat)
        FRAME_OBJS.append(_lip)
    shell.data.materials.clear()
    shell.data.materials.append(_fmat)
    for _sl in shell.material_slots:
        _sl.material = _fmat
    print(f"[render] keret: {'vilagos tolgy' if WOODFRAME else 'feher'}")
    print(f"[render] mu={ART:.4f} keret-nyilas={inner*2:.4f} "
          f"kitoltes={ART/(inner*2)*100:.0f}%")
    FRAME_OBJS.append(shell)

# A frissen importalt gravir-gorbek bound_box-a hamis (a world_bbox docstringje
# pont erre int) - a keszlet 2.3 egyseg szelesnek merte magat a 0.4-es muvon.
# Ezert MINDEN bbox-alapu szamitasbol (kamera-illesztes, asztalra ultetes)
# kizarjuk oket; a tenyleges kiterjedesuk ugyis a retegeken belul van.
ENGRAVE_OBJS = []
# shelf: a mu mar az import elott 84 fokkal elfordult, a gravir laposan a
# levegoben maradna - ott egyszeruen nincs overlay (codex)
if ENGRAVE and VIEW != "shelf" and (SRC / "engrave_labels.svg").exists():
    _n_before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=str(SRC / "engrave_labels.svg"))
    _eng = [o for o in bpy.data.objects if o not in _n_before and o.type == "CURVE"]
    _zt = max(o.location.z for o in objs) + THICK * 1.05
    # sotetebb es vastagabb, mint az elso valtozat: a 0.16-os barna + 0.15 mm-es
    # extrude a plate tavolsagabol olvashatatlan volt (reviewer P1)
    _em = wood("engrave", (0.085, 0.042, 0.020, 1), 0.75, grain=False)
    for o in _eng:
        # A retegek origojat az origin_set attette a sajat bbox-kozepukre, ezert
        # az objs[0].location masolasa a cimkeket a terben szorta szet. A helyes
        # igazitas ugyanaz az eltolas, amit a retegek kaptak: (-cx, -cy). A
        # lepteket nem kell allitani - azonos viewBox, azonos importer-skala.
        o.location.x -= cx
        o.location.y -= cy
        o.location.z = _zt
        if FRAME and not RECESSED:
            # a nem-sullyesztett keret 0.72-re zsugoritja a muvet - a gravirt
            # ugyanugy kell, kulonben tulmeretes es elcsuszott (codex)
            o.scale = tuple(c * 0.72 for c in o.scale)
            o.location.x *= 0.72
            o.location.y *= 0.72
        o.data.extrude = 0.00015
        if o.data.materials:
            o.data.materials[0] = _em
        else:
            o.data.materials.append(_em)
        objs.append(o)
        ENGRAVE_OBJS.append(o)
    # Minden gorbe a SAJAT alatta levo feluletere uljon, ne a globalis stack-
    # tetore: a cim az also margosavban ~15 mm-rel a hatlap ELOTT lebegett, es
    # a vetett arnyeka masodik, elmosott feliratkent jelent meg (reviewer,
    # styled). Sugarvetes lefele, a keret- es gravir-objektumokat atugorva.
    bpy.context.view_layer.update()
    _dg = bpy.context.evaluated_depsgraph_get()
    import mathutils as _mu2
    for o in _eng:
        _b = world_bbox([o])
        _cx0 = (min(q.x for q in _b) + max(q.x for q in _b)) / 2
        _cy0 = (min(q.y for q in _b) + max(q.y for q in _b)) / 2
        _orig = _mu2.Vector((_cx0, _cy0, _zt + 0.5))
        for _ in range(6):
            _ok, _loc, _n, _i, _obj, _mw = scene.ray_cast(
                _dg, _orig, _mu2.Vector((0, 0, -1)))
            if not _ok:
                break
            _oo = getattr(_obj, "original", _obj)
            if _oo in ENGRAVE_OBJS or _oo in FRAME_OBJS:
                _orig = _loc + _mu2.Vector((0, 0, -0.0005))
                continue
            o.location.z = _loc.z + 0.0004
            break
    print(f"[render] gravir-overlay: {len(_eng)} gorbe")

if VIEW == "styled":
    # A real room built from CC0 geometry, lit by an HDRI. The point is the
    # camera: props at their own depths parallax correctly through an orbit,
    # and the HDRI background rotates with the view. A flat backdrop plate
    # cannot do either - it stayed nailed down while the frame turned, which
    # is what gave the video away.
    import os
    AST = pathlib.Path(__file__).resolve().parent / "pipeline" / "assets"

    def bring(name, loc, rot_z=0.0, scale=1.0):
        bf = AST / "models" / name / f"{name}.blend"
        if not bf.exists():
            print(f"[render] hianyzo eszkoz: {name}")
            return []
        before = set(bpy.data.objects)
        bpy.ops.wm.append(filepath=str(bf) + "/Collection/" + name,
                          directory=str(bf) + "/Collection/", filename=name)
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            if o.parent:
                continue
            o.location = (loc[0] * SIZE, loc[1] * SIZE, loc[2] * SIZE)
            o.rotation_euler.z += math.radians(rot_z)
            o.scale = tuple(c * scale for c in o.scale)
        return new

    # A referencia-kompozicio (VyvaStudio 22-es kep): enyhen hatradolt keret
    # vilagos tolgy komodon, lathato asztal-el + also szekrenyfront, sima meleg-
    # feher fal, balra vesszokosar, jobbra ket feher facettalt vaza.
    # Pontos merev transzformacio TETSZOLEGES dolesszogre: a 88/90 fokos
    # elteres egyszer mar a lap moge sullyesztette a gravirt.
    _th = math.radians(86.5)
    _ct, _st = math.cos(_th), math.sin(_th)
    for o in objs + FRAME_OBJS:
        o.rotation_euler = (_th, 0, 0)
        ox, oy, oz = o.location.x, o.location.y, o.location.z
        o.location = (ox, oy * _ct - oz * _st, oy * _st + oz * _ct)
    bpy.context.view_layer.update()
    _wb = world_bbox([o for o in objs if o not in ENGRAVE_OBJS] + FRAME_OBJS)
    _zmin = min(q.z for q in _wb)
    print(f"[render] styled ules: zmin={_zmin:.4f}")
    for o in objs + FRAME_OBJS:
        o.location.z -= _zmin

    OAK = (0.590, 0.450, 0.295, 1)
    # komod-lap lathato elullso ellel (a referencian latszik az asztal ele)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -SIZE * 0.16, -SIZE * 0.021))
    tb = bpy.context.object
    tb.scale = (SIZE * 5.0, SIZE * 1.05, SIZE * 0.042)
    tb.data.materials.append(wood("tabletop", OAK, 0.55, grain=True))
    # szekrenytest a lap alatt, ket ajtofronttal (kozepen res)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -SIZE * 0.14, -SIZE * 0.62))
    _body = bpy.context.object
    _body.scale = (SIZE * 4.9, SIZE * 1.0, SIZE * 1.15)
    _body.data.materials.append(wood("cabinet", (0.470, 0.350, 0.225, 1),
                                     0.62, grain=True))
    for _dz in (0.155, 0.395):
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(0, -SIZE * 0.655, -SIZE * (0.042 + _dz)))
        _dw = bpy.context.object
        _dw.scale = (SIZE * 2.3, SIZE * 0.02, SIZE * 0.20)
        _dw.data.materials.append(wood("drawer", tuple(c * 0.97 for c in OAK[:3]) + (1,),
                                       0.55, grain=True))
        bpy.ops.mesh.primitive_cylinder_add(radius=SIZE * 0.009, depth=SIZE * 0.11,
                                            location=(0, -SIZE * 0.672,
                                                      -SIZE * (0.042 + _dz)),
                                            rotation=(0, math.radians(90), 0))
        _hd = bpy.context.object
        _hd.data.materials.append(wood("handle", (0.16, 0.12, 0.09, 1), 0.4,
                                       grain=False))

    # sima melegfeher fal kozvetlenul a keret mogott
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, SIZE * 0.30, SIZE * 1.2))
    _wall = bpy.context.object
    _wall.rotation_euler = (math.radians(90), 0, 0)
    _wall.scale = (SIZE * 12, SIZE * 7, 1.0)
    _wall.data.materials.append(wood("wall", (0.860, 0.775, 0.625, 1), 0.92, grain=False))

    # balra vesszokosar az asztalon, jobbra ket feher facettalt vaza -
    # a vazak procedurálisak: alacsony oldalszamu, flat-shaded kup-henger
    import os
    AST = pathlib.Path(__file__).resolve().parent / "pipeline" / "assets"

    def bring(name, loc, rot_z=0.0, scale=1.0):
        bf = AST / "models" / name / f"{name}.blend"
        if not bf.exists():
            print(f"[render] hianyzo eszkoz: {name}")
            return []
        before = set(bpy.data.objects)
        bpy.ops.wm.append(filepath=str(bf) + "/Collection/" + name,
                          directory=str(bf) + "/Collection/", filename=name)
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            if o.parent:
                continue
            o.location = (loc[0] * SIZE, loc[1] * SIZE, loc[2] * SIZE)
            o.rotation_euler.z += math.radians(rot_z)
            o.scale = tuple(c * scale for c in o.scale)
        return new

    bring("wicker_basket_01", (-0.78, -0.38, 0.0), rot_z=20, scale=0.46)

    # jobbra kesz modell a szamolt edenyek helyett (felhasznaloi keres)
    bring("antique_ceramic_vase_01", (0.78, -0.34, 0.0), rot_z=-15, scale=0.62)


if VIEW == "exploded":
    # The reference listing's best-converting gallery image: the sheets fanned
    # apart so the buyer SEES that they are buying six separate layers.
    for o in list(bpy.data.objects):
        # the wall/floor planes of the product-shot setups only pollute this
        # view - the reference floats on white void
        if o.type == "MESH" and max(o.dimensions) > SIZE * 3:
            bpy.data.objects.remove(o, do_unlink=True)
    for o in list(FRAME_OBJS):
        # a keret-test a teljes stack melysegevel keszul; robbantva ez tomor
        # doboznak latszik. Lapitsuk a lapok vastagsagara. A sik hatlapot pedig
        # dobjuk el: a legyezoben csak egy ertelmezhetetlen feher teglalap.
        if o.dimensions.z < THICK * 0.5:
            FRAME_OBJS.remove(o)
            bpy.data.objects.remove(o, do_unlink=True)
        elif o.dimensions.z > THICK * 4:
            o.scale.z *= (THICK * 2.5) / o.dimensions.z
    # a lapok szama a fajlokbol, ne az objektumszambol: a gravir-gorbekkel
    # egyutt a keret a 230. legyezo-poziciora repult (codex)
    nmax = len(svgs)
    # A referencia robbantott kepen a lapok szine sotet acel-teal, a hatlap
    # fekete, es MINDEN lap vagott elet fekete vonal emeli ki (a lezervagott
    # lemez egett ele). Mesh-re konvertalunk: az oldallapok kulon sotet
    # anyagot kapnak, amit a curve-objektum nem tud.
    _expl_faces = [(0.006, 0.008, 0.009, 1), (0.030, 0.055, 0.065, 1),
                   (0.060, 0.100, 0.115, 1), (0.105, 0.165, 0.185, 1),
                   (0.220, 0.290, 0.315, 1), (0.480, 0.560, 0.590, 1)]
    _edge_mat = wood("expl_edge", (0.016, 0.011, 0.008, 1), 0.75, grain=False)
    for _i, _o in enumerate(list(objs)):
        if _o in ENGRAVE_OBJS:
            continue
        _o.data.extrude *= 2.0
        bpy.ops.object.select_all(action="DESELECT")
        _o.select_set(True)
        bpy.context.view_layer.objects.active = _o
        bpy.ops.object.convert(target="MESH")
        _m = _o.data
        if _i < nmax - 1:
            _fm = wood(f"expl_face{_i}", _expl_faces[min(_i, 5)], 0.6, grain=False)
            _m.materials.clear()
            _m.materials.append(_fm)
        _m.materials.append(_edge_mat)
        _ei = len(_m.materials) - 1
        for _poly in _m.polygons:
            if abs(_poly.normal.z) < 0.5:
                _poly.material_index = _ei
    # ALLITOTT lapok melysegi sorban (a felhasznalo 21-es referencia-kepe):
    # minden lap fuggolegesen all, a hatso (grafit hatlap) balra-hatul, minden
    # kovetkezo elorebb (a kamera fele) es kicsit jobbra. A regi vizszintes
    # legyezot a felhasznalo lecserelte erre a kompozicora.
    STEP_X = SIZE * 0.035
    STEP_Y = SIZE * 0.155
    LIFT = SIZE * AY / 2 + SIZE * 0.01
    for o in objs + FRAME_OBJS:
        k = o.location.z / max(1e-9, THICK + GAP)  # hanyadik lap
        if o in FRAME_OBJS:
            # a keret a vizlapok ele, de a terkep-reteg MOGE: a referencian a
            # szarazfold-darabok ralognak a keretlecre
            k = nmax + 0.4
        elif o in ENGRAVE_OBJS:
            k = nmax + 1.35
        elif o.location.z / max(1e-9, THICK + GAP) > nmax - 1.5:
            # a szarazfold-lap a legelso elem, a keret elott
            k = nmax + 1.2
        o.rotation_euler = (math.radians(90), 0, 0)
        ox, oy, oz = o.location.x, o.location.y, o.location.z
        o.location = (ox + k * STEP_X, -oz - k * STEP_Y, oy + LIFT)
    # a keret kulso merete nagyobb a lapoknal: kozepre igazitva az alja lejjebb
    # logott, es "elcsuszott panelnek" olvasodott (reviewer) - also el flush
    bpy.context.view_layer.update()
    _shb = world_bbox([o for o in objs if o not in ENGRAVE_OBJS])
    _frb = world_bbox(FRAME_OBJS)
    _dzf = min(q.z for q in _shb) - min(q.z for q in _frb)
    for o in FRAME_OBJS:
        o.location.z += _dzf
    # feher "vakolat" padlo lagy kontakt-arnyekkal - a referencia feher urben
    # all, alig lathato arnyekkal
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 12,
                                     location=(SIZE * 0.3, -SIZE, -0.0008))
    _fl = bpy.context.object
    _fl.name = "expl_floor"
    _fl.data.materials.append(wood("expl_floor", (0.955, 0.95, 0.945, 1), 0.92,
                                   grain=False))
    # feher vakolatra kerul, mint a referencian - az atlatszo hatter itt
    # feketenek renderelodik minden sotet nezegoteben
    scene.render.film_transparent = False

if VIEW == "plate":
    # stand the piece up, nothing else in the scene
    for o in objs + FRAME_OBJS:
        # pontosan 90: a 88 fok es a 90 fokos pozicio-atkepzes kozti elteres
        # melysegben elnyelte a 0,2 mm-es gravir-rest, es a cimkek a lap moge
        # sullyedtek a kep nagy reszen
        o.rotation_euler = (math.radians(90), 0, 0)
        ox, oy, oz = o.location.x, o.location.y, o.location.z
        o.location = (ox, -oz, oy)
    # ultetes a padlora + vilagos padlolap: a darab alljon valahol, ne
    # lebegjen fekete urben (reviewer P3)
    bpy.context.view_layer.update()
    _pb = world_bbox([o for o in objs if o not in ENGRAVE_OBJS] + FRAME_OBJS)
    _pzmin = min(q.z for q in _pb)
    for o in objs + FRAME_OBJS:
        o.location.z -= _pzmin
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 8, location=(0, -SIZE * 0.5, -0.0004))
    bpy.context.object.data.materials.append(
        wood("studio_floor", (0.90, 0.885, 0.862, 1), 0.85, grain=False))

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
        wood("backwall", (0.552, 0.392, 0.231, 1), 0.88, grain=True))
    def prop(kind, x, y, s_, col, rot=0.0):
        if kind == "cyl":
            bpy.ops.mesh.primitive_cylinder_add(radius=SIZE * s_,
                                                depth=SIZE * s_ * 2.3,
                                                location=(x, y, SIZE * s_ * 1.15))
        elif kind == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=SIZE * s_,
                                                 location=(x, y, SIZE * s_))
        else:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, SIZE * s_ * 0.5))
            bpy.context.object.scale = (SIZE * s_ * 2.6, SIZE * s_ * 1.7, SIZE * s_)
        o = bpy.context.object
        o.rotation_euler = (0, 0, math.radians(rot))
        o.data.materials.append(wood(f"p{len(bpy.data.objects)}", (*col, 1), 0.62,
                                     grain=(kind == "book")))
        return o

    # front right: a small stack of books, like the reference
    # everything sits CLOSER to the frame and partly in front of it, otherwise
    # the props fall outside the crop and the scene reads as an empty sweep
    # recognisable objects, not abstract blocks: a real book stack (thin slabs
    # of different sizes), a potted plant (pot + leaf clumps on stems) and a
    # small carved figure
    for k, (dz, w_, col, rot) in enumerate([
            (0.00, 0.135, (0.42, 0.16, 0.11), 6),
            (0.05, 0.125, (0.24, 0.28, 0.34), -4),
            (0.10, 0.115, (0.55, 0.42, 0.22), 9)]):
        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(SIZE * 0.78, -SIZE * 0.55, SIZE * (dz + 0.025)))
        b = bpy.context.object
        b.scale = (SIZE * w_ * 2.4, SIZE * w_ * 1.6, SIZE * 0.048)
        b.rotation_euler = (0, 0, math.radians(rot))
        b.data.materials.append(wood(f"bk{k}", (*col, 1), 0.55, grain=True))
    # potted plant, left
    bpy.ops.mesh.primitive_cone_add(radius1=SIZE * 0.13, radius2=SIZE * 0.17,
                                    depth=SIZE * 0.26,
                                    location=(-SIZE * 0.82, SIZE * 0.20, SIZE * 0.13))
    bpy.context.object.data.materials.append(
        wood("pot", (0.52, 0.26, 0.15, 1), 0.7, grain=False))
    for lx, ly, lz, lr in [(-0.86, 0.22, 0.42, 0.15), (-0.74, 0.16, 0.36, 0.12),
                           (-0.90, 0.14, 0.30, 0.11), (-0.78, 0.26, 0.50, 0.10)]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=SIZE * lr,
                                             location=(SIZE * lx, SIZE * ly, SIZE * lz))
        bpy.context.object.scale = (1.0, 0.8, 0.55)
        bpy.context.object.data.materials.append(
            wood(f"leaf{lx}", (0.10, 0.26, 0.11, 1), 0.75, grain=False))
    # small carved figure, front left
    prop("cyl", -SIZE * 0.60, -SIZE * 0.52, 0.075, (0.33, 0.19, 0.10))
    prop("sphere", -SIZE * 0.59, -SIZE * 0.52, 0.058, (0.37, 0.22, 0.12))
    # a tall vessel, right background
    prop("cyl", SIZE * 0.98, SIZE * 0.72, 0.30, (0.47, 0.31, 0.18))
    # a patterned runner under everything, just catching the bottom edge
    bpy.ops.mesh.primitive_plane_add(size=SIZE * 5, location=(0, -SIZE * 0.75, 0.0006),
                                     rotation=(0, 0, 0))
    bpy.context.object.data.materials.append(
        wood("runner", (0.55, 0.40, 0.30, 1), 0.9, grain=True))

# ------------------------------------------------------------------ camera + light
# Distance from the framing we want, not a guessed multiplier: at focal length f
# on a 36 mm sensor, a camera d away sees d*36/f across. Solve for the piece plus
# a margin, then add back what the tilt foreshortens. The earlier fixed 1.75x
# multiplier cropped the piece.
LENS, MARGIN = 85.0, 1.22
if FRAME:
    # the frame extends past the art, so the camera must be told the object is
    # bigger - otherwise it fits the art and crops the frame away
    MARGIN *= 1.45 * (SIZE / ART if ART else 1.0)
if VIEW == "exploded":
    # aim at the fan's true centre - a guessed rotation left the subject in a
    # corner of a mostly empty frame
    bpy.context.view_layer.update()
    _pts = world_bbox([o for o in bpy.data.objects if o.type in ("CURVE", "MESH")
                       and o not in ENGRAVE_OBJS and o.name != "expl_floor"])
    cx = (min(q.x for q in _pts) + max(q.x for q in _pts)) / 2
    cy = (min(q.y for q in _pts) + max(q.y for q in _pts)) / 2
    cz = (min(q.z for q in _pts) + max(q.z for q in _pts)) / 2
    ext = max(max(q.x for q in _pts) - min(q.x for q in _pts),
              max(q.y for q in _pts) - min(q.y for q in _pts),
              max(q.z for q in _pts) - min(q.z for q in _pts))
    # allo lapok, 3/4-es nezet balrol-elolrol, enyhen felulrol - a 21-es
    # referencia-kep kameraja. 55 mm: merheto perspektiva-konvergencia,
    # ahogy a referencian, a 85 mm-es tavkep tul lapos volt ehhez.
    D = ext * 3.7
    print(f"[render] exploded fit: ext={ext:.3f} D={D:.3f} c=({cx:.2f},{cy:.2f},{cz:.2f})")
    # atlos nezet balrol, mint a referencian - de az egesz stack a vasznon
    loc = (cx - D * 0.30, cy - D * 0.80, cz + D * 0.11)
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.data.lens = 48.0
    _dir = (cx - loc[0], cy - loc[1], cz - loc[2])
    import mathutils as _mu
    cam.rotation_euler = _mu.Vector(_dir).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam
    print(f"[render] nezet=exploded kozeppont=({cx:.2f},{cy:.2f},{cz:.2f})")
elif VIEW == "styled":
    # A fix 0.62*SIZE celmagassag negyzetes mure volt merve; a 2:1-es terkep
    # kozepe ~0.20-nal van, es a kep felso fele ures fal maradt (reviewer P1,
    # codex). Illesszuk a kamerat a TENYLEGES keret-bboxra: a keret toltse ki
    # a magassag ~65-75%-at.
    bpy.context.view_layer.update()
    _fb = world_bbox([o for o in objs if o not in ENGRAVE_OBJS] + FRAME_OBJS)
    _fW = max(q.x for q in _fb) - min(q.x for q in _fb)
    _fH = max(q.z for q in _fb) - min(q.z for q in _fb)
    _fcz = (min(q.z for q in _fb) + max(q.z for q in _fb)) / 2
    # a referencia arany: a keret a kepszelesseg ~56%-a, korulotte lelegzo fal
    # es komod - a korabbi 74%-os kitoltes tul szoros volt ehhez a kephez
    LENS = 60.0
    D = max(_fW * LENS / 36.0 / 0.54, _fH * LENS / 24.0 / 0.44) * SCENE_ZOOM
    # a cel a keretkozep ala tolodik: a termek feljebb ul a kepben, alatta
    # LATSZIK a komod teste (a felhasznalo kerese: ne csak asztallap legyen)
    TGT = _fcz - _fH * 0.28
    camz = _fcz + _fH * 0.30
    # ~20 fokos 3/4-es szog + enyhe letekintes: a frontalis kamera lapitotta
    # a retegek melyseget (reviewer); a referencia-foto igy keszult
    _lx = -D * 0.36
    # kozel vizszintes kamera: igy a komod ELULSO frontja latszik
    camz = _fcz + _fH * 0.05
    bpy.ops.object.camera_add(location=(_lx, -D, camz))
    import mathutils as _mu3
    _cam = bpy.context.object
    _cam.rotation_euler = _mu3.Vector((0 - _lx, D, TGT - camz)).to_track_quat(
        '-Z', 'Y').to_euler()
    bpy.context.view_layer.objects.active = _cam
    cam = bpy.context.object
    cam.data.lens = LENS
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = D
    cam.data.dof.aperture_fstop = 2.8
    scene.camera = cam
    print(f"[render] nezet=styled tavolsag={D:.3f}")
elif VIEW == "plate":
    # 0.78: a keret a vaszon ~85%-at toltse ki - az 1.0-s szorzoval a kep fele
    # ures fal es padlo volt (reviewer P1)
    D = SIZE * MARGIN * LENS / 36.0 * 0.78
    # a darab mar a padlon ul, a kozepe nem z=0 - oda celozzunk
    bpy.context.view_layer.update()
    _pc = world_bbox([o for o in objs if o not in ENGRAVE_OBJS] + FRAME_OBJS)
    _pcz = (min(q.z for q in _pc) + max(q.z for q in _pc)) / 2
    bpy.ops.object.camera_add(location=(0, -D, _pcz), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.object
    cam.data.lens = LENS
    scene.camera = cam
    print(f"[render] nezet=plate (atlatszo) tavolsag={D:.3f}")
elif VIEW == "lifestyle":
    D = SIZE * MARGIN * LENS / 36.0 * 1.02
    bpy.ops.object.camera_add(location=(0, -D, SIZE * 0.62),
                              rotation=(math.radians(90), 0, 0))
    cam = bpy.context.object
    cam.data.lens = LENS
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = D
    cam.data.dof.aperture_fstop = 2.8   # recognisable but clearly out of focus
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
KEY_E = SIZE * SIZE * (95 if VIEW == "lifestyle" else 105 if VIEW == "plate" else 110)
key = bpy.data.lights.new("key", "AREA"); key.energy = KEY_E
# a small emitter throws a hard, short shadow off every cut edge - that step
# shadow IS the depth cue, and a broad soft light erased it
key.size = SIZE * (0.35 if VIEW == "plate" else 2.0)
if VIEW in ("lifestyle", "plate", "styled"):
    key.color = (1.0, 0.80, 0.60)          # ~2850K, a referencia meleg estifeny-tonusa
ko = bpy.data.objects.new("key", key); scene.collection.objects.link(ko)
if VIEW == "plate":
    # lower and further round: a grazing key lengthens every step shadow
    ko.location = (-SIZE * 1.7, -SIZE * 1.5, SIZE * 0.75)
    ko.rotation_euler = (math.radians(68), 0, math.radians(-42))
else:
    ko.location = (-SIZE * 1.1, -SIZE * 1.1, SIZE * 1.5)
    ko.rotation_euler = (math.radians(38), 0, math.radians(-40))

FILL_E = SIZE * SIZE * (26 if VIEW == "lifestyle" else 9 if VIEW == "plate" else 22)
fill = bpy.data.lights.new("fill", "AREA"); fill.energy = FILL_E; fill.size = SIZE * 5
if VIEW == "lifestyle":
    fill.color = (0.99, 0.98, 0.97)
fo = bpy.data.objects.new("fill", fill); scene.collection.objects.link(fo)
fo.location = (SIZE * 1.6, -SIZE * 0.9, SIZE * 0.9); fo.rotation_euler = (math.radians(65), 0, math.radians(60))

world = bpy.data.worlds.new("w"); scene.world = world
world.use_nodes = True
if VIEW == "exploded":
    # a vilag itt jon letre, MINDEN nezet-blokk utan - a korabban beallitott
    # hatter csendben elveszett. Node nelkul a legegyszerubb es debugolhato.
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.982, 0.980, 0.978, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 2.3
if SCENE_HDRI:
    _hdr = pathlib.Path(__file__).resolve().parent / "pipeline" / "assets" / "hdris" / f"{SCENE_HDRI}.hdr"
    if _hdr.exists():
        _wt = world.node_tree
        _env = _wt.nodes.new("ShaderNodeTexEnvironment")
        _env.image = bpy.data.images.load(str(_hdr))
        _map = _wt.nodes.new("ShaderNodeMapping")
        _map.inputs["Rotation"].default_value[2] = math.radians(120)
        _co = _wt.nodes.new("ShaderNodeTexCoord")
        _wt.links.new(_co.outputs["Generated"], _map.inputs["Vector"])
        _wt.links.new(_map.outputs["Vector"], _env.inputs["Vector"])
        _bg = _wt.nodes["Background"]
        _wt.links.new(_env.outputs["Color"], _bg.inputs["Color"])
        # 1.0 left the room nearly black behind the frame. The reference is a
        # bright, airy daylight interior; the background has to carry light.
        _bg.inputs[1].default_value = 2.6
        print(f"[render] HDRI: {SCENE_HDRI}")
if VIEW == "lifestyle":
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.78, 0.76, 0.72, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
elif VIEW == "plate":
    # vilagos studio-hatter: a darab alljon fenyben, ne fekete urben
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.930, 0.895, 0.835, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.15
elif VIEW != "exploded":
    # Ez a sotet alap-hatter irta felul csendben az exploded nezet feher
    # vakolat-hatteret is - a debug-lanc (magenta-teszt, objektum-dump) vegen a
    # 0,55 x 0,06 = 0,033 pontosan a mert 43-as szurket adta.
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.52, 0.48, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.06


if ORBIT:
    # 144 Cycles frames took three hours per video - fifteen hours for five.
    # These are flat-shaded paper planes with one key light: Eevee renders them
    # in seconds and the difference is invisible at 1080 px.
    try:
        scene.render.engine = "BLENDER_EEVEE"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    es = scene.eevee
    for attr, val in (("taa_render_samples", 24), ("use_shadows", True),
                      ("use_raytracing", True), ("use_gtao", True)):
        if hasattr(es, attr):
            setattr(es, attr, val)
    # a short left-right arc reads as "turning it in your hand" and shows the
    # layer edges - a static hero cannot show depth, which is the whole product
    import os
    base = OUT[:-4] if OUT.endswith(".png") else OUT
    scene.cycles.samples = 48
    scene.render.resolution_x = scene.render.resolution_y = 1100
    for f in range(ORBIT):
        # f/ORBIT, not f/(ORBIT-1): the last frame must NOT repeat the first,
        # or the loop stutters on every cycle
        t = f / ORBIT if ORBIT > 1 else 0.5
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
