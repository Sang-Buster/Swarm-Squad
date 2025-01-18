import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = "https://github.com/Swarm-Squad/Swarm-Squad"
WEB = "https://swarm-squad.com/"
DOC = "https://docs.swarm-squad.com/"
CONTACT_ICON_WIDTH = 25

footer = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Footer(
                    height=30,
                    fixed=True,
                    className="footer-container",
                    style={
                        "backgroundColor": "rgba(0,0,0,0)",
                    },
                    mb=5,
                    withBorder=False,
                    children=[
                        dmc.Group(
                            children=[
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon="mdi:github",
                                            width=CONTACT_ICON_WIDTH,
                                        )
                                    ],
                                    href=GITHUB,
                                ),
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon="mdi:web",
                                            width=CONTACT_ICON_WIDTH,
                                        )
                                    ],
                                    href=WEB,
                                ),
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon="mdi:book-open-variant-outline",
                                            width=CONTACT_ICON_WIDTH,
                                        )
                                    ],
                                    href=DOC,
                                ),
                            ],
                            position="center",
                        )
                    ],
                )
            ],
            span=12,
        )
    ]
)
