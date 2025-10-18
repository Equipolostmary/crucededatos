import streamlit as st
import pandas as pd
from gspread_pandas import Spread, Client
from google.oauth2 import service_account

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Lost Mary - Puntos de Venta",
    page_icon="💜",
    layout="wide"
)

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
    }
    .main {
        background-color: #f8f6ff;
        border-radius: 15px;
        padding: 20px;
    }
    .title {
        text-align: center;
        font-size: 38px;
        color: #7a42f4;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 160px;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #d6c4ff;
        padding: 10px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO Y TÍTULO ---
st.image("lost_mary_logo.png", use_column_width=False, width=200)
st.markdown("<div class='title'>📊 Base de Datos de Puntos de Venta</div>", unsafe_allow_html=True)
st.markdown("### Busca una tienda por su número (columna **NO.TIENDA**)")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# Reemplaza con tu archivo JSON de credenciales de servicio
SHEET_NAME = "Base Lost Mary"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0/edit?gid=0"

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = Client(scope=None, creds=credentials)
spreadsheet = Spread(SHEET_NAME, client=client)
df = spreadsheet.sheet_to_df(index=None)

# --- BUSCADOR ---
busqueda = st.text_input("🔍 Introduce el número de tienda:")
if busqueda:
    resultados = df[df["NO.TIENDA"].astype(str).str.contains(busqueda, case=False, na=False)]
    if not resultados.empty:
        st.success(f"Se encontraron {len(resultados)} resultado(s):")
        st.dataframe(resultados, use_container_width=True)
    else:
        st.error("No se encontró ninguna tienda con ese número.")
else:
    st.info("Introduce un número de tienda para comenzar la búsqueda.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#7a42f4;'>© 2025 Lost Mary · App creada con Streamlit</p>",
    unsafe_allow_html=True
)
