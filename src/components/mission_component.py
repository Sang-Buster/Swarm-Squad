import sqlite3

import pandas as pd
from dash import dash_table, dcc, html


def read_mission_data():
    try:
        conn = sqlite3.connect("./src/data/swarm_squad.db")
        df = pd.read_sql_query("SELECT * from mission", conn)
        conn.close()
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError):
        df = pd.DataFrame(
            columns=["Agent Name", "Status", "Mission", "Completion", "Duration"]
        )

    columns = [{"name": i, "id": i} for i in df.columns]
    return df, columns


mission_data, mission_columns = read_mission_data()

layout = html.Div(
    [
        dcc.Dropdown(
            id="mission_dropdown",
            value=None,
            clearable=True,
            placeholder="Select an mission...",
        ),
        dash_table.DataTable(
            id="mission_table",
            columns=mission_columns,
            data=mission_data.to_dict("records"),
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "lightgrey"}
            ],
            style_as_list_view=True,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "0 15px"},
        ),
    ]
)
