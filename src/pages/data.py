import dash
import dash_mantine_components as dmc
from dash import html

dash.register_page(
    __name__,
    path="/data",
    order=2,  # Third page
    title="Data | Swarm Squad",
    description="Data analysis and visualization",
)

layout = html.Div(
    [
        html.Div(className="illumination-4"),
        html.Div(className="illumination-5"),
        html.Div(className="stars"),
        dmc.Container(
            [
                dmc.Title("Data Analysis", style={"color": "white"}, size="h1"),
                # Add your data content here
            ],
            fluid=True,
            style={"height": "100vh", "position": "relative"},
        ),
    ],
    style={"minHeight": "100vh", "position": "relative", "overflow": "hidden"},
)
