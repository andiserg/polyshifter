from dataclasses import dataclass

from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from polyshifter.models import Polygon, Segment


@dataclass(slots=True, frozen=True)
class PolygonsPlotVisualization:
    original_polygon: Polygon
    offset_polygon: Polygon
    offset_arrow: Segment

    def plot(self) -> None:
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_polygon(ax, self.offset_polygon, "red", "Offset Polygon")
        self._plot_polygon(ax, self.original_polygon, "blue", "Original Polygon")
        self._plot_arrow(ax)

        ax.set_title("Polygon Segment Offset")
        ax.set_xlabel("X-coord")
        ax.set_ylabel("Y-coord")
        ax.legend()
        ax.set_aspect("equal", adjustable="box")
        plt.show()

    def _plot_polygon(self, ax: Axes, polygon: Polygon, color: str, label: str) -> None:
        x_coords = [float(p.x) for p in polygon.points]
        y_coords = [float(p.y) for p in polygon.points]

        ax.plot(x_coords, y_coords, color=color, label=label, marker="o", linestyle="-")

        for x, y in zip(x_coords[:-1], y_coords[:-1], strict=True):
            ax.text(float(x), float(y), f"({x},{y})", fontsize=8, ha="right")

    def _plot_arrow(self, ax: Axes) -> None:
        start = self.offset_arrow.p1
        end = self.offset_arrow.p2

        ax.annotate(
            "",
            xy=(float(end.x), float(end.y)),
            xytext=(float(start.x), float(start.y)),
            arrowprops={"arrowstyle": "->", "color": "green", "lw": 2},
            annotation_clip=False,
        )
