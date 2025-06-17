# Polyshifter

**Polyshifter** is a Python application for offset segments of 2D polygons.

### Implementation details

- Offsets are applied to a single polygon segment by a given magnitude along the normal vector.
- Intersections with neighboring segments are recalculated to preserve polygon continuity.
- Orientation of adjacent edges is verified to remain unchanged after transformation.
- Arithmetic operations are performed using `fractions.Fraction` for accuracy and stability.
- Visualization includes both the original and modified polygon outlines, as well as an arrow showing the direction and magnitude of the offset.

### Requirements

- Python 3.10+
- `matplotlib`

Install the project and dependencies using [uv](https://github.com/astral-sh/uv):
```bash
uv sync
```

### Tests

Unit tests are recommended using pytest, especially for geometric correctness and edge cases like parallel segments.

Run tests with:
```bash
uv sync --all-extras
pytest
```

### Code Quality

The code has been checked using the following static analysis tools:

- ruff – for linting and code style enforcement;
- mypy – for static type checking.

To run checks locally:
```
ruff check src
mypy src
```