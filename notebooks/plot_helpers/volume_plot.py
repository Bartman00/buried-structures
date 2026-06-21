from find_extremes import find_extreme
import numpy as np
import plotly.graph_objects as go

def volume_plot(x: np.ndarray, y: np.ndarray, z: np.ndarray,
                values: list[float]) -> go.Figure:
    
    isomin, isomax = find_extreme(values, min), find_extreme(values, max)

    fig = go.Figure(data=go.Volume(
        x=x,
        y=y,
        z=z,
        value=values,
        isomin=(isomin + (isomax - isomin)*0.05),
        isomax=isomax,
        opacity=0.2, # needs to be small to see through all surfaces
        surface_count=25, # needs to be a large number for good volume rendering,
        colorscale='Turbo'
        ))


    fig.update_layout(title=f"Boussinesq Pressure",
        width = 800, height=600,
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