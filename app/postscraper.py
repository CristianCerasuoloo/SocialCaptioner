import tempfile
from io import BytesIO

import instaloader
import requests
from PIL import Image


class PostScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=False, download_videos=False
        )

    def get_post(self, shortcode) -> tuple | None:
        """
        Fetches a single Instagram post by its shortcode.
        Returns a tuple containing the path to the image and the caption.
        :param shortcode: The shortcode of the Instagram post.
        :return: (image_path, caption)
        """
        # TODO raise expection if privde or invalid shortcode

        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

            # get caption
            if post.caption is None:
                caption = "*No caption*"
            else:
                caption = post.caption

            response = requests.get(post.url)
            img = Image.open(BytesIO(response.content))
            # temporarily save the image to display it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                img.save(tmp_file, format="PNG")
                img_path = tmp_file.name

            return (img_path, caption)
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error fetching post: {e}")
            return None
