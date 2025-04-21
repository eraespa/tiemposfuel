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

    # ✅ Interpretar la primera celda como hora real de comienzo
    hora_base_str = df['duracion'].iloc[0]  # ejemplo: "10:00"
    try:
        hora_inicio = datetime.strptime(hora_base_str.strip(), "%H:%M")
    except ValueError:
        st.error("La primera celda de la columna 'duracion' debe tener el formato HH:MM")
        st.stop()

    # Convertir la columna 'duracion' a timedelta para las filas restantes
    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')

    # Construir resultados
    resultados = []

    for index, row in df.iterrows():
        if index == 0:
            hora_actual = hora_inicio
        else:
            duracion_anterior = df['duracion_td'].iloc[index - 1]
            hora_actual = resultados[-1]['hora_dt'] + duracion_anterior if pd.notnull(duracion_anterior) else resultados[-1]['hora_dt']

        resultado = {
            'Hora Comienzo': hora_actual.strftime('%H:%M'),
            'Duración': row['duracion'],
            'Lugar': row.get('lugar', ''),
            'Contenido': row.get('contenido', ''),
            'Personas': row.get('personas', 'No disponible'),
            'Acciones': row.get('acciones', ''),
            'Misión': row.get('mision', ''),
            'hora_dt': hora_actual  # 🛠️ Usado solo internamente para el cálculo
        }
        resultados.append(resultado)

    # Mostrar lista de actos
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
