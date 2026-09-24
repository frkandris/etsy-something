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
    assert scale == pytest.approx(2 / 3)
    for k in layers:
        before = panel.difference(layers[k]).area
        after = panel.difference(fitted[k])
        assert panel.buffer(-19.99).contains(after)
        assert after.area == pytest.approx(before * scale**2, abs=0.2)
    assert fitted[2].difference(fitted[1]).area < 0.01


@pytest.mark.parametrize('geom', [GeometryCollection(), LineString([(0, 0), (1, 1)])])
def test_empty_material_has_actionable_error(geom):
    with pytest.raises(ValueError, match='No polygon material remains'):
        trace.frailest(geom)
