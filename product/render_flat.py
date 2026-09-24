"""Straight-on gallery renders of a layered piece: flat-lay hero and close-ups.

The gallery that sells this niche (MarLaserCut, measured 2026-09-24) is not a
perspective 3D render in a wooden frame. It shows the piece straight-on, lying
on a light plaster surface, with crisp sheet-to-sheet shadows, and then crops
into the detail. An orthographic top-down camera with a raking sun gives that;
the close-ups are rendered at full resolution, not upscaled crops.

  blender -b --python-exit-code 1 -P product/render_flat.py -- LAYERS OUT.png \
      [--crop x0,y0,x1,y1] [--palette FILE] [--bg TEXTURE] [--size 2700x2025]

--crop is in panel fractions, y measured from the TOP edge.
"""
import argparse
import json
import math
import pathlib
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("layers")
ap.add_argument("out")
ap.add_argument("--crop", default=None, help="x0,y0,x1,y1 panel fractions, y from the top")
ap.add_argument("--palette", default=None, help="sheet colours, sRGB 0-255; default LAYERS/palette.json")
ap.add_argument("--bg", default=None, help="surface texture; default: plain light grey")
ap.add_argument("--bg-tile", type=float, default=0.45, help="m of surface one texture tile covers")
ap.add_argument("--bg-tones", default="#B9BAB8,#ECECEA",
                help="dark,light: the texture keeps its mottling, not its colour")
ap.add_argument("--size", default="2700x2025")
ap.add_argument("--margin", type=float, default=0.12, help="surface visible around the piece")
ap.add_argument("--shift", type=float, default=0.0,
                help="hero: move the piece up by this fraction of the frame (room for a caption)")
ap.add_argument("--thick", type=float, default=1.5, help="mm per sheet")
ap.add_argument("--gap", type=float, default=1.2, help="mm spacer between sheets")
ap.add_argument("--lift", type=float, default=5.0, help="mm between the surface and the back sheet")
ap.add_argument("--sun", default="135,40", help="azimuth,elevation in degrees")
ap.add_argument("--exposure", type=float, default=0.0)
ap.add_argument("--samples", type=int, default=96)
a = ap.parse_args(argv)

MM = 0.001
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
src = pathlib.Path(a.layers)
svgs = sorted(src.glob("layer_*_of_*.svg"), key=lambda p: int(p.stem.split("_")[1]))
if not svgs:
    raise SystemExit(f"no layer SVGs in {src}")
palette = json.loads(pathlib.Path(a.palette or src / "palette.json").read_text())
if len(palette) < len(svgs):
    raise SystemExit(f"palette has {len(palette)} colours for {len(svgs)} sheets")


def linear(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return (*(ch(v) for v in rgb), 1.0)


def paper(name, rgb):
    """Matte card with a faint fibre bump - flat colour reads as plastic."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = linear(rgb)
    bsdf.inputs["Roughness"].default_value = 0.92
    bsdf.inputs["Specular IOR Level"].default_value = 0.15
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 2500.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.04
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def mesh_bounds(objects):
    """Tessellated vertices: bound_box of SVG-imported curves is unreliable."""
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in objects:
        oe = o.evaluated_get(dg)
        me = oe.to_mesh()
        pts += [oe.matrix_world @ v.co for v in me.vertices]
        oe.to_mesh_clear()
    return (min(p.x for p in pts), min(p.y for p in pts),
            max(p.x for p in pts), max(p.y for p in pts))


sheets = []
for i, f in enumerate(svgs):
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=str(f))
    mat = paper(f"sheet_{i + 1}", palette[i])
    for o in (o for o in bpy.data.objects if o not in before and o.type == "CURVE"):
        o.data.dimensions = "2D"
        o.data.fill_mode = "BOTH"
        o.data.extrude = a.thick * MM / 2
        o.data.materials.clear()
        o.data.materials.append(mat)
        o.location.z = (a.lift + i * (a.thick + a.gap) + a.thick / 2) * MM
        sheets.append(o)

x0, y0, x1, y1 = mesh_bounds(sheets)
for o in sheets:
    o.location.x -= (x0 + x1) / 2
    o.location.y -= (y0 + y1) / 2
W, H = x1 - x0, y1 - y0

# surface
bpy.ops.mesh.primitive_plane_add(size=max(W, H) * 6)
surface = bpy.context.object
sm = bpy.data.materials.new("surface")
sm.use_nodes = True
sb = sm.node_tree.nodes["Principled BSDF"]
sb.inputs["Roughness"].default_value = 0.95
if a.bg:
    nt = sm.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(pathlib.Path(a.bg).resolve()))
    mapping = nt.nodes.new("ShaderNodeMapping")
    s = max(W, H) * 6 / a.bg_tile
    mapping.inputs["Scale"].default_value = (s, s, 1)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["UV"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
    # Photo textures carry their own tint and exposure; map the mottling onto
    # a chosen light grey so the surface frames the piece instead of muddying it.
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    stretch = nt.nodes.new("ShaderNodeMapRange")
    stretch.inputs["From Min"].default_value = 0.25
    stretch.inputs["From Max"].default_value = 0.75
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    dark, light = (h.strip().lstrip("#") for h in a.bg_tones.split(","))
    ramp.color_ramp.elements[0].color = linear([int(dark[i:i + 2], 16) for i in (0, 2, 4)])
    ramp.color_ramp.elements[1].color = linear([int(light[i:i + 2], 16) for i in (0, 2, 4)])
    nt.links.new(tex.outputs["Color"], bw.inputs["Color"])
    nt.links.new(bw.outputs["Val"], stretch.inputs["Value"])
    nt.links.new(stretch.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], sb.inputs["Base Color"])
else:
    sb.inputs["Base Color"].default_value = (0.78, 0.78, 0.77, 1)
surface.data.materials.append(sm)

# light: one raking sun for the sheet-to-sheet shadows, a dim world as fill
az, el = (math.radians(float(v)) for v in a.sun.split(","))
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2
sun.data.angle = math.radians(3.0)
sun.rotation_euler = (math.pi / 2 - el, 0, az)
scene.collection.objects.link(sun)
scene.world = bpy.data.worlds.new("fill")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.85, 0.87, 0.9, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45

# orthographic camera, straight down
rw, rh = (int(v) for v in a.size.lower().split("x"))
aspect = rw / rh
if a.crop:
    fx0, fy0, fx1, fy1 = (float(v) for v in a.crop.split(","))
    cx = -W / 2 + W * (fx0 + fx1) / 2
    cy = H / 2 - H * (fy0 + fy1) / 2
    view_w, view_h = W * (fx1 - fx0), H * (fy1 - fy0)
else:
    view_w, view_h = W * (1 + 2 * a.margin), H * (1 + 2 * a.margin)
    frame_h = max(view_h, view_w / aspect)
    cx, cy = 0.0, -a.shift * frame_h
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.type = "ORTHO"
cam.data.ortho_scale = max(view_w, view_h * aspect) if aspect >= 1 else max(view_h, view_w / aspect)
cam.location = (cx, cy, 1.0)
scene.collection.objects.link(cam)
scene.camera = cam

scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
for backend in ("METAL", "OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = backend
        prefs.get_devices()
        if any(d.type == backend for d in prefs.devices):
            for d in prefs.devices:
                d.use = True
            scene.cycles.device = "GPU"
            break
    except TypeError:
        continue
scene.cycles.samples = a.samples
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = rw, rh
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "Standard"   # the palette, not a film look
scene.view_settings.exposure = a.exposure
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = str(pathlib.Path(a.out).resolve())
bpy.ops.render.render(write_still=True)
print(f"[flat] {len(svgs)} sheets, panel {W / MM:.0f}x{H / MM:.0f} mm, "
      f"{'crop ' + a.crop if a.crop else 'hero'} -> {a.out}")
