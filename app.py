import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cruce de Datos Lost Mary", layout="wide")
st.title("📊 Panel Integral de Puntos de Venta")

st.markdown(
    "Visualización de **Ventas Mensuales**, **Promos Mensuales** y **VGifts** sincronizados desde Google Sheets."
)

# --- Función segura para leer Google Sheet como Excel ---
@st.cache_data
def cargar_hoja_google(sheet_id, sheet_name=None):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        df = pd.read_excel(url, sheet_name=sheet_name, engine="openpyxl")
        # aseguramos que siempre sea DataFrame
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame()
        return df
    except Exception as e:
        st.warning(f"⚠️ Error al cargar hoja {sheet_name or ''} del Sheet {sheet_id}: {e}")
        return pd.DataFrame()  # siempre devuelve un DataFrame vacío

# --- IDs de tus hojas de Google Sheets ---
ID_PROMOS = "17yBlMXh_ux0g8CB2v3sQSjPRKS6Ia3p8PZuojR0PQgk"
ID_VGIFTS = "1op3cZuu7-Nvpe0m_XGDqw1M4PVzoGk4sxwivnhoj4rQ"
ID_VENTAS = "1ejOvvW83sOqnx3pIs-uYVF1-LaHxawG4GkyjXM4o-7g"

# --- Carga de datos ---
promos = cargar_hoja_google(ID_PROMOS)
vgifts = cargar_hoja_google(ID_VGIFTS)
ventas = cargar_hoja_google(ID_VENTAS)

# --- Función segura para mostrar shapes ---
def mostrar_shape(nombre, df):
    if not isinstance(df, pd.DataFrame):
        st.sidebar.warning(f"{nombre}: no es un DataFrame")
    elif df.empty:
        st.sidebar.info(f"{nombre}: vacío")
    else:
        st.sidebar.write(f"{nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")

st.sidebar.header("📁 Dimensiones de los datos cargados")
mostrar_shape("Promos", promos)
mostrar_shape("VGifts", vgifts)
mostrar_shape("Ventas", ventas)

# --- Comprobaciones de vacíos ---
if isinstance(promos, pd.DataFrame) and promos.empty:
    st.warning("⚠️ La hoja de **Promos** está vacía o no pudo cargarse.")
if isinstance(vgifts, pd.DataFrame) and vgifts.empty:
    st.warning("⚠️ La hoja de **VGifts** está vacía o no pudo cargarse.")
if isinstance(ventas, pd.DataFrame) and ventas.empty:
    st.warning("⚠️ La hoja de **Ventas** está vacía o no pudo cargarse.")

# --- Normalización de columnas ---
def normalizar(df):
    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
    df.columns = df.columns.astype(str).str.strip().str.lower()
    return df

promos = normalizar(promos)
vgifts = normalizar(vgifts)
ventas = normalizar(ventas)

# --- Vista previa opcional ---
st.subheader("Vista previa de los datos")
if not promos.empty:
    st.write("**Promos**", promos.head())
if not vgifts.empty:
    st.write("**VGifts**", vgifts.head())
if not ventas.empty:
    st.write("**Ventas**", ventas.head())
