from dataclasses import dataclass

from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from polyshifter.models import Polygon


@dataclass(slots=True, frozen=True)
class PolygonsPlotVisualization:
    original_polygon: Polygon
    offset_polygon: Polygon

    def plot(self) -> None:
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_polygon(ax, self.offset_polygon, "red", "Offset Polygon")
        self._plot_polygon(ax, self.original_polygon, "blue", "Original Polygon")

        ax.set_title("Polygon Segment Offset")
        ax.set_xlabel("X-coordinate")
        ax.set_ylabel("Y-coordinate")
        ax.legend()
        ax.grid(True)
        ax.set_aspect("equal", adjustable="box")
        plt.show()

    def _plot_polygon(self, ax: Axes, polygon: Polygon, color: str, label: str) -> None:
        x_coords = [float(p.x) for p in polygon.points]
        y_coords = [float(p.y) for p in polygon.points]

        ax.plot(x_coords, y_coords, color=color, label=label, marker="o", linestyle="-")

        for i, p in enumerate(polygon.points):
            if all((
                i == len(polygon.points) - 1,
                polygon.points[0] == polygon.points[-1],
                len(polygon.points) > 1,
            )):
                continue
            ax.text(float(p.x), float(p.y), f"({p.x:2f},{p.y:2f})", fontsize=8, ha="right")
