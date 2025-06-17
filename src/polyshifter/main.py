from polyshifter import cli
from polyshifter.services import offset_segment
from polyshifter.visual import PolygonsPlotVisualization

def main() -> None:
    original_polygon = cli.mapped_input(
        "Enter polygon points as a list of tuples: ",
        cli.map_polygon,
    )
    segment_index = cli.mapped_input(
        "Enter polygon segment index: ",
        cli.map_segment_index,
        len(original_polygon.segments),
    )
    offset_magnitude = cli.mapped_input(
        "Enter polygon offset magnitude: ",
        cli.map_offset_magnitude,
    )

    try:
        offset_polygon = offset_segment(
            original_polygon, segment_index, offset_magnitude,
        )

        visualization = PolygonsPlotVisualization(
            original_polygon=original_polygon,
            offset_polygon=offset_polygon,
        )

        visualization.plot()
    except (IndexError, ValueError) as e:
        print(f"Error during offset operation: {e}")


if __name__ == "__main__":
    main()
