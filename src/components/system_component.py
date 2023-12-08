from dash import dcc, html, dash_table
import pandas as pd
import sqlite3

def read_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('./src/data/swarmsquad.db')

    # Read the data from the database into a DataFrame
    df = pd.read_sql_query("SELECT * from agent", conn)

    # Close the connection to the database
    conn.close()

    # Create the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]

    return df.to_dict('records'), columns

data, columns = read_data()

layout = html.Div([
    dash_table.DataTable(
        id='system_table',
        columns=columns,
        data=data,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'lightgrey'
            }
        ],
    ),
])