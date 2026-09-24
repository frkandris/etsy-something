"""The map model is north-up (Y grows north), like DXF; SVG grows Y downward.

Both world-map writers once wrote `H - y` into the DXF as well, so every cut
file came out upside down relative to its SVG and its own labels.
"""
import importlib.util
from pathlib import Path
import re

from shapely.geometry import Polygon

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'product/pipeline' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _dxf_vertices(text):
    lines = text.split('\n')
    return [(float(lines[i + 4]), float(lines[i + 6])) for i in range(len(lines) - 6)
            if lines[i] == 'VERTEX' and lines[i + 3] == '10' and lines[i + 5] == '20']


def test_worldmap_dxf_keeps_north_up_and_svg_puts_north_on_top(tmp_path):
    worldmap = _load('10_worldmap')
    apex_north = Polygon([(10, 10), (50, 90), (90, 10)])      # peak points north
    worldmap.to_dxf(apex_north, tmp_path / 'map.dxf')
    worldmap.to_svg(apex_north, 100, 100, tmp_path / 'map.svg')
    dxf = _dxf_vertices((tmp_path / 'map.dxf').read_text())
    assert max(dxf, key=lambda p: p[1]) == (50, 90)             # DXF: north is +Y
    d = re.search(r' d="([^"]+)"', (tmp_path / 'map.svg').read_text()).group(1)
    pts = [tuple(map(float, xy.split(','))) for xy in re.findall(r'-?[\d.]+,-?[\d.]+', d)]
    assert min(pts, key=lambda p: p[1]) == (50, 10)             # SVG: north is top
