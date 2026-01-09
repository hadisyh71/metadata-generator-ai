import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Universal AI Control Center",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS & STYLING (TAMPILAN MEWAH)
# ==========================================
st.markdown("""
    <style>
    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* MAIN THEME COLORS */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* BUTTON STYLING (GRADIENT) */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        width: 100%;
        padding: 10px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        color: black !important;
        font-weight: bold;
    }

    /* ADVERTISING BOX (SIDEBAR) */
    .ad-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #F59E0B;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 0.9em;
    }
    
    /* HEADER BANNER (FREE USER) */
    .ad-header-banner {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        color: black;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    /* PRICING CARD STYLING */
    .tier-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        justify-content: space-between;
        min-height: 480px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sub-link {
        display: block;
        width: 100%;
        padding: 12px;
        margin-top: auto;
        text-decoration: none !important;
        color: white !important;
        font-weight: bold;
        border-radius: 12px;
        transition: 0.3s;
        text-align: center;
        font-size: 0.9em;
    }
    
    /* TIER COLORS */
    .bg-stock { border-top: 4px solid #3B82F6; }
    .btn-stock { background: #3B82F6; }
    
    .bg-sosmed { border-top: 4px solid #8B5CF6; }
    .btn-sosmed { background: #8B5CF6; }
    
    .bg-prompt { border-top: 4px solid #10B981; }
    .btn-prompt { background: #10B981; }
    
    .bg-full { 
        border: 2px solid #F59E0B; 
        background: rgba(245, 158, 11, 0.05); 
    }
    .btn-full { 
        background: #F59E0B; 
        color: #000 !important; 
    }
    
    .best-value-tag {
        background: #F59E0B;
        color: black;
        font-size: 0.7em;
        padding: 4px 12px;
        border-radius: 10px;
        font-weight: bold;
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
    }
    
    /* TEXT UTILITIES */
    h3 { font-size: 1.1em !important; }
    .desc-text {
        font-size: 0.8em;
        color: #D1D5DB;
        line-height: 1.6;
        text-align: left;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. KAMUS BAHASA (LANGUAGE DICTIONARY) - EXPANDED
# ==========================================
with st.sidebar:
    app_lang = st.radio("Language / Bahasa:", ("🇮🇩 Indonesia", "🌎 English (Global)"), horizontal=True)

if app_lang == "🇮🇩 Indonesia":
    t = {
        # General UI
        "tab1": "📸 Metadata Stok & Sosmed", "tab2": "🎨 AI Prompt Generator",
        "ctrl_title": "🌐 PUSAT KONTROL", "acc_mode": "Mode Akses:", "btn_price": "ℹ️ Lihat Pilihan Paket",
        "title_main": "✨ Universal AI Control Center",
        "run_btn": "JALANKAN 🚀",
        "process_txt": "Sedang memproses...",
        "success_txt": "✅ Selesai!",
        
        # Advertising Texts
        "ad_sidebar_title": "📢 SPONSOR",
        "ad_sidebar_text": "<b>Jasa Foto Produk Pro</b><br><small style='color:#D1D5DB;'>Bikin produkmu auto-laris. Diskon khusus user aplikasi!</small>",
        "ad_sidebar_btn": "Hubungi via Email →",
        "ad_header_text": "🚀 <b>MAU FITUR SULTAN?</b><br><span style='font-size:0.8em;'>Upgrade ke Paket FULL hanya 49rb! Akses Metadata + Prompt Generator.</span>",
        "ad_warning": "📢 Akun Free antrean server lebih lama (Low Priority).",
        
        # Error Messages (Localized)
        "err_vendor": "⚠️ Model ini belum tersedia (Coming Soon).",
        "err_premium_coming_soon": "⚠️ Maaf, Server Premium untuk model ini sedang dalam maintenance (Coming Soon). Mohon gunakan Groq (Llama 4) atau gunakan API Key sendiri di Mode Free.",
        "err_api_req": "API Key / Token Wajib Diisi!",
        "err_idea_req": "Mohon isi ide konten Anda terlebih dahulu.",
        "err_plan": "Paket '{type}' Anda tidak mencakup '{plat}'. Silakan Upgrade.",
        "lbl_enter_api": "Masukkan API Key",
        "help_api": "Dapatkan API Key di dashboard provider terkait.",
        
        # Prompt Generator Specific
        "pg_mode": "Pilih Mode:",
        "pg_idea": "Ide Dasar:",
        "pg_placeholder": "Contoh: Kucing cyberpunk naik motor di Jakarta...",
        "pg_style": "Gaya Visual:",
        "pg_target": "Target AI:",
        "pg_ratio": "Rasio:",
        "pg_btn": "GENERATE MANTRA AJAIB ✨",
        "pg_free_info": "🔓 **Mode Gratis:** Upgrade ke **PROMPT/FULL Access** untuk fitur 'Auto-Enhance' & 'Award Winning Style'.",
        "pg_upsell": "💡 <a href='mailto:hadisyh71@gmail.com'>Beli Token PROMPT Only (29rb)</a> untuk hasil lebih stabil.",
        
        # Pricing Labels
        "p_stock_p": "29rb", "p_sosmed_p": "29rb", "p_prompt_p": "29rb", "p_full_p": "49rb", "p_btn": "Pilih Paket",
        "p_link_full": "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20Full%20(IDR)",
        
        # Pricing Descriptions
        "d_stock": "✅ <b>Optimasi Adobe Stock</b><br>✅ Generator 50 Keyword<br>✅ Auto Title & Deskripsi<br>✅ Format CSV Ready<br>🚫 Tanpa Iklan",
        "d_sosmed": "✅ <b>Viral Hook Generator</b><br>✅ Thread Twitter Otomatis<br>✅ Caption IG/TikTok<br>✅ Multi-Bahasa<br>🚫 Tanpa Iklan",
        "d_prompt": "✅ <b>Midjourney & Video AI</b><br>✅ Auto Negative Prompt<br>✅ Style Preset (Cinematic)<br>✅ Parameter Teknis<br>🚫 Tanpa Iklan",
        "d_full": "🔥 <b>SEMUA FITUR (3 in 1)</b><br>✅ Akses Stok + Sosmed + Prompt<br>⚡ <b>Prioritas Server (Cepat)</b><br>✅ Support 24/7<br>✅ Early Access Fitur Baru"
    }
else:
    # English (Default Global)
    t = {
        # General UI
        "tab1": "📸 Metadata Engine", "tab2": "🎨 AI Prompt Architect",
        "ctrl_title": "🌐 CONTROL CENTER", "acc_mode": "Access Mode:", "btn_price": "ℹ️ View Pricing",
        "title_main": "✨ Universal AI Control Center",
        "run_btn": "RUN ENGINE 🚀",
        "process_txt": "Generating metadata...",
        "success_txt": "✅ Batch Processing Complete!",
        
        # Advertising Texts
        "ad_sidebar_title": "📢 SPONSORED",
        "ad_sidebar_text": "<b>Professional Photo Services</b><br><small style='color:#D1D5DB;'>High-end photography for your business.</small>",
        "ad_sidebar_btn": "Contact for Quote →",
        "ad_header_text": "🚀 <b>UNLOCK PRO FEATURES?</b><br><span style='font-size:0.8em;'>Get FULL Access for only $9/mo! Metadata + Prompt Tools included.</span>",
        "ad_warning": "📢 Free Tier has lower server priority. Upgrade for lightning speed.",
        
        # Error Messages (Localized)
        "err_vendor": "⚠️ This model is Coming Soon.",
        "err_premium_coming_soon": "⚠️ Premium Server for this model is under maintenance (Coming Soon). Please use Groq (Llama 4) or use your own Key in Free Mode.",
        "err_api_req": "API Key / Token Required!",
        "err_idea_req": "Please enter your content idea first.",
        "err_plan": "Your Plan '{type}' does not include '{plat}'. Please Upgrade.",
        "lbl_enter_api": "Enter API Key",
        "help_api": "Get your API Key from the provider dashboard.",
        
        # Prompt Generator Specific
        "pg_mode": "Select Mode:",
        "pg_idea": "Basic Concept:",
        "pg_placeholder": "Example: A cyberpunk cat riding a motorcycle in Jakarta...",
        "pg_style": "Visual Style:",
        "pg_target": "Target AI:",
        "pg_ratio": "Aspect Ratio:",
        "pg_btn": "GENERATE MAGIC PROMPT ✨",
        "pg_free_info": "🔓 **Free Mode:** Upgrade to **PROMPT/FULL Access** for 'Auto-Enhance' & 'Award Winning Style' features.",
        "pg_upsell": "💡 <a href='mailto:hadisyh71@gmail.com'>Buy PROMPT Only Token ($5)</a> for stable results.",
        
        # Pricing Labels
        "p_stock_p": "$5", "p_sosmed_p": "$5", "p_prompt_p": "$5", "p_full_p": "$9", "p_btn": "Subscribe",
        "p_link_full": "mailto:hadisyh71@gmail.com?subject=Buy%20Full%20Token%20(USD)",
        
        # Pricing Descriptions
        "d_stock": "✅ <b>Adobe Stock Optimized</b><br>✅ 50 Keywords Generator<br>✅ SEO Title & Desc<br>✅ Clean Format<br>🚫 No Ads Experience",
        "d_sosmed": "✅ <b>Viral Scripts & Hooks</b><br>✅ Twitter Thread Maker<br>✅ IG/TikTok Captions<br>✅ Multi-Language Output<br>🚫 No Ads Experience",
        "d_prompt": "✅ <b>Pro AI Prompts</b><br>✅ Auto Negative Prompt<br>✅ Video AI Camera Moves<br>✅ Midjourney Parameters<br>🚫 No Ads Experience",
        "d_full": "🔥 <b>ALL FEATURES (3 in 1)</b><br>✅ Stock + Sosmed + Prompt<br>⚡ <b>Priority Server (Fast)</b><br>✅ 24/7 Support<br>✅ Unlimited Usage"
    }

# ==========================================
# 4. FUNGSI POP-UP PRICING (4 KOLOM)
# ==========================================
@st.dialog("💎 Choose Your Power")
def show_subscription_tiers():
    st.markdown(f"<p style='text-align: center; color: #9CA3AF;'>Select specific tools or get the full bundle.</p>", unsafe_allow_html=True)
    
    # Grid Layout 4 Kolom
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""<div class="tier-wrapper bg-stock"><div><h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3><h1 style="margin: 10px 0;">{t['p_stock_p']}</h1><div class="desc-text">{t['d_stock']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-stock">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="tier-wrapper bg-sosmed"><div><h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3><h1 style="margin: 10px 0;">{t['p_sosmed_p']}</h1><div class="desc-text">{t['d_sosmed']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-sosmed">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="tier-wrapper bg-prompt"><div><h3 style="color: #10B981; margin: 0;">🎨 PROMPT</h3><h1 style="margin: 10px 0;">{t['p_prompt_p']}</h1><div class="desc-text">{t['d_prompt']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-prompt">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div style="position: relative; height: 100%;"><div class="best-value-tag">BEST VALUE</div><div class="tier-wrapper bg-full"><div><h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3><h1 style="margin: 10px 0;">{t['p_full_p']}</h1><div class="desc-text">{t['d_full']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-full">{t['p_btn']}</a></div></div>""", unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR LOGIC (CONTROL CENTER)
# ==========================================
with st.sidebar:
    st.header(t['ctrl_title'])
    
    # --- ACCESS MODE ---
    access_mode = st.radio(t['acc_mode'], ("Free (Standard)", "Premium (Pro Access)"))
    
    if st.button(t['btn_price']):
        show_subscription_tiers()
    
    st.divider()
    
    # --- AI ENGINE SELECTION (UNLOCKED ALL) ---
    vendor = st.selectbox("AI Engine (Model):", (
        "Groq (Llama 4 - Fast)", 
        "Google (Gemini - Smart)", 
        "OpenAI (GPT-4o - Precise)"
    ))
    
    final_key = None
    selected_model = None
    access_type = "Free"
    
    # --- MENENTUKAN ID MODEL (BACKEND) ---
    if "Groq" in vendor:
        selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
    elif "Google" in vendor:
        selected_model = "gemini-1.5-flash"
    elif "OpenAI" in vendor:
        selected_model = "gpt-4o"
    
    # --- INPUT CREDENTIALS LOGIC ---
    if access_mode == "Free (Standard)":
        # BYOK LOGIC (Pakai Bahasa dari Dictionary)
        label_api = f"{t['lbl_enter_api']} {vendor.split()[0]}:"
        
        if "Groq" in vendor:
            final_key = st.text_input(label_api, type="password", help=t['help_api'])
        elif "Google" in vendor:
            final_key = st.text_input(label_api, type="password", help=t['help_api'])
        elif "OpenAI" in vendor:
            final_key = st.text_input(label_api, type="password", help=t['help_api'])
            
        # IKLAN SIDEBAR (Hanya di Free Mode)
        st.divider()
        st.markdown(f"""
        <div class="ad-box">
            <div class="ad-title">{t['ad_sidebar_title']}</div>
            {t['ad_sidebar_text']}<br>
            <a href="mailto:hadisyh71@gmail.com" style="color:#F59E0B; font-weight:bold; text-decoration:none;">{t['ad_sidebar_btn']}</a>
        </div>
        """, unsafe_allow_html=True)
            
    else:
        # PREMIUM MODE (User Masukin Token, Kita Supply API Key)
        user_token = st.text_input("Member Token:", type="password")
        
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                # Klasifikasi Tipe Token
                if user_token.startswith("FULL-"): access_type = "Full Access"
                elif user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("PRM-"): access_type = "Prompt Only"
                
                st.success(f"💎 Premium Active: {access_type}")
                
                # --- LOGIKA KUNCI PREMIUM ---
                # Hanya Groq yang aktif di Premium. Lainnya Coming Soon.
                if "Groq" in vendor:
                    st.caption(f"✅ Connected to {vendor.split()[0]} (Premium Server)")
                    final_key = st.secrets["GROQ_API_KEY"]
                else:
                    # Tampilkan pesan Coming Soon (Dari Dictionary)
                    st.warning(t['err_premium_coming_soon'])
                    final_key = None # Kunci akses agar tidak jalan
                    
            elif user_token:
                st.error("Invalid Token!")
        except:
            pass

# ==========================================
# 6. FUNGSI EKSEKUTOR AI (ENGINE)
# ==========================================
def run_ai(api_key, provider, model, prompt):
    try:
        if "Groq" in provider:
            client = Groq(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
            
        elif "Google" in provider:
            genai.configure(api_key=api_key)
            m = genai.GenerativeModel(model)
            resp = m.generate_content(prompt)
            return resp.text
            
        elif "OpenAI" in provider:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
            
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# 7. MAIN LAYOUT & TABS
# ==========================================
st.title(t['title_main'])

# Tampilkan Banner Iklan (Jika User Free)
if access_type == "Free":
    st.markdown(f"""<div class="ad-header-banner">{t['ad_header_text']}</div>""", unsafe_allow_html=True)

# Membuat 2 Tab Utama
tab1, tab2 = st.tabs([t['tab1'], t['tab2']])

# ==========================================
# TAB 1: METADATA ENGINE (STOCK & SOSMED)
# ==========================================
with tab1:
    col_plat, col_lang = st.columns([2,1])
    
    with col_plat:
        platform = st.selectbox("Target Platform:", (
            "Adobe Stock", "Shutterstock", 
            "Instagram Caption", "TikTok Script", 
            "YouTube Shorts", "X (Twitter) Thread", 
            "Threads Post", "LinkedIn Post", "Facebook Ads"
        ))
        
    with col_lang:
        out_lang = st.selectbox("Output Lang:", (
            "English", "Indonesian", "Spanish", 
            "French", "German", "Japanese"
        ))
    
    # Opsi Tambahan
    tone, specific_niche, custom_info = "", "", ""
    if platform not in ["Adobe Stock", "Shutterstock"]:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tone = st.selectbox("Tone:", ("Viral & Catchy", "Professional", "Casual", "Sales/Urgent", "Funny"))
        with col_t2:
            specific_niche = st.selectbox("Niche:", ("Travel", "Food", "Fashion", "Tech", "Health", "Lifestyle", "Product"))
        custom_info = st.text_input("Extra Info (Optional):")

    uploaded_files = st.file_uploader("Upload Assets (Max 10)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], key="meta_up")
    
    if access_mode == "Free (Standard)" and uploaded_files:
        st.warning(t['ad_warning'])

    # TOMBOL EKSEKUSI (RUN)
    if st.button(t['run_btn'], key="btn_meta"):
        
        # Validasi Izin
        is_allowed = True
        if access_type == "Prompt Only": is_allowed = False
        elif access_type == "Sosmed Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = False
        elif access_type == "Stock Only" and platform not in ["Adobe Stock", "Shutterstock"]: is_allowed = False
        
        if not final_key:
            st.error(t['err_api_req'])
        elif not is_allowed:
            st.error(t['err_plan'].format(type=access_type, plat=platform))
        elif uploaded_files:
            
            progress = st.progress(0)
            total = len(uploaded_files)
            
            for i, file in enumerate(uploaded_files):
                progress.progress((i)/total)
                
                with st.expander(f"Processing: {file.name}", expanded=True):
                    col1, col2 = st.columns([1,3])
                    with col1:
                        st.image(file, use_container_width=True)
                    with col2:
                        st.write(t['process_txt'])
                        
                        prompt = ""
                        if platform in ["Adobe Stock", "Shutterstock"]:
                            prompt = f"Analyze image '{file.name}'. Output strictly: Title, Description, 50 Keywords. Target: {platform}. English only."
                        elif platform == "X (Twitter) Thread":
                            prompt = f"Create viral THREAD for '{file.name}'. Tone: {tone}, Niche: {specific_niche}, Lang: {out_lang}. 4 Tweets (Hook, Value, Tip, CTA)."
                        else:
                            prompt = f"Target: {platform} | Tone: {tone} | Niche: {specific_niche} | Lang: {out_lang}. Extra: {custom_info}. Create viral content for '{file.name}'."
                        
                        res = run_ai(final_key, vendor, selected_model, prompt)
                        st.text_area("Result:", value=res, height=250)
                
                if access_mode == "Free (Standard)":
                    time.sleep(2)
            
            progress.progress(1.0)
            st.success(t['success_txt'])

# ==========================================
# TAB 2: PROMPT ARCHITECT (GENERATOR)
# ==========================================
with tab2:
    # Cek Status Premium
    is_prompt_premium = False
    if access_type == "Full Access" or access_type == "Prompt Only":
        is_prompt_premium = True
    else:
        st.info(t['pg_free_info'])

    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        p_mode = st.selectbox(t['pg_mode'], ("🖼️ Text to Image", "🔄 Image to Image", "🎬 Text to Video", "📸➡️🎬 Image to Video"))
    with col_mode2:
        p_target = st.selectbox(t['pg_target'], ("Midjourney v6", "Dall-E 3", "Leonardo AI", "Stable Diffusion XL", "Runway Gen-2", "Kling AI"))

    p_idea = st.text_area(t['pg_idea'], placeholder=t['pg_placeholder'])
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        p_style = st.selectbox(t['pg_style'], ("Cinematic Photography", "3D Pixar/Disney", "Anime Studio Ghibli", "Cyberpunk/Neon", "Dark Fantasy", "Corporate Vector", "Sketch/Drawing"))
    with col_opt2:
        p_ratio = st.selectbox(t['pg_ratio'], ("--ar 16:9 (Landscape)", "--ar 9:16 (Story/Reels)", "--ar 1:1 (Square)", "--ar 4:5 (IG Feed)"))

    # TOMBOL GENERATE PROMPT
    if st.button(t['pg_btn'], key="btn_prompt"):
        
        if not final_key:
            st.error(t['err_api_req'])
        elif not p_idea:
            st.warning(t['err_idea_req'])
        else:
            with st.spinner("Meracik Mantra Ajaib..."):
                
                sys_prompt = f"""
                Act as a Professional Prompt Engineer for {p_target}.
                Mode: {p_mode}.
                Style: {p_style}.
                Ratio: {p_ratio}.
                User Concept: '{p_idea}'.
                
                Task: Create a detailed, high-quality prompt.
                1. Translate to English if needed.
                2. Include technical camera parameters.
                3. Include lighting and texture details.
                """
                
                if is_prompt_premium:
                    sys_prompt += " Add 'Award winning, 8k, masterpiece' keywords. Also generate a Negative Prompt block."
                
                final_prompt = run_ai(final_key, vendor, selected_model, sys_prompt)
                
                st.subheader("✨ Hasil Mantra (Copy This):")
                st.code(final_prompt, language="markdown")
                
                if not is_prompt_premium:
                    st.markdown(f"<small style='color:#F59E0B;'>{t['pg_upsell']}</small>", unsafe_allow_html=True)
