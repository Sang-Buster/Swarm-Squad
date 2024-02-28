from dash import dcc, html, dash_table
import pandas as pd
import sqlite3

def read_system_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('./src/data/swarm_squad.db')

    # Read the data from the database into a DataFrame
    df = pd.read_sql_query("SELECT * from system", conn)

    # Close the connection to the database
    conn.close()

    # Create the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]

    return df, columns

system_data, system_columns = read_system_data()

layout = html.Div([
    dcc.Dropdown(
        id='system_dropdown',
        options=[{'label': i, 'value': i} for i in system_data['Agent Name'].unique()],
        value=None,
        clearable=True,
        placeholder="Select an agent...",
    ),
    dash_table.DataTable(
        id='system_table',
        columns=system_columns,
        data=system_data.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'lightgrey'
            }
        ],
        style_as_list_view=True,
    ),
])