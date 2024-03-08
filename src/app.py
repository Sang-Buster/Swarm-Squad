import dash
from dash import Dash, html, dcc, Input, Output
from flask_cors import CORS

# Imports for swarm table info page
from components import agent_component, telemetry_component, mission_component, system_component

# Imports for swarm position info page
import pandas as pd
import sqlite3
from flask import Response
import json
from collections import OrderedDict

# Imports for map component in index page
import os
def read_map_html():
    with open(os.path.join(os.path.dirname(__file__), 'components', 'map_component.html'), 'r') as f:
        return f.read()


##################
# Create the app #
##################
app = Dash(__name__, update_title=None, title='Swarm Squad')
server = app.server
CORS(server)


##############
# Index page #
##############
index_page = html.Div(id='index-layout', children=[
    html.Div(id='title', children=[
        html.Img(src='/assets/favicon.ico', style={'height':'250px', 'width':'250px'}),
        html.H1('Swarm Squad', style={'marginTop':'-10px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    html.Div(children=[
        html.Div([
            html.Iframe(id='map', srcDoc=read_map_html(), style={"height": "780px", "width": "100%"})
        ], style={'width': '100%', 'margin': "0 auto"}),
        dcc.Interval(
            id='map-refresh',
            interval=5000,  # in milliseconds
            n_intervals=0
        )
    ]),    
    html.Div(id='subpage-buttons', children=[
        html.A(
            html.Button('Swarm Table', id='table_page-button'),
            href='/table',
            target='_blank'
        ),
        html.A(
            html.Button('Position Info', id='info_page-button'),
            href='/info',
            target='_blank'
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px'}),
    dcc.Interval(
        id='index_interval-component',
        interval=500,
        n_intervals=0
    )
])


#########################
# Swarm table info page #
#########################
table_page = html.Div(id='info-layout', children=[
    html.Div(id='agent', children=[html.H3('Agent List'), agent_component.layout]),
    html.Div(id='telemetry', children=[html.H3('Telemetry Data'), telemetry_component.layout]),
    html.Div(id='mission', children=[html.H3('Mission Detail'), mission_component.layout]),
    html.Div(id='system', children=[html.H3('System Health'), system_component.layout]),
    dcc.Interval(
        id='table_interval-component',
        interval=500,
        n_intervals=0
    )
])


##############
# App layout #
##############
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-title'),
    html.Div(id='page-content', children=[
        index_page,
        table_page,
    ]),
])

app.clientside_callback(
    """
    function(pathname) {
        if (pathname === '/table') {
            document.title = 'Swarm Table | Swarm Squad'
        } else if (pathname === '/info') {
            document.title = 'Swarm Info | Swarm Squad'
        } else {
            document.title = 'Swarm Squad'
        }
    }
    """,
    Output('page-title', 'children'),
    Input('url', 'pathname')
)


###########################
# Map component callbacks #
###########################
# Get the initial modification time
file_path = os.path.join(os.path.dirname(__file__), 'components', 'map_component.html')
last_mod_time = os.path.getmtime(file_path)

@app.callback(
    Output('map', 'srcDoc'),
    [Input('map-refresh', 'n_intervals')]
)
def refresh_map(n):
    global last_mod_time
    current_mod_time = os.path.getmtime(file_path)
    if current_mod_time > last_mod_time:
        last_mod_time = current_mod_time
        return read_map_html()
    return dash.no_update


#############################
# Agent component callbacks #
#############################
# Callback to update the agent table
@app.callback(
    Output('agent_table', 'data'),
    [Input('agent_dropdown', 'value'),
     Input('table_interval-component', 'n_intervals')]
)
def update_agent_table(selected_agent, n):
    agent_df, _ = agent_component.read_agent_data()
    agent_df = agent_df.round(4)
    if selected_agent:
        filtered_agent_df = agent_df[agent_df['Agent Name'] == selected_agent]
    else:
        filtered_agent_df = agent_df
    return filtered_agent_df.to_dict('records')

# Callback to update the dropdown menu
@app.callback(
    Output('agent_dropdown', 'options'),
    Input('agent_table', 'data')
)
def update_dropdown_options(agent_table_data):
    if agent_table_data is None:
        return []
    df = pd.DataFrame(agent_table_data)
    return [{'label': i, 'value': i} for i in df['Agent Name'].unique()]


#################################
# Telemetry component callbacks #
#################################
# Callback to update the agent table
@app.callback(
    Output('telemetry_table', 'data'),
    [Input('telemetry_dropdown', 'value'),
     Input('table_interval-component', 'n_intervals')]
)
def update_telemetry_table(selected_agent, n):
    telemetry_df, _ = telemetry_component.read_telemetry_data()
    def round_string_numbers(s):
        if isinstance(s, str):
            return ','.join([str(round(float(i), 4)) for i in s.split(',')])
        else:
            return s
    for col in telemetry_df.columns:
        telemetry_df[col] = telemetry_df[col].apply(round_string_numbers)    
    telemetry_df = telemetry_df.round(4)
    if selected_agent:
        filtered_telemetry_df = telemetry_df[telemetry_df['Agent Name'] == selected_agent]
    else:
        filtered_telemetry_df = telemetry_df
    return filtered_telemetry_df.to_dict('records')

# Callback to update the dropdown menu
@app.callback(
    Output('telemetry_dropdown', 'options'),
    Input('telemetry_table', 'data')
)
def update_telemetry_dropdown(telemetry_table_data):
    if telemetry_table_data is None:
        return []
    df = pd.DataFrame(telemetry_table_data)
    return [{'label': i, 'value': i} for i in df['Agent Name'].unique()]


###############################
# Mission component callbacks #
###############################
# Callback to update the agent table
@app.callback(
    Output('mission_table', 'data'),
    [Input('mission_dropdown', 'value'),
     Input('table_interval-component', 'n_intervals')]
)
def update_mission_table(selected_mission, n):
    mission_df, _ = mission_component.read_mission_data()
    mission_df = mission_df.round(4)
    if selected_mission:
        filtered_mission_df = mission_df[mission_df['Mission'] == selected_mission]
    else:
        filtered_mission_df = mission_df
    return filtered_mission_df.to_dict('records')

# Callback to update the dropdown menu
@app.callback(
    Output('mission_dropdown', 'options'),
    Input('mission_table', 'data')
)
def update_mission_dropdown(mission_table_data):
    if mission_table_data is None:
        return []
    df = pd.DataFrame(mission_table_data)
    return [{'label': i, 'value': i} for i in df['Mission'].unique()]


##############################
# System component callbacks #
##############################
# Callback to update the agent table
@app.callback(
    Output('system_table', 'data'),
    [Input('system_dropdown', 'value'),
     Input('table_interval-component', 'n_intervals')]
)
def update_system_table(selected_system, n):
    system_df, _ = system_component.read_system_data()
    system_df = system_df.round(4)
    if selected_system:
        filtered_system_df = system_df[system_df['Agent Name'] == selected_system]
    else:
        filtered_system_df = system_df
    return filtered_system_df.to_dict('records')

# Callback to update the dropdown menu
@app.callback(
    Output('system_dropdown', 'options'),
    Input('system_table', 'data')
)
def update_system_dropdown(system_table_data):
    if system_table_data is None:
        return []
    df = pd.DataFrame(system_table_data)
    return [{'label': i, 'value': i} for i in df['Agent Name'].unique()]


#################################
# Swarm position info callbacks #
#################################
@server.route('/info')
def info_page():
    conn = sqlite3.connect('./src/data/swarm_squad.db')
    agent_df = pd.read_sql('SELECT * FROM telemetry', conn)
    conn.close()

    droneNames = agent_df['Agent Name'].unique().tolist()
    droneCoords = agent_df.groupby('Agent Name')['Location'].apply(list).tolist()
    dronePitch = agent_df.groupby('Agent Name')['Pitch'].apply(list).tolist()
    droneYaw = agent_df.groupby('Agent Name')['Yaw'].apply(list).tolist()
    droneRoll = agent_df.groupby('Agent Name')['Roll'].apply(list).tolist()

    data = OrderedDict([
        ('droneNames', droneNames),
        ('droneCoords', droneCoords),
        ('dronePitch', dronePitch),
        ('droneYaw', droneYaw),
        ('droneRoll', droneRoll),
    ])

    response = Response(json.dumps(data), mimetype='application/json')

    return response


##############
# URL Set-up #
##############
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/table':
        return table_page
    elif pathname == '/info':
        return info_page
    elif pathname == '/' or pathname == '/index':
        return index_page
    else:
        return '404 - Page not found'


###############
# Run the app #
###############
if __name__ == '__main__':
    app.run_server(debug=True)