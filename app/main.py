from __future__ import annotations

import os
import tempfile
import streamlit as st

from src.pipeline import pdf_to_pptx, PipelineConfig


st.set_page_config(page_title="PDF → PPTX (TFG)", page_icon="📄", layout="centered")

st.title("📄➡️📊 PDF → PPTX (MVP)")
st.caption("Sube un PDF y genera una presentación PPTX básica (1 slide por página).")

uploaded = st.file_uploader("Sube tu PDF", type=["pdf"])

col1, col2 = st.columns(2)
with col1:
    max_pages = st.number_input("Máx. páginas (0 = todas)", min_value=0, value=0, step=1)
with col2:
    bullets_per_slide = st.number_input("Bullets por slide", min_value=3, value=7, step=1)

title = st.text_input("Título de la presentación", value="Presentación generada desde PDF")

generate = st.button("Generar PPTX ✅", type="primary", disabled=(uploaded is None))

if generate and uploaded is not None:
    with st.spinner("Procesando PDF y creando PPTX..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "input.pdf")
            out_path = os.path.join(tmpdir, "output.pptx")

            # Guardar PDF subido
            with open(pdf_path, "wb") as f:
                f.write(uploaded.getbuffer())

            cfg = PipelineConfig(
                max_pages=None if max_pages == 0 else int(max_pages),
                bullets_per_slide=int(bullets_per_slide),
            )

            pdf_to_pptx(pdf_path, out_path, title=title, config=cfg)

            with open(out_path, "rb") as f:
                pptx_bytes = f.read()

    st.success("¡PPTX generado!")
    st.download_button(
        label="⬇️ Descargar PPTX",
        data=pptx_bytes,
        file_name="presentacion_generada.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )