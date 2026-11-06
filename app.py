import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuramos la página con un estilo limpio
st.set_page_config(page_title="Simulador Boeing 737", layout="centered")

st.title(" Simulador de Vuelo 4D")
st.subheader("Ruta: MSLP (Comalapa) ➔ MSSS (Ilopango)")

def calcular_haversine_vectorizado(latitudes, longitudes):
    R_NM = 3440.069
    lat_rad = np.radians(latitudes)
    lon_rad = np.radians(longitudes)
    dlat = np.diff(lat_rad)
    dlon = np.diff(lon_rad)
    a = np.sin(dlat/2.0)**2 + np.cos(lat_rad[:-1]) * np.cos(lat_rad[1:]) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R_NM * c

# Matriz oficial
ruta_oficial = np.array([
    [13.4408, -89.0558, 101],
    [13.4600, -89.1000, 2500],
    [13.5000, -89.2500, 3000],
    [13.7000, -89.1500, 3400],
    [13.6994, -89.1198, 2000]
])

# Botón interactivo en la web
if st.button("Ejecutar Análisis Aeronáutico"):
    try:
        latitudes = ruta_oficial[:, 0]
        longitudes = ruta_oficial[:, 1]
        altitudes = ruta_oficial[:, 2]

        if np.any(altitudes < 0):
            st.error(" Error crítico: Violación física. Se detectaron altitudes negativas.")
        else:
            distancias = calcular_haversine_vectorizado(latitudes, longitudes)
            distancia_total = np.sum(distancias)
            
            consumo_base = 1600.0
            altitud_media = (altitudes[:-1] + altitudes[1:]) / 2.0
            eficiencia = 1 - (altitud_media / 40000.0)
            tiempos = distancias / 250.0
            combustible_total = np.sum(tiempos * (consumo_base * eficiencia))
            costo_total = combustible_total * 1.15
            
            # Mostramos resultados en tarjetas bonitas
            col1, col2, col3 = st.columns(3)
            col1.metric("Distancia", f"{distancia_total:.2f} NM")
            col2.metric("Combustible", f"{combustible_total:.2f} kg")
            col3.metric("Costo Estimado", f"${costo_total:.2f} USD")
            
            # Gráfica 3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(latitudes, longitudes, altitudes, marker='o', color='blue')
            st.pyplot(fig) # Comando web para mostrar gráficas
            st.success(" Simulación completada con éxito.")
            
    except Exception as e:
        st.error(f"Error en el sistema: {e}")
