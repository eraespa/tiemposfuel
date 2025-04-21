
import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# --- Fuente Red Hat (desde Google Fonts) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;700&display=swap');

body {
    font-family: 'Red Hat Display', sans-serif;
}

.bloque {
    font-family: 'Red Hat Display', sans-serif;
    margin-bottom: 50px;
}

.hora {
    font-size: 48px;
    font-weight: 700;
    display: inline-block;
    width: 80px;
}

.titulo {
    font-size: 24px;
    font-weight: 700;
    display: inline-block;
    vertical-align: top;
    margin-left: 10px;
    text-transform: uppercase;
}

.info {
    font-size: 16px;
    margin-left: 90px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- Cargar datos desde el CSV publicado ---
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))

    # Preparar datos
    hora_inicio_str = str(df['comienzo'].iloc[0]).strip()
    try:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M:%S")
    except ValueError:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M")

    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')
    df['personas'] = df['personas'].fillna("")
    df['acciones'] = df['acciones'].fillna("")
    df['mision'] = df['mision'].fillna("")
    df['lugar'] = df['lugar'].fillna("")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Programa del evento", unsafe_allow_html=True)

    for i, row in df.iterrows():
        hora_str = hora_actual.strftime("%-H:%M")
        duracion = str(row['duracion'])[:5]
        lugar = row['lugar']
        contenido = row['contenido']
        personas = row['personas']
        acciones = row['acciones']
        mision = row['mision']

        html = f"""
        <div class="bloque">
            <div>
                <span class="hora">{hora_str}</span>
                <span class="titulo">{contenido}</span>
            </div>
            <div class="info">
                {duracion}<br>
                {lugar}<br>
                {personas}<br>
                {acciones}<br>
                {mision}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

        if pd.notnull(row['duracion_td']):
            hora_actual += row['duracion_td']
else:
    st.error("No se pudo cargar el CSV.")
