import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS (Tampilan Profesional & Dark Mode)
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
    .tier-label { font-size: 0.8em; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES, MODEL, & TIER
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (Token Access)"))
    
    st.divider()
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key = None
    selected_model = None
    is_premium = False
    access_type = "Free"

    if access_mode == "Free (With Ads)":
        final_key = st.text_input(f"Your {vendor} API Key:", type="password")
        if vendor == "Groq (Llama 4)": selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif vendor == "Google (Gemini)": selected_model = "gemini-1.5-flash"
        elif vendor == "OpenAI (GPT-4o)": selected_model = "gpt-4o-mini"
    else:
        # SISTEM TOKEN 3 TIER
        user_token = st.text_input("Enter Your Member Token:", type="password")
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                is_premium = True
                # Logika Cek Tier berdasarkan Prefix
                if user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("FULL-"): access_type = "Full Access"
                else: access_type = "Standard Premium"

                st.success(f"💎 Premium Active: {access_type}")
                if vendor == "Groq (Llama 4)": final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)": final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)": final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token:
                st.error("Invalid or Expired Token!")
        except:
            st.error("Token System Error. Check Secrets.")

    st.divider()
    platform = st.selectbox("Target Platform:", 
        ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    
    output_lang = st.selectbox("Output Language:", 
        ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    specific_niche = ""
    custom_info = ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        specific_niche = st.selectbox("Content Niche:", ("Traveling", "Food", "Fashion", "Business", "Tech", "Health", "Product Promotion"))
        custom_info = st.text_input("Extra Info (e.g. Discount 50%, Location):")

# 3. LOGIKA ENGINE AI
def run_ai_engine(api_key, provider, model_name, prompt):
    if provider == "Groq (Llama 4)":
        client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    elif provider == "Google (Gemini)":
        genai.configure(api_key=api_key); model = genai.GenerativeModel(model_name); resp = model.generate_content(prompt); return resp.text
    elif provider == "OpenAI (GPT-4o)":
        client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content

# 4. TAMPILAN UTAMA
st.title("✨ Universal AI Metadata Engine")

# INFO PREMIUM & EMAIL OTOMATIS
if access_mode == "Free (With Ads)":
    st.markdown(f"""
        <div class="ad-container">
            <h3 style="color: #3B82F6; margin-top: 0;">Mau Akses Premium?</h3>
            <p>Pilih paket: <b>Stock (29rb)</b>, <b>Sosmed (29rb)</b>, atau <b>Full (49rb)</b>.</p>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 8px; border: 1px solid #3B82F6; display: inline-block;">
                <p style="margin: 0; font-size: 1.1em;">
                    Email ke: <a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Metadata%20Pro&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Member.%0A%0APaket%20yang%20dipilih:%20(Stock/Sosmed/Full)%0AMohon%20instruksi%20pembayarannya." 
                    style="color: #00f2ff; font-weight: bold; text-decoration: none;">hadisyh71@gmail.com</a>
                </p>
            </div>
            <p style="margin-top: 10px; font-size: 0.8em; color: #6B7280;">Klik email di atas untuk kirim request otomatis.</p>
        </div>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    # VALIDASI TIER
    is_allowed = False
    if access_mode == "Free (With Ads)" or access_type == "Full Access":
        is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]:
        is_allowed = True
    elif access_type == "Sosmed Only" and platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        is_allowed = True
    
    if not final_key:
        st.error("Please provide Token or API Key!")
    elif not is_allowed:
        st.error(f"Maaf, paket '{access_type}' Anda tidak mencakup platform '{platform}'. Silakan upgrade ke Paket Komplit!")
    elif uploaded_files:
        if access_mode == "Free (With Ads)": time.sleep(2)
        for file in uploaded_files:
            with st.expander(f"Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    if platform in ["Adobe Stock", "Shutterstock"]:
                        prompt = f"Expert Stock SEO. Create {platform} metadata for '{file.name}' in English."
                    else:
                        prompt = f"Social Media Expert. Target: {platform} | Niche: {specific_niche} | Lang: {output_lang}. Info: {custom_info}. Create viral caption."
                    
                    try:
                        result = run_ai_engine(final_key, vendor, selected_model, prompt)
                        st.text_area("Output:", value=result, height=250, key=f"t_{file.name}")
                    except Exception as e: st.error(f"Error: {e}")
        st.balloons()
