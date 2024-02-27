import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
import pandas as pd
import sqlite3
from flask import jsonify
from flask_cors import CORS
from components import agent_component, telemetry_component, mission_component, system_component
with open(os.path.join(os.path.dirname(__file__), 'components', 'map_component.html'), 'r') as f:map_html_content = f.read()

app = dash.Dash(__name__)
CORS(app.server)
app.title = 'Swarm Squad'
server = app.server


# Index page
index_page = html.Div(id='index-page', children=[
    html.Center(id='title', children=[
        html.Img(src='/assets/swarm_squad-B.svg', style={'height':'100px', 'width':'100px'}),
        html.H1('Swarm Squad', style={'marginTop':'-10px'})
    ]),
    html.Center(id='map-container', children=[
        html.Div([
            html.Iframe(srcDoc=map_html_content, style={"height": "780px", "width": "100%"})
        ], style={'width': '100%', 'margin': "0 auto"})
    ]),
    html.Center(id='info-buttons', children=[
        html.A(
            html.Button('Swarm Info', id='info_page-button'),
            href='/info',
            target='_blank'
        ),
        html.A(
            html.Button('Position Info', id='drone_page-button'),
            href='/drone',
            target='_blank'
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px'}),
    dcc.Interval(
        id='index_interval-component',
        interval=500,
        n_intervals=0
    )
])

# Swarm info page
info_layout = html.Div(id='info-layout', children=[
    html.Div(id='agent', children=[html.H3('Agent List'), agent_component.layout]),
    html.Div(id='telemetry', children=[html.H3('Telemetry Data'), telemetry_component.layout]),
    html.Div(id='mission', children=[html.H3('Mission Detail'), mission_component.layout]),
    html.Div(id='system', children=[html.H3('System Health'), system_component.layout]),
    dcc.Interval(
        id='info_interval-component',
        interval=500,
        n_intervals=0
    )
])

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[
        index_page,
        info_layout,
    ]),
])



# Agent component callbacks
@app.callback(
    Output('agent_table', 'data'),
    Input('info_interval-component', 'n_intervals')
)
def update_agent_table(n):
    data, _ = agent_component.read_data()
    return data



# Telemetry component callbacks
@app.callback(
    Output('telemetry_table', 'data'),
    Input('info_interval-component', 'n_intervals')
)
def update_telemetry_table(n):
    data, _ = telemetry_component.read_data()
    return data



# Mission component callbacks
@app.callback(
    Output('mission_table', 'data'),
    Input('info_interval-component', 'n_intervals')
)
def update_mission_table(n):
    data, _ = mission_component.read_data()
    return data



# System component callbacks
@app.callback(
    Output('system_table', 'data'),
    Input('info_interval-component', 'n_intervals')
)
def update_system_table(n):
    data, _ = system_component.read_data()
    return data



# Map component callbacks 
droneTrajectories = [] # Initialize droneTrajectories as an empty list

@server.route('/drone')
def get_drones():
    conn = sqlite3.connect('./src/data/swarm_squad.db')
    agent_df = pd.read_sql('SELECT * FROM telemetry', conn)
    conn.close()

    droneNames = agent_df['Agent Name'].unique().tolist()
    droneCoords = agent_df.groupby('Agent Name')['Location'].apply(list).tolist()
    droneTrajectories.append(droneCoords)

    return jsonify({'droneNames': droneNames, 'droneCoords': droneCoords, 'droneTrajectories': droneTrajectories})


# Update the page content based on the URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/info':
        return info_layout
    elif pathname == '/' or pathname == '/index':
        return index_page
    else:
        return '404 - Page not found'



if __name__ == '__main__':
    app.run_server(debug=True)