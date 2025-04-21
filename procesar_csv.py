import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import timedelta

# URL del archivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'

# Descargar el archivo CSV desde la URL
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    st.write("CSV descargado correctamente.")
    csv_text = response.text
    
    # Convertir el CSV a un DataFrame de pandas
    data = StringIO(csv_text)
    df = pd.read_csv(data)
    
    # Mostrar las primeras filas del CSV para confirmar la carga
    st.write("Primeras filas del CSV:", df.head())

    # Asegurarse de que los datos sean válidos
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M', errors='coerce')  # Convertir la columna 'hora' a datetime
    df['duracion'] = pd.to_timedelta(df['duracion'], errors='coerce')  # Convertir la columna 'duracion' a timedelta

    # Lista para almacenar los resultados
    resultados = []

    # Iterar por cada fila y calcular la hora final
    hora_inicio = None
    for index, row in df.iterrows():
        if pd.isnull(row['hora']) or pd.isnull(row['duracion']):
            continue  # Si 'hora' o 'duracion' son inválidos, saltar esa fila
        hora_inicio = row['hora'] if hora_inicio is None else hora_inicio
        hora_final = hora_inicio + row['duracion']
        
        # Agregar la información en el formato requerido
        resultado = {
            'Hora': hora_inicio.strftime('%H:%M'),
            'Duración': str(row['duracion']),
            'Lugar': row['lugar'],
            'Contenido': row['contenido'],
            'Personas': row['personas'],
            'Acciones': row['acciones'],
            'Misión': row['mision']
        }
        resultados.append(resultado)
        
        # Actualizar la hora de inicio para el siguiente acto
        hora_inicio = hora_final

    # Mostrar los resultados como una lista ordenada
    st.write("Lista de actos ordenados:")
    for item in resultados:
        st.write(f"**Hora**: {item['Hora']} - **Duración**: {item['Duración']} - **Lugar**: {item['Lugar']}")
        st.write(f"**Contenido**: {item['Contenido']}")
        st.write(f"**Personas**: {item['Personas']}")
        st.write(f"**Acciones**: {item['Acciones']}")
        st.write(f"**Misión**: {item['Misión']}")
        st.write("-" * 50)

else:
    st.write(f"Error al descargar el CSV. Código de estado: {response.status_code}")
