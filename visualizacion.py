import pandas as pd
import os
import folium
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium



covid = pd.read_json('dat\Covid.json', orient ='column')
print(covid)
print(covid.columns)
print(covid.info())

    

st.title('Cinco gráficos que explican la situación del coronavirus en el mundo')

sidebar_covid = st.sidebar.header("Análisis COVID-19")
sidebar_image = st.sidebar.image('imagenes\coronavirus.png', use_column_width=True)
sidebar_covid_text = st.sidebar.write("El Covid-19 es una pandemia que se ha extendido por todo el mundo. La mayoría de los países del mundo han sido afectados. El manejo de cada país es diferente, de acuerdo con la política del gobierno, lo que da lugar a diferencias en la tendencia de aumento o disminución de los casos de COVID en diferentes países.  \n Analizaremos los datos de la pandemia a nivel mundial, basándonos en los reportes de la fecha más reciente.  \n Con ello queremos obtener información acerca de la situación global actual e identificar los países más afectados.")



agree = st.checkbox('Mostrar dataset')

if agree:
    covid


###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")



st.header("Situación global. Casos, muertes y recuperados por continente.")
st.write("Los siguientes gráficos diferencian entre el total de casos detectados, el número de personas que se han recuperado de la infección y las personas fallecidas.")
seleccion = st.radio("Selecciona:",("Recuperados", "Total muertes", "Total casos"))

if seleccion == "Recuperados":
    st.bar_chart(covid.groupby('continent')['recovered'].sum())
    
    
elif seleccion == "Total muertes":
    st.bar_chart(covid.groupby('continent')['total deaths'].sum())


elif seleccion == "Total casos":
    st.bar_chart(covid.groupby('continent')['total cases'].sum())

st.write("Los fallecimientos diarios suponen uno de los métodos más efectivos para estudiar cómo se comporta el coronavirus en el mundo. Aunque cada país tenga criterios diferentes a la hora de contabilizarlos, arroja una mayor fiabilidad que los casos confirmados, que no reflejan el número real de contagios. El gráfico anterior muestra las últimas cifras de muertes diarias reportadas.")
st.write("El mapa del coronavirus también se dibuja con el número de contagios totales. Europa encabeza esta tabla con más de 200 millones de infectados en total. Le siguen Asia, América del Norte, America del Sur, Oceania y Africa.")



###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")



st.header("Situación global. Casos, muertes y recuperados por país.")
st.write("Número de casos registrados de COVID-19, por países. El color indica el número de casos, muertes y recuperados registrados en cada país.")

world_covid_data = pd.read_json("dat\Covid.json")
country_geo = os.path.join('dat\world-countries.json')

seleccion3 = st.selectbox('Selecciona :', ['recovered', 'total deaths', 'total cases'])

if seleccion3 == 'recovered':
    m = folium.Map(location=[0, 0], zoom_start=2)
    m.choropleth(
        geo_data=country_geo,
        name='choropleth',
        data=world_covid_data,
        columns=['country', 'recovered'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name='COVID'
        )
    folium.LayerControl().add_to(m)
    

elif seleccion3 == 'total deaths': 
    m = folium.Map(location=[0, 0], zoom_start=2)
    m.choropleth(
         geo_data=country_geo,
         name='choropleth',
         data=world_covid_data,
         columns=['country', 'total deaths'],
         key_on='feature.properties.name',
         fill_color='YlGn',
         fill_opacity=0.7,
         line_opacity=0.5,
         legend_name='COVID'
         )
    folium.LayerControl().add_to(m)
 
 
elif seleccion3 == 'total cases':
    m = folium.Map(location=[0, 0], zoom_start=2)
    m.choropleth(
        geo_data=country_geo,
        name='choropleth',
        data=world_covid_data,
        columns=['country', 'total cases'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name='COVID'
        )
    folium.LayerControl().add_to(m)

st_data = st_folium(m)


  
###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")




st.header("Aquí puedes encontrar datos acerca de la situación actual del país que elijas.")
seleccion2 = st.selectbox('Haz clic sobre cada país para consultar el detalle de casos totales, recuperaciones, casos activos y muertes:', covid['country'].unique())
covid[covid['country']==seleccion2]

st.write("En España los casos confirmados superan a los recuperados, una comparación empleada para analizar la evolución del coronavirus. Sin embargo, hay que tener en cuenta que aunque los casos totales superen a los recuperados, actualmente estos trascurren de forma más leve.")



###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")

    

st.header("Países con mayor cifra de muertes por COVID al día de hoy.")
st.write("Para analizar la gravedad de la situación, visualizamos los países con más muertes por COVID.")
more_deaths = pd.DataFrame(covid.groupby('country')['total deaths'].sum().nlargest(10).sort_values(ascending = True))
fig2 = px.bar(more_deaths, x = 'total deaths', y = more_deaths.index, height = 600, color = 'total deaths', orientation = 'h',
            color_continuous_scale = ['deepskyblue','red'], title = 'Países con más muertes por COVID')
st.plotly_chart(fig2)
st.write("Podemos observar que los países con la cifra de muertes más elevada a día de hoy son USA, Brasil e India, seguidos por Russia y México.")


###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")



st.header("Comparación de los países con mayor Tasa de Mortalidad y mayor Tasa de Recuperación.")
col1, col2, col3 = st.columns([4, 1, 4])
st.write("La tasa de mortalidad es una medida del número de muertes en una población en particular, escalado al tamaño de esa población, por unidad de tiempo.")
st.write("La tasa de recuperación es el número de casos recuperados entre el número de casos confirmados.")

with col1:
    covid["mortality_rate"] = round((covid['total deaths']/covid['population'])*100,2)
    covid_mortality_top = covid.sort_values(by="mortality_rate", ascending=False).head(15)
    fig3 = px.scatter(
        covid_mortality_top,
        x="mortality_rate",
        y="country",
        color="mortality_rate"
        )
    fig3.update_layout(title="Países con mayor tasa de mortalidad")
    st.plotly_chart(fig3, use_container_width=True)


with col3:
    covid["recovered_rate"] = round((covid['recovered']/covid['total cases'])*100,2)
    covid_recovered_top = covid.sort_values(by="recovered_rate", ascending=False).head(15)
    fig4 = px.scatter(
        covid_recovered_top,
        x="recovered_rate",
        y="country",
        color="recovered_rate"
        )
    fig4.update_layout(title="Países con mayor tasa de recuperación")
    st.plotly_chart(fig4, use_container_width=True)

st.write("A través de la visualización, podemos ver 15 países con una alta tasa de mortalidad y 15 países con una alta tasa de recuperación. Países europeos como Lituania o Grecia presentan menor tasa de mortalidad. Perú presenta la tasa de mortalidad más alta de Europa y Estados Unidos, el porcentaje ronda el 65%.")
st.write("Entre los países con una mayor tasa de recuperación están Qatar, Dinamarca, Noruega, Países Bajos y Suiza, con alrededor de 99% de recuperados.")


###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")



st.header("Relación entre el total de casos de algunos países comparado con el numero de test COVID realizados en el mismo.")
st.write("Los tests para certificar la realidad del impacto de la Covid-19 se han convertido en una prioridad global para conocer el alcance real del coronavirus.")
fig5=px.bar(covid.tail(15), x = 'country', y = 'total cases', 
       color = 'total tests', height = 500, color_continuous_scale = ['darkseagreen','green'], 
       hover_data = ['country', 'continent'])
st.plotly_chart(fig5, use_container_width=True)
st.write("Podemos ver, que, de los países seleccionados aleatoriamente, un mayor número de tests fueron realizados en España. Sin embargo, este no es el país con más casos de COVID. Esto puede suceder debido a políticas aplicadas en cada país por el gobierno o la alta responsabilidad de ciudadanos, que al sentirse enfermos realizan los tests como precaución. Segiuida España, podemos observar un mayor numero de tests realizados en Russia e Italia. Destaca Japón, que apesar de tener cifras bastante elevadas de contagios, no acumula una cifra de test realizados tan elevada.")


###Para dejar espacio adicional entre gráficos:
container = st.empty() 
container.write("        ")

st.write("          ")
st.write("          ")
st.write("          ")


