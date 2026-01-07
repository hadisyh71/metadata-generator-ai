import streamlit as st
from groq import Groq

# Konfigurasi Tema & Judul
st.set_page_config(page_title="AI Stock Metadata", page_icon="📸", layout="wide")

st.title("⚡ AI Stock Metadata Generator")
st.write("Optimalkan foto kamu untuk Adobe Stock & Shutterstock dalam hitungan detik.")

# Sidebar untuk Pengaturan
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Groq API Key", type="password", help="Dapatkan di console.groq.com")
    
    # PILIHAN PLATFORM
    platform = st.selectbox(
        "Pilih Format Platform:",
        ("Adobe Stock (Title & Keywords)", "Shutterstock (Description & Metadata)")
    )
    st.divider()
    st.info("Mode: Llama-3.2 Vision")

# Area Upload
uploaded_files = st.file_uploader("Upload Foto (Bisa banyak sekaligus)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("Generate Metadata 🚀"):
    if not api_key:
        st.error("Silakan masukkan Groq API Key di sidebar!")
    elif uploaded_files:
        client = Groq(api_key=api_key)
        
        for file in uploaded_files:
            with st.expander(f"Hasil untuk: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(file, use_container_width=True)
                
                with col2:
                    st.write(" sedang memproses...")
                    
                    # Logika Prompt berdasarkan Pilihan
                    if "Adobe Stock" in platform:
                        prompt = "Analyze this image and provide: 1. A descriptive Title (max 70 chars). 2. 25-30 Keywords separated by commas. Format: Title: [text] \n Keywords: [text]"
                    else:
                        prompt = "Analyze this image and provide: 1. Detailed Description (min 200 chars). 2. Technical Metadata tags. 3. 50 Keywords separated by commas. Format: Description: [text] \n Metadata: [text] \n Keywords: [text]"

                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(hasil)
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.success("Selesai!")
    else:
        st.warning("Pilih foto terlebih dahulu.")
