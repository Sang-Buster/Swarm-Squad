from dash import dcc, html

layout = html.Div([
    dcc.Graph(
        id='map',
        config={
            'mapboxAccessToken': '',  
            'responsive': True,
        },
        figure={
            'data': [],
            'layout': {
                'mapbox': {
                    'style': 'mapbox://styles/mapbox/streets-v12',
                    'center': {'lat': 29.1901,  'lon': -81.049,},
                    'zoom': 15.5,
                    'pitch': 90,
                },
                'autosize': True,
                'height': 790,
            }
        }
    )
], style={'width': '100%', 'margin': "0 auto"})