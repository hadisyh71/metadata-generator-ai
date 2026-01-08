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
    
    /* Tier Card Styling */
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
    
    .bg-stock { border: 1px solid #3B82F6; } .btn-stock { background: #3B82F6; }
    .bg-sosmed { border: 1px solid #8B5CF6; } .btn-sosmed { background: #8B5CF6; }
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
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 30px;'>Tingkatkan produktivitas dengan akses server prioritas.</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="tier-wrapper bg-stock"><div><h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Adobe & Shutterstock<br>✅ SEO Tagging Expert<br>✅ No-Ads Interface<br>✅ English Language</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20STOCK%20(29rb)." class="sub-link btn-stock">Subscribe Stock</a></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="tier-wrapper bg-sosmed"><div><h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ IG, TikTok, FB, YT, In<br>✅ Viral Hook & Hashtags<br>✅ 8+ Pilihan Bahasa<br>✅ Niche & Tone Options</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20SOSMED%20(29rb)." class="sub-link btn-sosmed">Subscribe Sosmed</a></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div style="position: relative; height: 100%;"><div class="best-value-tag">BEST VALUE</div><div class="tier-wrapper bg-full"><div><h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3><h1 style="margin: 15px 0;">49<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Akses Semua Fitur<br>✅ Prioritas Llama 4<br>✅ Unlimited Models<br>✅ Support 24/7</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full&body=Halo%20Admin,%20saya%20tertarik%20membeli%20Token%20Paket%20FULL%20(49rb)." class="sub-link btn-full">Subscribe Full Access</a></div></div>""", unsafe_allow_html=True)

# --- SIDEBAR & KONTROL ---
with st.sidebar:
    st.header("🌐 AI CONTROL CENTER")
    access_mode = st.radio("Access Mode:", ("Free (Standard)", "Premium (Pro Access)"))
    if st.button("ℹ️ Lihat Manfaat & Harga"): show_subscription_tiers()
    
    st.divider()
    vendor = st.selectbox("Choose AI Model:", ("Groq (Llama 4 - Fast)", "Google (Gemini - Smart)", "OpenAI (GPT-4o - Precise)"))
    
    final_key, selected_model, access_type = None, None, "Free"
    if access_mode == "Free (Standard)":
        final_key = st.text_input(f"Enter {vendor.split()[0]} API Key:", type="password")
        if "Groq" in vendor: selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif "Google" in vendor: selected_model = "gemini-1.5-flash"
        elif "OpenAI" in vendor: selected_model = "gpt-4o-mini"
    else:
        user_token = st.text_input("Enter Member Token:", type="password")
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                if user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("FULL-"): access_type = "Full Access"
                st.success(f"💎 Premium Active: {access_type}")
                # Menggunakan API Key Rahasia Anda
                if "Groq" in vendor: final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif "Google" in vendor: final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif "OpenAI" in vendor: final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
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
        if "Groq" in provider:
            client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
        elif "Google" in provider:
            genai.configure(api_key=api_key); model = genai.GenerativeModel(model_name); resp = model.generate_content(prompt); return resp.text
        elif "OpenAI" in provider:
            client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- MAIN AREA ---
st.title("✨ Universal AI Metadata Engine")

if access_mode == "Free (Standard)":
    st.info("💡 Pro Tips: Upgrade ke Premium untuk upload unlimited dan akses prioritas server tanpa input API Key sendiri.")
    if st.button("Lihat Harga & Detail Paket 💎"): show_subscription_tiers()

uploaded_files = st.file_uploader("Upload Assets (Max 10 files per batch for optimal stability)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    is_allowed = False
    if access_mode == "Free (Standard)" or access_type == "Full Access": is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    elif access_type == "Sosmed Only" and platform not in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    
    if not final_key: 
        st.error("Access Denied: Please provide API Key or Premium Token.")
    elif len(uploaded_files) > 10:
        st.warning("Batch limit reached (10 files). Please process in smaller batches for system stability.")
    elif not is_allowed: 
        st.error(f"Your Plan '{access_type}' does not include '{platform}'. Please upgrade.")
    elif uploaded_files:
        progress_bar = st.progress(0)
        total = len(uploaded_files)
        
        for idx, file in enumerate(uploaded_files):
            progress_bar.progress((idx) / total)
            
            with st.expander(f"Processing: {file.name} ({idx+1}/{total})", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    st.write(f"⏳ Generating metadata...")
                    
                    # --- PROMPT FIX FOR ADOBE STOCK (CLEAN FORMAT) ---
                    if platform in ["Adobe Stock", "Shutterstock"]:
                        prompt = f"""
                        Analyze this image for Stock Photography Metadata.
                        Output strictly in this format ONLY (No intro, no markdown code blocks, just text):
                        
                        Title: [Write a clear, SEO-friendly title]
                        Description: [Write a detailed description min 50 words]
                        Keywords: [List 50 keywords separated by commas]
                        
                        Target: {platform}
                        Image: '{file.name}'
                        """
                    else:
                        prompt = f"Social Media Expert. Target: {platform} | Tone: {tone} | Niche: {specific_niche} | Lang: {output_lang}. Extra: {custom_info}. Create viral content based on '{file.name}'."
                    
                    result = run_ai_engine(final_key, vendor, selected_model, prompt)
                    st.text_area("Result:", value=result, height=350, key=f"t_{file.name}")
            
            if idx < total - 1:
                with st.spinner(f"Processing next item... (Optimizing server load)"):
                    time.sleep(3)
        
        progress_bar.progress(1.0)
        st.success("✅ Batch Processing Complete!")
        st.balloons()
