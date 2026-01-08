import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS UNTUK UI MEWAH & TOMBOL CTA BERWARNA
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* Tombol Utama RUN ENGINE */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }

    /* Container Iklan/Promo */
    .ad-container {
        background: linear-gradient(145deg, #161B22, #0D1117);
        border: 1px solid #30363D; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 30px; border-left: 5px solid #3B82F6;
    }

    /* Style Khusus Tombol Subscribe agar TIDAK HITAM */
    div.stLinkButton > a {
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 12px !important;
        text-decoration: none !important;
        display: block !important;
    }
    .btn-stock > div.stLinkButton > a { background: #3B82F6 !important; } /* Biru */
    .btn-sosmed > div.stLinkButton > a { background: #8B5CF6 !important; } /* Ungu */
    .btn-full > div.stLinkButton > a { 
        background: #F59E0B !important; 
        color: #000 !important; 
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    } /* Oranye/Emas */

    /* Card di dalam Pop-up */
    .tier-card {
        background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; 
        border: 1px solid #30363D; text-align: center; height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI POP-UP PENJELASAN TIER DENGAN CTA BERWARNA ---
@st.dialog("💎 Pilih Paket Premium Anda")
def show_subscription_tiers():
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 25px;'>Dapatkan hasil instan tanpa iklan dan akses model AI tercepat.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="tier-card" style="border: 1px solid #3B82F6;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #3B82F6; margin-bottom: 0;'>📦 STOCK</h3><h1 style='margin:10px 0;'>29<span style='font-size: 0.5em;'>rb</span></h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8; margin-bottom: 20px;'>✅ Adobe & Shutterstock<br>✅ SEO Tagging Expert<br>✅ Tanpa Iklan<br>✅ English Language</div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-stock">', unsafe_allow_html=True)
        st.link_button("Subscribe Stock", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20STOCK%20(29rb).", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tier-card" style="border: 1px solid #8B5CF6;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #8B5CF6; margin-bottom: 0;'>📱 SOSMED</h3><h1 style='margin:10px 0;'>29<span style='font-size: 0.5em;'>rb</span></h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8; margin-bottom: 20px;'>✅ IG, TikTok, FB Ads<br>✅ Viral Hook & Hashtags<br>✅ 8+ Pilihan Bahasa<br>✅ Niche Specific</div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-sosmed">', unsafe_allow_html=True)
        st.link_button("Subscribe Sosmed", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20SOSMED%20(29rb).", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="tier-card" style="border: 2px solid #F59E0B; position: relative; background: rgba(245, 158, 11, 0.05);">', unsafe_allow_html=True)
        st.markdown('<span style="background: #F59E0B; color: black; font-size: 0.7em; padding: 2px 10px; border-radius: 10px; position: absolute; top: -12px; left: 50%; transform: translateX(-50%); font-weight: bold;">BEST VALUE</span>', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #F59E0B; margin-bottom: 0;'>🔥 FULL</h3><h1 style='margin:10px 0;'>49<span style='font-size: 0.5em;'>rb</span></h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8; margin-bottom: 20px;'>✅ Akses Semua Fitur<br>✅ Prioritas Llama 4<br>✅ Unlimited Models<br>✅ Support 24/7</div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-full">', unsafe_allow_html=True)
        st.link_button("Subscribe Full Access", "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20FULL%20(49rb).", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

# 2. SIDEBAR: KONTROL AKSES
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (Token Access)"))
    
    if st.button("ℹ️ Lihat Manfaat & Harga"):
        show_subscription_tiers()
    
    st.divider()
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key = None
    selected_model = None
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
                if user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("FULL-"): access_type = "Full Access"
                
                st.success(f"💎 Premium Active: {access_type}")
                if vendor == "Groq (Llama 4)": final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)": final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)": final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token: st.error("Invalid or Expired Token!")
        except: st.error("Token System Error. Check Secrets.")

    st.divider()
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    specific_niche = ""
    custom_info = ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        specific_niche = st.selectbox("Content Niche:", ("Traveling", "Food", "Fashion", "Business", "Tech", "Health", "Product Promotion"))
        custom_info = st.text_input("Extra Info (Optional):")

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

if access_mode == "Free (With Ads)":
    st.markdown("""
        <div class="ad-container">
            <h3 style="color: #3B82F6; margin-top: 0;">🚀 Tingkatkan ke Premium</h3>
            <p>Akses fitur eksklusif tanpa iklan & tanpa ribet input API Key pribadi.</p>
        </div>
    """, unsafe_allow_html=True)
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
