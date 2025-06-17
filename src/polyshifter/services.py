from fractions import Fraction

from polyshifter.models import Polygon, Segment, Point


def offset_segment(self, segment_index: int, offset_magnitude: float) -> Polygon:
    if not (0 <= segment_index < len(self.segments)):
        raise IndexError("Segment index out of bounds.")

    magnitude: Fraction = Fraction(str(offset_magnitude))

    original_segment = self.segments[segment_index]
    perp_vec = original_segment.perpendicular_vector(magnitude < 0)

    norm_perp = perp_vec.get_normalized()

    offseted_segment = Segment(
        Point(
            original_segment.p1.x + norm_perp.x * abs(magnitude),
            original_segment.p1.y + norm_perp.y * abs(magnitude),
        ),
        Point(
            original_segment.p2.x + norm_perp.x * abs(magnitude),
            original_segment.p2.y + norm_perp.y * abs(magnitude),
        ),
    )

    prev_index = (segment_index - 1 + len(self.segments)) % len(self.segments)
    next_index = (segment_index + 1) % len(self.segments)

    prev_segment = self.segments[prev_index]
    next_segment = self.segments[next_index]

    new_p1 = prev_segment.line_intersection(offseted_segment)
    new_p2 = offseted_segment.line_intersection(next_segment)

    if new_p1 is None or new_p2 is None:
        raise ValueError(
            f"Could not find intersection for the "
            f"first point of segment {segment_index}. "
            "Previous segment is parallel to the offset segment's shifted line.",
        )

    new_points_coords_list = [(p.x, p.y) for p in self.points[:-1]]
    new_points_coords_list[segment_index] = (new_p1.x, new_p1.y)
    new_points_coords_list[
        (segment_index + 1) % (len(self.points) - 1)
        ] = (new_p2.x, new_p2.y)

    if new_points_coords_list:
        new_points_coords_list.append(new_points_coords_list[0])

    res = Polygon(new_points_coords_list)

    if not all((
        next_segment.is_same_dir(res.segments[next_index]),
        prev_segment.is_same_dir(res.segments[prev_index]),
    )):
        raise ValueError(
            f"Offset segment {segment_index} does not "
            f"preserve the original polygon's direction.",
        )

    return res