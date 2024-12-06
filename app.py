import streamlit as st
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Recuerda que existen varias formas de mostrar contenido en tu página web...

Ya sea como el título con una cadena (o un f-string), o como este párrafo usando las funciones `st.`.
''')

'''
## Parámetros de la carrera

Vamos a pedir los siguientes datos:
- Fecha y hora
- Longitud y latitud de recogida
- Longitud y latitud de entrega
- Número de pasajeros
'''

# Formulario para obtener los parámetros de la carrera
pickup_longitude = st.number_input('Longitud de recogida', value=0.0)
pickup_latitude = st.number_input('Latitud de recogida', value=0.0)
dropoff_longitude = st.number_input('Longitud de entrega', value=0.0)
dropoff_latitude = st.number_input('Latitud de entrega', value=0.0)
passenger_count = st.number_input('Número de pasajeros', min_value=1, max_value=6, value=1)

# URL de la API de predicción
url = 'https://taxifare.lewagon.ai/predict'  # Reemplaza con tu URL si tienes una API propia

# Construir el diccionario de parámetros
data = {
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}

# Realizar la solicitud a la API
response = requests.get(url, params=data)

# Si la solicitud es exitosa, mostrar el resultado
if response.status_code == 200:
    prediction = response.json()['fare']
    st.markdown(f'El costo estimado del viaje es: ${prediction:.2f}')
else:
    st.markdown('Error al obtener la predicción. Inténtalo de nuevo más tarde.')
