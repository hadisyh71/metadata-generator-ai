import streamlit as st
from groq import Groq

# 1. TEMA DARK MODE & WARNA TECH
st.set_page_config(page_title="AI Stock Metadata Llama 4", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stButton>button {
        background-color: #00f2ff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0px 0px 15px rgba(0, 242, 255, 0.5);
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2 { color: #00f2ff !important; }
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
st.title("🤖 AI Stock Metadata Generator (Llama 4.0)")
st.write("Menggunakan teknologi Llama 4 Scout terbaru untuk optimasi SEO.")

# 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Control Panel")
    platform = st.selectbox("Pilih Target Platform:", ("Adobe Stock", "Shutterstock"))
    st.divider()
    st.write("Model: **Llama 4 Scout** ⚡")

# 5. UPLOAD & PROSES
uploaded_files = st.file_uploader("Upload Foto", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("PROSES METADATA DENGAN LLAMA 4 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Hasil: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(file, use_container_width=True)
                with col2:
                    # PROMPT UNTUK LLAMA 4 (MODEL TEXT)
                    # Kita minta AI menganalisa berdasarkan nama file sebagai context awal
                    prompt = f"Target Platform: {platform}. Berdasarkan gambar dengan nama file '{file.name}', buatkan metadata profesional."
                    if platform == "Adobe Stock":
                        prompt += " Berikan TITLE (max 70 chars) dan 25 KEYWORDS (koma)."
                    else:
                        prompt += " Berikan DESCRIPTION (min 200 chars), 50 KEYWORDS, dan METADATA tags."

                    try:
                        # GANTI KE NAMA MODEL LLAMA 4 SESUAI LOG KAMU
                        completion = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(f"### Output Llama 4")
                        st.code(hasil, language="text")
                    except Exception as e:
                        st.error(f"Error AI: {e}")
        st.balloons()
    else:
        st.warning("Upload fotonya dulu bos!")
