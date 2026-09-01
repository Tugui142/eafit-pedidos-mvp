import streamlit as st
import streamlit.components.v1 as components
from views import comprador, vendedor

# Configuración global de la página
st.set_page_config(
    page_title="EAFIT Pedidos",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección silenciosa del contenedor de Tag Manager para trackear el checkout
components.html(
    """
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-TFLKS522');</script>
    """,
    height=0, width=0
)

# Navegación principal
st.sidebar.image("https://via.placeholder.com/150x50?text=Logo+EAFIT", use_column_width=True)
st.sidebar.title("Navegación")
modulo = st.sidebar.radio("Selecciona tu perfil:", ["Comprador", "Vendedor (Restaurante)"])

if modulo == "Comprador":
    comprador.render()
elif modulo == "Vendedor (Restaurante)":
    vendedor.render()
