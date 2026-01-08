import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI

# 1. KONFIGURASI HALAMAN & TEMA PRO
st.set_page_config(page_title="Universal AI Metadata", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
    }
    .status-box {
        background-color: #161B26; border: 1px solid #1F2937;
        padding: 15px; border-radius: 12px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES & MODEL
with st.sidebar:
    st.header("🌐 MULTI-MODEL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (My Own Key)", "Premium (Auto Access)"))
    
    st.divider()
    
    # Pilihan Vendor AI
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key = None
    selected_model = None

    if access_mode == "Free (My Own Key)":
        st.info(f"Using {vendor}. Please provide your API Key.")
        final_key = st.text_input(f"Your {vendor} API Key:", type="password")
        # Daftar model manual untuk user gratis
        if vendor == "Groq (Llama 4)": selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif vendor == "Google (Gemini)": selected_model = "gemini-1.5-flash"
        elif vendor == "OpenAI (GPT-4o)": selected_model = "gpt-4o-mini"
    else:
        member_pass = st.text_input("Member Password:", type="password")
        if member_pass == "MEMBER2026":
            st.success("Premium Active!")
            # Ambil key dari Secrets sesuai vendor
            if vendor == "Groq (Llama 4)":
                final_key = st.secrets["GROQ_API_KEY"]
                selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
            elif vendor == "Google (Gemini)":
                final_key = st.secrets["GEMINI_API_KEY"]
                selected_model = "gemini-1.5-flash"
            elif vendor == "OpenAI (GPT-4o)":
                final_key = st.secrets["OPENAI_API_KEY"]
                selected_model = "gpt-4o"
        elif member_pass:
            st.error("Invalid Password")

# 3. LOGIKA PEMROSESAN MULTI-MODEL
def generate_metadata(api_key, provider, model_name, prompt):
    if provider == "Groq (Llama 4)":
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content
    elif provider == "Google (Gemini)":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content(prompt)
        return resp.text
    elif provider == "OpenAI (GPT-4o)":
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content

# 4. TAMPILAN UTAMA
st.title("✨ Universal AI Metadata Engine")
uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI ENGINE 🚀"):
    if not final_key:
        st.error("API Key or Password Required!")
    elif uploaded_files:
        for file in uploaded_files:
            with st.expander(f"Analysis: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    platform = st.selectbox("Format:", ("Adobe Stock", "Shutterstock"), key=f"p_{file.name}")
                    prompt = f"Expert SEO for {platform}. Create Title & 30 Keywords for image '{file.name}' in English."
                    
                    try:
                        result = generate_metadata(final_key, vendor, selected_model, prompt)
                        st.text_area("Result:", value=result, height=300, key=f"t_{file.name}")
                    except Exception as e:
                        st.error(f"Error: {e}")
