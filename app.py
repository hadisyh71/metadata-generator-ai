import streamlit as st
from groq import Groq

# 1. SETTING WARNA & TEMA (Harus di paling atas)
st.set_page_config(page_title="AI Stock Metadata Tech", page_icon="🤖", layout="wide")

# CSS untuk memaksa warna Tombol dan Teks menjadi nuansa Tech
st.markdown("""
    <style>
    /* Warna Tombol PROSES */
    .stButton>button {
        background-color: #00f2ff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0px 0px 15px rgba(0, 242, 255, 0.5);
    }
    /* Warna Label di Sidebar */
    [data-testid="stSidebar"] label {
        color: #00f2ff !important;
        font-weight: bold;
    }
    /* Menghilangkan menu Streamlit di atas untuk kesan SaaS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. KONEKSI KE API (Secara Rahasia)
try:
    # Pastikan kamu sudah isi GROQ_API_KEY di Streamlit Cloud > Settings > Secrets
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key tidak ditemukan di Secrets. Selesaikan dulu langkah di Dashboard Streamlit.")
    st.stop()

# 3. TAMPILAN UTAMA
st.title("🤖 AI Stock Metadata Generator")
st.write("Sistem Otomatisasi Metadata - Llama 3.2 Vision Preview")

# 4. SIDEBAR PANEL
with st.sidebar:
    st.header("⚙️ Control Panel")
    platform = st.selectbox(
        "Pilih Target Platform:",
        ("Adobe Stock", "Shutterstock")
    )
    st.divider()
    st.write("Status: **Online** 🟢")
    st.info("Format metadata akan disesuaikan otomatis.")

# 5. UPLOAD & PROSES
uploaded_files = st.file_uploader("Upload Foto Produk (Bisa banyak sekaligus)", 
                                  accept_multiple_files=True, 
                                  type=['png', 'jpg', 'jpeg'])

if st.button("PROSES METADATA SEKARANG 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Hasil Analisis: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(file, use_container_width=True)
                
                with col2:
                    # Logika instruksi AI (Prompt)
                    if platform == "Adobe Stock":
                        prompt = "Analyze image for Adobe Stock. Provide: TITLE (max 70 chars) and 25 KEYWORDS (comma separated)."
                    else:
                        prompt = "Analyze image for Shutterstock. Provide: DESCRIPTION (min 200 chars), 50 KEYWORDS, and METADATA tags."

                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(f"**Format: {platform}**")
                        st.code(hasil, language="text")
                    except Exception as e:
                        st.error(f"Error AI: {e}")
        st.balloons()
    else:
        st.warning("Upload fotonya dulu bosku!")
