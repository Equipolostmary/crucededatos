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
        return df
    except Exception as e:
        st.error(f"Error al cargar hoja {sheet_name or ''} del Sheet {sheet_id}: {e}")
        return pd.DataFrame()

# --- IDs de tus hojas de Google Sheets ---
ID_PUNTOS = "17yBlMXh_ux0g8CB2v3sQSjPRKS6Ia3p8PZuojR0PQgk"
ID_VGIFTS = "1op3cZuu7-Nvpe0m_XGDqw1M4PVzoGk4sxwivnhoj4rQ"
ID_VENTAS = "1ejOvvW83sOqnx3pIs-uYVF1-LaHxawG4GkyjXM4o-7g"

# --- Carga de datos ---
puntos = cargar_hoja_google(ID_PUNTOS, sheet_name=None)
vgifts = cargar_hoja_google(ID_VGIFTS, sheet_name=None)
ventas = cargar_hoja_google(ID_VENTAS, sheet_name=None)

# Sidebar: mostrar forma en que se cargaron
st.sidebar.header("📁 Dimensiones de los datos cargados")
st.sidebar.write(f"Puntos: {puntos.shape}")
st.sidebar.write(f"VGifts: {vgifts.shape}")
st.sidebar.write(f"Ventas: {ventas.shape}")

# Si alguna de las hojas es vacía, mostrar advertencia
if puntos.empty:
    st.warning("⚠️ La hoja de **Puntos de venta** está vacía o no pudo cargarse.")
if vgifts.empty:
    st.warning("⚠️ La hoja de **VGifts** está vacía o no pudo cargarse.")
if ventas.empty:
    st.warning("⚠️ La hoja de **Ventas** está vacía o no pudo cargarse.")

# --- Normalización de columnas: hacer todo minúsculas y eliminar espacios extremos ---
def normalizar(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

puntos = normalizar(puntos)
vgifts = normalizar(vgifts)
ventas = normalizar(ventas)

# --- Usar columna común “no.tienda” (o variantes) ---
# A veces la columna puede venir como "no.tienda", "no tienda", "no_tienda", etc.
def asegurar_columna_clave(df, posibles):
    for c in posibles:
        if c in df.columns:
            return c
    return None

clave = asegurar_columna_clave(puntos, ["no.tienda", "no tienda", "no_tienda", "numero de tienda"])
if clave is None:
    st.error("No se encontró la columna clave `numero de tienda` en la hoja de Puntos.")
    st.stop()

# Renombrar clave para todas las hojas si existe
for df in (puntos, vgifts, ventas):
    for c in [clave]:
        if c in df.columns:
            df.rename(columns={c: "no_tienda"}, inplace=True)

# --- Cruzar los datos ---
# Merge puntos + ventas
df_merge = pd.merge(puntos, ventas, on="no_tienda", how="outer", suffixes=("_puntos", "_ventas"))
# Luego unir VGifts
df_merge = pd.merge(df_merge, vgifts, on="no_tienda", how="outer", suffixes=("", "_vgifts"))

st.success("Datos combinados correctamente ✅")

# --- Filtros de interfaz ---
st.header("🔍 Buscar y filtrar puntos de venta")
col1, col2 = st.columns(2)

with col1:
    buscar = st.text_input("🔎 Buscar por número o texto:")
with col2:
    # Si hay columna “area” (o similar), mostrar filtro de área
    posibles_area = [c for c in df_merge.columns if "area" in c]
    area_sel = None
    if posibles_area:
        area = posibles_area[0]
        opciones = sorted(df_merge[area].dropna().unique().tolist())
        area_sel = st.selectbox("Filtrar por área:", ["(Todas)"] + opciones)

# Aplicar filtros
df_filtrado = df_merge.copy()

if buscar:
    mask = df_filtrado.apply(lambda row: row.astype(str).str.contains(buscar, case=False, na=False).any(), axis=1)
    df_filtrado = df_filtrado[mask]

if area_sel and area_sel != "(Todas)":
    df_filtrado = df_filtrado[df_filtrado[area] == area_sel]

st.subheader("📋 Puntos de venta combinados")
st.dataframe(df_filtrado, use_container_width=True)

# --- Indicadores / KPIs simples ---
st.markdown("---")
st.markdown("### 📊 Indicadores rápidos")
colA, colB, colC = st.columns(3)

with colA:
    total = df_merge["no_tienda"].nunique()
    st.metric("Total puntos de venta", total)
with colB:
    # puntos con promociones
    cnt_promos = df_merge[~df_merge.filter(like="promo").isna().all(axis=1)]["no_tienda"].nunique()
    st.metric("Puntos con promos", cnt_promos)
with colC:
    # puntos sin datos de ventas
    cnt_sin_ventas = df_merge[df_merge.filter(like="venta").isna().all(axis=1)]["no_tienda"].nunique()
    st.metric("Sin registro de ventas", cnt_sin_ventas)
