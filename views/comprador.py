import streamlit as st
import pandas as pd

def init_cart():
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

def add_to_cart(producto, precio):
    st.session_state.carrito.append({"producto": producto, "precio": precio})
    st.toast(f"✅ Agregaste {producto}", icon="🛒")

def render():
    init_cart()
    
    # Inyección de CSS para simular wireframe / prototipo de media fidelidad
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 6px;
            font-weight: 600;
            background-color: #333333;
            color: white;
            border: 1px solid #222;
        }
        .stButton>button:hover {
            background-color: #555555;
            color: white;
        }
        div[data-testid="stImage"] img {
            border-radius: 8px;
            object-fit: cover;
            filter: grayscale(100%); /* Efecto boceto/escala de grises en imágenes */
        }
        </style>
    """, unsafe_allow_html=True)

    # Cabecera tipo App
    st.subheader("👋 Hola, ¿Qué vas a pedir hoy?")
    st.caption("📍 Entregar en: Campus Universitario")

    st.divider()

    # Base de datos simulada con URLs de imágenes
    datos_menu = pd.DataFrame({
        "Restaurante": ["Nikkei Village", "Frisby", "Subway", "The Corral", "Juan Valdez", "Bigo's", "Nativos"],
        "Plato": ["Sushi Roll 10pz", "Combo Frisby", "Sub del Día", "Hamburguesa Todoterreno", "Latte Frio", "Papas Fritas", "Bowl de Acai"],
        "Precio": [22000, 25000, 18000, 28000, 8500, 5000, 14000],
        "Tiempo Prep (min)": [15, 10, 8, 12, 5, 5, 5],
        "Imagen": [
            "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&q=80",
            "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&q=80",
            "https://images.unsplash.com/photo-1616075677936-391490218731?w=400&q=80",
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80",
            "https://images.unsplash.com/photo-1461023058943-0708e5f23a54?w=400&q=80",
            "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=400&q=80",
            "https://images.unsplash.com/photo-1494597564530-871f2b93ac55?w=400&q=80"
        ]
    })

    st.markdown("### 🏪 Restaurantes Destacados")

    # Renderizado en formato de Tarjetas (Cards) estilo wireframe
    for idx, row in datos_menu.iterrows():
        with st.container():
            col_img, col_info, col_btn = st.columns([1.5, 3, 1.2])
            
            with col_img:
                st.image(row["Imagen"], use_container_width=True)
                
            with col_info:
                st.markdown(f"**{row['Plato']}**")
                st.caption(f"🏪 {row['Restaurante']} • ⭐ 4.8")
                st.caption(f"⏱️ {row['Tiempo Prep (min\")} min")
                
            with col_btn:
                st.write(f"**${row['Precio']:,}**")
                st.button("Agregar", key=f"btn_{idx}", on_click=add_to_cart, args=(row['Plato'], row['Precio']), use_container_width=True)
        st.markdown("---")

    # Módulo de Checkout Flotante (Sidebar)
    if st.session_state.carrito:
        st.sidebar.markdown("### 🛒 Tu Canasta")
        
        subtotal = sum(item["precio"] for item in st.session_state.carrito)
        recargo_servicio = 1500 
        total = subtotal + recargo_servicio

        for i, item in enumerate(st.session_state.carrito):
            col_item, col_price = st.sidebar.columns([3, 1])
            col_item.text(f"1x {item['producto']}")
            col_price.text(f"${item['precio']:,}")
            
        st.sidebar.divider()
        st.sidebar.markdown(f"Costo de productos: **${subtotal:,}**")
        st.sidebar.markdown(f"Tarifa de servicio: **${recargo_servicio:,}**")
        st.sidebar.subheader(f"Total: ${total:,}")

        franja = st.sidebar.time_input("🕐 ¿A qué hora pasas?")
        metodo_pago = st.sidebar.selectbox("💳 Método de Pago", [
            "Descuento Nómina EAFIT", 
            "Saldo Carné", 
            "Apple Pay / Tarjeta", 
            "Efectivo"
        ])

        if st.sidebar.button("Hacer Pedido", use_container_width=True):
            st.sidebar.success("🎉 ¡Tu pedido está en camino a la cocina!")
            st.session_state.carrito.clear()
            st.rerun()
