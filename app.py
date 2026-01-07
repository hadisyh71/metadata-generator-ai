import streamlit as st
from groq import Groq

# 1. TEMA & KONFIGURASI (Warna Tech)
st.set_page_config(
    page_title="AI Stock Metadata Tech", 
    page_icon="🤖", 
    layout="wide"
)

# Custom CSS untuk nuansa Tech
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #00f2ff;
        color: black;
        border-radius: 10px;
        font-weight: bold;
    }
    .stSelectbox label, .stHeader {
        color: #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEM KEAMANAN API KEY (Mengambil dari Secrets)
# Pastikan kamu sudah isi GROQ_API_KEY di menu Settings > Secrets di Streamlit Cloud
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key tidak ditemukan! Pastikan sudah setting di Dashboard Streamlit > Settings > Secrets.")
    st.stop()

# 3. HEADER
st.title("🤖 AI Stock Metadata Generator")
st.write("Sistem Otomatisasi Metadata berbasis Llama 3.2 Vision.")

# 4. SIDEBAR (Pilihan Platform)
with st.sidebar:
    st.header("⚙️ Control Panel")
    platform = st.selectbox(
        "Pilih Target Platform:",
        ("Adobe Stock", "Shutterstock")
    )
    st.divider()
    st.write("Status: **Online** 🟢")
    st.info("Mode ini otomatis menyesuaikan format judul & keyword spesifik tiap platform.")

# 5. AREA UPLOAD
uploaded_files = st.file_uploader("Upload Foto Produk/Stok (Bisa banyak sekaligus)", 
                                  accept_multiple_files=True, 
                                  type=['png', 'jpg', 'jpeg'])

if st.button("PROSES METADATA SEKARANG 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Hasil Analisis: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(file, use_container_width=True, caption="Preview Image")
                
                with col2:
                    # LOGIKA REVISI DATA (Adobe vs Shutterstock)
                    if platform == "Adobe Stock":
                        prompt = """
                        Analyze this image for Adobe Stock. 
                        Provide:
                        1. Title: Descriptive, max 70 chars, no brands.
                        2. Keywords: 25 comma-separated keywords, ordered by relevance.
                        Format: 
                        TITLE: [text]
                        KEYWORDS: [text]
                        """
                    else:
                        prompt = """
                        Analyze this image for Shutterstock. 
                        Provide:
                        1. Description: Detailed caption, at least 200 chars.
                        2. Keywords: 50 comma-separated keywords.
                        3. Metadata: Technical tags (category, orientation).
                        Format:
                        DESCRIPTION: [text]
                        KEYWORDS: [text]
                        METADATA: [text]
                        """

                    try:
                        # Proses AI
                        completion = client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(f"### Output {platform}")
                        st.code(hasil, language="text") # Pake st.code supaya gampang di-copy user
                    except Exception as e:
                        st.error(f"Gagal memproses gambar ini: {e}")
        st.balloons()
    else:
        st.warning("Silakan upload foto dulu bosku!")
