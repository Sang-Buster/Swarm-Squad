import os


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
