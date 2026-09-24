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
