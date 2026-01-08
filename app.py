import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS (Tampilan Profesional)
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES & PILIHAN MODEL
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (Token Access)"))
    
    st.divider()
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key = None
    selected_model = None

    if access_mode == "Free (With Ads)":
        final_key = st.text_input(f"Your {vendor} API Key:", type="password")
        if vendor == "Groq (Llama 4)": selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif vendor == "Google (Gemini)": selected_model = "gemini-1.5-flash"
        elif vendor == "OpenAI (GPT-4o)": selected_model = "gpt-4o-mini"
    else:
        # SISTEM TOKEN UNIK
        user_token = st.text_input("Enter Your Member Token:", type="password")
        
        # Mengambil daftar token yang valid dari Secrets
        try:
            # Kita akan menyimpan tokens di secrets dalam format list/string
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            
            if user_token in valid_tokens and user_token != "":
                st.success("💎 Premium Token Active!")
                if vendor == "Groq (Llama 4)": final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)": final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)": final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token:
                st.error("Invalid or Expired Token!")
        except:
            st.error("Token System Error. Please contact Admin.")

    st.divider()
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    specific_niche = ""
    custom_info = ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        specific_niche = st.selectbox("Pilih Niche Konten:", ("Traveling/Nature", "Food/Culinary", "Fashion/Beauty", "Business/Startup", "Tech/Gadget", "Health/Fitness", "Personal Branding", "Product Promotion"))
        custom_info = st.text_input("Info Tambahan (Opsional):")

# 3. LOGIKA ENGINE AI & TAMPILAN (Sama seperti sebelumnya)
def run_ai_engine(api_key, provider, model_name, prompt):
    if provider == "Groq (Llama 4)":
        client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    elif provider == "Google (Gemini)":
        genai.configure(api_key=api_key); model = genai.GenerativeModel(model_name); resp = model.generate_content(prompt); return resp.text
    elif provider == "OpenAI (GPT-4o)":
        client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content

st.title("✨ Universal AI Metadata Engine")

if access_mode == "Free (With Ads)":
    st.markdown("""<div style="background-color: #161B26; padding: 15px; border: 1px dashed #3B82F6; border-radius: 12px; text-align: center; margin-bottom: 25px;">
        <h4 style="color: #3B82F6;">Mau Akses Premium?</h4>
        <p>Email ke: <b>admin@hadisyh.my.id</b> untuk beli Token Member (Rp 49rb/bulan)</p>
    </div>""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    if not final_key:
        st.error("Provide Token or API Key!")
    elif uploaded_files:
        if access_mode == "Free (With Ads)": time.sleep(2)
        for file in uploaded_files:
            with st.expander(f"Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    if "Stock" in platform or "Shutterstock" in platform:
                        prompt = f"Expert Stock SEO. Create {platform} Title/Description & Keywords for '{file.name}' in English."
                    else:
                        prompt = f"Social Media Expert. Target: {platform} | Niche: {specific_niche} | Language: {output_lang}. Context: {file.name} | Info: {custom_info}. Create viral caption."
                    try:
                        result = run_ai_engine(final_key, vendor, selected_model, prompt)
                        st.text_area(f"Output:", value=result, height=250, key=f"t_{file.name}")
                    except Exception as e: st.error(f"Error: {e}")
