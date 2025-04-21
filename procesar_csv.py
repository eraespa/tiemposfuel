import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# URL del archivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'

# Descargar el archivo CSV desde la URL
response = requests.get(url)

if response.status_code == 200:
    st.write("CSV descargado correctamente.")
    csv_text = response.text

    # Leer CSV como DataFrame
    data = StringIO(csv_text)
    df = pd.read_csv(data)

    # Reemplazar valores nulos en 'personas' con "No disponible"
    df['personas'] = df['personas'].fillna("No disponible")

    # ✅ Usar la segunda celda como la hora de comienzo (en formato timedelta)
    hora_base_td = pd.to_timedelta(df['duracion'].iloc[1], errors='coerce')
    if pd.isnull(hora_base_td):
        st.error("La segunda celda de la columna 'duracion' debe tener el formato HH:MM:SS")
        st.stop()

    # Convertir timedelta a datetime para operaciones
    hora_inicio = datetime.combine(datetime.today(), datetime.min.time()) + hora_base_td

    # Convertimos toda la columna 'duracion' a timedelta
    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')

    # Lista de resultados
    resultados = []

    for index, row in df.iterrows():
        if index == 0:
            resultado = {
                'Hora Comienzo': "Sin hora",
                'Duración': row['duracion'],
                'Lugar': row.get('lugar', ''),
                'Contenido': row.get('contenido', ''),
                'Personas': row.get('personas', 'No disponible'),
                'Acciones': row.get('acciones', ''),
                'Misión': row.get('mision', ''),
                'hora_dt': None
            }
        else:
            if index == 1:
                hora_actual = hora_inicio
            else:
                duracion_anterior = df['duracion_td'].iloc[index - 1]
                hora_anterior = resultados[-1]['hora_dt']
                hora_actual = hora_anterior + duracion_anterior if pd.notnull(duracion_anterior) else hora_anterior

            resultado = {
                'Hora Comienzo': hora_actual.strftime('%H:%M'),
                'Duración': row['duracion'],
                'Lugar': row.get('lugar', ''),
                'Contenido': row.get('contenido', ''),
                'Personas': row.get('personas', 'No disponible'),
                'Acciones': row.get('acciones', ''),
                'Misión': row.get('mision', ''),
                'hora_dt': hora_actual
            }
        resultados.append(resultado)

    # Mostrar resultados
    st.write("Lista de actos ordenados:")

    for item in resultados:
        st.write(f"**Hora Comienzo**: {item['Hora Comienzo']} - **Duración**: {item['Duración']} - **Lugar**: {item['Lugar']}")
        st.write(f"**Contenido**: {item['Contenido']}")
        st.write(f"**Personas**: {item['Personas']}")
        st.write(f"**Acciones**: {item['Acciones']}")
        st.write(f"**Misión**: {item['Misión']}")
        st.write("-" * 50)

else:
    st.error(f"No se pudo descargar el archivo CSV. Código de estado: {response.status_code}")
