import streamlit as st

def main():
    # URL de destino
    target_url = "https://elmilopy.github.io/ocr"
    
    # Inserta una etiqueta meta para la redirección automática
    st.markdown(
        f'<meta http-equiv="refresh" content="0; url={target_url}">', 
        unsafe_allow_html=True
    )
    
    # Mensaje alternativo en caso de que la redirección no se active automáticamente
    st.write("Si no eres redireccionado automáticamente, haz clic en [este enlace]({target_url}).")

if __name__ == "__main__":
    main()