from dash import dcc, html, dash_table
import pandas as pd
import sqlite3


def read_system_data():
    try:
        conn = sqlite3.connect("./src/data/swarm_squad.db")
        df = pd.read_sql_query("SELECT * from system", conn)
        conn.close()
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError):
        # Match exact columns from system_fake_data.py
        df = pd.DataFrame(
            columns=[
                "Agent Name",
                "Battery Level",
                "GPS Accuracy",
                "Connection Strength/Quality",
                "Communication Status",
            ]
        )

    columns = [{"name": i, "id": i} for i in df.columns]
    return df, columns


system_data, system_columns = read_system_data()

layout = html.Div(
    [
        dcc.Dropdown(
            id="system_dropdown",
            value=None,
            clearable=True,
            placeholder="Select an agent...",
        ),
        dash_table.DataTable(
            id="system_table",
            columns=system_columns,
            data=system_data.to_dict("records"),
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "lightgrey"}
            ],
            style_as_list_view=True,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "0 15px"},
        ),
    ]
)
