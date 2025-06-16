from ast import literal_eval
from typing import ParamSpec, TypeVar, Callable

from polyshifter.geometry import Polygon

P = ParamSpec('P')
T = TypeVar('T')


def mapped_input(
    prompt: str,
    mapper: Callable[[str, P.args], T] | Callable[[str], T],
    *args: P.args,
) -> T:
    while True:
        user_input = input(prompt)
        try:
            value = mapper(user_input, *args)
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")


def map_polygon(value: str) -> Polygon:
    points_coords = literal_eval(value)

    if not isinstance(points_coords, list) or not all(
        isinstance(p, tuple) and len(p) == 2 and all(isinstance(coord, (int, float)) for coord in p) for p in points_coords
    ):
        raise ValueError("Invalid polygon format.")

    polygon = Polygon(points_coords)
    return polygon


def map_segment_index(value: str, polygon_segments_count: int) -> int:
    segment_index = int(value)
    if not (0 <= segment_index < polygon_segments_count):
        raise ValueError("Segment index out of bounds.")
    return segment_index


def map_offset_magnitude(value: str) -> float:
    offset_magnitude = float(value)
    return offset_magnitude
