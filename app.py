import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime as dt
import base64
import dash_daq as daq
import pandas as pd
import numpy as np
import json as json
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
#import dash_auth


app = dash.Dash(__name__, title='GeoSTATS',
				external_stylesheets = [dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])

server = app.server

# DATOS
df = pd.read_csv("assets/vh_nl.csv", encoding='ISO-8859-1')
emp = pd.read_csv("assets/empresas.csv", encoding='ISO-8859-1')
pts = pd.read_csv("assets/temp_hume.csv", encoding='ISO-8859-1')

# IMAGENES
img1 = 'assets/info.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/layers.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')


# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Graph
trace_list2 = [
    go.Scattermapbox(hoverinfo="skip", mode = "markers", lat=emp.latitud, lon=emp.longitud, opacity=0.7), #, line = {'color': '#a60000','width':4}
    go.Scattermapbox(hoverinfo="skip", mode = "markers", lat=pts.ycoord, lon=pts.xcoord, opacity=0.7, marker = {'color': 'green','size':20}), #
    # go.Scattermapbox(hoverinfo="skip", mode = "lines", lon = lons_p3, lat = lats_p3, line = {'color': '#ed3232','width':4}, opacity=0.7,),
    # go.Scattermapbox(hoverinfo="skip", mode = "lines", lon = lons_p4, lat = lats_p4, line = {'color': '#ed5732','width':4}, opacity=0.7,),
    # go.Scattermapbox(hoverinfo="skip", mode = "lines", lon = lons_p5, lat = lats_p5, line = {'color': '#ed7a32','width':4, }, opacity=0.7),
]

mapa = go.Figure(data=trace_list2)
mapa.update_layout(clickmode='event+select', 
     mapbox=dict(
        accesstoken=mapbox_access_token,
        center=dict(lat=25.754798621861305, lon=-100.29721126556669),
        style="streets",
        zoom=10,
    ),
    showlegend=False,
    margin = dict(t=0, l=0, r=0, b=0),
)


app.layout = html.Div([

	# FILTROS
	dbc.Button(
		html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
			style={'width':'100%',}
		), 
		id="open-offcanvas", 
		n_clicks=0,
		style={'position':'absolute','z-index':'1','right':'1%','top':'1%','width':'5%','background-color':'#9e9595','border':'none'}),
    dbc.Offcanvas([

    	dbc.Row([

			dbc.Col([

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),		

				html.H5('Temperatura'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

				html.H5('Humedad'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

	            html.H5('Vegetación'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

				html.H5('Particulas PM#'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

	            html.H5('Empresas contaminantes'),

	            daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

	            html.H5('Escuelas'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

	            html.H5('Automóviles'),

				daq.BooleanSwitch(
	                id = '',
	                on=False,
	                color="#2A4A71",
	                style={'float':'left'}, 
	                className='px-4'
	            ),

	            html.H5('Población'),

			])

    	])

    	],
        id="offcanvas",
        title="Filtros",
        is_open=False,
        placement='end'
    ),

	# TITULO
	dbc.Row([

		dbc.Col([
		
			html.H1('GeoSTATS', style={'text-align':'center','color':'white'}),
		
		], className='d-flex justify-content-center')

	], className='m-0', style={'height':'10vh', 'position':'absolute','z-index':'1','left':'40%'}),

	# MAPA Y FILTROS
	dbc.Row([

		# MAPA
		dbc.Col([

			html.Div([

				dcc.Graph(
	                id = 'mapa',
	                figure = mapa,
	                config={
	                        'modeBarButtonsToRemove':
	                        ['lasso2d', 'pan2d','zoom2d',
	                        'zoomIn2d', 'zoomOut2d', 'autoScale2d',
	                        'resetScale2d', 'hoverClosestCartesian',
	                        'hoverCompareCartesian', 'toggleSpikelines',
	                        'select2d',],
	                        'displaylogo': False
	                    },
	                style={'height':'100vh'}
				)

			]),

		], style={'padding':'0'}),

	], className='m-0', style={'height':'100vh','z-index':'2'})

], className='m-0', style={'height':'100vh'})

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
