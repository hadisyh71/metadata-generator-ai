import streamlit as st
from groq import Groq

# 1. TEMA DARK MODE & WARNA TECH (Langsung di Kode)
st.set_page_config(page_title="AI Stock Metadata Tech", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    /* Paksa Tema Gelap */
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    
    /* Tombol Cyan Neon */
    .stButton>button {
        background-color: #00f2ff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0px 0px 15px rgba(0, 242, 255, 0.5);
    }
    /* Warna Text Sidebar */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2 {
        color: #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KONEKSI KE API
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key tidak ditemukan di Secrets!")
    st.stop()

# 3. HEADER
st.title("🤖 AI Stock Metadata Generator")
st.write("Sistem Otomatisasi Metadata Profesional")

# 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Control Panel")
    platform = st.selectbox(
        "Pilih Target Platform:",
        ("Adobe Stock", "Shutterstock")
    )
    st.divider()
    st.write("Status: **Online** 🟢")

# 5. UPLOAD & PROSES
uploaded_files = st.file_uploader("Upload Foto", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("PROSES METADATA SEKARANG 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Hasil Analisis: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(file, use_container_width=True)
                with col2:
                    # PROMPT DISESUAIKAN
                    if platform == "Adobe Stock":
                        prompt = "Analyze image for Adobe Stock. Provide TITLE (max 70 chars) and 25 KEYWORDS (comma separated)."
                    else:
                        prompt = "Analyze image for Shutterstock. Provide DESCRIPTION (min 200 chars), 50 KEYWORDS, and METADATA tags."

                    try:
                        # PAKAI MODEL TERBARU: llama-3.2-11b-vision-instant
                        completion = client.chat.completions.create(
                            model="llama-3.2-11b-vision-instant",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(f"### Format: {platform}")
                        st.code(hasil, language="text")
                    except Exception as e:
                        st.error(f"Error AI: {e}")
        st.balloons()
    else:
        st.warning("Upload fotonya dulu bos!")
