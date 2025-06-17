from fractions import Fraction

import pytest
import math

from polyshifter.geometry import Polygon
from tests.params import POLYGON_OFFSET_PARAMS


@pytest.mark.parametrize("points, seg_idx, offset, res_points", POLYGON_OFFSET_PARAMS)
def test_map(points, seg_idx, offset, res_points):
    polygon = Polygon(points)

    if res_points == ValueError:
        with pytest.raises(ValueError):
            polygon.offset_segment(seg_idx, offset)
    else:
        offset_polygon = polygon.offset_segment(seg_idx, offset)
        compare_polygons(offset_polygon, Polygon(res_points))

def compare_polygons(p1: Polygon, p2: Polygon, accuracy: int = 3):
    assert len(p1.points) == len(p2.points), "Polygons have different number of points."

    for p1_point, p2_point in zip(p1.points, p2.points):
        assert floor_value(p1_point.x, accuracy) == floor_value(p2_point.x, accuracy)
        assert floor_value(p1_point.y, accuracy) == floor_value(p2_point.y, accuracy)

def floor_value(value: Fraction, accuracy: int = 4) -> Fraction:
    return math.floor(value * 10**accuracy) / 10**accuracy
