import streamlit as st
import requests
import pandas as pd
from io import StringIO

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

    # Mostrar la lista completa de datos
    st.write("Lista de actos ordenados:")

    # Iterar por cada fila y mostrar los resultados en el formato solicitado
    for index, row in df.iterrows():
        st.write(f"**Duración**: {row['duracion']} - **Lugar**: {row['lugar']}")
        st.write(f"**Contenido**: {row['contenido']}")
        st.write(f"**Personas**: {row['personas']}")
        st.write(f"**Acciones**: {row['acciones']}")
        st.write(f"**Misión**: {row['mision']}")
        st.write("-" * 50)

else:
    st.write(f"Error al descargar el CSV. Código de estado: {response.status_code}")
