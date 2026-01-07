import streamlit as st
from groq import Groq

# Tema Wide agar lega
st.set_page_config(page_title="AI Stock Metadata", page_icon="📸", layout="wide")

st.title("⚡ AI Stock Metadata Generator")
st.write("Khusus untuk kontributor Adobe Stock & Shutterstock.")

# Sidebar untuk pengaturan
with st.sidebar:
    st.header("Konfigurasi")
    # Bagian ini nanti bisa kita sembunyikan jika sudah pakai 'Secrets'
    api_key = st.text_input("Masukkan Groq API Key", type="password")
    
    st.divider()
    platform = st.selectbox(
        "Pilih Format Platform:",
        ("Adobe Stock (Title & Keywords)", "Shutterstock (Description & Metadata)")
    )
    st.info("AI menggunakan model Llama-3.2 Vision terbaru.")

# Area Upload
uploaded_files = st.file_uploader("Upload Foto (Bisa banyak)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("Mulai Proses Antrian 🚀"):
    if not api_key:
        st.error("Silakan isi API Key di sidebar dulu!")
    elif uploaded_files:
        client = Groq(api_key=api_key)
        
        for file in uploaded_files:
            # Membuat kotak (card) untuk setiap hasil
            with st.expander(f"Hasil: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(file, use_container_width=True)
                
                with col2:
                    # Instruksi AI berbeda tergantung pilihan platform
                    if "Adobe Stock" in platform:
                        prompt = "Analyze this image. Provide a catchy Title (max 70 chars) and 25 essential SEO keywords separated by commas."
                    else:
                        prompt = "Analyze this image. Provide a detailed Description (min 200 chars) and 50 keywords separated by commas."

                    try:
                        chat_completion = client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.markdown(chat_completion.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Gagal memproses: {e}")
    else:
        st.warning("Pilih foto dulu ya.")
