import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time

# Configuración mínima de la página - SIN CSS personalizado
st.set_page_config(
    page_title="Sistema de Consulta de Tiendas",
    page_icon="🛒",
    layout="centered"
)

# Desactivar caché problemático
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    """Cargar datos desde Google Sheets"""
    try:
        sheet_id = "1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = pd.read_csv(StringIO(response.text))
        data.columns = data.columns.str.strip()
        
        return data
    except Exception as e:
        return pd.DataFrame()

def main():
    # Header simple
    st.title("🏪 Sistema de Consulta de Tiendas")
    st.markdown("---")
    
    # Cargar datos una sola vez al inicio
    if 'data' not in st.session_state:
        with st.spinner("Cargando base de datos..."):
            st.session_state.data = load_data()
    
    data = st.session_state.data
    
    if data.empty:
        st.error("No se pudieron cargar los datos. Por favor, verifica la conexión.")
        return
    
    # Buscador simple
    st.subheader("Buscar Tienda")
    search_input = st.text_input(
        "Ingrese el número de tienda:",
        placeholder="Ej: 1001, 1002, etc...",
        key="main_search"
    )
    
    if not search_input:
        st.info("Por favor, ingrese un número de tienda para buscar")
        return
    
    # Buscar la tienda
    try:
        # Pequeña pausa para evitar renderizado rápido
        time.sleep(0.1)
        
        # Buscar en la primera columna
        result = data[data.iloc[:, 0].astype(str).str.strip() == search_input.strip()]
        
        if result.empty:
            st.error(f"No se encontró la tienda con número: {search_input}")
            return
        
        tienda_info = result.iloc[0]
        st.success(f"Tienda encontrada: {search_input}")
        
        # Información General - SIN COLUMNAS COMPLEJAS
        st.subheader("Información General")
        
        campos_generales = [
            ("NOTIENDA", "Número de Tienda"),
            ("NOMBRE DE TIENDA", "Nombre de Tienda"), 
            ("TIPO DE TIENDA", "Tipo de Tienda"),
            ("EMPLEADO", "Empleado"),
            ("AREA", "Área"),
            ("CIUDAD", "Ciudad"),
            ("DIRECCION", "Dirección"),
            ("CP", "Código Postal"),
            ("CORREO", "Correo Electrónico"),
            ("PUNTOS TOTALES", "Puntos Totales"),
            ("VENTA", "Ventas"),
            ("PROMOS BM100", "Promociones BM100")
        ]
        
        for campo_db, campo_display in campos_generales:
            valor = tienda_info.get(campo_db, "N/A")
            if pd.isna(valor):
                valor = "N/A"
            st.write(f"**{campo_display}:** {valor}")
        
        st.markdown("---")
        
        # Datos Mensuales - SIN EXPANDERS
        st.subheader("Datos Mensuales")
        
        # Agosto
        st.write("**AGOSTO**")
        col1, col2 = st.columns(2)
        with col1:
            valor = tienda_info.get("VENTAS", "N/A")
            st.metric("VENTAS", valor)
        with col2:
            valor = tienda_info.get("PROMOS 3*13", "N/A")
            st.metric("PROMOS 3*13", valor)
        
        # Septiembre
        st.write("**SEPTIEMBRE**")
        col1, col2 = st.columns(2)
        with col1:
            valor = tienda_info.get("VENTAS", "N/A")
            st.metric("VENTAS", valor)
        with col2:
            valor = tienda_info.get("PROMOS 3*13", "N/A")
            st.metric("PROMOS 3*13", valor)
        
        # Octubre
        st.write("**OCTUBRE**")
        col1, col2 = st.columns(2)
        with col1:
            valor = tienda_info.get("VENTAS", "N/A")
            st.metric("VENTAS", valor)
        with col2:
            valor = tienda_info.get("PROMOS 3*2", "N/A")
            st.metric("PROMOS 3*2", valor)
        
        # Noviembre
        st.write("**NOVIEMBRE**")
        col1, col2 = st.columns(2)
        with col1:
            valor = tienda_info.get("VENTAS", "N/A")
            st.metric("VENTAS", valor)
        with col2:
            valor = tienda_info.get("PROMOS", "N/A")
            st.metric("PROMOS", valor)
        
        # Diciembre
        st.write("**DICIEMBRE**")
        col1, col2, col3 = st.columns(3)
        with col1:
            valor = tienda_info.get("VENTAS", "N/A")
            st.metric("VENTAS", valor)
        with col2:
            valor = tienda_info.get("PROMOS", "N/A")
            st.metric("PROMOS", valor)
        with col3:
            valor = tienda_info.get("FOTOS", "N/A")
            st.metric("FOTOS", valor)
            
    except Exception as e:
        st.error(f"Error al procesar la búsqueda: {str(e)}")

if __name__ == "__main__":
    main()
    
    # Footer simple
    st.markdown("---")
    st.caption("Sistema Corporativo • 2025 • Todos los derechos reservados")
