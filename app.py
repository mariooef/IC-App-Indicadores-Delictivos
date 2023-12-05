from config import st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import folium
from  streamlit_folium import folium_static
from utils import cargar_parquet
from streamlit_option_menu import option_menu

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
viridis_palette = px.colors.sequential.Plasma
info_color = viridis_palette[6] 

#----------------------------- Definición de variables--------------------------------------------------------------------------------

app_container = st.container()
url = ""


#----------------------------------------------------- INICIO APP -------------------------------------------------------------

# Intro
with app_container:
        st.header("MCD UNISON - TEAM 2")
        st.markdown("<h4>(Contando algunas historias)</h4>",unsafe_allow_html=True)

# 1. as sidebar menu
with st.sidebar:
    section = option_menu("Menu", ["Presentación", "Historia Región", 'Historia Temperatura'], 
        icons=['bar-chart-line-fill', 'geo-alt-fill', 'thermometer-sun'], menu_icon="cast", default_index=0)

# Selector de secciones
#section = st.sidebar.radio("Selecciona una historia:", ["Presentación", "Historia Región", "Historia Temperatura"])

# Historia 1: Tipos de Delitos en Regiones
if section == "Historia Región":

    url = "https://lottie.host/362eb15a-f06f-48e6-85e5-03fca0c40a96/X63xklhiL7.json"
    lottie_inicial = load_lottie(url)

#---------------------------- Carga de datos -------------------------------------------
    df_delitos_mas_pred = cargar_parquet("DelitosMasPredCoord")
    df_frec_rel_region = cargar_parquet("FrecRelRegionCoordKPI")

    if (df_delitos_mas_pred is not None) & (df_frec_rel_region is not None):
        df_delitos_mas_pred.rename(columns = {'Latitud': 'lat'}, inplace = True)
        df_delitos_mas_pred.rename(columns = {'Longitud': 'lon'}, inplace = True)
        df_frec_rel_region.rename(columns = {'Latitud': 'lat'}, inplace = True)
        df_frec_rel_region.rename(columns = {'Longitud': 'lon'}, inplace = True)
        st.toast("Datos cargados exitosamente:")
    else:
        st.error("Hubo un problema al cargar los dataframes.")

        st.title("Historia Región: Tipos de Delitos en Regiones")

#---------------------------------------------------------------------------------------------

    with st.container():
        col1, col2 = st.columns([1, 8])

        with col1:
            st_lottie(lottie_inicial, height=100)
        with col2:
            st.title("Historia Región: Tipos de Delitos en Regiones")

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        with col1:
            kpi_total = df_delitos_mas_pred['numero_delitos'].sum()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Total Delitos</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(kpi_total):,}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col2:
            region_max_numdelitos = df_delitos_mas_pred.loc[df_delitos_mas_pred['numero_delitos'].idxmax()]['tipo_delito']
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito predominante entre ciudades</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{region_max_numdelitos}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col3:
            kpi_region = df_delitos_mas_pred.groupby('region')['numero_delitos'].sum().reset_index()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Región más conflictiva</p>"
            region_max_delitos = df_delitos_mas_pred.loc[df_delitos_mas_pred['numero_delitos'].idxmax()]['region']
            region_max_numdelitos = kpi_region[kpi_region['region'] == region_max_delitos]['numero_delitos']
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{region_max_delitos} ({int(region_max_numdelitos):,})</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)      
        with col4:
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito más frecuente</p>"
            df_frecuente_tipo = pd.DataFrame(df_frec_rel_region[df_frec_rel_region["numero_delitos_rel"] == df_frec_rel_region["numero_delitos_rel"].max()])
            styled_info_message = f'''
                <div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">
                    {info_title}
                    <p style='font-size: 24px; font-weight: bold;'>{df_frecuente_tipo.iloc[1, 4]} ({df_frecuente_tipo.iloc[1, 3]}) y {df_frecuente_tipo.iloc[0, 4]} ({df_frecuente_tipo.iloc[0, 3]})</p>
                </div>
            '''
            st.markdown(styled_info_message, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("Contexto de la Historia"):
        st.markdown("### Información detallada")
        st.markdown("✨ **Destacado**: Aquí hay información importante.")
        st.info("""Podemos
                sospechar que debido a su cercanÍa con la frontera, los municipios y regiones en el norte
                del estado pueden tener mayor incidencia en actividades como la trata de personas o
                el narcomenudeo. También, se puede pensar que la actividad agrícola que existe en el
                sur del estado puede influir sobre el comportamiento delictivo. En efecto, cuatro de
                los cinco municipios con mayor superficie sembrada se encuentran en esta región. Esto
                puede confirmarse en la siguiente [página](https://www.gob.mx/agricultura/es/articulos/produccion-agropecuaria-y-pesquera-en-sonora?idiom=es)""")

    with st.container():
       
        regiones = ['Todas'] + list(df_delitos_mas_pred['region'].unique())
        region_seleccionada = st.selectbox('Selecciona una región', regiones)

        if region_seleccionada == 'Todas':
            df_filtrado = df_delitos_mas_pred
            df_filtrador = df_frec_rel_region
        else:
            df_filtrado = df_delitos_mas_pred[df_delitos_mas_pred['region'] == region_seleccionada]
            df_filtrador = df_frec_rel_region[df_frec_rel_region['region'] == region_seleccionada]
        
        with st.container():
            st.markdown("""<h3>Delitos Totales</h3>""", unsafe_allow_html=True)

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.treemap(df_filtrado, 
                        path=['region', 'tipo_delito'],  
                        values='numero_delitos',               
                        color='numero_delitos',                
                        hover_data=['numero_delitos'],        
                        title='Treemap de Delitos por Región y Tipo (Frecuencia Total)',
                        color_continuous_scale='plasma')

                fig.update_layout(
                    margin=dict(t=0, l=0, r=0, b=0),
                    coloraxis_showscale=True,
                )

                fig.update_layout(coloraxis_colorbar=dict(title='Total Delitos'))
                st.plotly_chart(fig, use_container_width=True, width="100%", height=600)

            with col2:
                #st.map(df_filtrado,
                #latitude='lat',
                #longitude='lon',
                #size='numero_delitos')

                connect_center = [df_filtrador['lat'].mean(), df_filtrador['lon'].mean()]
                map = folium.Map(location=connect_center, zoom_start=6)

                for index, row in df_filtrador.iterrows():
                    color = px.colors.sequential.Plasma[index % len(px.colors.sequential.Plasma)]
                    size = row['numero_delitos']
                    folium.CircleMarker(
                            location=[row['lat'], row['lon']],
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=f"{row['region']}: {row['numero_delitos']} delitos"
                        ).add_to(map)
                    
                folium_static(map, width=700, height=500)
            
            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""<h3>Frecuencia Relativa</h3>""", unsafe_allow_html=True)
            
            figR = px.treemap(df_filtrador, 
                        path=['region', 'tipo_delito'],  
                        values='numero_delitos_rel',               
                        color='numero_delitos_rel',                
                        hover_data=['numero_delitos_rel'],        
                        title='Treemap de Delitos por Región y Tipo (Frecuencia Relativa)',
                        color_continuous_scale='plasma')

            figR.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                coloraxis_showscale=True,
            )

            figR.update_layout(coloraxis_colorbar=dict(title='Frecuencia Relativa'))

            st.plotly_chart(figR, use_container_width=True, width="100%", height=600)

            st.info("""Proporción de delito que ocurrió en una región. Ejemplo: aproximadamente del 51% de los homicidios en Sonora ocurrieron en la región Sur.""")

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""<h3>Frecuencia regional con respecto a la población</h3>""", unsafe_allow_html=True)
            
            figR = px.treemap(df_filtrador, 
                        path=['region', 'tipo_delito'],  
                        values='indicador_pob',               
                        color='indicador_pob',                
                        hover_data=['indicador_pob'],        
                        title='Treemap de Delitos por Región y Tipo (Indicador Poblacional)',
                        color_continuous_scale='plasma')

            figR.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                coloraxis_showscale=True,
            )

            figR.update_layout(coloraxis_colorbar=dict(title='Frecuencia Relativa'))

            st.plotly_chart(figR, use_container_width=True, width="100%", height=600)

            st.info("""Proporción tomando en cuenta la población. Ejemplo: en la región Sur ocurrió aproximadamente 1.5 veces más homicidio considerando su población total.""")

    with st.expander("Datos"):
        st.write(df_delitos_mas_pred)
        st.write(df_frec_rel_region)

# Historia 2: Influencia de la Temperatura en Delitos
elif section == "Historia Temperatura":

    #---------------------------- Carga de datos -------------------------------------------
    df_scatter_municipal = cargar_parquet("ScatterMunicipal")
    df_scatter_regional = cargar_parquet("ScatterRegional")
    df_coefConMuni = cargar_parquet("CoefCorMunicipio")
    df_coefRegion = cargar_parquet("CoefCorRegion")
    df_meteoro_clima_mun = cargar_parquet("MeteorologiaClimatologiaMun")

    #----------------------------------------------------------------------------------------

    st.snow()
    url = "https://lottie.host/9c982922-aa69-43c6-8bdd-d36127870f26/vxKK73nzj6.json"
    lottie_inicial = load_lottie(url)

    if (df_scatter_municipal is not None) & (df_scatter_regional is not None) & (df_meteoro_clima_mun is not None):
        st.toast("Datos cargados exitosamente:")
    else:
        st.error("Hubo un problema al cargar los dataframes.")

        st.title("Historia Región: Tipos de Delitos en Regiones")

    with st.container():
        col1, col2 = st.columns([1, 8])

        with col1:
            st_lottie(lottie_inicial, height=100)
        with col2:
            st.title("Historia Temperatura: Influencia de la Temperatura en Delitos")
    
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            delito_mas_repite = df_coefConMuni['delito'].mode()[0]
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito más correlacionado entre Municipio</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{delito_mas_repite}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col2:
            delito_mas_repite = df_coefRegion['delito'].mode()[0]
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito más correlacionado entre Regiones</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{delito_mas_repite}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col3:
            #bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
            #df_meteoro_clima_mun['rango_temperatura'] = pd.cut(df_meteoro_clima_mun['temperatura_promedio'], bins=bins, labels=['0-5', '5-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50'])
            #rango_max_delitos = df_meteoro_clima_mun.groupby('rango_temperatura')['numero_delitos'].sum().idxmax()
            #info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Rango de Temperatura, mayor no. delitos</p>"
            #info_message = f"<p style='font-size: 24px; font-weight: bold;'>{rango_max_delitos} °C</p>"
            #styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            #st.markdown(styled_info_message, unsafe_allow_html=True)
            coeficiente_mas_alto = max_val = df_coefConMuni['val'].max()
            max_row = df_coefConMuni[df_coefConMuni['val'] == max_val]
            result = max_row['delito'].values[0] + '-' + max_row['municipio'].values[0]
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Coeficiente correlación más alto</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{result} ({round(max_row['val'].values[0], 2)})</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col4:
            bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
            df_scatter_municipal['rango_temperatura'] = pd.cut(df_scatter_municipal['temperatura_promedio'], bins=bins, labels=['0-5', '5-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50'])
            rango_max_frecuencia_relativa = df_scatter_municipal.groupby('rango_temperatura')['frecuencia_relativa'].sum().idxmax()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Rango de Temperatura mayor frecuencia de delito</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{rango_max_frecuencia_relativa} °C</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Contexto de la Historia"):
        st.markdown("### Información detallada")
        st.markdown("✨ **Destacado**: Aquí hay información importante.")
        st.info("""En esta historia se relaciona la temperatura, una variable climatológica temporal, con el comportamiento delictivo. 
                El estado de Sonora se caracteriza por tener un clima árido y extremo, alcanzando en ciertas regiones temperaturas de hasta 50 ℃. 
                Esta relación ya ha sido analizada en otras regiones y se han hecho estudios indicando que, en efecto, existe una cierta correlación entre las dos variables. 
                En general, es natural pensar que climas extremos provoquen ciertas respuestas o irritabilidad en el ser humano, y como consecuencia, 
                cambiar hasta cierto nivel la conducta y la interacción social.""")
        
    with st.container():

        st.markdown("""<h3>Violencia-Municipio en Función de la Temperatura Promedio y Frecuencia Relativa</h3>""", unsafe_allow_html=True)

        fig = px.scatter(df_scatter_municipal, 
                    x='temperatura_promedio', 
                    y='frecuencia_relativa', 
                    color='par',
                    size='frecuencia_relativa',
                    hover_data=['par'],
                    color_continuous_scale="plasma")
                
        fig.update_xaxes(title_text='Temperatura Promedio')
        fig.update_yaxes(title_text='Frecuencia Relativa')
        fig.update_layout(legend_title_text='Tipo Delito - Municipio')
                
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""<h3>Violencia-Región en Función de la Temperatura y Frecuencia Relativa</h3>""", unsafe_allow_html=True)

        fig = px.scatter(df_scatter_regional, 
                    x='temperatura_promedio', 
                    y='frecuencia_relativa', 
                    color='par',
                    size='frecuencia_relativa',
                    hover_data=['par'],
                    color_continuous_scale="plasma")
                
        fig.update_xaxes(title_text='Temperatura Promedio')
        fig.update_yaxes(title_text='Frecuencia Relativa')
        fig.update_layout(legend_title_text='Tipo Delito - Región')
                
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""<h3>Distribución de la temperatura promedio</h3>""", unsafe_allow_html=True)

        fig = px.violin(df_meteoro_clima_mun, 
                        x='temperatura_promedio', 
                        box=True,
                        points="all",
                        width=800, height=500,
                        orientation='h')
        fig.update_xaxes(title_text='Temperatura Promedio')

        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Datos"):
        st.write(df_scatter_municipal)
        st.write(df_scatter_regional)
        st.write(df_coefConMuni)
        st.write(df_coefRegion)
        st.write(df_meteoro_clima_mun)

# Página de Inicio
else:

    #--------------------------------------- Carga de datos -----------------------------------------------------------------------------

    df_delictiva_mun_coord = cargar_parquet("DelictivaMunCoordenadas")
    df_municipio_mas_delictivo = cargar_parquet("MunicipiosMasDelictivosRegion")
    df_delitos_mas_frec = cargar_parquet("DelitosMasFrec")

    if (df_delictiva_mun_coord is not None) & (df_municipio_mas_delictivo is not None)  & (df_delitos_mas_frec is not None):
        st.toast("Datos cargados exitosamente:")
    else:
        st.error("Hubo un problema al cargar los dataframes.")
    
    #--------------------------------------------------------------------------------------------------------------------------------------

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
         info_inicial = st.info("""El objetivo general es presentar los hallazgos obtenidos con el análisis de los datos de frecuencia o incidencia delictiva, 
                                la región o zona dentro del estado de Sonora, y la temperatura, una variable climatológica. 
                                Al ser datos de frecuencia con distintos tipos de variables, el tablero que se presenta contiene gráficas sencillas que permitan ver proporciones 
                                y correlación entre estas características.""")
         
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            kpi_total = df_delictiva_mun_coord['numero_delitos'].sum()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Total Delitos</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(kpi_total):,}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col2:
            region_max_numdelitos = df_delictiva_mun_coord.loc[df_delictiva_mun_coord['numero_delitos'].idxmax()]['tipo_delito']
            num_max_numdelitos = df_delictiva_mun_coord[df_delictiva_mun_coord['tipo_delito']==region_max_numdelitos]['numero_delitos'].sum()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Delito más predominante</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{region_max_numdelitos} ({int(num_max_numdelitos):,})</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)
        with col3:
            promedio_delitos_por_año = df_delictiva_mun_coord['numero_delitos'].sum() / df_delictiva_mun_coord['anio'].nunique()
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Promedio delito por año</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{int(promedio_delitos_por_año):,}</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)      
        with col4:
            kpi_total = df_delictiva_mun_coord['numero_delitos'].sum()
            mes_max_incidencia = df_delictiva_mun_coord.loc[df_delictiva_mun_coord['numero_delitos'].idxmax()]['mes']
            porcentaje_mes_max = (df_delictiva_mun_coord[df_delictiva_mun_coord['mes'] == mes_max_incidencia]['numero_delitos'].sum() / kpi_total) * 100
            info_title = f"<p style='font-size: 18px; margin-bottom: 5px;'>Mes más conflictivo</p>"
            info_message = f"<p style='font-size: 24px; font-weight: bold;'>{mes_max_incidencia} ({porcentaje_mes_max:,.2f}%)</p>"
            styled_info_message = f'<div style="color: white; background-color: {info_color}; padding: 10px; border-radius: 5px; height: 115px;">{info_title}{info_message}</div>'
            st.markdown(styled_info_message, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Contexto de la Historia"):
        st.markdown("### Información detallada")
        st.markdown("✨ **Destacado**: Aquí hay información importante.")
        st.info("""Historia relacionada
                al comportamiento delictivo general a nivel estatal, regional y municipal del estado de
                Sonora, evitando relacionarlo con otros factores. Ante esto, la misma contiene
                algunas estadísticas básicas sobre la incidencia delictiva de la misma entidad, como por
                ejemplo, la frecuencia total de delitos por región. También, se incluye una selección de
                los delitos con mayor incidencia a nivel estatal y los municipios con mayor actividad
                delictiva del estado. Este relato nos permite dar un panorama general de este problema
                social, y dar a conocer las regiones y delitos con los que se trabajarán en las historias
                restantes.""")
        
        st.markdown("""<h3>Listado de Municipios con Mayor Frecuencia Delictiva por Región</h3>""", unsafe_allow_html=True)
        regiones_unicas = df_municipio_mas_delictivo['region'].unique()
        df_regiones_unicas = pd.DataFrame({'region': regiones_unicas})

        for index, row in df_regiones_unicas.iterrows():
            region = row['region']
            filtro_region = pd.DataFrame(df_municipio_mas_delictivo[df_municipio_mas_delictivo['region'] == region])
            listado_municipios = f"• {region}: {', '.join([municipio for municipio in filtro_region['municipio']])}"
            st.markdown(listado_municipios, unsafe_allow_html=True)

        columna1 = df_delitos_mas_frec['tipo_delito'][:5].tolist()
        columna2 = df_delitos_mas_frec['tipo_delito'][5:10].tolist()
        columna3 = df_delitos_mas_frec['tipo_delito'][10:].tolist()

        st.markdown("""<h3>Los 15 delitos más frecuentes a nivel estatal son</h3>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('\n'.join(f'- {tipo_delito}' for tipo_delito in columna1))

        with col2:
            st.markdown('\n'.join(f'- {tipo_delito}' for tipo_delito in columna2))

        with col3:
            st.markdown('\n'.join(f'- {tipo_delito}' for tipo_delito in columna3))

    st.markdown("""<h3>Mapa Delitos Nivel Municipal</h3>""", unsafe_allow_html=True)
    st.markdown("""<iframe title="testIC" width="100%" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiYjg5ZjkwMjktYjRiMi00OGY0LWIwMTQtZTZlZjliZmVjODU5IiwidCI6IjY3NTUzNjQ1LTBkYjMtNDQ4MC1iMTI3LTZmODE5YTc5ZTM2NyIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        df_delitos_ordenado = df_municipio_mas_delictivo.sort_values(by='numero_delitos', ascending=False)
        fig = px.bar(df_delitos_ordenado, x='numero_delitos', y='municipio', color='region',
             labels={'numero_delitos': 'Cantidad de Delitos', 'municipio': 'Municipio'},
             title='Municipios con mayor frecuencia delictiva por región y los 15 delitos más frecuentes',
             barmode='stack',
             color_continuous_scale='plasma')
        st.plotly_chart(fig)
    with col2:
        fig = px.funnel(df_delitos_mas_frec, x='numero_delitos', y='tipo_delito', title='15 delitos más frecuentes')
        fig.update_xaxes(title_text='Número de Delitos')
        fig.update_yaxes(title_text='Tipo de Delito')
        st.plotly_chart(fig)

    with st.expander("Datos"):
        st.write(df_delictiva_mun_coord)
        st.write(df_municipio_mas_delictivo)
        st.write(df_delitos_mas_frec)
        st.write(df_delitos_mas_frec)