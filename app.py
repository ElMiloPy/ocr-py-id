import streamlit as st
import base64, requests
from datetime import datetime

st.title("OCR de Cédulas o Pasaportes - Demo")

# 1. Seleccionar imágenes (máximo 2) y previsualizarlas en una fila
uploaded_files = st.file_uploader("Selecciona imágenes (máximo 2)", accept_multiple_files=True, type=['png','jpg','jpeg'])
if uploaded_files:
    if len(uploaded_files) > 2:
        st.warning("Solo se procesarán las primeras 2 imágenes.")
        uploaded_files = uploaded_files[:2]
    with st.expander("Previsualización"):
        cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            cols[i].image(file, caption=file.name, use_container_width=True)

# 2. Llamada al servidor para obtener los datos del OCR
if st.button("Enviar"):
    if uploaded_files:
        images_base64 = [base64.b64encode(file.read()).decode('utf-8') for file in uploaded_files]
        url = "https://radically-inspired-dodo.ngrok-free.app/id-ocr"  # Ajusta la URL según tu entorno
        payload = {"images": images_base64}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        try:
            result = response.json()
        except Exception:
            st.error("Error al decodificar la respuesta del servidor")
            result = {}
        if "text_data" in result:
            st.session_state.ocr_result = result
            st.success("Datos recibidos del servidor")
        else:
            error_msg = result.get("detail", "No se encontraron datos en la respuesta")
            st.error(error_msg)
    else:
        st.warning("Selecciona al menos una imagen.")

# 3. Mostrar el formulario prellenado y, al pulsar "Checked", enviar los datos al endpoint /checked
if "ocr_result" in st.session_state:
    data = st.session_state.ocr_result
    st.subheader("Formulario OCR")
    st.warning("Puedes corregir los datos incorrectos y apretar el boton \"Chequeado\" para mejorar la detección.")
    with st.form("formulario_ocr"):
        st.write("Tipo:", data.get("type", "N/A"))
        form_data = {}
        for key, value in data.get("text_data", {}).items():
            form_data[key] = st.text_input(key, value)
        if st.form_submit_button("Chequeado"):
            payload = {"type": data.get("type", "N/A"), "text_data": form_data}
            url = "https://radically-inspired-dodo.ngrok-free.app/checked"  # Ajusta la URL según tu entorno
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            if response.ok:
                st.success("¡¡Gracias por probar la demo!!")
            else:
                st.error("Error al enviar datos: " + response.text)
