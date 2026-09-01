import streamlit as st
import pandas as pd

def init_cart():
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

def add_to_cart(producto, precio):
    st.session_state.carrito.append({"producto": producto, "precio": precio})
    st.toast(f"✅ {producto} agregado al carrito")

def render():
    init_cart()
    st.title("🛒 Pedidos EAFIT")
    
    # Simulación de datos (a reemplazar con GET a Google Sheets)
    datos_menu = pd.DataFrame({
        "Restaurante": ["Bigo's", "Bigo's", "Subway", "Nikkei"],
        "Plato": ["Hamburguesa Sencilla", "Papas Fritas", "Combo del Día", "Sushi Roll"],
        "Precio": [15000, 5000, 18000, 22000],
        "Tiempo Prep (min)": [10, 5, 8, 15],
        "Abierto_Finde": [True, True, False, True]
    })

    # Filtros dinámicos
    with st.expander("🔍 Filtrar Opciones", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_restaurante = st.multiselect("Restaurante", datos_menu["Restaurante"].unique())
        with col2:
            filtro_tiempo = st.slider("Tiempo máximo de espera (min)", 5, 30, 15)
        with col3:
            solo_finde = st.checkbox("Solo abiertos fin de semana")

    # Aplicar filtros
    df_filtrado = datos_menu[datos_menu["Tiempo Prep (min)"] <= filtro_tiempo]
    if filtro_restaurante:
        df_filtrado = df_filtrado[df_filtrado["Restaurante"].isin(filtro_restaurante)]
    if solo_finde:
        df_filtrado = df_filtrado[df_filtrado["Abierto_Finde"] == True]

    # Catálogo
    st.markdown("### Menú Disponible")
    for idx, row in df_filtrado.iterrows():
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.write(f"**{row['Plato']}** ({row['Restaurante']})")
            st.caption(f"⏱️ {row['Tiempo Prep (min)']} min de preparación")
        with c2:
            st.write(f"${row['Precio']:,}")
        with c3:
            st.button("Agregar", key=f"btn_{idx}", on_click=add_to_cart, args=(row['Plato'], row['Precio']))
        st.divider()

    # Módulo de Checkout y Validación de Negocio
    if st.session_state.carrito:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Tu Pedido")
        
        subtotal = sum(item["precio"] for item in st.session_state.carrito)
        recargo_servicio = 1500 # Validando disposición de pago
        total = subtotal + recargo_servicio

        for i, item in enumerate(st.session_state.carrito):
            st.sidebar.text(f"1x {item['producto']} - ${item['precio']:,}")
            
        st.sidebar.markdown(f"**Subtotal:** ${subtotal:,}")
        st.sidebar.markdown(f"**Costo por servicio (App):** ${recargo_servicio:,}")
        st.sidebar.markdown(f"### Total: ${total:,}")

        franja = st.sidebar.time_input("Hora de recogida")
        metodo_pago = st.sidebar.selectbox("Método de Pago", [
            "Descuento por Nómina EAFIT", 
            "Pago con Carné (Saldo)", 
            "Pasarela (Tarjeta/PSE)", 
            "Efectivo en punto"
        ])

        if st.sidebar.button("Pagar y Confirmar Pedido", use_container_width=True):
            # Aquí iría el POST a Google Sheets
            st.sidebar.success("¡Pedido confirmado! El restaurante ya recibió tu comanda.")
            st.session_state.carrito.clear()
            st.rerun()
