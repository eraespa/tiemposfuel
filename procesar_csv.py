import streamlit as st
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# --- Estilos visuales usando Red Hat ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;700&display=swap');

* {
    font-family: 'Red Hat Display', sans-serif;
}

.bloque {
    margin-bottom: 40px;
    display: flex;
    flex-direction: column;
}

.fila {
    display: flex;
    align-items: baseline;
}

.hora {
    font-size: 48px;
    font-weight: 700;
    width: 80px;
}

.titulo {
    font-size: 24px;
    font-weight: 700;
    margin-left: 12px;
    text-transform: uppercase;
}

.info {
    font-size: 14px;
    margin-left: 92px;
    line-height: 1.1;
}
</style>
""", unsafe_allow_html=True)

# --- Descargar y cargar datos ---
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT28iAUmYbEsRIMQMjNxXU0LKJhyRqOsgUzZ3Ly2BFBfnp6ed8FJL8SYOod5q-BnoXWcUVuJtt6M7as/pub?gid=1605730138&single=true&output=csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))

    # Obtener hora inicial
    hora_inicio_str = str(df['comienzo'].iloc[0]).strip()
    try:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M:%S")
    except ValueError:
        hora_actual = datetime.strptime(hora_inicio_str, "%H:%M")

    # Limpieza
    df['duracion_td'] = pd.to_timedelta(df['duracion'], errors='coerce')
    for col in ['personas', 'acciones', 'mision', 'lugar']:
        df[col] = df[col].fillna("").astype(str)

    # Mostrar contenido
    st.markdown("## Programa del evento", unsafe_allow_html=True)

    for i, row in df.iterrows():
        hora_str = hora_actual.strftime("%-H:%M")
        duracion = str(row['duracion'])[:5] if pd.notnull(row['duracion']) else ""
        contenido = row['contenido']
        lugar = row['lugar']
        personas = row['personas']
        acciones = row['acciones']
        mision = row['mision']

        html = f"""
        <div class="bloque">
            <div class="fila">
                <div class="hora">{hora_str}</div>
                <div class="titulo">{contenido}</div>
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

        # Sumar duración si válida
        if pd.notnull(row['duracion_td']):
            hora_actual += row['duracion_td']
else:
    st.error("No se pudo cargar el CSV.")
