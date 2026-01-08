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
    access_mode = st.radio("Access Mode:", ("Free (With Ads)", "Premium (No Ads)"))
    
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
        member_pass = st.text_input("Member Password:", type="password")
        if member_pass == "MEMBER2026":
            st.success("💎 Premium Active!")
            try:
                if vendor == "Groq (Llama 4)": final_key = st.secrets["GROQ_API_KEY"]; selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                elif vendor == "Google (Gemini)": final_key = st.secrets["GEMINI_API_KEY"]; selected_model = "gemini-1.5-flash"
                elif vendor == "OpenAI (GPT-4o)": final_key = st.secrets["OPENAI_API_KEY"]; selected_model = "gpt-4o"
            except: st.error("API Key not found in Secrets!")

    st.divider()
    
    # PILIHAN PLATFORM & NICHE
    platform = st.selectbox("Target Platform:", 
        ("Adobe Stock", "Shutterstock", "Instagram Caption", "TikTok Script", "Facebook Ads"))
    
    # --- FITUR BARU: PILIHAN BAHASA ---
    output_lang = st.selectbox("Output Language:", (
        "English", "Indonesian", "Spanish", "French", "German", "Japanese", "Korean", "Arabic"
    ))
    
    specific_niche = ""
    custom_info = ""
    if platform in ["Instagram Caption", "TikTok Script", "Facebook Ads"]:
        specific_niche = st.selectbox("Pilih Niche Konten:", (
            "Traveling/Nature", "Food/Culinary", "Fashion/Beauty", "Business/Startup", 
            "Tech/Gadget", "Health/Fitness", "Personal Branding", "Product Promotion"
        ))
        custom_info = st.text_input("Info Tambahan (Opsional):", placeholder="Diskon, lokasi, dll")

# 3. LOGIKA ENGINE AI
def run_ai_engine(api_key, provider, model_name, prompt):
    if provider == "Groq (Llama 4)":
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content
    elif provider == "Google (Gemini)":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content(prompt)
        return resp.text
    elif provider == "OpenAI (GPT-4o)":
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content

# 4. TAMPILAN UTAMA
st.title("✨ Universal AI Metadata Engine")

if access_mode == "Free (With Ads)":
    st.markdown("""
        <div style="background-color: #161B26; padding: 15px; border: 1px dashed #3B82F6; border-radius: 12px; text-align: center; margin-bottom: 25px;">
            <p style="color: #6B7280; font-size: 12px;">ADVERTISEMENT</p>
            <h4 style="color: #3B82F6;">Upgrade to Premium for No Ads</h4>
            <a href="https://hadisyh.my.id/bayar" target="_blank" style="color: #8B5CF6; font-weight: bold;">Upgrade Now</a>
        </div>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("RUN AI GENERATOR 🚀"):
    if not final_key:
        st.error("Please provide API Key or Member Password!")
    elif uploaded_files:
        if access_mode == "Free (With Ads)":
            with st.spinner("Processing with Ads..."): time.sleep(2)
        
        for file in uploaded_files:
            with st.expander(f"Result: {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(file, use_container_width=True)
                with col2:
                    # PROMPT DINAMIS (Metadata Stok selalu Inggris, Sosmed bebas)
                    if "Stock" in platform or "Shutterstock" in platform:
                        actual_lang = "English"
                        prompt = f"Expert Stock SEO. Create {platform} Title/Description & Keywords for '{file.name}' in {actual_lang}."
                    else:
                        actual_lang = output_lang
                        prompt = f"""
                        Act as a Social Media Expert. 
                        Target: {platform} | Niche: {specific_niche} | Language: {actual_lang}
                        Context: {file.name} | Info: {custom_info}
                        Task: Create an engaging caption in {actual_lang} with hook, viral hashtags, and CTA.
                        """

                    try:
                        result = run_ai_engine(final_key, vendor, selected_model, prompt)
                        st.text_area(f"Output ({actual_lang}):", value=result, height=250, key=f"t_{file.name}")
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.balloons()
