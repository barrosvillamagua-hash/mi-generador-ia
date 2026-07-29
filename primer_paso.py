import streamlit as st
from transformers import pipeline

# Configuración del título de la página web
st.title("🚀 Mi Generador de Contenido con IA Avanzado")
st.write("Crea publicaciones profesionales personalizadas y descárgalas en un clic.")

# --- BARRA LATERAL PARA EL TONO ---
st.sidebar.header("⚙️ Configuración del Post")
tono = st.sidebar.selectbox(
    "Elige el tono de la publicación:",
    ["Profesional y Serio", "Divertido y Cercano", "Llamativo y de Ventas"]
)

# Cargamos el modelo de IA en la memoria
@st.cache_resource
def cargar_modelo():
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

redactor = cargar_modelo()

# Caja de texto para el tema
tema = st.text_input("¿Sobre qué tema quieres la publicación?", placeholder="Ej. Consejos de finanzas, Nueva cafetería...")

# Botón para generar
if st.button("Generar Publicación ✨"):
    if tema:
        with st.spinner("La IA está redactando..."):
            prompt_final = f"Escribe una publicación corta para redes sociales sobre este tema: {tema}. El tono debe ser obligatoriamente {tono}. Responde solo con la publicación."
            mensajes = [{"role": "user", "content": prompt_final}]
            
            # Ejecutamos el modelo
            resultado = redactor(mensajes, max_new_tokens=150, temperature=0.7)
            
            # EXTRACTOR DIRECTO Y SEGURO (Evita el error de índices)
            try:
                # Intentamos extraer el contenido del mensaje directamente
                texto_generado = resultado[0]["generated_text"][-1]["content"]
            except:
                try:
                    # Alternativa si el formato de la lista varía
                    texto_generado = resultado[0]["generated_text"]
                except:
                    # Caso de emergencia si devuelve texto plano
                    texto_generado = str(resultado)
            
            # Guardamos el resultado en la memoria de la página
            st.session_state["post_listo"] = texto_generado
    else:
        st.warning("Por favor, escribe un tema primero.")

# --- RESULTADO, CONTADOR Y BOTÓN DE DESCARGA ---
if "post_listo" in st.session_state:
    st.success("¡Publicación lista!")
    st.text_area("Resultado:", value=st.session_state["post_listo"], height=200)
    
    # 📊 MEJORA: CONTADOR DE PALABRAS Y CARACTERES AUTOMÁTICO
    texto = st.session_state["post_listo"]
    num_palabras = len(texto.split())
    num_caracteres = len(texto)
    st.info(f"📊 **Estadísticas:** {num_palabras} palabras | {num_caracteres} caracteres")
    
    # Botón de descarga del archivo de texto (.txt)
    st.download_button(
        label="📥 Descargar Publicación en Bloque de Notas",
        data=st.session_state["post_listo"],
        file_name="publicacion_ia.txt",
        mime="text/plain"
    )