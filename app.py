import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Metadata Pro", page_icon="✨", layout="wide")

# 2. CSS FINAL: UI MEWAH & HEADER AMAN (TIDAK DISEMBUNYIKAN)
st.markdown("""
    <style>
    /* --- HANYA SEMBUNYIKAN MENU TITIK TIGA & FOOTER (HEADER TETAP ADA) --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* --- THEME COLORS --- */
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* --- BUTTON STYLING --- */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
    
    /* --- STYLE KHUSUS IKLAN (AD BOX) --- */
    .ad-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #F59E0B; /* Garis Orange Iklan */
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 0.9em;
    }
    .ad-title { color: #F59E0B; font-weight: bold; font-size: 0.8em; margin-bottom: 5px; letter-spacing: 1px; }
    .ad-header-banner {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        padding: 15px; border-radius: 12px; text-align: center; 
        margin-bottom: 25px; color: black; font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    /* --- TIER CARD STYLING --- */
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
    
    /* --- TIER COLORS --- */
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

# 3. FUNGSI POP-UP PENJELASAN TIER
@st.dialog("💎 Pilih Paket Premium Anda")
def show_subscription_tiers():
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 30px;'>Hilangkan Iklan & Akses Server Prioritas.</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="tier-wrapper bg-stock"><div><h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Adobe & Shutterstock<br>✅ No-Ads Experience<br>✅ English Language</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Stock" class="sub-link btn-stock">Subscribe Stock</a></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="tier-wrapper bg-sosmed"><div><h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3><h1 style="margin: 15px 0;">29<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Fitur Viral Sosmed<br>✅ No-Ads Experience<br>✅ 8+ Pilihan Bahasa</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Sosmed" class="sub-link btn-sosmed">Subscribe Sosmed</a></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div style="position: relative; height: 100%;"><div class="best-value-tag">BEST VALUE</div><div class="tier-wrapper bg-full"><div><h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3><h1 style="margin: 15px 0;">49<span style="font-size: 0.5em;">rb</span></h1><div style="text-align: left; font-size: 0.85em; color: #D1D5DB; line-height: 1.8;">✅ Akses Semua Fitur<br>✅ No-Ads Forever<br>✅ Unlimited Models<br>✅ Support 24/7</div></div><a href="mailto:hadisyh71@gmail.com?subject=Beli%20Token%20AI%20Full" class="sub-link btn-full">Subscribe Full Access</a></div></div>""", unsafe_allow_html=True)

# 4. SIDEBAR & KONTROL (TERMASUK IKLAN SIDEBAR)
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
        
        # --- IKLAN 1: SIDEBAR (CONTOH GAMBAR) ---
        st.divider()
        # GANTI LINK DI BAWAH SESUAI KEBUTUHAN ANDA
        st.markdown("""<div class="ad-box"><div class="ad-title">📢 SPONSORED</div>
        <b>Jasa Foto Produk Pro</b><br><small style="color:#D1D5DB;">Bikin foto produkmu auto-laris. Diskon khusus pengguna aplikasi ini!</small><br>
        <a href="#" style="color:#F59E0B; font-weight:bold; text-decoration:none;">Hubungi @HadiCreative →</a></div>""", unsafe_allow_html=True)

    else:
        user_token = st.text_input("Enter Member Token:", type="password")
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                if user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("FULL-"): access_type = "Full Access"
                st.success(f"💎 Premium Active: {access_type}")
                # Mengambil API Key Rahasia dari Secrets
                if "Groq" in vendor: final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif "Google" in vendor: final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif "OpenAI" in vendor: final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token: st.error("Invalid Token!")
        except: st.error("Token System Error.")

    st.divider()
    
    # --- PILIHAN PLATFORM LENGKAP ---
    platform = st.selectbox("Target Platform:", 
        (
            "Adobe Stock", 
            "Shutterstock", 
            "Instagram Caption", 
            "TikTok Script", 
            "YouTube Shorts", 
            "X (Twitter) Thread",
            "Threads Post",
            "LinkedIn Post", 
            "Pinterest Pin", 
            "Facebook Ads",
            "Medium/Blog Intro"
        ))
    
    output_lang = st.selectbox("Output Language:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"))
    
    tone = ""
    specific_niche, custom_info = "", ""
    if platform not in ["Adobe Stock", "Shutterstock"]:
        tone = st.selectbox("Tone of Voice:", ("Viral & Catchy", "Professional", "Casual/Friendly", "Urgent/Sales", "Funny/Humorous", "Inspirational"))
        specific_niche = st.selectbox("Content Niche:", ("Traveling", "Food & Beverage", "Fashion & Beauty", "Business & Tech", "Health & Wellness", "Lifestyle & Vlog", "Product Promotion", "Educational"))
        custom_info = st.text_input("Extra Context (Optional):")

# 5. LOGIKA ENGINE AI
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

# 6. MAIN AREA (TAMPILAN UTAMA & IKLAN HEADER)
st.title("✨ Universal AI Metadata Engine")

# --- IKLAN 2: HEADER BANNER (HANYA MUNCUL JIKA FREE) ---
if access_mode == "Free (Standard)" and access_type == "Free":
    st.markdown("""<div class="ad-header-banner">
    🚀 MAU BEBAS IKLAN & SERVER CEPAT? <br>
    <span style="font-size:0.8em; font-weight:normal;">Upgrade ke Paket FULL hanya 49rb/bulan. Akses semua fitur tanpa ribet!</span>
    </div>""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Assets (Max 10 files per batch)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

# --- IKLAN 3: WARNING AD (DI ATAS TOMBOL RUN) ---
if access_mode == "Free (Standard)" and uploaded_files:
    st.warning("📢 Akun Free memiliki antrean server lebih lama (Low Priority). Gunakan Token Premium untuk proses secepat kilat!")

if st.button("RUN AI GENERATOR 🚀"):
    is_allowed = False
    # Logika Cek Akses Tier
    if access_mode == "Free (Standard)" or access_type == "Full Access": is_allowed = True
    elif access_type == "Stock Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    elif access_type == "Sosmed Only" and platform not in ["Adobe Stock", "Shutterstock"]: is_allowed = True
    
    if not final_key: 
        st.error("Access Denied: Please provide API Key or Premium Token.")
    elif len(uploaded_files) > 10:
        st.warning("Batch limit reached (10 files). Please process in smaller batches.")
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
                    # --- IKLAN 4: IN-RESULT AD (DI DALAM KOTAK HASIL) ---
                    if access_mode == "Free (Standard)":
                        st.markdown("""<div style="font-size: 0.75em; color: #9CA3AF; margin-bottom: 8px; border-bottom: 1px solid #374151; padding-bottom: 5px;">
                        💡 <b>AD:</b> Mau hasil jernih? Beli Preset Lightroom Premium di @HadiCreative</div>""", unsafe_allow_html=True)

                    st.write(f"⏳ Generating metadata...")
                    
                    # --- PROMPT LOGIC LENGKAP ---
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
                    elif platform == "X (Twitter) Thread":
                        prompt = f"""
                        You are a Twitter/X influencer expert. Create a viral THREAD based on this image.
                        Tone: {tone} | Niche: {specific_niche} | Lang: {output_lang}
                        
                        Format strictly:
                        Tweet 1: (Hook that grabs attention)
                        Tweet 2: (Value/Context from image)
                        Tweet 3: (Insight/Tip)
                        Tweet 4: (Call to Action)
                        
                        Context: {custom_info}
                        """
                    else:
                        prompt = f"Social Media Expert. Target: {platform} | Tone: {tone} | Niche: {specific_niche} | Lang: {output_lang}. Extra: {custom_info}. Create viral content based on '{file.name}'."
                    
                    result = run_ai_engine(final_key, vendor, selected_model, prompt)
                    st.text_area("Result:", value=result, height=350, key=f"t_{file.name}")
            
            # --- IKLAN 5: GAP AD (DI ANTARA FILE) ---
            if idx < total - 1:
                if access_mode == "Free (Standard)":
                     st.markdown("""<div style="text-align: center; border: 1px dashed #4B5563; padding: 10px; margin: 15px 0; border-radius: 8px; font-size: 0.8em; color: #D1D5DB;">
                     ✨ <b>PRO TIPS:</b> Lelah copy-paste satu-satu? Paket <b>FULL ACCESS</b> support export ke Excel otomatis!</div>""", unsafe_allow_html=True)
                
                with st.spinner(f"Processing next item... (Free Tier Delay)"):
                    time.sleep(3) # Delay server tetap ada
        
        progress_bar.progress(1.0)
        st.success("✅ Batch Processing Complete!")
        st.balloons()
