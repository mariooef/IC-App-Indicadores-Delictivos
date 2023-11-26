import streamlit as st
from PIL import Image
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Contando una Historia con Datos", page_icon="📊", layout="wide")

url = "https://lottie.host/e8a1108f-ade8-4192-a487-0cea229574d8/u8vVG9oEEo.json"

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_inicial = load_lottie(url)

#intro

with st.container():
    text_column, animation_column = st.columns(1)
    st.header("MCD UNISON - TEAM 2")
    st.title("Análisis Incidencia Delictiva con Datos")
    with text_column:
        st.write("El impacto de la incidencia delictiva en Sonora en las distintas regiones,\
                sin duda alguna cierto tipos de delitos son más predominantes en unas regiones que otras \
                pero ¿cuáles son esos delitos?, ahora bien, la temperatura es algo que sin duda alguna influye en el comportamiento humano, \
                ¿influye para la generación de algún tipo de delito?")
    with animation_column:
        st_lottie(lottie_inicial, height=400)