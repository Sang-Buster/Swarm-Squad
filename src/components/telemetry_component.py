import sqlite3

import pandas as pd
from dash import dash_table, dcc, html


def read_telemetry_data():
    try:
        conn = sqlite3.connect("./src/data/swarm_squad.db")
        df = pd.read_sql_query("SELECT * from telemetry", conn)
        conn.close()
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError):
        df = pd.DataFrame(
            columns=[
                "Agent Name",
                "Location",
                "Destination",
                "Altitude",
                "Pitch",
                "Yaw",
                "Roll",
                "Airspeed/Velocity",
                "Acceleration",
                "Angular Velocity",
            ]
        )

    columns = [{"name": i, "id": i} for i in df.columns]
    return df, columns


telemetry_data, telemetry_columns = read_telemetry_data()

layout = html.Div(
    [
        dcc.Dropdown(
            id="telemetry_dropdown",
            value=None,
            clearable=True,
            placeholder="Select an agent...",
        ),
        dash_table.DataTable(
            id="telemetry_table",
            columns=telemetry_columns,
            data=telemetry_data.to_dict("records"),
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "lightgrey"}
            ],
            style_as_list_view=True,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "0 15px"},
        ),
    ]
)
