import requests
import pandas as pd
from datetime import datetime, timedelta

# URL del archivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'

# Descargar el archivo CSV desde la URL
response = requests.get(url)
csv_text = response.text

# Convertir el CSV a un DataFrame de pandas
from io import StringIO
data = StringIO(csv_text)
df = pd.read_csv(data)

# Verificar las columnas del DataFrame
print("Columnas disponibles:", df.columns)

# Asegurarnos de que los valores en 'hora' sean válidos y convertirlos
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M', errors='coerce')  # Cambia 'errors' a 'coerce' para manejar valores inválidos
df['duracion'] = pd.to_timedelta(df['duracion'], errors='coerce')  # Similar para duración

# Lista para almacenar los resultados
resultados = []

# Iterar por cada fila y calcular la hora final
hora_inicio = None
for index, row in df.iterrows():
    if pd.isnull(row['hora']):
        print(f"Valor inválido en la columna 'hora' en la fila {index}. Se saltará esta fila.")
        continue  # Si la hora es inválida, saltar la fila
    hora_inicio = row['hora'] if hora_inicio is None else hora_inicio
    hora_final = hora_inicio + row['duracion']
    resultados.append({
        'Hora de Inicio': hora_inicio.strftime('%H:%M'),
        'Hora de Finalización': hora_final.strftime('%H:%M'),
        'Lugar': row['lugar'],  # Usar 'lugar' en minúscula
        'Contenido': row['contenido'],  # Usar 'contenido' en minúscula
        'Personas': row['personas'],  # Usar 'personas' en minúscula
        'Acciones': row['acciones'],  # Usar 'acciones' en minúscula
        'Misión': row['mision']  # Usar 'mision' en minúscula
    })
    hora_inicio = hora_final  # Actualizar la hora de inicio para el siguiente acto

# Mostrar el resultado
for item in resultados:
    print(f"Hora de Inicio: {item['Hora de Inicio']}, Hora de Finalización: {item['Hora de Finalización']}")
    print(f"Lugar: {item['Lugar']}")
    print(f"Contenido: {item['Contenido']}")
    print(f"Personas: {item['Personas']}")
    print(f"Acciones: {item['Acciones']}")
    print(f"Misión: {item['Misión']}")
    print('-' * 50)
