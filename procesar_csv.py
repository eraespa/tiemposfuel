import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# URL del archivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'

# Descargar y leer CSV
response = requests.get(url)

if response.status_code == 200:
    st.write("CSV descargado correctamente.")
    df = pd.read_csv(StringIO(response.text))

    # Verificamos si la columna 'comienzo' existe y tiene un valor válido
    if 'comienzo' not in df.columns or pd.isnull(df['comienzo'].iloc[0]):
        st.error("La columna 'comienzo' debe existir y tener una hora en la primera fila.")
        st.stop()

    # Leemos la hora inicial desde la columna 'comienzo' (formato HH:MM o HH:MM:SS)
    hora_inicio_str = str(df['comienzo'].iloc[0]).strip()
    try:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M:%S")
    except ValueError:
        try:
            hora_actual = datetime.strptime(hora_inicio_str, "%H:%M")
        except:
            st.error("El valor de 'comienzo' debe estar en formato HH:MM o HH:MM:SS.")
            st.stop()

    # Convertimos la columna 'duracion' a timedelta
    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')
    df['personas'] = df['personas'].fillna("No disponible")

    st.write("Lista de actos ordenados:")

    # Iteramos por las filas y mostramos la información
    for i, row in df.iterrows():
        # Mostrar hora actual
        hora_str = hora_actual.strftime("%H:%M")
        duracion_str = row['duracion']
        lugar = row.get('lugar', '')
        contenido = row.get('contenido', '')
        personas = row.get('personas', '')
        acciones = row.get('acciones', '')
        mision = row.get('mision', '')

        # Mostrar info en pantalla
        st.write(f"**Hora Comienzo**: {hora_str} - **Duración**: {duracion_str} - **Lugar**: {lugar}")
        st.write(f"**Contenido**: {contenido}")
        st.write(f"**Personas**: {personas}")
        st.write(f"**Acciones**: {acciones}")
        st.write(f"**Misión**: {mision}")
        st.write("-" * 50)

        # Sumar duración si es válida
        if pd.notnull(row['duracion_td']):
            hora_actual += row['duracion_td']

else:
    st.error(f"No se pudo descargar el CSV. Código de estado: {response.status_code}")
