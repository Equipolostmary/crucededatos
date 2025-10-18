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
@st.cache_data(ttl=600)
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
    st.image("https://via.placeholder.com/150x50?text=LOGO", width=150)  # Reemplaza con tu logo
with col2:
    st.title("Sistema Corporativo de Consulta de Tiendas")

# Cargar datos
data = load_data()

# Buscador principal
st.subheader("Buscador de Tiendas")
search_term = st.text_input("Ingrese el número de tienda:", placeholder="Ej: 1001")

if search_term:
    # Buscar coincidencias
    result = data[data.iloc[:, 0].astype(str).str.contains(search_term, na=False)]
    
    if not result.empty:
        st.success(f"✅ Se encontró la tienda {search_term}")
        
        # Mostrar datos en formato profesional
        tienda_data = result.iloc[0]
        
        with st.container():
            st.subheader("Datos Generales de la Tienda")
            cols = st.columns(4)
            fields = [
                ("NOTIENDA", "Número de Tienda"),
                ("NOMBRE DE TIENDA", "Nombre"),
                ("TIPO DE TIENDA", "Tipo"),
                ("EMPLEADO", "Empleado"),
                ("AREA", "Área"),
                ("CIUDAD", "Ciudad"),
                ("DIRECCION", "Dirección"),
                ("CP", "Código Postal"),
                ("CORREO", "Correo Electrónico"),
                ("PUNTOS TOTALES", "Puntos Totales"),
                ("VENTA", "Venta"),
                ("PROMOS BM100", "Promociones BM100")
            ]
            
            for idx, (col_name, display_name) in enumerate(fields):
                cols[idx % 4].metric(
                    display_name,
                    tienda_data.get(col_name, "N/A")
                )

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
            with st.expander(f"{mes}"):
                cols = st.columns(len(categorias))
                for idx, cat in enumerate(categorias):
                    cols[idx].metric(
                        cat,
                        tienda_data.get(cat, "N/A")
                    )
    else:
        st.error("❌ No se encontró ninguna tienda con ese número")

else:
    st.info("👆 Ingrese un número de tienda para comenzar la búsqueda")

# Footer corporativo
st.markdown("---")
st.markdown("**Sistema Corporativo** • 2025 • Todos los derechos reservados")
