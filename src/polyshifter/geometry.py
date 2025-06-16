import math
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def get_normalized(self):
        length = self.distance_to(Point(0, 0))
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        return Point(self.x / length, self.y / length)


@dataclass(slots=True, frozen=True)
class Segment:
    p1: Point
    p2: Point

    def direction_vector(self):
        return Point(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    def perpendicular_vector(self) -> Point:
        direction = self.direction_vector()
        return Point(-direction.y, direction.x)

    def line_intersection(self, segment: 'Segment') -> Point | None:
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = segment.p1.x, segment.p1.y
        x4, y4 = segment.p2.x, segment.p2.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den

        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)

        return Point(intersection_x, intersection_y)

    def is_same_dir(self, segment: 'Segment') -> bool:
        dir1 = self.direction_vector().get_normalized()
        dir2 = segment.direction_vector().get_normalized()
        return abs(dir1.x * dir2.y - dir1.y * dir2.x) < 1e-9



@dataclass(slots=True)
class Polygon:
    points: list[Point]
    segments: list[Segment]

    def __init__(self, points_coords: list[tuple]):
        if not points_coords or len(points_coords) < 3:
            raise ValueError("Polygon must have at least 3 points.")

        self.points = [Point(x, y) for x, y in points_coords]

        if len(self.points) > 1 and self.points[0] != self.points[-1]:
            raise ValueError("Polygon must be closed: the first and last points must be the same.")

        self.segments = self._create_segments()

    def _create_segments(self):
        segments = []
        for i in range(len(self.points) - 1):
            segments.append(Segment(self.points[i], self.points[i + 1]))
        return segments

    def offset_segment(self, segment_index: int, offset_magnitude: float) -> 'Polygon':
        if not (0 <= segment_index < len(self.segments)):
            raise IndexError("Segment index out of bounds.")

        original_segment = self.segments[segment_index]
        perp_vec = original_segment.perpendicular_vector()

        norm_perp = perp_vec.get_normalized()

        offset_segment = Segment(
            Point(
                original_segment.p1.x + norm_perp.x * offset_magnitude,
                original_segment.p1.y + norm_perp.y * offset_magnitude
            ),
            Point(
                original_segment.p2.x + norm_perp.x * offset_magnitude,
                original_segment.p2.y + norm_perp.y * offset_magnitude
            )
        )

        prev_index = (segment_index - 1 + len(self.segments)) % len(self.segments)
        next_index = (segment_index + 1) % len(self.segments)

        prev_segment = self.segments[prev_index]
        next_segment = self.segments[next_index]

        new_p1 = prev_segment.line_intersection(offset_segment)
        new_p2 = offset_segment.line_intersection(next_segment)

        if not all((new_p1, new_p2)):
            raise ValueError(
                f"Could not find intersection for the first point of segment {segment_index}. "
                "Previous segment is parallel to the offset segment's shifted line."
            )

        new_points_coords_list = [(p.x, p.y) for p in self.points[:-1]]
        new_points_coords_list[segment_index] = (new_p1.x, new_p1.y)
        new_points_coords_list[(segment_index + 1) % (len(self.points) - 1)] = (new_p2.x, new_p2.y)

        if new_points_coords_list:
            new_points_coords_list.append(new_points_coords_list[0])

        res = Polygon(new_points_coords_list)

        if not all((
            next_segment.is_same_dir(res.segments[next_index]),
            prev_segment.is_same_dir(res.segments[prev_index])
        )):
            raise ValueError(
                f"Offset segment {segment_index} does not preserve the original polygon's direction."
            )

        return res
