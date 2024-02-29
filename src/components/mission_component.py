from dash import dcc, html, dash_table
import pandas as pd
import sqlite3

def read_mission_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('./src/data/swarm_squad.db')

    # Read the data from the database into a DataFrame
    df = pd.read_sql_query("SELECT * from mission", conn)

    # Close the connection to the database
    conn.close()

    # Create the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]

    return df, columns

mission_data, mission_columns = read_mission_data()

layout = html.Div([
    dcc.Dropdown(
        id='mission_dropdown',
        value=None,
        clearable=True,
        placeholder="Select an mission...",
    ),
    dash_table.DataTable(
        id='mission_table',
        columns=mission_columns,
        data=mission_data.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'lightgrey'
            }
        ],
        style_as_list_view=True,
        style_table={'overflowX': 'auto'},  
        style_cell={'textAlign': 'center', 'padding': '0 15px'}, 
    ),
])