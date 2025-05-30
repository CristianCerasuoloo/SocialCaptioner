import streamlit as st
from app.captioner.blib_captioner import BlipCaptioner
# from app.captioner.gpt_captioner import GPTCaptioner
from app.example.example import CaptionExample
import tempfile

blip = BlipCaptioner()

st.title("🖼️ Caption Generator")

uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])
examples = [CaptionExample(line) for line in st.text_area("Caption esempio (una per riga)", height=100).splitlines()]
social = st.selectbox("Seleziona il social media", ["Instagram", "Facebook", "Twitter", "LinkedIn"])
mood = st.selectbox("Seleziona il mood", ["None", "Informative", "Funny", "Inspirational", "Promotional"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.image(tmp_path, caption="Immagine caricata", use_column_width=True)

    if st.button("Genera caption"):
        caption = blip(tmp_path, social="Instagram", mood = None if mood == "None" else mood, examples=examples)
        st.write(f"**BLIP:** {caption}")

    #     if examples and "OPENAI_API_KEY" in st.secrets:
    #         gpt = GPTCaptioner(api_key=st.secrets["OPENAI_API_KEY"])
    #         styled = gpt.personalize_caption(caption, examples)
    #         st.write(f"**Stile utente:** {styled}")
