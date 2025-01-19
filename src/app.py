import dash
from dash import Dash, html, dcc
from pages.footer import footer
from pages.nav import navbar
from flask_cors import CORS
from utils.websocket_manager import WebSocketManager

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

# Initialize WebSocket manager and attach it to the app
app.ws_manager = WebSocketManager()

server = app.server
# Enable CORS for the Flask server
CORS(
    server,
    resources={
        r"/websocket/*": {
            "origins": ["http://localhost:8050", "http://127.0.0.1:8050"],
            "allow_headers": ["*"],
            "expose_headers": ["*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "supports_credentials": True,
        }
    },
)


@server.before_first_request
def start_websocket():
    app.ws_manager.start_websocket()


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
    try:
        app.run_server(debug=True)
    finally:
        app.ws_manager.cleanup_websocket()
