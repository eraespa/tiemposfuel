
import requests
import pandas as pd
from datetime import timedelta

# URL del archivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'

# Descargar el archivo CSV desde la URL
response = requests.get(url)
csv_text = response.text

# Convertir el CSV a un DataFrame de pandas
from io import StringIO
data = StringIO(csv_text)
df = pd.read_csv(data)

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

# Mostrar los resultados en el formato solicitado
for item in resultados:
    print(f"{item['Hora']} - {item['Duración']} - {item['Lugar']}")
    print(f"Contenido: {item['Contenido']}")
    print(f"Personas: {item['Personas']}")
    print(f"Acciones: {item['Acciones']}")
    print(f"Misión: {item['Misión']}")
    print('-' * 50)
