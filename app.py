import streamlit as st
import pandas as pd
import base64
from gspread_pandas import Spread, Client
from google.oauth2 import service_account

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Lost Mary - Puntos de Venta",
    page_icon="💜",
    layout="wide"
)

# --- LOGO EMBEBIDO (base64 del logo que me enviaste) ---
lost_mary_logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQCAYAAADGWyb/...recortado...
"""  # Aquí va el base64 completo (lo incluiré si lo deseas con el logo exacto).

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    body { background-color: #ffffff; }
    .main { background-color: #f8f6ff; border-radius: 15px; padding: 20px; }
    .logo-title {
        text-align: center;
        margin-bottom: 30px;
    }
    .logo-title img {
        width: 180px;
    }
    .logo-title h1 {
        color: #7a42f4;
        font-size: 36px;
        margin-top: 10px;
        font-weight: bold;
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

# --- CABECERA CON LOGO Y TÍTULO ---
st.markdown(f"""
    <div class="logo-title">
        <img src="data:image/png;base64,{lost_mary_logo_base64}">
        <h1>Base de Datos de Puntos de Venta</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Busca una tienda por su número (columna **NO.TIENDA**)")

# --- CONEXIÓN CON GOOGLE SHEETS ---
SHEET_NAME = "Base Lost Mary"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0/edit?gid=0"

try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = Client(scope=None, creds=credentials)
    spreadsheet = Spread(SHEET_NAME, client=client)
    df = spreadsheet.sheet_to_df(index=None)
except Exception as e:
    st.error("⚠️ No se pudo conectar con Google Sheets. Revisa el correo de la cuenta de servicio y los permisos de la hoja.")
    st.stop()

# --- BUSCADOR ---
busqueda = st.text_input("🔍 Introduce el número de tienda:")

if busqueda:
    resultados = df[df["NO.TIENDA"].astype(str).str.contains(busqueda.strip(), case=False, na=False)]
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
