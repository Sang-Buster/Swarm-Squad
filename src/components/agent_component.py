import sqlite3

import pandas as pd
from dash import dash_table, dcc, html


def read_agent_data():
    try:
        # Create a connection to the SQLite database
        conn = sqlite3.connect("./src/data/swarm_squad.db")

        # Read the data from the database into a DataFrame
        df = pd.read_sql_query("SELECT * from agent", conn)

        # Close the connection to the database
        conn.close()

    except (sqlite3.OperationalError, pd.io.sql.DatabaseError):
        # If table doesn't exist, create empty DataFrame with matching columns from fake data
        df = pd.DataFrame(
            columns=["Agent Name", "Agent Type", "Status", "Mode", "Alert Count"]
        )

    # Create the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]

    return df, columns


agent_data, agent_columns = read_agent_data()

layout = html.Div(
    [
        dcc.Dropdown(
            id="agent_dropdown",
            value=None,
            clearable=True,
            placeholder="Select an agent...",
        ),
        dash_table.DataTable(
            id="agent_table",
            columns=agent_columns,
            data=agent_data.to_dict("records"),
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "lightgrey"}
            ],
            style_as_list_view=True,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "0 15px"},
        ),
    ]
)
