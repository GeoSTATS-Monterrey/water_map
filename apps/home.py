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


# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

df = pd.read_csv("assets/vh_nl.csv", encoding='ISO-8859-1')

# App Layout

layout = html.Div([

	# TITULO
	dbc.Row([

		dbc.Col([
		
			html.H1('Inventario de Vehículos Registrados en Nuevo León'),
		
		])

	], className='m-0'),

    #comparar vs inegi, no hay datos
], className='m-0')