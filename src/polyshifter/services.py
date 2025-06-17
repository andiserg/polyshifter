from dataclasses import dataclass
from fractions import Fraction

from polyshifter.models import Polygon, Segment, Point

@dataclass(slots=True, frozen=True)
class OutputData:
    polygon: Polygon
    offset_arrow: Segment


def offset_segment(
    polygon: Polygon,
    segment_index: int,
    offset_magnitude: float,
) -> OutputData:
    if not (0 <= segment_index < len(polygon.segments)):
        raise IndexError("Segment index out of bounds.")

    magnitude: Fraction = Fraction(str(offset_magnitude))
    segment = polygon.segments[segment_index]

    perp_vec = segment.perpendicular_vector(magnitude < 0)
    norm_perp = perp_vec.get_normalized()

    offseted_segment = Segment(
        Point(
            segment.p1.x + norm_perp.x * abs(magnitude),
            segment.p1.y + norm_perp.y * abs(magnitude),
        ),
        Point(
            segment.p2.x + norm_perp.x * abs(magnitude),
            segment.p2.y + norm_perp.y * abs(magnitude),
        ),
    )

    # calculate offset arrow
    center_before = segment.get_midpoint()
    center_after = Point(
        center_before.x + norm_perp.x * abs(magnitude),
        center_before.y + norm_perp.y * abs(magnitude),
    )

    prev_index = (segment_index - 1 + len(polygon.segments)) % len(polygon.segments)
    next_index = (segment_index + 1) % len(polygon.segments)

    new_p1 = polygon.segments[prev_index].line_intersection(offseted_segment)
    new_p2 = polygon.segments[next_index].line_intersection(offseted_segment)

    if new_p1 is None or new_p2 is None:
        raise ValueError(
            f"Could not find intersection for the "
            f"first point of segment {segment_index}. "
            "Previous segment is parallel to the offset segment's shifted line.",
        )

    new_points_coords_list = [(p.x, p.y) for i, p in enumerate(polygon.points[:-1])]
    new_points_coords_list[segment_index] = (new_p1.x, new_p1.y)
    new_points_coords_list[next_index] = (new_p2.x, new_p2.y)
    new_points_coords_list.append(new_points_coords_list[0])

    res = Polygon(new_points_coords_list)

    # Check that neighbor segments preserve the original polygon's direction
    if not all((
        polygon.segments[next_index].is_same_dir(res.segments[next_index]),
        polygon.segments[prev_index].is_same_dir(res.segments[prev_index]),
    )):
        raise ValueError(
            f"Offset segment {segment_index} does not "
            f"preserve the original polygon's direction.",
        )

    return OutputData(res, Segment(center_before, center_after))
