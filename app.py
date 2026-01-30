import streamlit as st

# ---------- CONFIG PÁGINA ----------
st.set_page_config(
    page_title="TFG · Procesamiento de PDFs",
    page_icon="📄",
    layout="centered"
)

# ---------- ESTILOS CUSTOM ----------
st.markdown("""
<style>
    body {
        background-color: #0f172a;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #9ca3af;
        margin-bottom: 2.5rem;
    }
    .upload-box {
        border: 2px dashed #38bdf8;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        background-color: #020617;
    }
</style>
""", unsafe_allow_html=True)

# ---------- CONTENIDO ----------
st.markdown('<div class="main-title">Procesamiento Inteligente de PDFs</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sube un documento PDF para su análisis automático</div>', unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📎 Arrastra tu PDF aquí o haz clic para seleccionarlo",
    type=["pdf"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FEEDBACK ----------
if uploaded_file is not None:
    st.success(f"✅ PDF cargado correctamente: **{uploaded_file.name}**")
    st.info("ℹ️ El procesamiento se añadirá en próximas versiones.")
else:
    st.caption("Solo se aceptan archivos PDF · Tamaño recomendado < 10MB")
