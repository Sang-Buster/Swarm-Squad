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
                                    className="footer-icon",
                                ),
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon="mdi:web",
                                            width=CONTACT_ICON_WIDTH,
                                        )
                                    ],
                                    href=WEB,
                                    className="footer-icon",
                                ),
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon="mdi:book-open-variant-outline",
                                            width=CONTACT_ICON_WIDTH,
                                        )
                                    ],
                                    href=DOC,
                                    className="footer-icon",
                                ),
                            ],
                            position="center",
                            className="footer-icons-group",
                        )
                    ],
                )
            ],
            span=12,
        )
    ]
)
