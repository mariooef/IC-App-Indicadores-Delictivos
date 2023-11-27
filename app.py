import streamlit as st
from PIL import Image
import requests
#from streamlit_lottie import st_lottie
import pandas as pd
import os
import plotly.express as px
import folium
from streamlit_folium import st_folium
import datetime
import numpy as np

#os.chdir("C:\Proyectos\Maestria\IngenieriaCaracteristicas\Proyectos\IC-App-Indicadores-Delictivos")
st.set_page_config(page_title="Contando una Historia con Datos", page_icon="📊", layout="wide")

def css_load(css_file):
    try:
        with open(css_file, "r") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Archivo CSS no encontrado: {css_file}")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSS: {str(e)}")

#def load_lottie(url):
#    r = requests.get(url)
#    if r.status_code != 200:
#        return None
#    return r.json()

css_load(f"style/main.css")
app_container = st.container()
url = ""


# ----------------Datos Prueba--------------------------------------------------------------------------------------------------------

# DataFrame dummy para delitos
data_delitos = {
    'Año': [2019, 2019, 2020, 2020, 2021, 2021],
    'Mes': [1, 2, 1, 2, 1, 2],
    'Región': ['Norte', 'Norte', 'Sur', 'Sur', 'Este', 'Este'],
    'Municipio': ['Hermosillo', 'Cajeme', 'Navojoa', 'Guaymas', 'Nogales', 'San Luis Río Colorado'],
    'Tipo_De_Licto': ['Robo', 'Homicidio', 'Robo', 'Homicidio', 'Robo', 'Homicidio'],
    'Cantidad': [20, 5, 15, 3, 25, 8],
    'Latitud': [29.072967, 27.916080, 27.072967, 27.918333, 31.308617, 32.463056],  # Agrega las coordenadas reales de los municipios
    'Longitud': [-110.955919, -110.964444, -109.735028, -110.898333, -110.942617, -114.777778]  # Agrega las coordenadas reales de los municipios
}

df_delitos = pd.DataFrame(data_delitos)

# DataFrame dummy para temperatura
data_temperatura = {
    'Fecha': [datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2020, 1, 1), datetime.date(2020, 1, 2), datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)],
    'Temperatura': [25, 28, 22, 20, 30, 32],
    'Municipio': ['Hermosillo', 'Cajeme', 'Navojoa', 'Guaymas', 'Nogales', 'San Luis Río Colorado'],
    'Tipo_De_Licto': ['Robo', 'Homicidio', 'Robo', 'Homicidio', 'Robo', 'Homicidio'],
    'Cantidad': [20, 5, 15, 3, 25, 8],
    'Latitud': [29.072967, 27.916080, 27.072967, 27.918333, 31.308617, 32.463056],  # Agrega las coordenadas reales de los municipios
    'Longitud': [-110.955919, -110.964444, -109.735028, -110.898333, -110.942617, -114.777778]  # Agrega las coordenadas reales de los municipios
}

df_temperatura = pd.DataFrame(data_temperatura)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# Intro
with app_container:
        st.header("MCD UNISON - TEAM 2")

# Selector de secciones
section = st.sidebar.radio("Selecciona una historia:", ["Presentación", "Historia Región", "Historia Temperatura"])

# Historia 1: Tipos de Delitos en Regiones
if section == "Historia Región":
    st.title("Historia Región: Tipos de Delitos en Regiones")
    # Agregar gráficas y elementos interactivos aquí...

    st.markdown("""<h3>Tipos de Delitos en Regiones</h3>""", unsafe_allow_html=True)
    fig = px.bar(df_delitos, x='Región', y='Cantidad', color='Tipo_De_Licto', barmode='group')
    st.plotly_chart(fig)

    st.markdown("""<h3>Mapa Coroplético de Incidencia de Delitos por Región</h3>""", unsafe_allow_html=True)

    centro_mapa = [df_delitos['Latitud'].mean(), df_delitos['Longitud'].mean()]
    m = folium.Map(location=centro_mapa, zoom_start=6)

    for index, row in df_delitos.iterrows():
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=f"{row['Municipio']} ({row['Región']}): {row['Cantidad']} delitos ({row['Tipo_De_Licto']})"
        ).add_to(m)

    # Guardar el mapa como un archivo HTML temporal
    mapa_html = f"data/mapa_temp.html"
    m.save(mapa_html)

    # Mostrar el mapa en Streamlit usando HTML
    st.markdown("""<iframe src="data/mapa_temp.html" width="100%" height="500" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

    st.markdown("""<h3>Gráficas con Power BI</h3>""", unsafe_allow_html=True)
    st.markdown("""<iframe title="testIC" width="70%" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiNTczNDMzNGItMGY5Yi00ZmM5LWE4NjctNWNjYjJmNzY4ZjQ2IiwidCI6IjY3NTUzNjQ1LTBkYjMtNDQ4MC1iMTI3LTZmODE5YTc5ZTM2NyIsImMiOjR9&pageName=ReportSectionc7b0f916ac6d03fe4d85" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

# Historia 2: Influencia de la Temperatura en Delitos
elif section == "Historia Temperatura":
    st.title("Historia Temperatura: Influencia de la Temperatura en Delitos")
    # Agregar gráficas y elementos interactivos aquí...
    
    st.title("Influencia de la Temperatura en Delitos")

    scatter_fig = px.scatter(df_temperatura, x='Temperatura', y='Cantidad', color='Tipo_De_Licto', size='Cantidad')
    st.plotly_chart(scatter_fig)

# Página de Inicio
else:
    url = "https://lottie.host/e8a1108f-ade8-4192-a487-0cea229574d8/u8vVG9oEEo.json"
    #lottie_inicial = load_lottie(url)

    with app_container:
        st.title("Análisis Incidencia Delictiva con Datos (Contando algunas historias)")
        animation_column, text_column = st.columns(2)
        with animation_column:
            imagen_url = "images/stats.png"
            st.image(imagen_url, caption='', use_column_width=True, width=0.5)
            #st_lottie(lottie_inicial, height=300)
        with text_column:
            st.markdown("""
                <div style='text-align: justify; display: flex; align-items: center; height: 100%; width: 60%; justify-content: left'>
                    El impacto de la incidencia delictiva en Sonora en las distintas regiones,
                    sin duda alguna ciertos tipos de delitos son más predominantes en unas regiones que otras,
                    pero ¿cuáles son esos delitos? Ahora bien, la temperatura es algo que sin duda alguna influye en el comportamiento humano,
                    ¿influye para la generación de algún tipo de delito?
                </div>
            """, unsafe_allow_html=True)
