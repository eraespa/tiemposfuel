
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

# Mostrar las primeras filas para verificar los datos
print(df.head())

# Suponiendo que las columnas sean 'Hora' y 'Duración'
# Convertir las columnas 'Hora' y 'Duración' a los formatos adecuados
df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M')  # Cambia el formato si es necesario
df['Duración'] = pd.to_timedelta(df['Duración'], errors='coerce')

# Lista para almacenar los resultados
resultados = []

# Iterar por cada fila y calcular la hora final
hora_inicio = None
for index, row in df.iterrows():
    hora_inicio = row['Hora'] if hora_inicio is None else hora_inicio
    hora_final = hora_inicio + row['Duración']
    resultados.append({
        'Hora de Inicio': hora_inicio.strftime('%H:%M'),
        'Hora de Finalización': hora_final.strftime('%H:%M'),
        'Lugar': row['Lugar'],  # Suponiendo que haya una columna Lugar
        'Contenido': row['Contenido'],  # Suponiendo que haya una columna Contenido
        'Personas': row['Personas'],  # Suponiendo que haya una columna Personas
        'Acciones': row['Acciones'],  # Suponiendo que haya una columna Acciones
        'Misión': row['Misión']  # Suponiendo que haya una columna Misión
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
