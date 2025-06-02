import logging
import tempfile

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from app.chain import captioning
from app.postscraper import PostScraper
from frontend.constants import MOODS, SOCIAL_MEDIA_LIST

# Carica le variabili dal file .env
load_dotenv()


# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scraper = PostScraper()

st.set_page_config(layout="centered")
st.title("🖼️ Social Captioner")

uploaded_file = st.file_uploader("Upload an image!", type=["jpg", "jpeg", "png"])
social = st.selectbox("Choose the social media.", SOCIAL_MEDIA_LIST)
mood = st.selectbox(
    "Choose the mood you want to inject in the caption.", MOODS, index=5
)

# Inizializza session_state se non esiste
if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = None

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    img = Image.open(tmp_path)
    img.thumbnail((300, 300))
    st.image(img, caption="Uploaded image")

    context = st.text_area(
        "Insert your description of the scene, what the image means to you, or any other context or instruction you want to provide.",
    )

    # st.subheader("✏️ Examples (optional)")

    # # Inizializza session_state per contenere le caption esempio
    # if "example_captions" not in st.session_state:
    #     st.session_state.example_captions = []

    # # Bottone per aggiungere un nuovo campo di esempio
    # if st.button("+ Add example"):
    #     st.session_state.example_captions.append(random.choice(DEFAULT_EXAMPLES))

    # # Visualizza tutti gli input di esempio
    # for i, caption in enumerate(st.session_state.example_captions):
    #     st.session_state.example_captions[i] = st.text_input(
    #         f"Example {i + 1}", value=caption, key=f"example_{i}"
    #     )

    if social.lower() == "instagram":
        st.subheader("📷 Instagram Post Fetcher")

        st.markdown(
            "Paste the URL of a single **public** Instagram post to extract its image and caption."
        )
        with st.form("instagram_post_form"):
            st.session_state.fetched_posts = st.session_state.get("fetched_posts", [])

            post_url = st.text_input("Instagram Post URL (public only)", "")
            fetch_submit = st.form_submit_button("Fetch Post")

            if fetch_submit and post_url:
                with st.spinner("Fetching the post..."):
                    try:
                        # Extract shortcode from the URL
                        if "instagram.com/p/" not in post_url:
                            raise ValueError("Not a valid Instagram post URL.")

                        shortcode = post_url.rstrip("/").split("/")[-1]

                        # Get Post object
                        post = scraper.get_post(shortcode)
                        if post:
                            st.session_state.fetched_posts.append(post)

                            st.success(
                                f"Post fetched successfully! Fetched {len(st.session_state.fetched_posts)} posts in total."
                            )
                        else:
                            st.error("Post not found or is private.")

                    except Exception as e:
                        logger.exception("Error fetching post %s", e)
                        st.error(
                            f"Something went wrong. Make sure the URL is correct and the post is public.\n\n**Error:** {e}"
                        )

            posts = st.session_state.fetched_posts
            if posts:
                cols_per_row = 3
                rows = (len(posts) + cols_per_row - 1) // cols_per_row

                for row in range(rows):
                    cols = st.columns(cols_per_row)
                    for i in range(cols_per_row):
                        idx = row * cols_per_row + i
                        if idx < len(posts):
                            post = posts[idx]

                            if post.is_carousel:
                                img_path = post.resource_path[
                                    0
                                ]  # DIsplay the first image of the carousel
                                caption = post.caption + "[0]"
                            else:
                                img_path = post.resource_path
                                caption = post.caption

                            print("Displaying post %d: %s %s", idx, img_path, caption)
                            with cols[i]:
                                # Thumbnail rendering
                                try:
                                    img = Image.open(img_path)
                                    img.thumbnail((200, 200))  # Resize to thumbnail
                                    st.image(
                                        img,
                                        caption=caption[:60] + "..."
                                        if len(caption) > 60
                                        else caption,
                                    )
                                except Exception as e:
                                    logger.exception("Error loading image: %s", e)

                                    st.error("Image load error.")

    if st.button("✨ Generate"):
        try:
            with st.spinner("Generating ..."):
                captions = captioning(
                    tmp_path,
                    social.lower(),
                    mood.lower(),
                    user_context=context,
                    examples=[],  # [
                    #     caption
                    #     for caption in st.session_state.example_captions
                    #     if caption != ""
                    # ],
                    posts=st.session_state.get("fetched_posts", []),
                )
                if not captions:
                    st.error("No caption generated.")
                    st.stop()
                st.session_state.generated_captions = captions
                st.session_state.selected_caption = None  # reset selezione

                st.success(
                    f"Generated {len(captions)} captions for {social} with mood '{mood}'!"
                )
        except Exception as e:
            logger.exception("Error generating captions: %s", e)
            st.error(
                "Something went wrong while generating the captions. Please try again later."
            )
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
