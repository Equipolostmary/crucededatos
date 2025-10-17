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
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame()
        return df
    except Exception as e:
        st.warning(f"⚠️ Error al cargar hoja {sheet_name or ''} del Sheet {sheet_id}: {e}")
        return pd.DataFrame()  # siempre devuelve un DataFrame vacío

# --- IDs de Google Sheets ---
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

# --- Asegurar columna clave 'no_tienda' para contar promociones ---
def encontrar_columna(df, posibles):
    for c in posibles:
        if c in df.columns:
            return c
    return None

clave_promos = encontrar_columna(promos, ["no.tienda","no tienda","no_tienda","numero de tienda"])
clave_ventas = encontrar_columna(ventas, ["no.tienda","no tienda","no_tienda","numero de tienda"])
clave_vgifts = encontrar_columna(vgifts, ["no.tienda","no tienda","no_tienda","numero de tienda"])

# Renombrar columna clave a 'no_tienda'
for df, clave in [(promos, clave_promos), (ventas, clave_ventas), (vgifts, clave_vgifts)]:
    if df is not None and not df.empty and clave:
        df.rename(columns={clave:"no_tienda"}, inplace=True)

# --- Contador de promociones por tienda ---
if not promos.empty and "no_tienda" in promos.columns:
    contador_promos = promos.groupby("no_tienda").size().reset_index(name="promos_subidas")
else:
    contador_promos = pd.DataFrame(columns=["no_tienda","promos_subidas"])

# --- Mostrar KPIs ---
st.markdown("---")
st.markdown("### 📊 Indicadores rápidos")
col1, col2, col3 = st.columns(3)

with col1:
    total_tiendas = len(pd.concat([promos["no_tienda"], ventas["no_tienda"]], ignore_index=True).unique()) if not promos.empty and not ventas.empty else 0
    st.metric("Total puntos de venta", total_tiendas)
with col2:
    total_promos = contador_promos["promos_subidas"].sum() if not contador_promos.empty else 0
    st.metric("Total promos subidas", total_promos)
with col3:
    puntos_sin_promos = total_tiendas - len(contador_promos) if not contador_promos.empty else total_tiendas
    st.metric("Puntos sin promos", puntos_sin_promos)

# --- Vista previa de contador ---
if not contador_promos.empty:
    st.subheader("Promos subidas por punto de venta")
    st.dataframe(contador_promos.sort_values("promos_subidas", ascending=False), use_container_width=True)
