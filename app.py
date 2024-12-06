import streamlit as st
import requests
import folium
from folium import plugins
import time
from geopy.geocoders import Nominatim

# Establecer tema oscuro para la página
st.set_page_config(page_title="Predicción de Tarifas de Taxi", page_icon="🚖", layout="centered", initial_sidebar_state="collapsed")

# Título principal
st.title('🚖 Predicción de Tarifas de Taxi')

# Imagen de fondo para darle un toque más cool
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://www.example.com/fondo.jpg');
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Descripción divertida
st.markdown("""
Este es un sitio donde puedes ingresar los detalles de tu viaje en taxi, ¡y ver cuánto podría costar! 😎
""")

# Ingreso de parámetros
st.header("📝 Ingrese los detalles del viaje")

# Fecha y hora
pickup_datetime = st.date_input("Fecha de recogida", value=pd.to_datetime('today'))
pickup_time = st.time_input("Hora de recogida", value=pd.to_datetime('now').time())

# Coordenadas de recogida
st.subheader("Ubicación de recogida:")
pickup_lat = st.number_input("Latitud de recogida:", value=40.7128, step=0.0001)
pickup_lon = st.number_input("Longitud de recogida:", value=-74.0060, step=0.0001)

# Coordenadas de destino
st.subheader("Ubicación de destino:")
dropoff_lat = st.number_input("Latitud de destino:", value=40.7308, step=0.0001)
dropoff_lon = st.number_input("Longitud de destino:", value=-73.9975, step=0.0001)

# Número de pasajeros
passenger_count = st.number_input("Número de pasajeros:", min_value=1, max_value=6, value=1)

# Animación de carga
def loading_animation():
    with st.spinner('Calculando la tarifa...'):
        time.sleep(2)

# Botón para hacer la predicción
if st.button("Predecir tarifa"):
    loading_animation()  # Animación antes de la predicción

    # Aquí se realizaría la llamada a la API para obtener la predicción
    api_url = 'https://taxifare.lewagon.ai/predict'  # URL de la API de Le Wagon o tu API
    params = {
        'pickup_datetime': f"{pickup_datetime} {pickup_time}",
        'pickup_latitude': pickup_lat,
        'pickup_longitude': pickup_lon,
        'dropoff_latitude': dropoff_lat,
        'dropoff_longitude': dropoff_lon,
        'passenger_count': passenger_count
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        prediction = response.json()['fare']
        st.success(f"🎉 ¡La tarifa estimada del taxi es: ${prediction:.2f}!")
    else:
        st.error("🚨 Hubo un error al obtener la predicción. Intenta nuevamente.")

# Mapa interactivo con rutas dinámicas y estilo cool
st.header("🌍 Mapa interactivo")

# Crear el mapa centrado en las coordenadas de la recogida
map_center = [pickup_lat, pickup_lon]
m = folium.Map(location=map_center, zoom_start=12, tiles="Stamen Toner")

# Marcadores con íconos personalizados
folium.Marker([pickup_lat, pickup_lon], popup="Ubicación de recogida", icon=folium.Icon(color="blue", icon="cloud")).add_to(m)
folium.Marker([dropoff_lat, dropoff_lon], popup="Ubicación de destino", icon=folium.Icon(color="red", icon="cloud")).add_to(m)

# Ruta dinámica con efectos
folium.PolyLine([(pickup_lat, pickup_lon), (dropoff_lat, dropoff_lon)], color="green", weight=5, opacity=1).add_to(m)

# Añadir un efecto de zona de transición entre los puntos
plugins.AntPath([(pickup_lat, pickup_lon), (dropoff_lat, dropoff_lon)], color="orange", weight=4).add_to(m)

# Agregar el mapa interactivo en Streamlit
st.markdown(f'<iframe srcdoc="{m._repr_html_()}" width="700" height="500"></iframe>', unsafe_allow_html=True)

# Nota de contacto o más información
st.markdown("""
Para más detalles o consultas, contáctanos en: support@taxiprediction.com 📩
""")
