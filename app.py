import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS (Tampilan Profesional & Pop-Up)
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    .tier-card {
        background-color: #161B26; padding: 20px; border-radius: 15px; 
        border: 1px solid #3B82F6; text-align: center; height: 100%;
    }
    .benefit-list { text-align: left; font-size: 0.9em; margin: 15px 0; color: #9CA3AF; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI POP-UP PENJELASAN TIER ---
@st.dialog("💎 Pilih Paket Premium Anda")
def show_subscription_tiers():
    st.write("Dapatkan hasil lebih akurat, tanpa iklan, dan akses model AI tercepat.")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="tier-card">', unsafe_allow_html=True)
        st.subheader("📦 Stock")
        st.title("29rb")
        st.markdown('<div class="benefit-list">✅ Adobe & Shutterstock<br>✅ Tanpa Iklan<br>✅ SEO Optimized<br>✅ English Support</div>', unsafe_allow_html=True)
        st.link_button("Subscribe Stock", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20STOCK%20(29rb).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tier-card" style="border: 2px solid #8B5CF6;">', unsafe_allow_html=True)
        st.subheader("📱 Sosmed")
        st.title("29rb")
        st.markdown('<div class="benefit-list">✅ IG, TikTok, FB<br>✅ Multi-Language<br>✅ Niche Specific<br>✅ Viral Hashtags</div>', unsafe_allow_html=True)
        st.link_button("Subscribe Sosmed", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20SOSMED%20(29rb).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="tier-card">', unsafe_allow_html=True)
        st.subheader("🔥 Full")
        st.title("49rb")
        st.markdown('<div class="benefit-list">✅ Akses Semua Fitur<br>✅ Prioritas Llama 4<br>✅ Unlimited Models<br>✅ Best Value</div>', unsafe_allow_html=True)
        st.link_button("Subscribe Full", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20FULL%20(49rb).")
        st.markdown('</div>', unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES & TIER
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (Token Access)"))
    
    # TOMBOL INFO TIER DI SIDEBAR
    if st.button("ℹ️ Lihat Manfaat & Harga"):
        show_subscription_tiers()
    
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
        user_token = st.text_input("Enter Your Member Token:", type="password")
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                is_premium = True
                if user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("FULL-"): access_type = "Full Access"
                
                st.success(f"💎 Premium Active: {access_type}")
                if vendor == "Groq (Llama 4)": final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)": final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)": final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token: st.error("Invalid or Expired Token!")
        except: st.error("Token System Error.")

    st.divider()
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
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

# BANNER UTAMA UNTUK FREE USER
if access_mode == "Free (With Ads)":
    with st.container(border=True):
        st.subheader("🚀 Tingkatkan Kreativitas Anda ke Level Premium")
        st.write("Hasilkan metadata dan caption viral tanpa iklan, tanpa API Key ribet, dan akses model AI tercanggih.")
        if st.button("Lihat Harga & Detail Paket 💎"):
            show_subscription_tiers()

uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    is_allowed = False
    if access_mode == "Free (With Ads)" or access_type == "Full Access": is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    elif access_type == "Sosmed Only" and platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]: is_allowed = True
    
    if not final_key: st.error("Provide Token or API Key!")
    elif not is_allowed: st.error(f"Maaf, paket '{access_type}' Anda tidak mencakup platform '{platform}'. Silakan upgrade paket!")
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
