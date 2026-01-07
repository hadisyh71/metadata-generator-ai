import streamlit as st
from groq import Groq

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="AI Metadata Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS CUSTOM UNTUK TAMPILAN PROFESIONAL "AI GENERATOR"
st.markdown("""
    <style>
    /* Import Font Inter untuk kesan modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* MENGUBAH TOMBOL UTAMA MENJADI GRADIEN */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
        transform: translateY(-2px);
    }

    /* MEMPERCANTIK FILE UPLOADER */
    [data-testid="stFileUploader"] {
        border: 2px dashed #3B82F6;
        border-radius: 12px;
        padding: 20px;
        background-color: rgba(59, 130, 246, 0.05);
    }
    [data-testid="stFileUploader"] section {
        background-color: transparent;
    }

    /* HEADER DAN JUDUL */
    h1 {
        background: linear-gradient(90deg, #F3F4F6 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        border-right: 1px solid #1F2937;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #9CA3AF !important;
        font-weight: 600;
    }

    /* EXPANDER (KARTU HASIL) */
    .streamlit-expanderHeader {
        background-color: #161B26;
        border-radius: 10px;
        border: 1px solid #1F2937;
    }
    
    /* MENYEMBUNYIKAN ELEMEN BAWAAN STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA APLIKASI ---

# Koneksi API Rahasia
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ Critical Error: API Key missing in Secrets.")
    st.stop()

# Header Utama
st.title("✨ Enterprise AI Metadata Engine")
st.write("Generate SEO-optimized metadata for stock photography platforms using Llama 4 Scout.")

# Sidebar
with st.sidebar:
    st.header("CONTROL CENTER")
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock"))
    
    st.divider()
    # Status Indicator
    st.markdown("""
        <div style='background-color: #161B26; padding: 10px; border-radius: 10px; border: 1px solid #1F2937;'>
            <span style='color: #10B981;'>●</span> System Status: <b>Operational</b><br>
            <span style='color: #3B82F6;'>●</span> AI Model: <b>Llama 4 Scout</b><br>
            <span style='color: #8B5CF6;'>●</span> Language: <b>English (US)</b>
        </div>
    """, unsafe_allow_html=True)

# Area Upload
st.subheader("Upload Assets")
uploaded_files = st.file_uploader("Drag and drop photos here (JPG, PNG)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

# Tombol Proses
if st.button("INITIALIZE AI PROCESSING ⚡"):
    if uploaded_files:
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)
        
        for i, file in enumerate(uploaded_files):
            # Update progress bar
            progress_bar.progress((i + 1) / total_files)
            
            with st.expander(f"✅ Analysis Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2], gap="large")
                with col1:
                    st.image(file, use_container_width=True)
                with col2:
                    # Prompt Bahasa Inggris Profesional
                    prompt = f"""
                    ROLE: Act as a Senior SEO Specialist for Stock Photography.
                    TASK: Analyze the image filename '{file.name}' and generate professional metadata for {platform}.
                    REQUIREMENTS:
                    - LANGUAGE: STRICTLY ENGLISH ONLY.
                    """
                    
                    if platform == "Adobe Stock":
                        prompt += """
                        - OUTPUT 1: A concise, descriptive TITLE (max 70 characters, no brand names).
                        - OUTPUT 2: Exactly 30 highly relevant KEYWORDS, comma-separated, ranked by importance.
                        """
                    else:
                        prompt += """
                        - OUTPUT 1: A detailed, storytelling DESCRIPTION (minimum 200 characters).
                        - OUTPUT 2: 50 diverse KEYWORDS (comma-separated).
                        - OUTPUT 3: Suggested category metadata.
                        """
                    
                    prompt += "FINAL OUTPUT FORMAT: Clean text, ready to copy-paste."

                    try:
                        # Menggunakan Llama 4 Scout
                        completion = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.5 # Agar hasil lebih konsisten/profesional
                        )
                        hasil = completion.choices[0].message.content
                        
                        # Tampilan Hasil dalam Kotak Kode
                        st.markdown(f"### 📄 {platform} Metadata Set")
                        st.code(hasil, language="text")
                        
                    except Exception as e:
                        st.error(f"AI Processing Error: {e}")
        
        progress_bar.empty()
        st.success("All assets processed successfully!")
        st.balloons()
    else:
        st.warning("Please upload at least one image asset to begin.")
