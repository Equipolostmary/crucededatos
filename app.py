import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Consulta de Tiendas",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para evitar errores de renderizado
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    """Cargar datos desde Google Sheets con manejo robusto de errores"""
    try:
        # URL directa para exportar como CSV
        sheet_id = "1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = pd.read_csv(StringIO(response.text))
        
        # Limpiar nombres de columnas
        data.columns = data.columns.str.strip()
        
        return data
    except Exception as e:
        st.error(f"Error cargando los datos: {str(e)}")
        return pd.DataFrame()

def main():
    # Header con logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏪 Sistema de Consulta de Tiendas")
        st.markdown("---")
    
    # Cargar datos
    with st.spinner("Cargando base de datos..."):
        data = load_data()
    
    if data.empty:
        st.error("No se pudieron cargar los datos. Por favor, verifica la conexión.")
        return
    
    # Buscador
    st.subheader("🔍 Buscar Tienda")
    search_input = st.text_input(
        "Ingrese el número de tienda:",
        placeholder="Ej: 1001, 1002, etc...",
        key="search_input"
    )
    
    if not search_input:
        st.info("Por favor, ingrese un número de tienda para buscar")
        return
    
    # Buscar la tienda
    try:
        # Buscar en la primera columna (columna A)
        result = data[data.iloc[:, 0].astype(str).str.strip() == search_input.strip()]
        
        if result.empty:
            st.error(f"❌ No se encontró la tienda con número: {search_input}")
            return
        
        tienda_info = result.iloc[0]
        st.success(f"✅ Tienda encontrada: {search_input}")
        
        # Mostrar información en pestañas
        tab1, tab2 = st.tabs(["📊 Información General", "📈 Datos Mensuales"])
        
        with tab1:
            mostrar_informacion_general(tienda_info)
        
        with tab2:
            mostrar_datos_mensuales(tienda_info)
            
    except Exception as e:
        st.error(f"Error al procesar la búsqueda: {str(e)}")

def mostrar_informacion_general(tienda_info):
    """Mostrar información general de la tienda"""
    st.subheader("Información General")
    
    # Definir campos a mostrar
    campos = [
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
    
    # Crear dos columnas para mejor distribución
    col1, col2 = st.columns(2)
    
    for i, (campo_db, campo_display) in enumerate(campos):
        valor = tienda_info.get(campo_db, "N/A")
        if pd.isna(valor):
            valor = "N/A"
        
        # Alternar entre columnas
        if i % 2 == 0:
            col1.metric(campo_display, valor)
        else:
            col2.metric(campo_display, valor)

def mostrar_datos_mensuales(tienda_info):
    """Mostrar datos mensuales de ventas y promociones"""
    st.subheader("Datos Mensuales")
    
    # Definir estructura de meses y sus campos
    meses = [
        {
            "nombre": "AGOSTO",
            "campos": ["VENTAS", "PROMOS 3*13"]
        },
        {
            "nombre": "SEPTIEMBRE", 
            "campos": ["VENTAS", "PROMOS 3*13"]
        },
        {
            "nombre": "OCTUBRE",
            "campos": ["VENTAS", "PROMOS 3*2"]
        },
        {
            "nombre": "NOVIEMBRE",
            "campos": ["VENTAS", "PROMOS"]
        },
        {
            "nombre": "DICIEMBRE", 
            "campos": ["VENTAS", "PROMOS", "FOTOS"]
        }
    ]
    
    # Mostrar cada mes en un expander
    for mes in meses:
        with st.expander(f"📅 {mes['nombre']}"):
            cols = st.columns(len(mes['campos']))
            
            for idx, campo in enumerate(mes['campos']):
                valor = tienda_info.get(campo, "N/A")
                if pd.isna(valor):
                    valor = "N/A"
                
                cols[idx].metric(campo, valor)

if __name__ == "__main__":
    main()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Sistema Corporativo • 2025 • Todos los derechos reservados"
        "</div>",
        unsafe_allow_html=True
    )
