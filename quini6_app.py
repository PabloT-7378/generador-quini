import streamlit as st
import random
import json
import os
from datetime import datetime

st.set_page_config(page_title="🎰 Quini 6 Generator", layout="centered")

ARCHIVO = "jugadas.json"

# ---------- Estilos personalizados ----------
st.markdown("""
    <style>
    .jugada {
        background-color: #f0f8ff;
        color: #000;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 18px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }
    .titulo-principal {
        text-align: center;
        color: #2c3e50;
    }
    .guardar-btn {
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Funciones ----------
def cargar_jugadas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar_jugada(jugada):
    jugadas = cargar_jugadas()
    jugadas.append({
        "numeros": jugada,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(ARCHIVO, "w") as f:
        json.dump(jugadas, f, indent=2)

def borrar_jugada(index):
    jugadas = cargar_jugadas()
    if 0 <= index < len(jugadas):
        del jugadas[index]
        with open(ARCHIVO, "w") as f:
            json.dump(jugadas, f, indent=2)

# ---------- Configuración de página ----------
#
st.markdown("<h1 class='titulo-principal'>🎰 Quini 6 - Generador de Números</h1>", unsafe_allow_html=True)

# ---------- Generación de jugadas ----------
cantidad = st.slider("🎯 Elegí cuántas jugadas querés generar", min_value=1, max_value=10, value=1)

if "jugadas_generadas" not in st.session_state:
    st.session_state.jugadas_generadas = []

if st.button("🔄 Generar Jugadas"):
    st.session_state.jugadas_generadas = [sorted(random.sample(range(1, 46), 6)) for _ in range(cantidad)]

# ---------- Mostrar jugadas generadas ----------
if st.session_state.jugadas_generadas:
    st.subheader("🎟️ Jugadas Generadas (No guardadas)")
    for i, jugada in enumerate(st.session_state.jugadas_generadas):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"<div class='jugada'>🎲 {jugada}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("💾", key=f"guardar_{i}", help="Guardar esta jugada"):
                guardar_jugada(jugada)
                st.success(f"✅ Jugada guardada: {jugada}")

# ---------- Jugadas guardadas ----------
st.header("📋 Historial de Jugadas Guardadas")
jugadas_guardadas = cargar_jugadas()

if not jugadas_guardadas:
    st.info("📭 Aún no guardaste ninguna jugada.")
else:
    for idx, j in enumerate(jugadas_guardadas):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"<div class='jugada'>📅 {j['fecha']}<br>🎯 {j['numeros']}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"borrar_{idx}", help="Eliminar esta jugada"):
                borrar_jugada(idx)
                st.rerun()
# ---------- Footer ----------
st.markdown("""
<hr style='margin-top: 50px;'>
<div style='text-align: center; font-size: 14px; color: gray;'>
  © 2025 Pablo Tapia - Todos los derechos reservados.
</div>
""", unsafe_allow_html=True)
