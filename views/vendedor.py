import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
# Alcances requeridos por la API de Google
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

@st.cache_resource(ttl=60) # Refresca los datos cada 60 segundos
def init_connection():
    # La conexión real buscará las credenciales en .streamlit/secrets.toml
    # Para visualizar la UI de inmediato sin credenciales, usamos un Try-Except
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
        client = gspread.authorize(creds)
        # sheet = client.open("EAFIT_Pedidos_DB")
        return client, True
    except Exception as e:
        return None, False

def render():
    st.title("👨‍🍳 Dashboard de Cocina - Gestión de Comandas")
    client, connected = init_connection()

    if not connected:
        st.warning("⚠️ Ejecutando en Modo Simulación. Configura `secrets.toml` para vincular tu Google Sheet.")

    # --- SIMULACIÓN DE DATOS (Mapeo de tu Google Sheet) ---
    # En producción, esto se lee con: sheet.worksheet("Comandas").get_all_records()
    if 'comandas_db' not in st.session_state:
        st.session_state.comandas_db = pd.DataFrame({
            "ID": ["#001", "#002", "#003"],
            "Cliente": ["Camila R.", "Carlos M.", "Andrés G."],
            "Pedido": ["Combo del Día", "Sushi Roll", "Hamburguesa Sencilla"],
            "Hora Recogida": ["12:15 PM", "12:30 PM", "12:45 PM"],
            "Estado": ["Pendiente", "En Preparación", "Listo"]
        })
    
    if 'inventario_db' not in st.session_state:
        st.session_state.inventario_db = pd.DataFrame({
            "Plato": ["Hamburguesa Sencilla", "Papas Fritas", "Combo del Día", "Sushi Roll"],
            "Disponible": [True, True, True, False]
        })

    # --- TABS PARA ORGANIZAR LA VISTA EN TABLET ---
    tab1, tab2 = st.tabs(["📋 Comandas Activas", "📦 Control de Inventario"])

    with tab1:
        st.subheader("Flujo de Pedidos Digitales")
        st.caption("Los pedidos presenciales se manejan en la caja tradicional.")
        
        # Diseño en Kanban (Columnas)
        col_pend, col_prep, col_listo = st.columns(3)
        
        for idx, row in st.session_state.comandas_db.iterrows():
            # Tarjeta de Comanda
            card_html = f"""
            <div style='border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; background-color: white;'>
                <h4 style='margin-top: 0;'>{row['ID']} - {row['Cliente']}</h4>
                <p style='color: #555; margin-bottom: 5px;'>🛒 {row['Pedido']}</p>
                <p style='font-weight: bold; color: #d93025; margin-bottom: 10px;'>⏱️ Recoger: {row['Hora Recogida']}</p>
            </div>
            """
            
            # Lógica de estados
            if row['Estado'] == "Pendiente":
                with col_pend:
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button("Cocinar 🍳", key=f"prep_{row['ID']}", use_container_width=True):
                        st.session_state.comandas_db.at[idx, 'Estado'] = "En Preparación"
                        # Aquí enviarías la alerta push por Telegram si lo deseas
                        st.rerun()
                        
            elif row['Estado'] == "En Preparación":
                with col_prep:
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button("Marcar Listo ✅", key=f"listo_{row['ID']}", use_container_width=True):
                        st.session_state.comandas_db.at[idx, 'Estado'] = "Listo"
                        st.rerun()
                        
            elif row['Estado'] == "Listo":
                with col_listo:
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button("Entregado 🛍️", key=f"entregado_{row['ID']}", use_container_width=True, type="primary"):
                        st.session_state.comandas_db.drop(idx, inplace=True)
                        st.rerun()

    with tab2:
        st.subheader("Disponibilidad en Tiempo Real")
        st.caption("Apaga los productos agotados para evitar que los usuarios los compren en la app.")
        
        for idx, row in st.session_state.inventario_db.iterrows():
            col_nombre, col_toggle = st.columns([4, 1])
            with col_nombre:
                st.write(f"**{row['Plato']}**")
            with col_toggle:
                # Toggle switch nativo de Streamlit
                disponible = st.toggle("Activo", value=row['Disponible'], key=f"inv_{idx}")
                if disponible != row['Disponible']:
                    st.session_state.inventario_db.at[idx, 'Disponible'] = disponible
                    # Aquí iría el POST a Google Sheets para actualizar la base de datos
                    st.toast(f"Inventario actualizado: {row['Plato']}")
