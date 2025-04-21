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

    # Reemplazar valores nulos en 'personas' con "No disponible"
    df['personas'] = df['personas'].fillna("No disponible")

    # Obtener la primera celda de la columna 'duracion' como hora de comienzo
    hora_inicio = pd.to_timedelta(df['duracion'].iloc[0], errors='coerce')  # Usar la primera duración como hora de inicio

    # Lista para almacenar los resultados
    resultados = []

    # Iterar por cada fila y calcular la hora de finalización
    for index, row in df.iterrows():
        if pd.isnull(row['duracion']):
            continue  # Si 'duracion' es inválido, saltar esa fila
        
        # Formatear la duración en horas: minutos
        hora_final = hora_inicio + pd.to_timedelta(row['duracion'], errors='coerce')

        # Formatear la hora para que no se muestre "0 days"
        hora_calculada = str(hora_inicio).split(' ')[-1]  # Solo mostrar el tiempo, no los días

        # Agregar la información en el formato solicitado
        resultado = {
            'Hora Calculada': hora_calculada,  # Mostrar solo la hora
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

    # Asegurarse de que se muestren todas las filas que tienen datos
    if len(resultados) > 0:
        for item in resultados:
            st.write(f"**Hora Calculada**: {item['Hora Calculada']} - **Duración**: {item['Duración']} - **Lugar**: {item['Lugar']}")
            st.write(f"**Contenido**: {item['Contenido']}")
            st.write(f"**Personas**: {item['Personas']}")
            st.write(f"**Acciones**: {item['Acciones']}")
            st.write(f"**Misión**: {item['Misión']}")
            st.write("-" * 50)
    else:
        st.write("No hay datos válidos para mostrar.")

else:
    st.write(f"Error al descargar el CSV. Código de estado: {response.status_code}")
