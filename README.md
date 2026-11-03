# simulador-vuelo-aero
Simulador de trayectorias 3D y análisis de rendimiento de vuelo para un Boeing 737-800 (Ruta Comalapa - Ilopango)

**Descripción del Proyecto**
Este repositorio contiene un simulador computacional desarrollado en Python para evaluar el rendimiento y la trayectoria espacial de un Boeing 737-800. El algoritmo modela la ruta de corto alcance entre el Aeropuerto Internacional de El Salvador (MSLP) y el Aeropuerto Internacional de Ilopango (MSSS). Utiliza trigonometría esférica (fórmula de Haversine) para el cálculo de distancias ortodrómicas y aplica un modelo de consumo de combustible dinámico ajustado a la altitud, garantizando rigor físico mediante procesamiento matricial.

**Objetivos Técnicos**

* Calcular la distancia real de vuelo aplicando la fórmula de Haversine vectorizada sobre un modelo terrestre esférico.
* Estimar el consumo de combustible integrando un factor de eficiencia aerodinámica dependiente de la altitud por segmento.
* Visualizar el perfil de la misión mediante una proyección espacial 3D de los waypoints de navegación.
* Asegurar la viabilidad de la simulación mediante un sistema de validación que bloquea altitudes negativas y errores de formato.

**Herramientas Implementadas**
- **Python:** Lógica central y manejo preventivo de errores.
- **NumPy:** Computación vectorizada y análisis matemático.
- **Matplotlib:** Renderizado de trayectorias aeronáuticas en 3D.

## Instalación y Ejecución
El proyecto está diseñado para ejecutarse en un entorno interactivo.
1. Abrir el archivo `.ipynb` en Google Colab.
2. Las dependencias requeridas (`numpy`, `matplotlib`) están preinstaladas en el entorno de Colab (ver `requirements.txt`).
3. Ejecutar la celda de código seleccionando `Entorno de ejecución > Ejecutar todo`.

## Casos de Prueba y Manejo de Errores
El algoritmo incluye un bloque de validación para casos frontera:
* **Ejecución normal:** La matriz con 5 waypoints oficiales procesará la distancia con Haversine y generará el perfil de elevación 3D.
* **Prueba de estrés (Altitudes negativas):** Si se modifica la altitud inicial de MSLP (101 ft) a un valor negativo (ej., -10 ft), el sistema bloquea el procesamiento matemático y emite una alerta de violación física por riesgo de colisión contra el terreno.
