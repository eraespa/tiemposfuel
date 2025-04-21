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

    # Inicializar la hora de inicio con la duración del primer acto
    hora_inicio = pd.to_timedelta(df['duracion'].iloc[0], errors='coerce')  # Hora de inicio es la duración de la primera línea

    # Lista para almacenar los resultados
    resultados = []

    # Iterar por cada fila y calcular la hora de finalización
    for index, row in df.iterrows():
        if pd.isnull(row['duracion']):
            continue  # Si 'duracion' es inválido, saltar esa fila
        
        # Calculamos la hora de finalización del acto anterior + duración del acto
        hora_final = hora_inicio + pd.to_timedelta(row['duracion'], errors='coerce')

        # Formateamos la hora calculada
        hora_calculada = hora_inicio

        # Agregar la información en el formato solicitado
        resultado = {
            'Hora Calculada': str(hora_calculada),  # Convertir la hora calculada en formato de texto
            'Duración': str(row['duracion']),
            'Lugar': row['lugar'],
            'Contenido': row['contenido'],
            'Personas': row['personas'],
            'Acciones': row['acciones'],
            'Misión': row['mision']
        }
        resultados.append(resultado)
        
        # Actualizamos la hora de inicio para el siguiente acto
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
