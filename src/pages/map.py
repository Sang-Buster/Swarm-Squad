import os

import dash
import dash_mantine_components as dmc
from dash import html

dash.register_page(
    __name__,
    path="/map",
    order=1,
    title="Map | Swarm Squad",
    description="Interactive map for swarm intelligence",
)


def read_map_html():
    mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN")
    if mapbox_token is None:
        raise ValueError(
            "MAPBOX_ACCESS_TOKEN not found in environment variables. Make sure your .env file exists and contains the token."
        )

    map_path = os.path.join("src", "components", "map_component.html")

    with open(map_path, "r") as f:
        content = f.read()
        content = content.replace("YOUR_MAPBOX_TOKEN_PLACEHOLDER", mapbox_token)
        return content


layout = html.Div(
    [
        dmc.Container(
            [
                dmc.Stack(
                    [
                        dmc.Center(
                            dmc.Paper(
                                html.Iframe(
                                    srcDoc=read_map_html(),
                                    style={
                                        "width": "90vw",
                                        "height": "80vh",
                                        "border": "none",
                                        "borderRadius": "10px",
                                        "backgroundColor": "transparent",
                                    },
                                ),
                                shadow="lg",
                                radius="md",
                                withBorder=True,
                                style={
                                    "backgroundColor": "transparent",
                                    "width": "90vw",
                                    "height": "80vh",
                                },
                            ),
                        ),
                    ],
                    justify="center",  # Centers content vertically
                    align="center",  # Centers content horizontally
                    spacing="xl",  # Adds space between title and map
                ),
            ],
            fluid=True,
            size="100%",
            style={
                "height": "100vh",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            },
        ),
    ],
    style={
        "minHeight": "100vh",
        "position": "relative",
        "overflow": "hidden",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
    },
)
