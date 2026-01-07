import streamlit as st

st.set_page_config(page_title="Bulk Metadata Generator", page_icon="⚡")

st.title("⚡ Bulk Metadata Generator (Groq Llama)")
st.write("Bisa upload banyak foto sekaligus untuk diproses.")

uploaded_files = st.file_uploader("Pilih Banyak Foto", accept_multiple_files=True)

if st.button("Mulai Proses Antrian 🚀"):
    if uploaded_files:
        for file in uploaded_files:
            st.write(f"Memproses: {file.name}...")
            # Di sini nanti kita tambahkan logika Groq API kamu
        st.success("Semua file berhasil diproses!")
    else:
        st.warning("Silakan upload file dulu.")
