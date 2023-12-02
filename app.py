import streamlit as st
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import folium
from  streamlit_folium import st_folium
import datetime
import numpy as np
import altair as alt
import utils
from utils import cargar_csv
from config import st

#------------------------ Estilos y formato --------------------------------------------------------------------------
def css_load(css_file):
    try:
        with open(css_file, "r") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Archivo CSS no encontrado: {css_file}")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSS: {str(e)}")

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

css_load(f"style/main.css")

# Aplicando una paleta de colores Viridis
viridis_palette = px.colors.sequential.Viridis
info_color = viridis_palette[4] 

#----------------------------- Definición de variables--------------------------------------------------------------------------------

app_container = st.container()
url = ""

#--------------------------------------- Carga de datos -----------------------------------------------------------------------------

df_delitos_mas_pred = cargar_csv("DelitosMasPred")
df_frec_rel_region = cargar_csv("FrecRelRegion")

if (df_delitos_mas_pred is not None) & (df_delitos_mas_pred is not None):
    st.toast("Datos cargados exitosamente:")

    with st.expander("Datos"):
        st.write(df_delitos_mas_pred)
        st.write(df_frec_rel_region)
else:
    st.error("Hubo un problema al cargar los dataframes.")

# ----------------Datos Prueba--------------------------------------------------------------------------------------------------------

# DataFrame dummy para delitos
data_delitos = {
    'Año': [2019, 2019, 2020, 2020, 2021, 2021],
    'Mes': [1, 2, 1, 2, 1, 2],
    'Región': ['Norte', 'Norte', 'Sur', 'Sur', 'Este', 'Este'],
    'Municipio': ['Hermosillo', 'Cajeme', 'Navojoa', 'Guaymas', 'Nogales', 'San Luis Río Colorado'],
    'Tipo_De_Licto': ['Robo', 'Homicidio', 'Robo', 'Homicidio', 'Robo', 'Homicidio'],
    'Cantidad': [20, 5, 15, 3, 25, 8],
    'lat': [29.072967, 27.916080, 27.072967, 27.918333, 31.308617, 32.463056],  # Agrega las coordenadas reales de los municipios
    'lon': [-110.955919, -110.964444, -109.735028, -110.898333, -110.942617, -114.777778]  # Agrega las coordenadas reales de los municipios
}

df_delitos = pd.DataFrame(data_delitos)

# DataFrame dummy para temperatura
data_temperatura = {
    'Fecha': [datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2020, 1, 1), datetime.date(2020, 1, 2), datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)],
    'Temperatura': [25, 28, 22, 20, 30, 32],
    'Municipio': ['Hermosillo', 'Cajeme', 'Navojoa', 'Guaymas', 'Nogales', 'San Luis Río Colorado'],
    'Tipo_De_Licto': ['Robo', 'Homicidio', 'Robo', 'Homicidio', 'Robo', 'Homicidio'],
    'Cantidad': [20, 5, 15, 3, 25, 8],
    'lat': [29.072967, 27.916080, 27.072967, 27.918333, 31.308617, 32.463056],  # Agrega las coordenadas reales de los municipios
    'lon': [-110.955919, -110.964444, -109.735028, -110.898333, -110.942617, -114.777778]  # Agrega las coordenadas reales de los municipios
}

df_temperatura = pd.DataFrame(data_temperatura)

#----------------------------------------------------- INICIO APP -------------------------------------------------------------

fig = px.treemap(df_delitos_mas_pred, 
                 path=['region', 'tipo_delito'],  
                 values='numero_delitos',               
                 color='numero_delitos',                
                 hover_data=['numero_delitos'],        
                 title='Treemap de Delitos por Región y Tipo',
                 color_continuous_scale='viridis')


# Agregar interactividad
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    coloraxis_showscale=True,
)

# Intro
with app_container:
        st.header("MCD UNISON - TEAM 2")
        st.markdown("<h4>(Contando algunas historias)</h4>",unsafe_allow_html=True)

# Selector de secciones
section = st.sidebar.radio("Selecciona una historia:", ["Presentación", "Historia Región", "Historia Temperatura"])

# Historia 1: Tipos de Delitos en Regiones
if section == "Historia Región":
    st.title("Historia Región: Tipos de Delitos en Regiones")

    st.markdown("""<h3>Tipos de Delitos en Regiones</h3>""", unsafe_allow_html=True)
    fig = px.bar(df_delitos, x='Región', y='Cantidad', color='Tipo_De_Licto', barmode='group')
    st.plotly_chart(fig)

    st.markdown("""<h3>Tipos de Delitos en Regiones</h3>""", unsafe_allow_html=True)
    fig = px.bar(df_delitos, x='Región', y='Cantidad', color='Tipo_De_Licto', barmode='group')
    st.plotly_chart(fig)

    # Filtrar por región
    region_seleccionada = st.selectbox("Selecciona una región:", df_delitos['Región'].unique())
    df_region = df_delitos[df_delitos['Región'] == region_seleccionada]
    
    chart = alt.Chart(df_region).mark_bar().encode(
        x='Tipo_De_Licto:N',
        y='sum(Cantidad):Q',
        tooltip=['Tipo_De_Licto:N', 'sum(Cantidad):Q']
    ).properties(width=500)

    st.altair_chart(chart, use_container_width=True)

    st.markdown("""<h3>Mapa Coroplético de Incidencia de Delitos por Región</h3>""", unsafe_allow_html=True)

    # Configurar el mapa centrado en la ubicación promedio
    connect_center = [df_delitos['lat'].mean(), df_delitos['lon'].mean()]
    map = folium.Map(location=connect_center, zoom_start=6)

    # Agregar marcadores para cada municipio
    for index, row in df_delitos.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=row['Municipio']).add_to(map)

    # Mostrar el mapa en Streamlit
    st.title("Mapa de Municipios con Delitos")
    st_folium(map, width=700, height=500)

    st.map(df_delitos,
    latitude='lat',
    longitude='lon',
    size='Cantidad')

    st.markdown("""<h3>Gráficas con Power BI</h3>""", unsafe_allow_html=True)
    st.markdown("""<iframe title="testIC" width="100%" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiNTczNDMzNGItMGY5Yi00ZmM5LWE4NjctNWNjYjJmNzY4ZjQ2IiwidCI6IjY3NTUzNjQ1LTBkYjMtNDQ4MC1iMTI3LTZmODE5YTc5ZTM2NyIsImMiOjR9&pageName=ReportSectionc7b0f916ac6d03fe4d85" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

# Historia 2: Influencia de la Temperatura en Delitos
elif section == "Historia Temperatura":
    st.markdown("""<h3>Influencia de la Temperatura en Delitos</h3>""", unsafe_allow_html=True)
    # Agregar gráficas y elementos interactivos aquí...

    scatter_fig = px.scatter(df_temperatura, x='Temperatura', y='Cantidad', color='Tipo_De_Licto', size='Cantidad')
    st.plotly_chart(scatter_fig)

    scatter = alt.Chart(df_temperatura).mark_circle().encode(
        x='Fecha:T',
        y='Temperatura:Q',
        color='Municipio:N',
        size='Cantidad:Q',
        tooltip=['Municipio:N', 'Fecha:T', 'Temperatura:Q', 'Cantidad:Q']
    ).properties(width=700, height=400)

    st.altair_chart(scatter, use_container_width=True)

# Página de Inicio
else:
    url = "https://lottie.host/e8a1108f-ade8-4192-a487-0cea229574d8/u8vVG9oEEo.json"
    lottie_inicial = load_lottie(url)

    with app_container:
        st.title("Análisis Incidencia Delictiva con Datos")
        animation_column, text_column = st.columns((4, 6))
        with animation_column:
            #imagen_url = "images/stats.png"
            #st.image(imagen_url, caption='', use_column_width=True, width=0.5)
            st_lottie(lottie_inicial, height=300)
        with text_column:
            st.write('')
            st.markdown("""
                <div style='text-align: justify; display: flex; align-items: center; height: 100%; width: 60%; justify-content: left; padding-bottom:5%; padding-top:5%'>
                    El impacto de la incidencia delictiva en Sonora en las distintas regiones,
                    sin duda alguna ciertos tipos de delitos son más predominantes en unas regiones que otras,
                    pero ¿cuáles son esos delitos? Ahora bien, la temperatura es algo que sin duda alguna influye en el comportamiento humano,
                    ¿influye para la generación de algún tipo de delito?
                </div>
            """, unsafe_allow_html=True)
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
        with col1:
            kpi_total = df_delitos_mas_pred['numero_delitos'].sum()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Total Delitos</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(kpi_total):,}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 100px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col2:
            kpi_region = df_delitos_mas_pred.groupby('region')['numero_delitos'].sum().reset_index()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Región mas conflictiva</p>"
            region_max_delitos = df_delitos_mas_pred.loc[df_delitos_mas_pred['numero_delitos'].idxmax()]['region']
            region_max_numdelitos = df_delitos_mas_pred.loc[df_delitos_mas_pred['numero_delitos'].idxmax()]['numero_delitos']
            #info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(kpi_region[kpi_region['region']=='Centro Norte']['numero_delitos'].iloc[0])}</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{region_max_delitos} ({int(region_max_numdelitos):,})</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 100px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col3:
            kpi_region = df_delitos_mas_pred.groupby('region')['numero_delitos'].sum().reset_index()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito mas frecuente</p>"
            df_frecuente_tipo = pd.DataFrame(df_frec_rel_region[df_frec_rel_region["numero_delitos_rel"] == df_frec_rel_region["numero_delitos_rel"].max()])
            #info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(kpi_region[kpi_region['region']=='Centro Norte']['numero_delitos'].iloc[0])}</p>"
            styled_info_message = f'''
                <div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 100px;">
                    {info_title}
                    <p style='font-size: 24px; font-weight: bold;'>{df_frecuente_tipo.iloc[1, 2]} ({df_frecuente_tipo.iloc[1, 1]}) y {df_frecuente_tipo.iloc[0, 2]} ({df_frecuente_tipo.iloc[0, 1]})</p>
                </div>
            '''
            #styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 100px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col4:
            region_max_numdelitos = df_delitos_mas_pred.loc[df_delitos_mas_pred['numero_delitos'].idxmax()]['tipo_delito']
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito predominante</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{region_max_numdelitos}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 100px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.plotly_chart(fig, use_container_width=True, width="100%", height=600)

        # Divisor para separar secciones
        st.markdown("<hr>", unsafe_allow_html=True)