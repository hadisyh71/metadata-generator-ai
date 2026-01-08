import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN & TEMA
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS untuk tampilan profesional dan Iklan
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    .ad-container {
        background-color: #161B26; border: 1px dashed #3B82F6;
        padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 25px;
    }
    [data-testid="stSidebar"] { background-color: #161B26; border-right: 1px solid #1F2937; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES & PILIHAN MODEL
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (No Ads)"))
    
    st.divider()
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key = None
    selected_model = None

    if access_mode == "Free (With Ads)":
        st.info(f"Using {vendor}. Please provide your API Key.")
        final_key = st.text_input(f"Your {vendor} API Key:", type="password")
        # Pemilihan model otomatis untuk user gratis
        if vendor == "Groq (Llama 4)": selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif vendor == "Google (Gemini)": selected_model = "gemini-1.5-flash"
        elif vendor == "OpenAI (GPT-4o)": selected_model = "gpt-4o-mini"
    else:
        member_pass = st.text_input("Member Password:", type="password")
        if member_pass == "MEMBER2026":
            st.success("💎 Premium Active!")
            try:
                if vendor == "Groq (Llama 4)":
                    final_key = st.secrets["GROQ_API_KEY"]
                    selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)":
                    final_key = st.secrets["GEMINI_API_KEY"]
                    selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)":
                    final_key = st.secrets["OPENAI_API_KEY"]
                    selected_model = "gpt-4o"
            except:
                st.error("API Key not found in Secrets!")
        elif member_pass:
            st.error("Invalid Password")

    st.divider()
    # DROPDOWN PLATFORM LUAS
    platform = st.selectbox("Target Platform:", 
        ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    
    niche = ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        niche = st.text_input("Describe Niche (e.g., Food, Travel, Tech):")

# 3. LOGIKA ENGINE AI
def run_ai_engine(api_key, provider, model_name, prompt):
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

# Tampilan Iklan Kondisional
if access_mode == "Free (With Ads)":
    st.markdown("""
        <div class="ad-container">
            <h4 style="color: #3B82F6;">🚀 Upgrade to Premium for No Ads</h4>
            <p>Get instant access without providing your own API Key.</p>
            <a href="https://hadisyh.my.id/bayar" style="color: #8B5CF6; font-weight: bold;">Upgrade Now</a>
        </div>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Assets (JPG, PNG)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    if not final_key:
        st.error("Please provide API Key or Member Password in the sidebar!")
    elif uploaded_files:
        if access_mode == "Free (With Ads)":
            with st.spinner("Processing with Ads..."):
                time.sleep(2) # Jeda sedikit agar iklan terlihat
        
        for file in uploaded_files:
            with st.expander(f"Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(file, use_container_width=True)
                with col2:
                    # Dinamis Prompt berdasarkan pilihan Dropdown
                    if platform == "Adobe Stock":
                        prompt = f"Expert Stock SEO. Create Title (70 chars) and 30 Keywords for image '{file.name}' in English."
                    elif platform == "Shutterstock":
                        prompt = f"Expert Stock SEO. Create Description (200 chars) and 50 Tags for image '{file.name}' in English."
                    else:
                        prompt = f"Social Media Expert. Create a viral {platform} for niche '{niche}' based on image '{file.name}'. Include hashtags and CTA. English language."

                    try:
                        result = run_ai_engine(final_key, vendor, selected_model, prompt)
                        st.text_area("Generated Metadata (Editable):", value=result, height=250, key=f"t_{file.name}")
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.balloons()
    else:
        st.warning("Please upload files first.")
