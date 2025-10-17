import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cruce de Datos Lost Mary", layout="wide")
st.title("📊 Panel Integral de Puntos de Venta")

st.markdown(
    "Visualización de **Ventas Mensuales**, **Promos Mensuales** y **VGifts** sincronizados desde Google Sheets."
)

# --- Función para leer Google Sheet como Excel ---
@st.cache_data
def cargar_hoja_google(sheet_id, sheet_name=None):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        df = pd.read_excel(url, sheet_name=sheet_name, engine="openpyxl")
        if df is None:
            return pd.DataFrame()
        return df
    except Exception as e:
        st.warning(f"⚠️ Error al cargar hoja {sheet_name or ''} del Sheet {sheet_id}: {e}")
        return pd.DataFrame()

# --- IDs de tus hojas de Google Sheets ---
ID_PROMOS = "17yBlMXh_ux0g8CB2v3sQSjPRKS6Ia3p8PZuojR0PQgk"
ID_VGIFTS = "1op3cZuu7-Nvpe0m_XGDqw1M4PVzoGk4sxwivnhoj4rQ"
ID_VENTAS = "1ejOvvW83sOqnx3pIs-uYVF1-LaHxawG4GkyjXM4o-7g"

# --- Carga de datos ---
promos = cargar_hoja_google(ID_PROMOS, sheet_name=None)
vgifts = cargar_hoja_google(ID_VGIFTS, sheet_name=None)
ventas = cargar_hoja_google(ID_VENTAS, sheet_name=None)

# --- Mostrar en sidebar ---
st.sidebar.header("📁 Dimensiones de los datos cargados")

def mostrar_shape(nombre, df):
    if df is not None and not df.empty:
        st.sidebar.write(f"{nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")
    else:
        st.sidebar.write(f"⚠️ {nombre}: vacío o no cargado")

mostrar_shape("Promos", promos)
mostrar_shape("VGifts", vgifts)
mostrar_shape("Ventas", ventas)

# --- Comprobaciones de vacíos ---
if promos.empty:
    st.warning("⚠️ La hoja de **Promos** está vacía o no pudo cargarse.")
if vgifts.empty:
    st.warning("⚠️ La hoja de **VGifts** está vacía o no pudo cargarse.")
if ventas.empty:
    st.warning("⚠️ La hoja de **Ventas** está vacía o no pudo cargarse.")

# --- Normalización de columnas ---
def normalizar(df):
    if df is None or df.empty:
        return pd.DataFrame()
    df.columns = df.columns.astype(str).str.strip().str.lower()
    return df

promos = normalizar(puntos)
vgifts = normalizar(vgifts)
ventas = normalizar(ventas)
