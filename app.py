import streamlit as st
from PIL import Image

st.set_page_config(page_title="Contando una Historia con Datos", page_icon="📊", layout="wide")

#intro

with st.container():
    st.header("MCD UNISON - TEAM 2")
    st.title("Análisis Incidencia Delictiva con Datos")
    st.write("El impacto de la incidencia delictiva en Sonora en las distintas regiones,\
             sin duda alguna cierto tipos de delitos son más predominantes en unas regiones que otras \
             pero ¿cuáles son esos delitos?, ahora bien, la temperatura es algo que sin duda alguna influye en el comportamiento humano, \
             ¿influye para la generación de algún tipo de delito?")
