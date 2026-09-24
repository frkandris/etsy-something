"""The tracing pipeline must measure real polygons inside mixed geometry."""
import importlib.util
from pathlib import Path
import sys

import pytest
from shapely.geometry import GeometryCollection, LineString, box

PIPE = Path(__file__).resolve().parents[1] / 'product/pipeline'
sys.path.insert(0, str(PIPE))
spec = importlib.util.spec_from_file_location('trace_pipeline', PIPE / '02_trace.py')
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)


def test_trace_measures_polygons_inside_nested_geometry_collection():
    mixed = GeometryCollection([box(0, 0, 10, 5), GeometryCollection([
        LineString([(20, 0), (30, 0)]), box(40, 0, 50, 8)])])
    assert trace.frailest(mixed) == pytest.approx(5, abs=0.001)
    assert trace.necks(mixed) == 0


def test_panel_fit_moves_deepest_eye_opening_with_every_other_sheet():
    panel = box(0, 0, 100, 100)
    deep_eye = box(70, 30, 80, 40)
    wide_eye = box(60, 20, 90, 50)
    layers = {1: panel.difference(deep_eye), 2: panel.difference(wide_eye)}
    fitted, scale, dx, dy = trace.fit_panel_openings(layers, panel, panel.buffer(-10))
    assert (scale, dx, dy) == (1, -25, 15)
    # The deepest hole must move too; otherwise nesting carves two false eyes.
    assert panel.difference(fitted[1]).symmetric_difference(box(45, 45, 55, 55)).area < 0.01
    assert fitted[2].difference(fitted[1]).area < 0.01
    assert fitted[1].contains(deep_eye)


def test_panel_fit_scales_all_openings_into_margin_without_depth_changes():
    panel = box(0, 0, 100, 100)
    layers = {1: panel.difference(box(60, 40, 80, 60)),
              2: panel.difference(box(10, 20, 100, 80))}
    fitted, scale, _, _ = trace.fit_panel_openings(layers, panel, panel.buffer(-20))
    # The outer millimetre is frame band, not opening (trace slivers live
    # there), so layer 2's opening spans x 10..99 and fits 60 mm: 60/89.
    assert scale == pytest.approx(60 / 89)
    edge = panel.difference(panel.buffer(-1.0))
    for k in layers:
        before = panel.difference(layers[k]).difference(edge).area
        after = panel.difference(fitted[k])
        assert panel.buffer(-19.99).contains(after)
        assert after.area == pytest.approx(before * scale**2, rel=1e-3)   # 0.01 mm grid
    assert fitted[2].difference(fitted[1]).area < 0.01


@pytest.mark.parametrize('geom', [GeometryCollection(), LineString([(0, 0), (1, 1)])])
def test_empty_material_has_actionable_error(geom):
    with pytest.raises(ValueError, match='No polygon material remains'):
        trace.frailest(geom)


def test_sheet_colours_set_the_order_not_luminance(tmp_path):
    """A pale sky can be the deepest sheet and cream foam the top one."""
    import json
    import subprocess
    import sys
    from pathlib import Path

    import numpy as np
    from PIL import Image

    root = Path(__file__).resolve().parents[1]
    art = np.zeros((60, 90, 3), dtype=np.uint8)
    art[:, :] = (240, 228, 200)          # pale sky   -> sheet 0 (backing)
    art[20:60, :] = (30, 50, 90)         # dark wave  -> sheet 1
    art[20:30, 30:60] = (250, 245, 235)  # cream foam -> sheet 2 (top), lightest
    art[21, 31] = (200, 60, 60)          # model drift: nearest colour wins
    Image.fromarray(art).save(tmp_path / 'art.png')
    subprocess.run([sys.executable, str(root / 'product/pipeline/01b_depth.py'),
                    '--art', str(tmp_path / 'art.png'), '--out', str(tmp_path / 'depth.png'),
                    '--sheet-colours', '#F0E4C8,#1E325A,#FAF5EB', '--min-region-pct', '0'],
                   check=True, capture_output=True)
    depth = np.asarray(Image.open(tmp_path / 'depth.png'))
    assert depth[5, 5] == 0 and depth[50, 10] == 127 and depth[25, 45] == 255
    palette = json.loads((tmp_path / 'palette_full.json').read_text())
    assert len(palette) == 3 and palette[2][0] > 240 and palette[1][2] < 100


def test_scene_makes_the_back_colour_a_solid_first_sheet(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path

    import numpy as np
    from PIL import Image

    root = Path(__file__).resolve().parents[1]
    art = np.zeros((40, 60, 3), dtype=np.uint8)
    art[:, :] = (240, 228, 200)          # sky touches every edge
    art[20:, :] = (30, 50, 90)
    Image.fromarray(art).save(tmp_path / 'art.png')
    subprocess.run([sys.executable, str(root / 'product/pipeline/01b_depth.py'),
                    '--art', str(tmp_path / 'art.png'), '--out', str(tmp_path / 'depth.png'),
                    '--sheet-colours', '#F0E4C8,#1E325A', '--scene', '--min-region-pct', '0'],
                   check=True, capture_output=True)
    depth = np.asarray(Image.open(tmp_path / 'depth.png'))
    assert depth.shape == (46, 66)
    assert depth[0].max() == 0 and depth[3:-3, 3:-3].min() > 0     # only the rim is cut away
    assert depth[5, 30] == 127 and depth[40, 30] == 255
    assert len(json.loads((tmp_path / 'palette_full.json').read_text())) == 3
