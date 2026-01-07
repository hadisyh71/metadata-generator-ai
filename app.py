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
    st.error("⚠️ API Key not found in Secrets!")
    st.stop()

# 3. HEADER
st.title("🤖 AI Stock Metadata Generator (Llama 4.0)")
st.write("Professional SEO Optimization for Stock Contributors.")

# 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Control Panel")
    platform = st.selectbox("Select Target Platform:", ("Adobe Stock", "Shutterstock"))
    st.divider()
    st.write("Model: **Llama 4 Scout** ⚡")
    st.write("Output Language: **English** 🇬🇧")

# 5. UPLOAD & PROSES
uploaded_files = st.file_uploader("Upload Photos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("PROCESS WITH LLAMA 4 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Result for: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(file, use_container_width=True)
                with col2:
                    # UPDATED PROMPT FOR ENGLISH OUTPUT
                    prompt = f"Act as a Stock Image SEO Expert. Target Platform: {platform}. Based on the filename '{file.name}', generate professional metadata in ENGLISH."
                    if platform == "Adobe Stock":
                        prompt += " Provide: TITLE (max 70 chars) and 25 KEYWORDS (comma separated)."
                    else:
                        prompt += " Provide: DESCRIPTION (min 200 chars), 50 KEYWORDS, and METADATA tags."
                    
                    prompt += " Final instruction: The entire output MUST be in English."

                    try:
                        completion = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        hasil = completion.choices[0].message.content
                        st.markdown(f"### {platform} English Output")
                        st.code(hasil, language="text")
                    except Exception as e:
                        st.error(f"AI Error: {e}")
        st.balloons()
    else:
        st.warning("Please upload some photos first.")
