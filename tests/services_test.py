from fractions import Fraction

import pytest
import math

from polyshifter.models import Polygon
from polyshifter.services import offset_segment
from tests.params import POLYGON_OFFSET_PARAMS


@pytest.mark.parametrize("points, seg_idx, offset, res_points", POLYGON_OFFSET_PARAMS)
def test_map(points, seg_idx, offset, res_points):
    if res_points is ValueError:
        with pytest.raises(ValueError):
            offset_segment(points, seg_idx, offset)
    else:
        res = offset_segment(points, seg_idx, offset)
        compare_polygons(res.result_polygon, Polygon(res_points))

def compare_polygons(p1: Polygon, p2: Polygon, accuracy: int = 3):
    assert len(p1.points) == len(p2.points), "Polygons have different number of points."

    for p1_point, p2_point in zip(p1.points, p2.points):
        assert floor_value(p1_point.x, accuracy) == floor_value(p2_point.x, accuracy)
        assert floor_value(p1_point.y, accuracy) == floor_value(p2_point.y, accuracy)

def floor_value(value: Fraction, accuracy: int = 4) -> Fraction:
    return math.floor(value * 10**accuracy) / 10**accuracy
