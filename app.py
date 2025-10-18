import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configuración mínima
st.set_page_config(page_title="Consulta Tiendas", layout="centered")

# Función simple para cargar datos
def load_data():
    try:
        sheet_id = "1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        response = requests.get(url, timeout=30)
        data = pd.read_csv(StringIO(response.text))
        return data
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

def main():
    st.title("Sistema de Consulta de Tiendas")
    st.write("---")
    
    # Cargar datos
    data = load_data()
    
    if data.empty:
        st.stop()
    
    # Buscador simple
    numero_tienda = st.text_input("Ingrese el número de tienda:")
    
    if not numero_tienda:
        st.info("Ingrese un número de tienda para buscar")
        return
    
    # Buscar
    try:
        # Buscar en la columna A
        result = data[data.iloc[:, 0].astype(str).str.strip() == numero_tienda.strip()]
        
        if result.empty:
            st.error(f"No se encontró la tienda: {numero_tienda}")
            return
        
        tienda = result.iloc[0]
        st.success(f"Tienda encontrada: {numero_tienda}")
        
        # Mostrar datos de forma lineal - SIN COLUMNAS COMPLEJAS
        st.write("### Información General")
        
        campos = [
            "NOTIENDA", "NOMBRE DE TIENDA", "TIPO DE TIENDA", "EMPLEADO",
            "AREA", "CIUDAD", "DIRECCION", "CP", "CORREO", 
            "PUNTOS TOTALES", "VENTA", "PROMOS BM100"
        ]
        
        for campo in campos:
            if campo in data.columns:
                valor = tienda[campo]
                if pd.isna(valor):
                    valor = "N/A"
                st.write(f"**{campo}:** {valor}")
        
        st.write("---")
        st.write("### Datos Mensuales")
        
        # Meses específicos
        meses = [
            ("AGOSTO", ["VENTAS", "PROMOS 3*13"]),
            ("SEPTIEMBRE", ["VENTAS", "PROMOS 3*13"]),
            ("OCTUBRE", ["VENTAS", "PROMOS 3*2"]),
            ("NOVIEMBRE", ["VENTAS", "PROMOS"]),
            ("DICIEMBRE", ["VENTAS", "PROMOS", "FOTOS"])
        ]
        
        for mes, campos_mes in meses:
            st.write(f"**{mes}**")
            for campo in campos_mes:
                if campo in data.columns:
                    valor = tienda[campo]
                    if pd.isna(valor):
                        valor = "N/A"
                    st.write(f"{campo}: {valor}")
            st.write("")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
    st.write("---")
    st.write("Sistema Corporativo • 2025")
