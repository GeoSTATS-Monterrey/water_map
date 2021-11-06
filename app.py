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
import dash_auth


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

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Graph
mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
mapa_data = pd.DataFrame(mapa_data)

#-- Graph
mapa = go.Figure(
    px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
    size = 'hechos_viales',
    size_max=1, 
    zoom=10,
    hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
    opacity=0.9))

mapa.update_layout(clickmode='event+select', 
     mapbox=dict(
        accesstoken=mapbox_access_token,
        center=dict(lat=25.693819980896006, lon=-100.31240109902377),
        style="dark"
    ),
	margin = dict(t=0, l=0, r=0, b=0))

# empresas = px.scatter_mapbox(emp,
#     lat = emp.latitud,
#     lon = emp.longitud,)

# mapa.update_traces(hovertemplate = '<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>',
#     showlegend = True,
#     name = 'Cámara Vial Inteligente')

# Juntamos Capas
# mapa.add_trace(empresas.data[0])
mapa.update_traces(marker_color="red",
    unselected_marker_opacity=1)

puntos = px.scatter_mapbox(pts,
    lat = pts.ycoord,
    lon = pts.xcoord,)

# mapa.update_traces(hovertemplate = '<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>',
#     showlegend = True,
#     name = 'Cámara Vial Inteligente')

# Juntamos Capas
mapa.add_trace(puntos.data[0])
mapa.update_traces(marker_color="green",
    unselected_marker_opacity=1)

app.layout = html.Div([

	# FILTROS
	dbc.Button(
		"Filtros", 
		id="open-offcanvas", 
		n_clicks=0,
		style={'position':'absolute'}),
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
		
			html.H1('GeoSTATS'),
		
		], className='d-flex justify-content-center')

	], className='m-0', style={'height':'10vh'}),

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
	                style={'height':'85vh'}
				)

			]),

		]),

	], className='m-0', style={'height':'90vh'})

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
