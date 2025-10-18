import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Consulta de Tiendas",
    page_icon="🛒",
    layout="wide"
)

# Cargar datos desde Google Sheets
@st.cache_resource(ttl=600)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0/export?format=csv"
    try:
        response = requests.get(sheet_url)
        response.raise_for_status()
        data = pd.read_csv(StringIO(response.text))
        return data
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

# Logo y cabecera
col1, col2 = st.columns([1, 4])
with col1:
    # Reemplaza con la URL de tu logo
    st.image("https://via.placeholder.com/150x50?text=LOGO", width=150)
with col2:
    st.title("Sistema Corporativo de Consulta de Tiendas")

# Cargar datos
data = load_data()

# Si no hay datos, mostrar un mensaje y detener la ejecución
if data.empty:
    st.error("No se pudieron cargar los datos. Por favor, revisa la conexión.")
    st.stop()

# Buscador principal
st.subheader("Buscador de Tiendas")
search_term = st.text_input("Ingrese el número de tienda:", placeholder="Ej: 1001")

if search_term:
    # Buscar coincidencias en la primera columna (columna 0)
    result = data[data.iloc[:, 0].astype(str).str.contains(search_term, na=False)]
    
    if not result.empty:
        st.success(f"✅ Se encontró la tienda {search_term}")
        tienda_data = result.iloc[0]
        
        # Mostrar datos generales en una tabla
        st.subheader("Datos Generales de la Tienda")
        # Seleccionar las columnas de datos generales
        general_columns = [
            "NOTIENDA", "NOMBRE DE TIENDA", "TIPO DE TIENDA", "EMPLEADO", 
            "AREA", "CIUDAD", "DIRECCION", "CP", "CORREO", 
            "PUNTOS TOTALES", "VENTA", "PROMOS BM100"
        ]
        # Filtrar las columnas que existen en los datos
        existing_columns = [col for col in general_columns if col in data.columns]
        general_df = tienda_data[existing_columns].to_frame().T
        st.dataframe(general_df, use_container_width=True)
        
        # Datos mensuales
        st.subheader("Datos Mensuales")
        meses_data = {
            'AGOSTO': ['VENTAS', 'PROMOS 3*13'],
            'SEPTIEMBRE': ['VENTAS', 'PROMOS 3*13'],
            'OCTUBRE': ['VENTAS', 'PROMOS 3*2'],
            'NOVIEMBRE': ['VENTAS', 'PROMOS'],
            'DICIEMBRE': ['VENTAS', 'PROMOS', 'FOTOS']
        }
        
        for mes, categorias in meses_data.items():
            # Filtrar las categorías que existen en los datos
            existing_cats = [cat for cat in categorias if cat in data.columns]
            if existing_cats:
                st.write(f"**{mes}**")
                # Crear un dataframe con las categorías existentes
                mes_df = tienda_data[existing_cats].to_frame().T
                st.dataframe(mes_df, use_container_width=True)
    else:
        st.error("❌ No se encontró ninguna tienda con ese número")
else:
    st.info("👆 Ingrese un número de tienda para comenzar la búsqueda")

# Footer corporativo
st.markdown("---")
st.markdown("**Sistema Corporativo** • 2025 • Todos los derechos reservados")
