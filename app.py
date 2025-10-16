import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Panel de Tiendas", layout="wide")

st.title("📊 Panel General de Puntos de Venta")

# --- Función para cargar Excel ---
@st.cache_data
def cargar_datos(ruta):
    return pd.read_excel(ruta)

# --- Cargar archivos ---
data_dir = "data"

try:
    ventas = cargar_datos(os.path.join(data_dir, "Ventas Mensuales.xlsx"))
    promos = cargar_datos(os.path.join(data_dir, "Promos Mensuales.xlsx"))
    vgifts = cargar_datos(os.path.join(data_dir, "VGifts.xlsx"))
except FileNotFoundError:
    st.error("⚠️ Asegúrate de tener los tres archivos en la carpeta 'data'")
    st.stop()

# --- Normalizar nombres de columnas ---
for df in [ventas, promos, vgifts]:
    df.columns = df.columns.str.strip().str.lower()

# --- Asegurar que la columna A (número de tienda) existe ---
for df in [ventas, promos, vgifts]:
    if df.columns[0] != "número de tienda" and df.columns[0] != "num tienda":
        df.rename(columns={df.columns[0]: "num_tienda"}, inplace=True)

# --- Unir los tres datasets ---
df_final = ventas.merge(promos, on="num_tienda", how="outer", suffixes=("_ventas", "_promos"))
df_final = df_final.merge(vgifts, on="num_tienda", how="outer")

# --- Filtros ---
st.sidebar.header("🔍 Filtros")

buscar = st.sidebar.text_input("Buscar punto o número:")
columnas = df_final.columns.tolist()
zona_col = next((c for c in columnas if "zona" in c.lower()), None)
if zona_col:
    zonas = sorted(df_final[zona_col].dropna().unique())
    zona_sel = st.sidebar.multiselect("Filtrar por zona:", zonas)
    if zona_sel:
        df_final = df_final[df_final[zona_col].isin(zona_sel)]

if buscar:
    df_final = df_final[df_final.apply(lambda row: buscar.lower() in str(row.values).lower(), axis=1)]

# --- Mostrar resultados ---
st.subheader("📍 Tiendas encontradas")
st.dataframe(df_final, use_container_width=True)

# --- Subida de nuevos archivos ---
st.sidebar.header("⬆️ Actualizar datos")
archivo_subido = st.sidebar.file_uploader("Sube un Excel actualizado (.xlsx)", type=["xlsx"])
if archivo_subido:
    nombre = archivo_subido.name
    with open(os.path.join(data_dir, nombre), "wb") as f:
        f.write(archivo_subido.getbuffer())
    st.sidebar.success(f"{nombre} actualizado correctamente. Recarga la página.")
