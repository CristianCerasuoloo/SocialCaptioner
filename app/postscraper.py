import tempfile
from io import BytesIO

import instaloader
import requests
from PIL import Image

from app.schemes.post import Post


class PostScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=False, download_videos=False
        )

    def get_post(self, shortcode) -> Post | None:
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
                caption = ""
            else:
                caption = post.caption

            # Check if the post has multiple media
            if post.typename == "GraphSidecar":
                is_carousel = True
                paths = []
                for idx, node in enumerate(post.get_sidecar_nodes()):
                    url = node.display_url
                    # You can display all images:
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    # temporarily save the image to display it
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".png"
                    ) as tmp_file:
                        img.save(tmp_file, format="PNG")
                        paths.append(tmp_file.name)

            else:
                is_carousel = False
                # Single image or video post
                response = requests.get(post.url)
                img = Image.open(BytesIO(response.content))
                # temporarily save the image to display it
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".png"
                ) as tmp_file:
                    img.save(tmp_file, format="PNG")
                    paths = tmp_file.name

            return Post(is_carousel=is_carousel, resource_path=paths, caption=caption)
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error fetching post: {e}")
            return None
