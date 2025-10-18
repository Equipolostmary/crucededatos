import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Consulta de Tiendas", page_icon="🛒", layout="wide")

# Título y logo
st.image("logo.png", width=200)  # Asegúrate de tener el logo en el mismo directorio
st.title("Sistema de Consulta de Tiendas")

# Cargar datos
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1gtk75CVDBdJA-hoxmIBsz2P_iVJ4kahadx1Eja2muj0/export?format=csv"
    data = pd.read_csv(url)
    return data

data = load_data()

# Buscador
st.sidebar.header("Buscador de Tiendas")
numero_tienda = st.sidebar.text_input("Número de Tienda (Columna A):")

if numero_tienda:
    # Buscar la tienda (la columna A se llama 'NOTIENDA' según la imagen)
    # Asegurémonos de que el tipo de dato sea string para comparar
    tienda = data[data['NOTIENDA'].astype(str).str.strip().str.upper() == numero_tienda.strip().upper()]
    
    if not tienda.empty:
        st.success(f"Tienda {numero_tienda} encontrada.")
        # Mostrar los datos de la tienda
        # Transponemos para mostrar cada campo en una fila
        tienda_data = tienda.iloc[0]
        st.subheader("Datos de la Tienda")
        
        # Crear dos columnas para mostrar los datos
        col1, col2 = st.columns(2)
        
        # Dividir los campos en dos grupos
        campos = tienda_data.index.tolist()
        mitad = len(campos) // 2
        
        with col1:
            for campo in campos[:mitad]:
                st.write(f"**{campo}:** {tienda_data[campo]}")
        
        with col2:
            for campo in campos[mitad:]:
                st.write(f"**{campo}:** {tienda_data[campo]}")
    else:
        st.error("Tienda no encontrada. Verifique el número.")
else:
    st.info("Por favor, ingrese un número de tienda en el buscador de la izquierda.")

# También podemos mostrar todas las tiendas si el usuario lo desea
if st.sidebar.checkbox("Mostrar todas las tiendas"):
    st.subheader("Todas las Tiendas")
    st.dataframe(data)
