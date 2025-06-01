import random
import tempfile

import streamlit as st

from app.chain import captioning
from frontend.constants import DEFAULT_EXAMPLES, MOODS, SOCIAL_MEDIA_LIST

st.set_page_config(layout="centered")
st.title("🖼️ Social Captioner")

uploaded_file = st.file_uploader("Upload an image!", type=["jpg", "jpeg", "png"])
social = st.selectbox("Choose the social media.", SOCIAL_MEDIA_LIST)
mood = st.selectbox("Chosse the mood you want to inject in the caption.", MOODS)

# Inizializza session_state se non esiste
if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = None

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.image(tmp_path, caption="Uploaded image", use_container_width=True)

    context = st.text_area(
        "Insert your description of the scene, what the image means to you, or any other context you want to provide.",
    )

    st.subheader("✏️ Examples (otpional)")

    # Inizializza session_state per contenere le caption esempio
    if "example_captions" not in st.session_state:
        st.session_state.example_captions = []

    # Bottone per aggiungere un nuovo campo di esempio
    if st.button("+ Add example"):
        st.session_state.example_captions.append(random.choice(DEFAULT_EXAMPLES))

    # Visualizza tutti gli input di esempio
    for i, caption in enumerate(st.session_state.example_captions):
        st.session_state.example_captions[i] = st.text_input(
            f"Example {i + 1}", value=caption, key=f"example_{i}"
        )

    if st.button("✨ Generate"):
        captions = captioning(
            tmp_path,
            social.lower(),
            mood.lower(),
            user_context=context,
            examples=[
                caption
                for caption in st.session_state.example_captions
                if caption != ""
            ],
        )
        if not captions:
            st.error("No caption generated.")
            st.stop()
        st.session_state.generated_captions = captions
        st.session_state.selected_caption = None  # reset selezione

    if "generated_captions" in st.session_state:
        st.subheader("💬 Generated captions:")
        for i, caption in enumerate(st.session_state.generated_captions):
            if st.button(f"{i + 1}: {caption}", key=f"caption_{i}"):
                st.session_state.selected_caption = caption

    # Mostra la caption selezionata in modo ben visibile
    if st.session_state.selected_caption:
        st.markdown("---")
        st.markdown("### ✅ Selected caption:")
        st.success(f"**{st.session_state.selected_caption}**")
