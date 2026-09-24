"""Cross-format smoke check using an offline source with known layer structure."""
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(not shutil.which('potrace'), reason='potrace is required for SVG tracing')
@pytest.mark.parametrize('full_panel', [False, True])
def test_real_trace_exports_matching_svg_dxf_set(tmp_path, full_panel):
    source = tmp_path / 'source.png'
    img = Image.new('L', (256, 256), 240 if full_panel else 0)
    draw = ImageDraw.Draw(img)
    for k in range(1, 7):
        inset = 10 + (k - 1) * 15
        draw.rectangle((inset, inset, 255 - inset, 255 - inset),
                       fill=(6 - k) * 40 if full_panel else k * 40)
    if full_panel:
        # Decorative negative space is allowed to be narrower than a 5 mm
        # morphological closing, even though material bridges must be safe.
        draw.rectangle((25, 20, 28, 55), fill=0)
    img.save(source)
    out = tmp_path / 'layers'
    palette = tmp_path / 'palette.json'
    palette.write_text(json.dumps([[k * 35] * 3 for k in range(7)]))
    subprocess.run([sys.executable, str(ROOT / 'product/pipeline/02_trace.py'),
                    '--src', str(source), '--out', str(out), '--levels', '6',
                    '--no-keyhole', '--min-part', '20', '--merge-below', '0.001',
                    '--palette', str(palette), *(['--full-panel', '--margin', '14'] if full_panel else [])],
                   check=True, capture_output=True)
    report = json.loads((out / 'report.json').read_text())
    assert report['all_ok'] and report['release_ready'] and not report['draft']
    svgs, dxfs = sorted(out.glob('layer_*.svg')), sorted(out.glob('layer_*.dxf'))
    assert len(svgs) == len(dxfs) == report['levels'] == 6
    assert {p.stem for p in svgs} == {p.stem for p in dxfs}
    assert report['backing_required'] == full_panel
    if full_panel:
        first_path = ET.parse(svgs[0]).getroot().find('{http://www.w3.org/2000/svg}path')
        rings = []
        for ring in first_path.get('d').split('Z'):
            values = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', ring)]
            if values:
                xs, ys = values[::2], values[1::2]
                rings.append((max(xs) - min(xs), max(ys) - min(ys)))
        assert any(1 < w < 5 and h > 20 for w, h in rings), rings
        assert (out / 'backing.svg').is_file() and (out / 'backing.dxf').is_file()
        assert json.loads((out / 'backing_palette.json').read_text()) == [0, 0, 0]
    assert len(json.loads((out / 'palette.json').read_text())) == 6
    for svg in svgs:
        tree = ET.parse(svg)
        assert tree.getroot().get('width') == '300.0mm'
        assert tree.getroot().find('{http://www.w3.org/2000/svg}path') is not None
    for dxf in dxfs:
        text = dxf.read_text()
        assert '$INSUNITS\n70\n4' in text
        assert text.rstrip().endswith('EOF')


def _svg_ys(path):
    d = ET.parse(path).getroot().find('{http://www.w3.org/2000/svg}path').get('d')
    return [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', d)][1::2]


def _dxf_ys(path):
    lines = path.read_text().split('\n')
    return [float(lines[i + 6]) for i in range(len(lines) - 6)
            if lines[i] == 'VERTEX' and lines[i + 5] == '20']


@pytest.mark.skipif(not shutil.which('potrace'), reason='potrace is required for SVG tracing')
def test_dxf_is_not_upside_down_relative_to_svg(tmp_path):
    # Symmetric, centred test art cannot show a vertical flip. Here the upper
    # layers sit high on the canvas, so an unflipped DXF lands them low.
    source = tmp_path / 'source.png'
    img = Image.new('L', (256, 256), 0)
    draw = ImageDraw.Draw(img)
    for k in range(1, 7):
        draw.rectangle((10 + (k - 1) * 12, 10 + (k - 1) * 8,
                        245 - (k - 1) * 12, 245 - (k - 1) * 30), fill=k * 40)
    img.save(source)
    out = tmp_path / 'layers'
    subprocess.run([sys.executable, str(ROOT / 'product/pipeline/02_trace.py'),
                    '--src', str(source), '--out', str(out), '--levels', '6',
                    '--no-keyhole', '--min-part', '20', '--merge-below', '0.001'],
                   check=True, capture_output=True)
    size = json.loads((out / 'report.json').read_text())['size_mm']
    top = sorted(out.glob('layer_*.svg'))[-1]
    svg_ys, dxf_ys = _svg_ys(top), _dxf_ys(top.with_suffix('.dxf'))
    assert max(svg_ys) < size / 2                       # SVG: near the top edge
    assert min(dxf_ys) == pytest.approx(size - max(svg_ys), abs=0.01)
    assert max(dxf_ys) == pytest.approx(size - min(svg_ys), abs=0.01)


@pytest.mark.skipif(not shutil.which('potrace'), reason='potrace is required for SVG tracing')
def test_scene_keeps_the_frame_band_on_every_sheet(tmp_path):
    # An edge-to-edge scene (sky touching the border, 01b_depth --scene): only
    # a thin rim is level 0. Hairline trace slivers at the panel edge used to
    # be scaled into a cut just inside the frame, and the frame was dropped.
    source = tmp_path / 'scene.png'
    img = Image.new('L', (306, 206), 0)
    draw = ImageDraw.Draw(img)
    draw.rectangle((3, 3, 302, 202), fill=60)                  # sheet 1: solid back
    draw.polygon([(3, 120), (150, 60), (302, 110), (302, 202), (3, 202)], fill=120)
    draw.polygon([(3, 160), (120, 110), (302, 150), (302, 202), (3, 202)], fill=180)
    draw.polygon([(3, 185), (150, 170), (302, 180), (302, 202), (3, 202)], fill=240)
    draw.ellipse((200, 30, 250, 80), fill=240)                 # floating accent
    img.save(source)
    out = tmp_path / 'layers'
    subprocess.run([sys.executable, str(ROOT / 'product/pipeline/02_trace.py'),
                    '--src', str(source), '--out', str(out), '--size', '300',
                    '--levels', '4', '--no-keyhole', '--min-part', '20',
                    '--merge-below', '0.001', '--margin', '12', '--connected'],
                   check=True, capture_output=True)
    report = json.loads((out / 'report.json').read_text())
    width, height = report['panel_mm']
    assert width == 300.0 and 190 < height < 205          # 3:2-ish, not a square
    for svg in sorted(out.glob('layer_*.svg')):
        root = ET.parse(svg).getroot()
        assert root.get('height') == f'{height}mm'
        values = [float(v) for v in re.findall(r'-?\d+\.?\d*',
                                               root.find('{http://www.w3.org/2000/svg}path').get('d'))]
        xs, ys = values[::2], values[1::2]
        assert min(xs) < 0.5 and max(xs) > width - 0.5, svg.name     # frame band present
        assert min(ys) < 0.5 and max(ys) > height - 0.5, svg.name
