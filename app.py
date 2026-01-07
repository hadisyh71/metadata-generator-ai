import streamlit as st
from groq import Groq

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="AI Metadata Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS CUSTOM: TAMPILAN GLASSMORPHISM & TEXT AREA PRO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* TEXT AREA YANG LEBIH PRO (Tidak Memanjang) */
    .stTextArea textarea {
        background-color: #161B26;
        color: #E5E7EB;
        border: 1px solid #374151;
        border-radius: 10px;
        font-family: 'Inter', sans-serif; /* Bukan font koding, biar enak dibaca */
        line-height: 1.6;
    }
    .stTextArea textarea:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    /* TOMBOL GRADIEN */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #6366F1 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5);
    }

    /* FILE UPLOADER STYLE */
    [data-testid="stFileUploader"] {
        border: 1px dashed #4B5563;
        border-radius: 12px;
        background-color: rgba(31, 41, 55, 0.3);
    }

    /* HIDE ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA APLIKASI ---

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ System Error: API Key missing in Secrets.")
    st.stop()

# Header
st.title("✨ Enterprise AI Metadata Engine")
st.write("Generate SEO-optimized metadata instantly. Powered by Llama 4.")

# Sidebar
with st.sidebar:
    st.header("CONTROL CENTER")
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock"))
    st.divider()
    st.info(f"Mode: **{platform} Optimization**")
    st.caption("AI Model: Llama 4 Scout (Text-Based)")

# Main Area
uploaded_files = st.file_uploader("Drop assets here to begin processing", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("INITIALIZE PROCESSING ⚡", use_container_width=True):
    if uploaded_files:
        progress_bar = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Gunakan Container biar rapi
            with st.container():
                st.markdown(f"### 📂 Result: {file.name}")
                col1, col2 = st.columns([1, 2], gap="medium")
                
                with col1:
                    st.image(file, use_container_width=True, caption="Asset Preview")
                
                with col2:
                    # Prompt yang sangat spesifik agar outputnya rapi
                    prompt = f"""
                    Role: Stock Photography SEO Expert.
                    Task: Create metadata for image filename '{file.name}'.
                    Platform: {platform}.
                    Language: English Only.
                    
                    Structure the output exactly like this (No intro text):
                    
                    TITLE:
                    [Insert Title Here]
                    
                    KEYWORDS:
                    [Insert Keywords Here]
                    """
                    
                    if platform == "Shutterstock":
                        prompt += """
                        DESCRIPTION:
                        [Insert Description Here]
                        """
                    
                    try:
                        completion = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.4
                        )
                        hasil = completion.choices[0].message.content
                        
                        # TAMPILAN BARU: TEXT AREA (Bukan Code Block)
                        # Ini membuat teks otomatis turun ke bawah (wrap) dan mudah diedit
                        st.text_area(
                            label="✨ AI Generated Metadata (Editable)",
                            value=hasil,
                            height=350, # Tinggi kotak pas agar terlihat semua
                            key=f"res_{file.name}"
                        )
                        
                        # Opsional: Tombol copy mentah di bawahnya jika user butuh
                        with st.expander("📋 View Raw Format (For Copy-Paste)"):
                            st.code(hasil, language="text")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        st.success("All tasks completed successfully!")
    else:
        st.warning("Please upload files first.")
