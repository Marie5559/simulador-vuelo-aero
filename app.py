import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Boeing 737", layout="centered")

st.title(" Simulador de Vuelo 4D Dinámico")
st.subheader("Ingresa o modifica las coordenadas de la ruta")

def calcular_haversine_vectorizado(latitudes, longitudes):
    R_NM = 3440.069
    lat_rad = np.radians(latitudes)
    lon_rad = np.radians(longitudes)
    dlat = np.diff(lat_rad)
    dlon = np.diff(lon_rad)
    a = np.sin(dlat/2.0)**2 + np.cos(lat_rad[:-1]) * np.cos(lat_rad[1:]) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R_NM * c

# Datos por defecto (MSLP a MSSS) en un formato editable
datos_iniciales = pd.DataFrame(
    [
        [13.4408, -89.0558, 101],
        [13.4600, -89.1000, 2500],
        [13.5000, -89.2500, 3000],
        [13.7000, -89.1500, 3400],
        [13.6994, -89.1198, 2000]
    ],
    columns=["Latitud (°)", "Longitud (°)", "Altitud (ft)"]
)

st.write("Haz clic en las celdas para editar los números, o usa los bordes para agregar filas nuevas:")
df_ruta = st.data_editor(datos_iniciales, num_rows="dynamic")

if st.button("Ejecutar Análisis Aeronáutico"):
    try:
        matriz_ruta = df_ruta.to_numpy()
        latitudes = matriz_ruta[:, 0]
        longitudes = matriz_ruta[:, 1]
        altitudes = matriz_ruta[:, 2]

        if np.any(altitudes < 0):
            st.error(" Error crítico: Violación física. Se detectaron altitudes negativas.")
        elif len(matriz_ruta) < 2:
            st.warning(" Debes ingresar al menos 2 waypoints para generar una ruta.")
        else:
            distancias = calcular_haversine_vectorizado(latitudes, longitudes)
            distancia_total = np.sum(distancias)
            
            consumo_base = 1600.0
            altitud_media = (altitudes[:-1] + altitudes[1:]) / 2.0
            eficiencia = 1 - (altitud_media / 40000.0)
            tiempos = distancias / 250.0
            combustible_total = np.sum(tiempos * (consumo_base * eficiencia))
            costo_total = combustible_total * 1.15
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Distancia", f"{distancia_total:.2f} NM")
            col2.metric("Combustible", f"{combustible_total:.2f} kg")
            col3.metric("Costo Estimado", f"${costo_total:.2f} USD")
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(latitudes, longitudes, altitudes, marker='o', color='blue')
            st.pyplot(fig)
            st.success(" Simulación completada con éxito.")
            
    except Exception as e:
        st.error("Error en el sistema: Verifica que no haya casillas vacías o letras en la matriz.")
