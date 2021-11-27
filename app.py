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
# import geopandas as gpd


app = dash.Dash(__name__, title='GeoSTATS',
				external_stylesheets = [dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])

# GOOGLE ANALYTICS TAGS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
		<script async src="https://www.googletagmanager.com/gtag/js?id=G-XLVYFYJ63V"></script>
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'G-XLVYFYJ63V');
		</script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server

# DATOS
est = pd.read_csv("assets/purple_air/estaciones.csv", encoding='ISO-8859-1')
df = pd.read_csv("assets/vh_nl.csv", encoding='ISO-8859-1')
emp = pd.read_csv("assets/empresas.csv", encoding='ISO-8859-1')
pts = pd.read_csv("assets/temp_hume.csv", encoding='ISO-8859-1')
eys = pd.read_csv("assets/escuelas_salud.csv", encoding='ISO-8859-1')
cyn = pd.read_csv("assets/conagua_nasa.csv", encoding='ISO-8859-1')

# IMAGENES
img1 = 'assets/info.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/layers.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')


# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Graph
# trace_list2 = [
#     go.Scattermapbox(mode = "markers", lat=emp.latitud, lon=emp.longitud, opacity=0.7, marker = {'color': 'purple','size':10}, hoverlabel = dict(font_size = 20)), #, line = {'color': '#a60000','width':4}
#     go.Scattermapbox(mode = "markers", lat=pts.ycoord, lon=pts.xcoord, opacity=0.7, marker = {'color': 'yellow','size':15}), #
#     go.Scattermapbox(mode = "markers", lon = est.lon, lat = est.lat, marker = {'color': est.temp,'size':est.temp*1.5, 'colorscale':'Reds'}),
#     # go.Densitymapbox(hoverinfo="skip", lat=est.lat, lon=est.lon, z=est.temp, radius=40, showscale=False, colorscale='Turbo')
#     # go.Scattermapbox(hoverinfo="skip", mode = "lines", lon = lons_p4, lat = lats_p4, line = {'color': '#ed5732','width':4}, opacity=0.7,),
#     # go.Scattermapbox(hoverinfo="skip", mode = "lines", lon = lons_p5, lat = lats_p5, line = {'color': '#ed7a32','width':4, }, opacity=0.7),
# ]

# mapa = go.Figure(data=trace_list2)
# mapa.update_layout(clickmode='event+select', 
#      mapbox=dict(
#         accesstoken=mapbox_access_token,
#         center=dict(lat=25.71804256894533, lon=-100.30914201555723),
#         style="dark",
#         zoom=10.5,
#     ),
#     showlegend=False,
#     margin = dict(t=0, l=0, r=0, b=0),
#     hoverlabel = dict(font_size = 20)
# )




mapa = go.Figure(px.scatter_mapbox(est,
    lat = est.lat,
    lon = est.lon,
    hover_name = est.id,
    zoom = 10,
    center = {'lat': 25.71804256894533,'lon': -100.30914201555723},
    custom_data = ['estacion','temp']
    ))
mapa.update_traces(
	hovertemplate = '%{customdata[0]} <br> Temperatura: %{customdata[1]}°C',
	# hovertemplate = '<b>Vía Libre (Fase 1)</b><br><extra></extra>',
    showlegend = True,
    name = 'Purple Air',
    marker_color=est.temp,
    marker_size=est.temp*1.3,
    )

# SMTTR
smttr_map = px.scatter_mapbox(pts,
    lat = pts.ycoord,
    lon = pts.xcoord,
    custom_data = ['Name'],
    #hover_data={'Name':True,}
    ) # 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, 
smttr_map.update_traces(
	hovertemplate = '%{customdata[0]}', #<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>
    showlegend = True,
    name = 'SMTTR',
    marker_color=pts.temp,
    marker_size = pts.temp*1.3)

# CONAGUA Y NASA
cyn_map = px.scatter_mapbox(cyn,
    lat = cyn.lat,
    lon = cyn.lon,
    custom_data = ['estacion','temperatura'],
    #hover_data={'Name':True,}
    ) # 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, 
cyn_map.update_traces(
	hovertemplate = '%{customdata[0]} <br> Temperatura: %{customdata[1]}°C', #<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>
    showlegend = True,
    name = 'Estaciones Meteorológicas',
    marker_color=cyn.temperatura,
    marker_size = cyn.temperatura*1.3)

# Mapa Empresas
empre_map = px.scatter_mapbox(emp,
    lat = emp.latitud,
    lon = emp.longitud,
    custom_data = ['raz_social','nombre_act'])
empre_map.update_traces(
	hovertemplate = '%{customdata[0]} <br> Giro: %{customdata[1]}',
	# hovertemplate = '<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>',
    showlegend = True,
    name = 'Empresas Contaminantes',
    marker_color="blue",
    marker_size = 10)

# Mapa Escuelas y salud
esc_sal_map = px.scatter_mapbox(eys,
    lat = eys.latitud,
    lon = eys.longitud,
    custom_data = ['raz_social','nombre_act'])
esc_sal_map.update_traces(
	hovertemplate = '%{customdata[0]} <br> Giro: %{customdata[1]}',
	# hovertemplate = '<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>',
    showlegend = True,
    name = 'Escuelas y Salud',
    marker_color="green",
    marker_size = 10)

# SMTTR
pm10_map = px.scatter_mapbox(est,
    lat = est.lat,
    lon = est.lon,
    hover_name = est.id,
    custom_data = ['estacion','pm10','pm2.5','pm1']
    )
pm10_map.update_traces(
	hovertemplate = '%{customdata[0]}, %{customdata[1]}, %{customdata[2]}, %{customdata[3]}', #<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>
    showlegend = True,
    name = 'PM10',
    marker_color=est.pm1,
    marker_size = est.pm1)

# Juntamos Capas
# mapa.add_trace(esc_sal_map.data[0])
mapa.add_trace(smttr_map.data[0])
mapa.add_trace(empre_map.data[0])
mapa.add_trace(cyn_map.data[0])
# mapa.add_trace(pm10_map.data[0])
mapa.update_layout(
    mapbox = dict(
        accesstoken = mapbox_access_token,
        style = 'streets'
    ),
    height = 800,
    hovermode = 'closest',
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
    )
# mapa.update_traces(
#     marker_size = 20
#     )
mapa.update_layout(
    legend = dict(
        yanchor = "top",
        y = 0.99,
        xanchor = "right",
        x = 0.99,
        font = dict(
            family = 'Helvetica',
            color = 'white'
        ),
        bgcolor = 'rgba(128, 128, 128, 0.4)'
    ),
    margin = dict(autoexpand = False),
    autosize = True)

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

				html.H5('Temperatura y humedad'),

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

			# dbc.Button("info", id="open", n_clicks=0),
	        # dbc.Modal(
	        #     [
	        #         dbc.ModalBody("aaaaaaaaaaaaaaaaaa"),
	        #         dbc.ModalFooter(
	        #             dbc.Button(
	        #                 "Close", id="close", className="ms-auto", n_clicks=0
	        #             )
	        #         ),
	        #     ],
	        #     id="modal",
	        #     is_open=False,
	        # ),
		
		], className='d-flex justify-content-center')

	], className='m-0', style={'height':'10vh', 'position':'absolute','z-index':'1','left':'40%'}),

	# MAPA Y FILTROS
	dbc.Row([

		# MAPA
		dbc.Col([

				html.Div([

					dcc.Loading([

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

					],
		            color="#2cdb63", type="cube"
		            ),

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

# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
