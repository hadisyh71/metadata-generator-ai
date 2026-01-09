import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Universal AI Control Center", page_icon="✨", layout="wide")

# 2. CSS FINAL: UI MEWAH, TAB STYLING, & IKLAN
st.markdown("""
    <style>
    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* THEME COLORS */
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* BUTTON STYLING */
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white; border-radius: 12px; border: none; font-weight: 600; width: 100%;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
    
    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; border-radius: 10px;
        background-color: rgba(255,255,255,0.05); color: white;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        color: black !important; font-weight: bold;
    }

    /* AD BOX STYLING */
    .ad-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #F59E0B;
        padding: 15px; border-radius: 10px; margin: 15px 0; font-size: 0.9em;
    }
    
    /* HEADER BANNER */
    .ad-header-banner {
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        padding: 15px; border-radius: 12px; text-align: center; 
        margin-bottom: 25px; color: black; font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    /* TIER CARD STYLING (UPDATED FOR 4 COLS) */
    .tier-wrapper {
        display: flex; flex-direction: column; height: 100%;
        background: rgba(255,255,255,0.03); padding: 20px; 
        border-radius: 15px; text-align: center; justify-content: space-between;
        min-height: 450px; border: 1px solid rgba(255,255,255,0.1);
    }
    .sub-link {
        display: block; width: 100%; padding: 10px; margin-top: auto;
        text-decoration: none !important; color: white !important;
        font-weight: bold; border-radius: 12px; transition: 0.3s;
        text-align: center; font-size: 0.9em;
    }
    .bg-stock { border-top: 4px solid #3B82F6; } .btn-stock { background: #3B82F6; }
    .bg-sosmed { border-top: 4px solid #8B5CF6; } .btn-sosmed { background: #8B5CF6; }
    .bg-prompt { border-top: 4px solid #10B981; } .btn-prompt { background: #10B981; }
    .bg-full { border: 2px solid #F59E0B; background: rgba(245, 158, 11, 0.05); } 
    .btn-full { background: #F59E0B; color: #000 !important; }
    
    .best-value-tag {
        background: #F59E0B; color: black; font-size: 0.7em; 
        padding: 4px 12px; border-radius: 10px; font-weight: bold;
        position: absolute; top: -15px; left: 50%; transform: translateX(-50%); z-index: 10;
    }
    
    h3 { font-size: 1.1em !important; }
    .desc-text { font-size: 0.8em; color: #D1D5DB; line-height: 1.6; text-align: left; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. KAMUS BAHASA (DICTIONARY) - MANFAAT SPESIFIK
with st.sidebar:
    app_lang = st.radio("Language / Bahasa:", ("🇮🇩 Indonesia", "🌎 English (Global)"), horizontal=True)

if app_lang == "🇮🇩 Indonesia":
    t = {
        "tab1": "📸 Metadata Stok & Sosmed", "tab2": "🎨 AI Prompt Generator",
        "ctrl_title": "🌐 PUSAT KONTROL", "acc_mode": "Mode Akses:", "btn_price": "ℹ️ Lihat Pilihan Paket",
        "ad_sidebar_title": "📢 SPONSOR",
        "ad_sidebar_text": "<b>Jasa Foto Produk Pro</b><br><small style='color:#D1D5DB;'>Bikin produkmu auto-laris. Diskon khusus user aplikasi!</small>",
        "ad_sidebar_btn": "Hubungi via Email →",
        "ad_header_text": "🚀 <b>MAU FITUR SULTAN?</b><br><span style='font-size:0.8em;'>Upgrade ke Paket FULL hanya 49rb! Akses Metadata + Prompt Generator.</span>",
        "title_main": "✨ Universal AI Control Center",
        "run_btn": "JALANKAN 🚀",
        "ad_warning": "📢 Akun Free antrean server lebih lama (Low Priority).",
        "process_txt": "Sedang memproses...", "success_txt": "✅ Selesai!",
        
        # Prompt Gen Specific
        "pg_mode": "Pilih Mode:", "pg_idea": "Ide Dasar (Indonesia/Inggris):", 
        "pg_style": "Gaya Visual:", "pg_target": "Target AI:", "pg_ratio": "Rasio:",
        "pg_btn": "GENERATE MANTRA AJAIB ✨",
        
        # Pricing Labels
        "p_stock_p": "29rb", "p_sosmed_p": "29rb", "p_prompt_p": "29rb", "p_full_p": "49rb",
        "p_btn": "Pilih Paket",
        
        # Manfaat Spesifik (Indonesia)
        "d_stock": "✅ <b>Optimasi Adobe Stock</b><br>✅ Generator 50 Keyword<br>✅ Auto Title & Deskripsi<br>✅ Format CSV Ready<br>🚫 Tanpa Iklan",
        "d_sosmed": "✅ <b>Viral Hook Generator</b><br>✅ Thread Twitter Otomatis<br>✅ Caption IG/TikTok<br>✅ Multi-Bahasa<br>🚫 Tanpa Iklan",
        "d_prompt": "✅ <b>Midjourney & Video AI</b><br>✅ Auto Negative Prompt<br>✅ Style Preset (Cinematic)<br>✅ Parameter Teknis<br>🚫 Tanpa Iklan",
        "d_full": "🔥 <b>SEMUA FITUR (3 in 1)</b><br>✅ Akses Stok + Sosmed + Prompt<br>⚡ <b>Prioritas Server (Cepat)</b><br>✅ Support 24/7<br>✅ Early Access Fitur Baru",
        
        "p_link_full": "mailto:hadisyh71@gmail.com?subject=Beli%20Token%20Full%20(IDR)"
    }
else:
    t = {
        "tab1": "📸 Metadata Engine", "tab2": "🎨 AI Prompt Architect",
        "ctrl_title": "🌐 CONTROL CENTER", "acc_mode": "Access Mode:", "btn_price": "ℹ️ View Pricing",
        "ad_sidebar_title": "📢 SPONSORED",
        "ad_sidebar_text": "<b>Professional Photo Services</b><br><small style='color:#D1D5DB;'>High-end photography for your business.</small>",
        "ad_sidebar_btn": "Contact for Quote →",
        "ad_header_text": "🚀 <b>UNLOCK PRO FEATURES?</b><br><span style='font-size:0.8em;'>Get FULL Access for only $9/mo! Metadata + Prompt Tools included.</span>",
        "title_main": "✨ Universal AI Control Center",
        "run_btn": "RUN ENGINE 🚀",
        "ad_warning": "📢 Free Tier has lower server priority. Upgrade for lightning speed.",
        "process_txt": "Generating metadata...", "success_txt": "✅ Batch Processing Complete!",
        
        # Prompt Gen Specific
        "pg_mode": "Select Mode:", "pg_idea": "Basic Concept:", 
        "pg_style": "Visual Style:", "pg_target": "Target AI:", "pg_ratio": "Aspect Ratio:",
        "pg_btn": "GENERATE MAGIC PROMPT ✨",
        
        # Pricing Labels
        "p_stock_p": "$5", "p_sosmed_p": "$5", "p_prompt_p": "$5", "p_full_p": "$9",
        "p_btn": "Subscribe",
        
        # Manfaat Spesifik (English)
        "d_stock": "✅ <b>Adobe Stock Optimized</b><br>✅ 50 Keywords Generator<br>✅ SEO Title & Desc<br>✅ Clean Format<br>🚫 No Ads Experience",
        "d_sosmed": "✅ <b>Viral Scripts & Hooks</b><br>✅ Twitter Thread Maker<br>✅ IG/TikTok Captions<br>✅ Multi-Language Output<br>🚫 No Ads Experience",
        "d_prompt": "✅ <b>Pro AI Prompts</b><br>✅ Auto Negative Prompt<br>✅ Video AI Camera Moves<br>✅ Midjourney Parameters<br>🚫 No Ads Experience",
        "d_full": "🔥 <b>ALL FEATURES (3 in 1)</b><br>✅ Stock + Sosmed + Prompt<br>⚡ <b>Priority Server (Fast)</b><br>✅ 24/7 Support<br>✅ Unlimited Usage",
        
        "p_link_full": "mailto:hadisyh71@gmail.com?subject=Buy%20Full%20Token%20(USD)"
    }

# 4. FUNGSI POP-UP PRICING (4 KOLOM)
@st.dialog("💎 Choose Your Power")
def show_subscription_tiers():
    st.markdown(f"<p style='text-align: center; color: #9CA3AF;'>Pilih tools spesifik atau ambil paket hemat.</p>", unsafe_allow_html=True)
    
    # Membagi jadi 4 Kolom
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""<div class="tier-wrapper bg-stock"><div><h3 style="color: #3B82F6; margin: 0;">📦 STOCK</h3><h1 style="margin: 10px 0;">{t['p_stock_p']}</h1><div class="desc-text">{t['d_stock']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-stock">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="tier-wrapper bg-sosmed"><div><h3 style="color: #8B5CF6; margin: 0;">📱 SOSMED</h3><h1 style="margin: 10px 0;">{t['p_sosmed_p']}</h1><div class="desc-text">{t['d_sosmed']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-sosmed">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="tier-wrapper bg-prompt"><div><h3 style="color: #10B981; margin: 0;">🎨 PROMPT</h3><h1 style="margin: 10px 0;">{t['p_prompt_p']}</h1><div class="desc-text">{t['d_prompt']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-prompt">{t['p_btn']}</a></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div style="position: relative; height: 100%;"><div class="best-value-tag">BEST VALUE</div><div class="tier-wrapper bg-full"><div><h3 style="color: #F59E0B; margin: 0;">🔥 FULL</h3><h1 style="margin: 10px 0;">{t['p_full_p']}</h1><div class="desc-text">{t['d_full']}</div></div><a href="{t['p_link_full']}" class="sub-link btn-full">{t['p_btn']}</a></div></div>""", unsafe_allow_html=True)

# 5. SIDEBAR LOGIC
with st.sidebar:
    st.header(t['ctrl_title'])
    access_mode = st.radio(t['acc_mode'], ("Free (Standard)", "Premium (Pro Access)"))
    if st.button(t['btn_price']): show_subscription_tiers()
    
    st.divider()
    vendor = st.selectbox("AI Engine:", ("Groq (Llama 3 - Fast)", "Google (Gemini - Smart)", "OpenAI (GPT-4o - Precise)"))
    
    final_key, selected_model, access_type = None, None, "Free"
    
    if access_mode == "Free (Standard)":
        final_key = st.text_input(f"Enter {vendor.split()[0]} API Key:", type="password")
        if "Groq" in vendor: selected_model = "meta-llama/llama-3.3-70b-versatile" 
        elif "Google" in vendor: selected_model = "gemini-1.5-flash"
        elif "OpenAI" in vendor: selected_model = "gpt-4o-mini"
        
        # IKLAN SIDEBAR
        st.divider()
        st.markdown(f"""<div class="ad-box"><div class="ad-title">{t['ad_sidebar_title']}</div>
        {t['ad_sidebar_text']}<br>
        <a href="mailto:hadisyh71@gmail.com" style="color:#F59E0B; font-weight:bold; text-decoration:none;">{t['ad_sidebar_btn']}</a></div>""", unsafe_allow_html=True)
    else:
        user_token = st.text_input("Member Token:", type="password")
        try:
            valid_tokens = st.secrets["VALID_TOKENS"].split(",") 
            if user_token in valid_tokens and user_token != "":
                if user_token.startswith("FULL-"): access_type = "Full Access"
                elif user_token.startswith("STK-"): access_type = "Stock Only"
                elif user_token.startswith("SOC-"): access_type = "Sosmed Only"
                elif user_token.startswith("PRM-"): access_type = "Prompt Only" # NEW TIER
                st.success(f"💎 Premium Active: {access_type}")
                if "Groq" in vendor: final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-3.3-70b-versatile"
                elif "Google" in vendor: final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif "OpenAI" in vendor: final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            elif user_token: st.error("Invalid Token!")
        except: pass

# 6. FUNGSI AI ENGINE
def run_ai(api_key, provider, model, prompt):
    try:
        if "Groq" in provider:
            client = Groq(api_key=api_key); resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
        elif "Google" in provider:
            genai.configure(api_key=api_key); m = genai.GenerativeModel(model); resp = m.generate_content(prompt); return resp.text
        elif "OpenAI" in provider:
            client = OpenAI(api_key=api_key); resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}]); return resp.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

# 7. MAIN LAYOUT
st.title(t['title_main'])

# IKLAN HEADER (Free Only)
if access_type == "Free":
    st.markdown(f"""<div class="ad-header-banner">{t['ad_header_text']}</div>""", unsafe_allow_html=True)

# TAB SYSTEM
tab1, tab2 = st.tabs([t['tab1'], t['tab2']])

# ==========================================
# TAB 1: METADATA ENGINE
# ==========================================
with tab1:
    col_plat, col_lang = st.columns([2,1])
    with col_plat:
        platform = st.selectbox("Target Platform:", 
            ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "YouTube Shorts", "X (Twitter) Thread", "Threads Post", "LinkedIn Post", "Facebook Ads"))
    with col_lang:
        out_lang = st.selectbox("Output Lang:", ("English", "Indonesian", "Spanish", "French", "German", "Japanese"))
    
    # Extra Options
    tone, specific_niche, custom_info = "", "", ""
    if platform not in ["Adobe Stock", "Shutterstock"]:
        col_t1, col_t2 = st.columns(2)
        with col_t1: tone = st.selectbox("Tone:", ("Viral & Catchy", "Professional", "Casual", "Sales/Urgent", "Funny"))
        with col_t2: specific_niche = st.selectbox("Niche:", ("Travel", "Food", "Fashion", "Tech", "Health", "Lifestyle", "Product"))
        custom_info = st.text_input("Extra Info (Optional):")

    uploaded_files = st.file_uploader("Upload Assets (Max 10)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], key="meta_up")
    
    # IKLAN WARNING
    if access_mode == "Free (Standard)" and uploaded_files: st.warning(t['ad_warning'])

    if st.button(t['run_btn'], key="btn_meta"):
        # Cek Izin Akses Tab 1
        is_allowed = True
        # Prompt Only tidak boleh akses Tab 1
        if access_type == "Prompt Only": is_allowed = False
        # Sosmed Only tidak boleh akses Stock
        elif access_type == "Sosmed Only" and platform in ["Adobe Stock", "Shutterstock"]: is_allowed = False
        # Stock Only tidak boleh akses Sosmed
        elif access_type == "Stock Only" and platform not in ["Adobe Stock", "Shutterstock"]: is_allowed = False
        
        if not final_key: st.error("API Key / Token Required!")
        elif not is_allowed: st.error(f"Your Plan '{access_type}' does not include '{platform}'. Please Upgrade.")
        elif uploaded_files:
            progress = st.progress(0); total = len(uploaded_files)
            for i, file in enumerate(uploaded_files):
                progress.progress((i)/total)
                with st.expander(f"Processing: {file.name}", expanded=True):
                    col1, col2 = st.columns([1,3])
                    with col1: st.image(file, use_container_width=True)
                    with col2:
                        st.write(t['process_txt'])
                        
                        # --- LOGIKA PROMPT METADATA ---
                        if platform in ["Adobe Stock", "Shutterstock"]:
                            prompt = f"""
                            Analyze image '{file.name}' for Stock Photography Metadata.
                            Output strictly in this format ONLY (No intro, just text):
                            Title: [SEO title max 70 chars]
                            Description: [Detailed description min 50 words]
                            Keywords: [List 50 keywords separated by commas]
                            Target: {platform}. Language: English (Stock must be English).
                            """
                        elif platform == "X (Twitter) Thread":
                            prompt = f"""
                            Create a viral THREAD based on image '{file.name}'.
                            Tone: {tone} | Niche: {specific_niche} | Lang: {out_lang}
                            Format strictly:
                            Tweet 1: (Hook that grabs attention)
                            Tweet 2: (Value/Context)
                            Tweet 3: (Insight/Tip)
                            Tweet 4: (Call to Action)
                            Context: {custom_info}
                            """
                        elif platform == "Instagram Caption":
                             prompt = f"""
                             Create an engaging Instagram Caption for '{file.name}'.
                             Include: 
                             1. A catchy Hook (First line).
                             2. Engaging Story/Body based on {tone} tone.
                             3. Call to Action (Q&A or Link).
                             4. 30 Relevant Hashtags block.
                             Lang: {out_lang}. Context: {custom_info}
                             """
                        else:
                            prompt = f"Social Media Expert. Target: {platform} | Tone: {tone} | Niche: {specific_niche} | Lang: {out_lang}. Extra: {custom_info}. Create viral content based on '{file.name}'."
                        
                        # Execute AI
                        res = run_ai(final_key, vendor, selected_model, prompt)
                        st.text_area("Result:", value=res, height=250)
                
                # IKLAN GAP
                if access_mode == "Free (Standard)": time.sleep(2)
            
            progress.progress(1.0); st.success(t['success_txt'])

# ==========================================
# TAB 2: PROMPT ARCHITECT (FITUR BARU)
# ==========================================
with tab2:
    # Logic: Prompt Gen hanya untuk Free, Prompt Only, dan Full Access. 
    # Stock/Sosmed Only tidak bisa pakai fitur Premium di sini (dapat basic).
    
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        p_mode = st.selectbox(t['pg_mode'], ("🖼️ Text to Image", "🔄 Image to Image", "🎬 Text to Video", "📸➡️🎬 Image to Video"))
    with col_mode2:
        p_target = st.selectbox(t['pg_target'], ("Midjourney v6", "Dall-E 3", "Leonardo AI", "Stable Diffusion XL", "Runway Gen-2", "Kling AI"))

    p_idea = st.text_area(t['pg_idea'], placeholder="Example: Kucing naik motor di kota tua Jakarta...")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        p_style = st.selectbox(t['pg_style'], ("Cinematic Photography", "3D Pixar/Disney", "Anime Studio Ghibli", "Cyberpunk/Neon", "Dark Fantasy", "Corporate Vector", "Sketch/Drawing"))
    with col_opt2:
        p_ratio = st.selectbox(t['pg_ratio'], ("--ar 16:9 (Landscape)", "--ar 9:16 (Story/Reels)", "--ar 1:1 (Square)", "--ar 4:5 (IG Feed)"))

    # IKLAN UPGRADE DI TAB 2
    is_prompt_premium = False
    if access_type == "Full Access" or access_type == "Prompt Only":
        is_prompt_premium = True
    else:
        st.info("🔓 **Free Mode Active:** Anda menggunakan fitur dasar. Upgrade ke **PROMPT/FULL Access** untuk mengaktifkan 'Auto-Enhance', 'Negative Prompt Otomatis', dan 'Video Camera Directives'.")

    # TOMBOL GENERATE PROMPT
    if st.button(t['pg_btn'], key="btn_prompt"):
        if not final_key: st.error("API Key / Token Required!")
        elif not p_idea: st.warning("Please enter your idea first.")
        else:
            with st.spinner("Meracik Mantra Ajaib..."):
                # RUMUS PROMPT ENGINEERING (Full Logic)
                sys_prompt = f"""
                Act as a Professional Prompt Engineer for {p_target}.
                Mode: {p_mode}. Style: {p_style}. Ratio: {p_ratio}.
                
                User Concept: "{p_idea}"
                
                Task: Convert the user concept into a HIGH-LEVEL, DETAILED prompt optimized for {p_target}.
                1. Translate idea to English (if in Indonesian).
                2. Add technical parameters (camera, lighting, render engine).
                3. Add style keywords naturally.
                4. For Midjourney, add parameters at the end.
                5. For Video, add camera movement (zoom, pan) keywords.
                
                OUTPUT ONLY THE RAW PROMPT TEXT. NO EXPLANATION.
                """
                
                # Auto-Enhance for Premium (Hanya untuk Full / Prompt Only)
                if is_prompt_premium:
                    sys_prompt += " Add 'Award winning, 8k, masterpiece' keywords. Also generate a Negative Prompt block below the main prompt."
                
                final_prompt = run_ai(final_key, vendor, selected_model, sys_prompt)
                
                st.subheader("✨ Hasil Mantra (Copy This):")
                st.code(final_prompt, language="markdown")
                
                if not is_prompt_premium:
                    st.markdown(f"<small style='color:#F59E0B;'>💡 Ingin hasil lebih stabil tanpa cacat? <a href='{t['p_link_full']}'>Beli Token PROMPT Only (29rb)</a></small>", unsafe_allow_html=True)
