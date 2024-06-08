import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd

est = pd.read_csv("data/esta.csv", encoding='ISO-8859-1')
df = pd.read_csv("data/vh_nl.csv", encoding='ISO-8859-1')
emp = pd.read_csv("data/empresas.csv", encoding='ISO-8859-1')
pts = pd.read_csv("data/temp_hume.csv", encoding='ISO-8859-1')
esc = pd.read_csv("data/esc_guar.csv", encoding='ISO-8859-1')
hos = pd.read_csv("data/hosp_asil.csv", encoding='ISO-8859-1')
cyn = pd.read_csv("data/conagua_nasa.csv", encoding='ISO-8859-1')
vmu_df = pd.read_csv("data/veh_mun_2020.csv", encoding='ISO-8859-1')
vmu = gpd.read_file('data/vehiculos_municipios.geojson')

mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

mapa = go.Figure(px.choropleth_mapbox(
    vmu_df,
    geojson=vmu,
    color=vmu_df.veh_percap,
    opacity=0.4,
    color_continuous_scale="oranges",
    locations="MUNICIPIO",
    featureidkey="properties.MUNICIPIO",
    custom_data=['MUNICIPIO', 'VEHICULOS', 'poblacion', 'veh_percap'],
    zoom=10,
    center={'lat': 25.71804256894533, 'lon': -100.30914201555723},
))
mapa.update_traces(
    showlegend=True,
    hovertemplate='<b>Municipio: </b>%{customdata[0]}<br><b>Cantidad de vehiculos: </b>%{customdata[1]}<br><b>Población: </b>%{customdata[2]}<br><b>Vehiculos por persona: </b>%{customdata[3]}',
    name='Vehiculos per cápita - ICVNL, INEGI'
)

smttr_map = px.scatter_mapbox(pts,
                              lat=pts.ycoord,
                              lon=pts.xcoord,
                              custom_data=['Name', 'temp', 'humedad', 'sens_ter'],
                              opacity=0.7,
                              # hover_data={'Name':True,}
                              )
smttr_map.update_traces(
    hovertemplate='<b>Estación: </b>%{customdata[0]}<br><b>Temperatura: </b>%{customdata[1]}<br><b>Humedad: </b>%{customdata[2]}<br><b>Sensasión Térmica: </b>%{customdata[3]}',
    showlegend=True,
    name='Temperatura - SMTTR',
    marker_color=pts.color,
    marker_size=pts.temp * 1.3)

# CONAGUA Y NASA
cyn_map = px.scatter_mapbox(cyn,
                            lat=cyn.lat,
                            lon=cyn.lon,
                            custom_data=['estacion', 'temperatura', 'fuente'],
                            opacity=0.7,
                            # hover_data={'Name':True,}
                            )
cyn_map.update_traces(
    hovertemplate='<b>Estación: </b>%{customdata[0]}<br><b>Temperatura: </b>%{customdata[1]}°C<br><b>Fuente: </b>%{customdata[2]}',
    showlegend=True,
    name='Temperatura - CONAGUA y NASA',
    marker_color=cyn.color,
    marker_size=cyn.temperatura * 1.3)

# Purple Air
ptemp_map = px.scatter_mapbox(est,
                              lat=est.lat,
                              lon=est.lon,
                              hover_name=est.id,
                              custom_data=['estacion', 'temp'],
                              opacity=0.7,
                              )
ptemp_map.update_traces(
    hovertemplate='<b>Estación: </b>%{customdata[0]} <br><b>Temperatura: </b>%{customdata[1]}°C',
    showlegend=True,
    name='Temperatura - Purple Air',
    marker_color=est.color_tempe,
    marker_size=est['temp'],
)

# Mapa Empresas
empre_map = px.density_mapbox(emp,
                              lat=emp.latitud,
                              lon=emp.longitud,
                              custom_data=['raz_social', 'nombre_act'],
                              opacity=0.7,
                              radius=10)
empre_map.update_traces(
    hovertemplate='<b>Nombre: </b>%{customdata[0]}<br><b>Giro: </b>%{customdata[1]}',
    showlegend=True,
    name='Empresas Contaminantes - INEGI',
    colorscale='Reds'
    # marker_color="blue",
    # marker_size = 10
)

# Mapa Escuelas y guarderías
esc_map = px.scatter_mapbox(esc,
                            lat=esc.latitud,
                            lon=esc.longitud,
                            custom_data=['raz_social', 'nombre_act'],
                            opacity=0.9, )
esc_map.update_traces(
    hovertemplate='<b>Nombre: </b>%{customdata[0]} <br><b>Giro: </b>%{customdata[1]}',
    showlegend=True,
    name='Escuelas y guarderías - INEGI',
    marker_color="#32a852",
    marker_size=5)

# Mapa Hospitales y asilos
hos_map = px.scatter_mapbox(hos,
                            lat=hos.latitud,
                            lon=hos.longitud,
                            custom_data=['raz_social', 'nombre_act'],
                            opacity=0.9, )
hos_map.update_traces(
    hovertemplate='<b>Nombre: </b>%{customdata[0]} <br><b>Giro: </b>%{customdata[1]}',
    showlegend=True,
    name='Hospirtales y asilos - INEGI',
    marker_color="#4e42f5",
    marker_size=5)

# PM10
pm10_map = px.scatter_mapbox(est,
                             lat=est.lat,
                             lon=est.lon,
                             hover_name=est.id,
                             custom_data=['estacion', 'pm1'],
                             opacity=0.7,
                             )
pm10_map.update_traces(
    hovertemplate='<b>Estación: </b>%{customdata[0]} <br><b>PM10: </b>%{customdata[1]}°C',
    showlegend=True,
    name='PM10 - Purple Air',
    marker_color=est['color_pm10'],
    marker_size=est['pm10'],
)

# PM2.5
pm25_map = px.scatter_mapbox(est,
                             lat=est.lat,
                             lon=est.lon,
                             hover_name=est.id,
                             custom_data=['estacion', 'pm2.5'],
                             opacity=0.7,
                             )
pm25_map.update_traces(
    hovertemplate='<b>Estación: </b>%{customdata[0]} <br><b>PM2.5: </b>%{customdata[1]}',
    showlegend=True,
    name='PM2.5 - Purple Air',
    marker_color=est['color_pm2.5'],
    marker_size=est['pm2.5'])

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
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style='light'
    ),
    height=800,
    hovermode='closest',
    margin=dict(t=0, l=0, r=0, b=0, pad=0)
)
mapa.update_layout(
    legend=dict(
        yanchor="bottom",
        y=0,
        xanchor="left",
        x=0,
        font=dict(
            family='Helvetica',
            color='white'
        ),
        bgcolor='rgba(128, 128, 128, 0.4)'
    ),
    margin=dict(autoexpand=False),
    autosize=True)

st.set_page_config(layout="wide")
st.plotly_chart(mapa, use_container_width=True)
