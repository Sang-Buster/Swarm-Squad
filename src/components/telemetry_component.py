from dash import dcc, html, dash_table
import pandas as pd
import sqlite3


def read_telemetry_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect("./src/data/swarm_squad.db")

    # Read the data from the database into a DataFrame
    df = pd.read_sql_query("SELECT * from telemetry", conn)

    # Close the connection to the database
    conn.close()

    # Create the columns for the DataTable
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
