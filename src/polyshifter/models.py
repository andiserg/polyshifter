from dataclasses import dataclass
from fractions import Fraction


@dataclass(slots=True)
class Point:
    x: Fraction
    y: Fraction

    def __init__(self, x: float | Fraction, y: float | Fraction):
        self.x = Fraction(str(x))
        self.y = Fraction(str(y))

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return Fraction(dx * dx + dy * dy) ** Fraction(1, 2)

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

    def perpendicular_vector(self, negative: bool) -> Point:
        direction = self.direction_vector()
        return Point(-direction.y, direction.x) if negative else Point(direction.y, -direction.x)

    def line_intersection(self, segment: 'Segment') -> Point | None:
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = segment.p1.x, segment.p1.y
        x4, y4 = segment.p2.x, segment.p2.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = Fraction(((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)), den)

        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)

        return Point(intersection_x, intersection_y)

    def is_same_dir(self, segment: 'Segment') -> bool:
        dir1 = self.direction_vector().get_normalized()
        dir2 = segment.direction_vector().get_normalized()
        dot = dir1.x * dir2.x + dir1.y * dir2.y
        return abs(dir1.x * dir2.y - dir1.y * dir2.x) < 1e-9 and dot > 0


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

    def _create_segments(self) -> list[Segment]:
        return [
            Segment(point, self.points[i + 1])
            for i, point in enumerate(self.points[:-1])
        ]
