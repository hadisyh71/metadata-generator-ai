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
    
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }

    .tier-wrapper {
        display: flex; flex-direction: column; height: 100%;
        background: rgba(255,255,255,0.03); padding: 25px; 
        border-radius: 20px; text-align: center; justify-content: space-between;
        min-height: 380px;
    }
    
    .sub-link {
        display: block; width: 100%; padding: 12px; margin-top: auto;
        text-decoration: none !important; color: white !important;
        font-weight: bold; border-radius: 12px; transition: 0.3s;
        text-align: center;
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
        position: absolute; top: -15px; left: 50%; transform: translateX(-50%); z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI POP-UP PENJELASAN TIER ---
@st.dialog("💎 Pilih Paket Premium Anda")
def show_subscription_tiers():
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 30px;'>Akses model AI tercepat tanpa gangguan iklan.</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="tier-wrapper bg-stock"><div><h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Adobe & Shutterstock<br>✅ SEO Tagging Expert<br>✅ Tanpa Iklan<br>✅ English Language</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20STOCK%20(29rb)." class="sub-link btn-stock">Subscribe Stock</a></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="tier-wrapper bg-sosmed"><div><h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ IG, TikTok, FB, YT, In<br>✅ Viral Hook & Hashtags<br>✅ 8+ Pilihan Bahasa<br>✅ Niche & Tone Options</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20SOSMED%20(29rb)." class="sub-link btn-sosmed">Subscribe Sosmed</a></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div style="position: relative; height: 100%;"><div class="best-value-tag">BEST VALUE</div><div class="tier-wrapper bg-full"><div><h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3><h1 style="margin: 15px 0;">49<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Akses Semua Fitur<br>✅ Prioritas Llama 4<br>✅ Unlimited Models<br>✅ Support 24/7</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20FULL%20(49rb)." class="sub-link btn-full">Subscribe Full Access</a></div></div>""", unsafe_allow_html=True)

# --- SIDEBAR & KONTROL ---
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
    platform = st.selectbox("Target Platform:", 
        ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "YouTube Shorts", "LinkedIn Post", "Pinterest Pin", "Facebook Ads"))
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    tone = ""
    specific_niche, custom_info = "", ""
    if platform not in ["Adobe Stock", "Shutterstock"]:
        tone = st.selectbox("Tone of Voice:", ("Viral & Catchy", "Professional", "Casual/Friendly", "Urgent/Sales", "Funny"))
        specific_niche = st.selectbox("Content Niche:", ("Traveling", "Food", "Fashion", "Business/Tech", "Health", "Lifestyle", "Product Promotion"))
        custom_info = st.text_input("Extra Context (Optional):")

# --- LOGIKA ENGINE AI ---
def run_ai_engine(api_key, provider, model_name, prompt):
    try:
        if provider == "Groq (Llama 4)":
            client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
        elif provider == "Google (Gemini)":
            genai.configure(api_key=api_key); model = genai.GenerativeModel(model_name); resp = model.generate_content(prompt); return resp.text
        elif provider == "OpenAI (GPT-4o)":
            client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- MAIN AREA ---
st.title("✨ Universal AI Metadata Engine")

if access_mode == "Free (With Ads)":
    st.info("💡 Tips: Untuk upload banyak file sekaligus, gunakan API Key Premium agar proses lebih cepat.")
    if st.button("Lihat Harga & Detail Paket 💎"): show_subscription_tiers()

uploaded_files = st.file_uploader("Upload Assets (Max 10 disarankan untuk API Free)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    # VALIDASI AKSES
    is_allowed = False
    if access_mode == "Free (With Ads)" or access_type == "Full Access": is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    elif access_type == "Sosmed Only" and platform not in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    
    if not final_key: 
        st.error("Silakan masukkan API Key (Free) atau Token (Premium) di sidebar!")
    elif not is_allowed: 
        st.error(f"Paket '{access_type}' Anda tidak mencakup platform '{platform}'.")
    elif uploaded_files:
        progress_bar = st.progress(0)
        total = len(uploaded_files)
        
        for idx, file in enumerate(uploaded_files):
            # Update progress bar
            progress_bar.progress((idx) / total)
            
            with st.expander(f"Processing: {file.name} ({idx+1}/{total})", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    st.write(f"⏳ Analyzing with {vendor}...")
                    if platform in ["Adobe Stock", "Shutterstock"]:
                        prompt = f"Expert Stock SEO. Create {platform} metadata (Title, Description, 50 Keywords) for '{file.name}' in English. Format: CSV ready."
                    else:
                        prompt = f"Social Media Expert. Target: {platform} | Tone: {tone} | Niche: {specific_niche} | Lang: {output_lang}. Extra: {custom_info}. Create viral content based on '{file.name}'."
                    
                    result = run_ai_engine(final_key, vendor, selected_model, prompt)
                    st.text_area("Result:", value=result, height=250, key=f"t_{file.name}")
            
            # --- JEDA 3 DETIK AGAR API TIDAK LIMIT ---
            # Kita tambahkan jeda jika ini bukan file terakhir
            if idx < total - 1:
                with st.spinner(f"Menunggu 3 detik agar API {vendor} aman..."):
                    time.sleep(3)
        
        # Progress bar penuh di akhir
        progress_bar.progress(1.0)
        st.success("✅ Semua Metadata Berhasil Dibuat!")
        st.balloons()
