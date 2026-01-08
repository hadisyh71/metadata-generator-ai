import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# CSS UNTUK UI MEWAH & FIX POSISI TOMBOL
st.markdown("""
    <style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* Tombol Utama RUN ENGINE */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }

    /* Container Kartu Langganan */
    .tier-wrapper {
        display: flex; flex-direction: column; height: 100%;
        background: rgba(255,255,255,0.03); padding: 25px; 
        border-radius: 20px; text-align: center; justify-content: space-between;
    }
    
    /* Link Button Custom agar Selalu di Bawah & Berwarna */
    .sub-link {
        display: block; width: 100%; padding: 12px; margin-top: 20px;
        text-decoration: none !important; color: white !important;
        font-weight: bold; border-radius: 12px; transition: 0.3s;
    }
    .sub-link:hover { opacity: 0.8; transform: scale(1.02); }
    
    .bg-stock { border: 1px solid #3B82F6; }
    .btn-stock { background: #3B82F6; }
    
    .bg-sosmed { border: 1px solid #8B5CF6; }
    .btn-sosmed { background: #8B5CF6; }
    
    .bg-full { border: 2px solid #F59E0B; background: rgba(245, 158, 11, 0.05); }
    .btn-full { background: #F59E0B; color: #000 !important; }

    .best-value-tag {
        background: #F59E0B; color: black; font-size: 0.7em; 
        padding: 4px 12px; border-radius: 10px; font-weight: bold;
        position: absolute; top: -15px; left: 50%; transform: translateX(-50%);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI POP-UP PENJELASAN TIER (FIXED POSITION) ---
@st.dialog("💎 Pilih Paket Premium Anda")
def show_subscription_tiers():
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 30px;'>Akses model AI tercepat tanpa gangguan iklan.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="tier-wrapper bg-stock">
                <div>
                    <h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3>
                    <h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1>
                    <div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">
                        ✅ Adobe & Shutterstock<br>✅ SEO Tagging Expert<br>✅ Tanpa Iklan<br>✅ English Language
                    </div>
                </div>
                <a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20STOCK%20(29rb)." class="sub-link btn-stock">Subscribe Stock</a>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="tier-wrapper bg-sosmed">
                <div>
                    <h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3>
                    <h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1>
                    <div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">
                        ✅ IG, TikTok, FB Ads<br>✅ Viral Hook & Hashtags<br>✅ 8+ Pilihan Bahasa<br>✅ Niche Specific
                    </div>
                </div>
                <a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20SOSMED%20(29rb)." class="sub-link btn-sosmed">Subscribe Sosmed</a>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="position: relative; height: 100%;">
                <div class="best-value-tag">BEST VALUE</div>
                <div class="tier-wrapper bg-full">
                    <div>
                        <h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3>
                        <h1 style="margin: 15px 0;">49<span style="font-size: 0.5em;">rb</span></h1>
                        <div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">
                            ✅ Akses Semua Fitur<br>✅ Prioritas Llama 4<br>✅ Unlimited Models<br>✅ Support 24/7
                        </div>
                    </div>
                    <a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20FULL%20(49rb)." class="sub-link btn-full">Subscribe Full Access</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- BAGIAN SIDEBAR & LOGIKA (Sama seperti sebelumnya) ---
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (Token Access)"))
    if st.button("ℹ️ Lihat Manfaat & Harga"): show_subscription_tiers()
    st.divider()
    vendor = st.selectbox("Choose AI Provider:", ("Groq (Llama 4)", "Google (Gemini)", "OpenAI (GPT-4o)"))
    
    final_key, selected_model, access_type = None, None, "Free"
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
            elif user_token: st.error("Invalid Token!")
        except: st.error("Token System Error.")

    st.divider()
    platform = st.selectbox("Target Platform:", ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    specific_niche, custom_info = "", ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        specific_niche = st.selectbox("Content Niche:", ("Traveling", "Food", "Fashion", "Business", "Tech", "Health", "Product Promotion"))
        custom_info = st.text_input("Extra Info (Optional):")

# --- LOGIKA ENGINE & MAIN AREA ---
def run_ai_engine(api_key, provider, model_name, prompt):
    if provider == "Groq (Llama 4)":
        client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    elif provider == "Google (Gemini)":
        genai.configure(api_key=api_key); model = genai.GenerativeModel(model_name); resp = model.generate_content(prompt); return resp.text
    elif provider == "OpenAI (GPT-4o)":
        client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content

st.title("✨ Universal AI Metadata Engine")

if access_mode == "Free (With Ads)":
    with st.container(border=True):
        st.subheader("🚀 Tingkatkan ke Premium")
        st.write("Akses fitur eksklusif tanpa iklan & tanpa ribet input API Key pribadi.")
        if st.button("Lihat Harga & Detail Paket 💎"): show_subscription_tiers()

uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    is_allowed = False
    if access_mode == "Free (With Ads)" or access_type == "Full Access": is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    elif access_type == "Sosmed Only" and platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]: is_allowed = True
    
    if not final_key: st.error("Provide Token or API Key!")
    elif not is_allowed: st.error(f"Paket '{access_type}' tidak mencakup platform ini.")
    elif uploaded_files:
        if access_mode == "Free (With Ads)": time.sleep(2)
        for file in uploaded_files:
            with st.expander(f"Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    if platform in ["Adobe Stock", "Shutterstock"]: prompt = f"Expert Stock SEO for '{file.name}' in English."
                    else: prompt = f"Social Media Expert. Target: {platform}, Niche: {specific_niche}, Lang: {output_lang}. Context: {file.name}. Create viral caption."
                    try:
                        result = run_ai_engine(final_key, vendor, selected_model, prompt)
                        st.text_area("Output:", value=result, height=250, key=f"t_{file.name}")
                    except Exception as e: st.error(f"Error: {e}")
