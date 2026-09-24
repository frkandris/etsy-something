"""Offline geometry fixtures for the flat map's release gate."""
import importlib.util
from pathlib import Path
import sys

import pytest
from shapely.geometry import box, mapping

PIPE = Path(__file__).resolve().parents[1] / 'product/pipeline'
sys.path.insert(0, str(PIPE))
spec = importlib.util.spec_from_file_location('flat_map', PIPE / '11_worldmap_flat.py')
flat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flat)


def test_entirely_thin_island_is_not_a_valid_release(tmp_path, monkeypatch):
    # At 100 mm total width, this country is about 1 mm tall. Erosion removes
    # the whole piece, so neck count alone misleadingly reports zero.
    feature = {'type': 'Feature', 'properties': {'CONTINENT': 'Africa', 'NAME': 'Thinland'},
               'geometry': mapping(box(0, 0, 10, 0.1))}
    monkeypatch.setattr(flat, 'fetch', lambda _: {'features': [feature]})
    out = tmp_path / 'output'
    out.mkdir()
    (out / 'old.svg').write_text('previous valid output')
    monkeypatch.setattr(sys, 'argv', ['flat_map', '--out', str(out), '--width', '100',
                                     '--min-island', '40', '--no-labels'])
    with pytest.raises(ValueError, match='Hibás vágásgeometria'):
        flat.main()
    assert (out / 'old.svg').read_text() == 'previous valid output'
    assert not (out / 'report.json').exists()


def test_flat_map_dxf_is_north_up_like_its_svg(tmp_path, monkeypatch):
    from shapely.geometry import Polygon
    # A country whose peak points north: in the DXF (Y up) the peak must have
    # the largest Y; the old `H - y` wrote the whole map upside down.
    feature = {'type': 'Feature', 'properties': {'CONTINENT': 'Africa', 'NAME': 'Peakland'},
               'geometry': mapping(Polygon([(0, 0), (20, 40), (40, 0)]))}
    monkeypatch.setattr(flat, 'fetch', lambda _: {'features': [feature]})
    out = tmp_path / 'output'
    monkeypatch.setattr(sys, 'argv', ['flat_map', '--out', str(out), '--width', '300',
                                     '--no-labels', '--draft'])
    flat.main()
    lines = (out / 'world_map.dxf').read_text().split('\n')
    cut = [(float(lines[i + 4]), float(lines[i + 6])) for i in range(len(lines) - 6)
           if lines[i] == 'VERTEX' and lines[i + 2] == 'CUT']
    peak = max(cut, key=lambda p: p[1])
    xs = [x for x, _ in cut]
    assert abs(peak[0] - (min(xs) + max(xs)) / 2) < 1.0
