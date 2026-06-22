from find_extremes import find_extreme
import numpy as np
import plotly.graph_objects as go

# Next, add options for display ratio, opacity, surface count, colorscale
# width, size, and title

def volume_plot(x: np.ndarray, y: np.ndarray, z: np.ndarray,
                values: list[float], display_ratio: float = 0.95,
                opacity: float = 0.2, surface_count: int = 25,
                colorscale: str = 'Turbo', title: str = '',
                width:int = 800, height:int = 600) -> go.Figure:
    """Creates and returns a plotly Volume Plot.

    x, y, z should be created with a numpy mgrid, then flattened s.t. when
    zipped together they represent every point in the plot.

    values should be assigned using zipped x, y, z coordinages:
    [func(Point(ix, iy, iz)) for ix, iy, iz in zip(x, y, z)]

    Args:
        x (np.ndarray): X Coordinates
        y (np.ndarray): Y Coordinates
        z (np.ndarray): Z Coordinates
        values (list[float]): Values to be color coated in the plot
        display_ratio (float, optional): How much to display, typically near 1.0. Defaults to 0.95.
        opacity (float, optional): Opacity of plot. Defaults to 0.2.
        surface_count (int, optional): Number of surfaces to display. Defaults to 25.
        colorscale (str, optional): Plotly colorscale. Defaults to 'Turbo'.
        title (str, optional): Leave blank to not include a title. Defaults to ''.
        width (int, optional): Figure width. Defaults to 800.
        height (int, optional): Figure height. Defaults to 600.

    Returns:
        go.Figure: Figure
    """    
    
    # Input asserts
    assert (0 < display_ratio <= 1.0), "Fix display_ratio s.t.: 0 < display_ratio <= 1.0"
    assert (1 <= surface_count <= 1000), "Fix surface_count s.t.: 1 <= surface_count <= 1000"
    assert (10 <= width <= 10000), "Fix width s.t.: 10 <= width <= 10000"
    assert (10 <= height <= 10000), "Fix height s.t.: 10 <= width <= 10000"

    values_min, values_max = find_extreme(values, min), find_extreme(values, max)

    isomin = values_min + (values_max - values_min) * (1 - display_ratio)
    isomax = values_max

    fig = go.Figure(data=go.Volume(
        x=x,
        y=y,
        z=z,
        value=values,
        isomin=isomin,
        isomax=isomax,
        opacity=opacity, # needs to be small to see through all surfaces
        surface_count=surface_count, # needs to be a large number for good volume rendering,
        colorscale=colorscale
        ))


    if title != '':
        fig.update_layout(title=title)
    
    fig.update_layout(width=width, height=height,
        scene=dict(
            xaxis_title="x (in)",
            yaxis_title = "y (in)",
            zaxis_title = "z (in)",
            zaxis=dict(autorange="reversed")
        ))
    return fig

if __name__ == "__main__":
    # Example usage:
    nested_data = [1, [5, [12, -5]], 8, [0]]
    print(f"Maximum: {find_extreme(nested_data, max)}") # Output: 12
    print(f"Minimum: {find_extreme(nested_data, min)}") # Output: -5