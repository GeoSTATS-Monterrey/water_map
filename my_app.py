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
import geopandas as gpd
import shapely.geometry


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
est = pd.read_csv("assets/purple_air/esta.csv", encoding='ISO-8859-1')
df = pd.read_csv("assets/vh_nl.csv", encoding='ISO-8859-1')
emp = pd.read_csv("assets/empresas.csv", encoding='ISO-8859-1')
pts = pd.read_csv("assets/temp_hume.csv", encoding='ISO-8859-1')
esc = pd.read_csv("assets/esc_guar.csv", encoding='ISO-8859-1')
hos = pd.read_csv("assets/hosp_asil.csv", encoding='ISO-8859-1')
cyn = pd.read_csv("assets/conagua_nasa.csv", encoding='ISO-8859-1')
vmu_df = pd.read_csv("assets/veh_mun_2020.csv", encoding='ISO-8859-1')
vmu = gpd.read_file('assets/vehiculos_municipios.geojson')

# IMAGENES
img1 = 'assets/info.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/layers.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

img3 = 'assets/close.png' # replace with your own image
encoded_img3 = base64.b64encode(open(img3, 'rb').read()).decode('ascii')

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

mapa = go.Figure(px.choropleth_mapbox(
	vmu_df, 
	geojson=vmu, 
	color=vmu_df.veh_percap,
	opacity = 0.4,
	color_continuous_scale="oranges",
	locations="MUNICIPIO", 
    featureidkey="properties.MUNICIPIO",
    custom_data = ['MUNICIPIO','VEHICULOS','poblacion','veh_percap'],
    zoom = 10,
    center = {'lat': 25.71804256894533,'lon': -100.30914201555723},
    ))
mapa.update_traces(
	showlegend = True, 
	hovertemplate = '<b>Municipio: </b>%{customdata[0]}<br><b>Cantidad de vehiculos: </b>%{customdata[1]}<br><b>Población: </b>%{customdata[2]}<br><b>Vehiculos por persona: </b>%{customdata[3]}',
	name = 'Vehiculos per cápita - ICVNL, INEGI'
	)

# SMTTR
smttr_map = px.scatter_mapbox(pts,
    lat = pts.ycoord,
    lon = pts.xcoord,
    custom_data = ['Name','temp','humedad','sens_ter'],
    opacity = 0.7,
    #hover_data={'Name':True,}
    )
smttr_map.update_traces(
	hovertemplate = '<b>Estación: </b>%{customdata[0]}<br><b>Temperatura: </b>%{customdata[1]}<br><b>Humedad: </b>%{customdata[2]}<br><b>Sensasión Térmica: </b>%{customdata[3]}',
    showlegend = True,
    name = 'Temperatura - SMTTR',
    marker_color=pts.color,
    marker_size = pts.temp*1.3)

# CONAGUA Y NASA
cyn_map = px.scatter_mapbox(cyn,
    lat = cyn.lat,
    lon = cyn.lon,
    custom_data = ['estacion','temperatura','fuente'],
    opacity = 0.7,
    #hover_data={'Name':True,}
    ) 
cyn_map.update_traces(
	hovertemplate = '<b>Estación: </b>%{customdata[0]}<br><b>Temperatura: </b>%{customdata[1]}°C<br><b>Fuente: </b>%{customdata[2]}',
    showlegend = True,
    name = 'Temperatura - CONAGUA y NASA',
    marker_color=cyn.color,
    marker_size = cyn.temperatura*1.3)

# Purple Air
ptemp_map = px.scatter_mapbox(est,
    lat = est.lat,
    lon = est.lon,
    hover_name = est.id,
    custom_data = ['estacion','temp'],
    opacity = 0.7,
    )
ptemp_map.update_traces(
	hovertemplate = '<b>Estación: </b>%{customdata[0]} <br><b>Temperatura: </b>%{customdata[1]}°C',
    showlegend = True,
    name = 'Temperatura - Purple Air',
    marker_color=est.color_tempe,
    marker_size = est['temp'],
    )

# Mapa Empresas
empre_map = px.density_mapbox(emp,
    lat = emp.latitud,
    lon = emp.longitud,
    custom_data = ['raz_social','nombre_act'],
    opacity = 0.7,
    radius=10)
empre_map.update_traces(
	hovertemplate = '<b>Nombre: </b>%{customdata[0]}<br><b>Giro: </b>%{customdata[1]}',
    showlegend = True,
    name = 'Empresas Contaminantes - INEGI',
    colorscale ='Reds'
    # marker_color="blue",
    # marker_size = 10
    )

# Mapa Escuelas y guarderías
esc_map = px.scatter_mapbox(esc,
    lat = esc.latitud,
    lon = esc.longitud,
    custom_data = ['raz_social','nombre_act'],
    opacity = 0.9,)
esc_map.update_traces(
	hovertemplate = '<b>Nombre: </b>%{customdata[0]} <br><b>Giro: </b>%{customdata[1]}',
    showlegend = True,
    name = 'Escuelas y guarderías - INEGI',
    marker_color="#32a852",
    marker_size = 5)

# Mapa Hospitales y asilos
hos_map = px.scatter_mapbox(hos,
    lat = hos.latitud,
    lon = hos.longitud,
    custom_data = ['raz_social','nombre_act'],
    opacity = 0.9,)
hos_map.update_traces(
	hovertemplate = '<b>Nombre: </b>%{customdata[0]} <br><b>Giro: </b>%{customdata[1]}',
    showlegend = True,
    name = 'Hospirtales y asilos - INEGI',
    marker_color="#4e42f5",
    marker_size = 5)

# PM10
pm10_map = px.scatter_mapbox(est,
    lat = est.lat,
    lon = est.lon,
    hover_name = est.id,
    custom_data = ['estacion','pm1'],
    opacity = 0.7,
    )
pm10_map.update_traces(
	hovertemplate = '<b>Estación: </b>%{customdata[0]} <br><b>PM10: </b>%{customdata[1]}°C',
    showlegend = True,
    name = 'PM10 - Purple Air',
    marker_color=est['color_pm10'],
    marker_size = est['pm10'],
    )

# PM2.5
pm25_map = px.scatter_mapbox(est,
    lat = est.lat,
    lon = est.lon,
    hover_name = est.id,
    custom_data = ['estacion','pm2.5'],
    opacity = 0.7,
    )
pm25_map.update_traces(
	hovertemplate = '<b>Estación: </b>%{customdata[0]} <br><b>PM2.5: </b>%{customdata[1]}',
    showlegend = True,
    name = 'PM2.5 - Purple Air',
    marker_color=est['color_pm2.5'],
    marker_size = est['pm2.5'])

# Juntamos Capas
mapa.add_trace(empre_map.data[0])
mapa.add_trace(pm10_map.data[0])
mapa.add_trace(pm25_map.data[0])
mapa.add_trace(cyn_map.data[0])
mapa.add_trace(smttr_map.data[0])
mapa.add_trace(ptemp_map.data[0])
mapa.add_trace(esc_map.data[0])
mapa.add_trace(hos_map.data[0])
# mapa.add_trace(esc_sal_map.data[0])

mapa.update_layout(
    mapbox = dict(
        accesstoken = mapbox_access_token,
        style = 'light'
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
        yanchor = "bottom",
        y = 0,
        xanchor = "left",
        x = 0,
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
	# dbc.Button(
	# 	html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
	# 		style={'width':'100%',}
	# 	), 
	# 	id="open-offcanvas", 
	# 	n_clicks=0,
	# 	style={'position':'absolute','z-index':'1','right':'1%','top':'1%','width':'5%','background-color':'#9e9595','border':'none'}),
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
		
			html.H1('GeoSTATS', style={'text-align':'center','color':'black'}),

			# dbc.Button([
			# 		html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
			# 		className="p-0 img-fluid", style={'margin':'0'})
			# 			],
			# 	id="open", 
			# 	n_clicks=0,
			# 	style={'background-color':'transparent','border':'none','color':'black','width':'30px','padding':'0 0 0 0'}),

	        dbc.Modal(
	            [
	                dbc.ModalBody([

	                	dbc.Button([
							html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
							className="p-0 img-fluid")
								],
						id="close", 
						n_clicks=0,
						style={'background-color':'transparent','border':'none','color':'black','width':'30px','padding':'0'}),

	                	html.Br(),

						"Resumen de geostats, ficha técnica, colaboradores, etc",

	                ]),
	            ],
	            id="modal",
	            is_open=False,
	        ),
		
		], className='d-flex justify-content-center', style={'float':'left'})

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

# @app.callback(
#     Output("offcanvas", "is_open"),
#     Input("open-offcanvas", "n_clicks"),
#     [State("offcanvas", "is_open")],
# )
# def toggle_offcanvas(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open

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
