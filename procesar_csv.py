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
    
    # Mostrar la tabla en Streamlit
    st.write("Tabla extraída del CSV:")
    st.dataframe(df)  # Muestra la tabla en un formato interactivo

else:
    st.write(f"Error al descargar el CSV. Código de estado: {response.status_code}")
