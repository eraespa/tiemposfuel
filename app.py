
import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# --- Estilos visuales usando Red Hat y recuadros ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;700&display=swap');

* {
    font-family: 'Red Hat Display', sans-serif;
}

.bloque {
    margin-bottom: 30px;
    display: flex;
    align-items: center;
}

.card {
    border: 2px solid black;
    border-radius: 16px;
    padding: 16px 24px;
    flex-grow: 1;
}

.fila {
    display: flex;
    align-items: flex-start;
}

.hora {
    font-size: 48px;
    font-weight: 700;
    width: 80px;
    text-align: right;
    margin-right: 16px;
    line-height: 1;
}

.contenido {
    display: flex;
    flex-direction: column;
}

.titulo {
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 4px;
    line-height: 1;
}

.info {
    font-size: 14px;
    line-height: 1.2;
}
</style>
""", unsafe_allow_html=True)

# --- Descargar y cargar datos ---
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))

    # Asegurarse de que la columna 'comienzo' no tenga valores vacíos o mal formateados
    df['comienzo'] = df['comienzo'].fillna('--').astype(str)
    df['comienzo'] = df['comienzo'].replace('', '--')

    # Filtrar filas donde 'comienzo' es '--', es decir, valores vacíos o incorrectos
    df = df[df['comienzo'] != '--']

    if df.empty:
        st.error("No hay eventos válidos para mostrar.")
        st.stop()

    # Obtener hora inicial de la primera fila de 'comienzo'
    hora_inicio_str = str(df['comienzo'].iloc[0]).strip()
    try:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M:%S")
    except ValueError:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M")

    # Limpieza de datos
    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')
    for col in ['personas', 'acciones', 'mision', 'lugar']:
        df[col] = df[col].fillna("").astype(str)

    # Mostrar el título
    st.markdown("## Programa del evento", unsafe_allow_html=True)

    for i, row in df.iterrows():
        hora_str = hora_actual.strftime("%-H:%M")  # Formato de hora sin ceros a la izquierda
        duracion = str(row['duracion'])[:5] if pd.notnull(row['duracion']) else ""
        contenido = row['contenido']
        lugar = row['lugar']
        personas = row['personas']
        acciones = row['acciones']
        mision = row['mision']

        # HTML para mostrar la información de cada evento
        html = f"""
        <div class="bloque">
            <div class="hora">{hora_str}</div>
            <div class="card">
                <div class="contenido">
                    <div class="titulo">{contenido}</div>
                    <div class="info">
                        {duracion}<br>
                        {lugar}<br>
                        {personas}<br>
                        {acciones}<br>
                        {mision}
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

        # Sumar la duración al horario actual
        if pd.notnull(row['duracion_td']):
            hora_actual += row['duracion_td']
else:
    st.error("No se pudo cargar el CSV.")
