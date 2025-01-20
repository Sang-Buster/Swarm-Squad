import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, callback
from dash_iconify import DashIconify

all_icons = [
    "mdi:home-outline",  # Home
    "mdi:map-search-outline",  # Map
    "mdi:database-outline",  # Data
    "mdi:message-processing-outline",  # Chat
    "mdi:chart-line",  # Plot
    "mdi:information-outline",  # Log
]


def navbar():
    return dmc.Grid(
        [
            dmc.ActionIcon(
                DashIconify(icon="zondicons:menu", width=20),
                color="white",
                variant="transparent",
                id="nav-btn",
                m=25,
                className="nav-container",
            ),
            dmc.Modal(
                [
                    *[  # Use unpacking to combine regular nav links
                        dbc.NavLink(
                            children=[
                                dmc.Group(
                                    [
                                        dmc.ActionIcon(
                                            DashIconify(
                                                icon=all_icons[idx],
                                                width=35,
                                                color="white",
                                            ),
                                            variant="transparent",
                                        ),
                                        page["name"],
                                    ],
                                    mt=20,
                                )
                            ],
                            href=page["path"],
                            style={
                                "color": "white",
                                "text-decoration": "none",
                                "font-family": "Arial, sans-serif",
                                "font-size": 15,
                            },
                            className="nav-link",
                            id={"type": "dynamic-link", "index": idx},
                        )
                        for idx, page in enumerate(dash.page_registry.values())
                        if page["module"] != "pages.not_found_404"
                    ],
                    # Add author link right after the navigation links
                    dbc.NavLink(
                        children=[
                            dmc.Group(
                                [
                                    dmc.Text(
                                        "Created by ",
                                        color="white",
                                        size="sm",
                                        style={
                                            "font-family": "Arial, sans-serif",
                                        },
                                    ),
                                    "Sang-Buster",
                                ],
                                mt=20,
                                position="left",  # Align items to the left
                                spacing="xs",  # Control spacing between "Created by" and "Sang-Buster"
                            )
                        ],
                        href="https://github.com/Sang-Buster",
                        target="_blank",
                        style={
                            "color": "white",
                            "text-decoration": "none",
                            "font-family": "Arial, sans-serif",
                            "font-size": 15,
                            "margin-top": "13px",
                        },
                        className="nav-link",
                        id={"type": "dynamic-link", "index": "author"},
                    ),
                ],
                title="Choose your exploration..",
                size="100%",
                id="full-modal",
                zIndex=10000,
                centered=True,
                overlayOpacity=0.85,
                withCloseButton=False,
                styles={
                    "modal": {
                        "background-color": "transparent",
                        "color": "white",
                        "backdrop-filter": "none",
                    }
                },
            ),
        ]
    )


@callback(
    Output("full-modal", "opened"),
    Input("nav-btn", "n_clicks"),
    State("full-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(_, opened):
    return not opened


@callback(
    Output("full-modal", "opened", allow_duplicate=True),
    Input({"type": "dynamic-link", "index": ALL}, "n_clicks"),
    State("full-modal", "opened"),
    prevent_initial_call=True,
)
def update_modal(n, opened):
    if True in n:
        return not opened
    return opened
