from polyshifter import cli
from polyshifter.services import offset_segment
from polyshifter.adapters import PolygonsPlotVisualizationAdapter

def main() -> None:
    coords = cli.mapped_input(
        "Enter polygon points as a list of tuples: ",
        cli.map_coords,
    )
    segment_index = cli.mapped_input(
        "Enter polygon segment index: ",
        cli.map_segment_index,
        len(coords) - 1 ,
    )
    offset_magnitude = cli.mapped_input(
        "Enter polygon offset magnitude: ",
        cli.map_offset_magnitude,
    )

    try:
        result = offset_segment(coords, segment_index, offset_magnitude)

        visualization = PolygonsPlotVisualizationAdapter(
            original_polygon=result.orig_polygon,
            offset_polygon=result.result_polygon,
            offset_arrow=result.offset_arrow,
        )

        visualization.plot()
    except (IndexError, ValueError) as e:
        print(f"Error during offset operation: {e}")


if __name__ == "__main__":
    main()
