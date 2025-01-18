import dash
from dash import Dash, html, dcc
from pages.footer import footer
from pages.nav import navbar


app = Dash(
    __name__,
    title="Swarm Squad",
    use_pages=True,
    update_title=False,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    meta_tags=[
        {
            "name": "description",
            "content": "A simulation framework for multi-agent systems.",
        },
        {
            "name": "keywords",
            "content": "Swarm Squad, Multi-agent systems, LLM, AI, Simulation, Dash",
        },
    ],
)

server = app.server
app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        footer,
        dcc.Store("past-launches-data"),
        dcc.Store("next-launch-data"),
        dcc.Store("last-update"),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
