import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from components import agent_component, telemetry_component, mission_component, system_component, map_component
import pandas as pd
import sqlite3



mapbox_scripts = ['https://api.mapbox.com/mapbox-gl-js/v2.9.1/mapbox-gl.js']
mapbox_stylesheets = ['https://api.mapbox.com/mapbox-gl-js/v2.9.1/mapbox-gl.css']
app = dash.Dash(__name__, external_stylesheets=mapbox_stylesheets, external_scripts=mapbox_scripts)
app.title = 'Swarm Squad'



# Define the layout of the app
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=500, # in milliseconds
        n_intervals=0
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[
        map_component.layout,  
        agent_component.layout,  
        telemetry_component.layout, 
        mission_component.layout, 
        system_component.layout, 
    ]),
])



# Index page
index_page = html.Div(id='index-page', children=[
    html.Center(id='title', children=[
        html.Img(src='/assets/SwarmSquad-B.svg', style={'height':'100px', 'width':'100px'}),
        html.H1('Swarm Squad', style={'margin-top':'-10px'})
    ]),
    html.Center(id='map', children=[map_component.layout]),
    html.Center(id='info-button', children=[
        html.A(
            html.Button('Swarm Info', id='info-button-text'),
            href='/info',
            target='_blank'
        )
    ]),
    dcc.Interval(
        id='interval-component',
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
        id='interval-component',
        interval=500,
        n_intervals=0
    )
])



# Agent component callbacks
@app.callback(
    Output('agent_table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_agent_table(n):
    data, _ = agent_component.read_data()
    return data



# Telemetry component callbacks
@app.callback(
    Output('telemetry_table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_telemetry_table(n):
    data, _ = telemetry_component.read_data()
    return data



# Mission component callbacks
@app.callback(
    Output('mission_table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_mission_table(n):
    data, _ = mission_component.read_data()
    return data



# System component callbacks
@app.callback(
    Output('system_table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_system_table(n):
    data, _ = system_component.read_data()
    return data



# Function to get agent data from the database
def get_agent_data():
    conn = sqlite3.connect('./src/data/swarmsquad.db')
    agent_df = pd.read_sql('SELECT * FROM agent', conn)
    conn.close()
    return agent_df

# Map component callbacks
@app.callback(
    Output('map', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_figure(n):
    # Get the agent data
    agent_df = get_agent_data()

    # Create a marker for each agent
    data = []
    for _, row in agent_df.iterrows():
        location_parts = row['Location'].split(',')
        lat, lon = map(float, location_parts[:2])
        data.append({
            'type': 'scattermapbox',
            'lat': [lat],
            'lon': [lon],
            'marker': {'size': 20},
            'name': row['Agent Name'],
        })

    # Return a dictionary that represents a plotly figure
    return {
        'data': data,
    }


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