# 🖼️ Social Captioner

Social Captioner is an AI-powered web app that generates engaging, personalized captions for your social media images. Whether you're targeting Instagram, Facebook, Twitter, or LinkedIn, this tool helps you match the perfect tone and message for each platform.

## 🔗 Use it Now
[Social Captioner](https://socialcaptioner.streamlit.app)

## 🚀 Features

### ✅ Caption Generation from Images
- Upload any image (JPG, PNG).
- Choose the social media platform: Instagram, Facebook, Twitter, LinkedIn.
- Select the mood you want for the caption:
    - Neutral, Informative, Funny, Inspirational, Promotional, etc.
- Optionally provide context (describe what the image means to you).
- Add example captions (click **+ Add example**) to guide the generation.

### 🎨 Interactive UI
- Click on a generated caption to select and highlight it clearly.
- View all generated captions with a clean layout.

### 📥 Instagram Post Scraping (Public Only)
- Input the URL of a public Instagram post to extract the images and caption.
- Captions are extracted and can be used to guide the app to follow the captioning style of the posts provided.

### 🧠 Smart Examples
- Add/remove/edit examples of rephrasing from the interface.

## 📸 Screenshot
**TODO**
Example of uploading an image and generating captions.

## 🛠 Tech Stack
- **Streamlit** for the frontend
- **Python** backend
- **instaloader** for Instagram scraping
- Custom captioning chain (via `app/chain.py`) using AI models:
    - **BLIP** for image understanding
    - **Gemini** for text generation
- **PIL**, **requests**, **logging** for media handling and utilities

## ⚠️ Limitations
- Instagram scraping works only with public post URLs.
- Rate limits or temporary blocks may occur if you fetch too frequently.
- Video content is currently not supported.

## 💡 Future Improvements
- Support full Instagram profile analysis
- Multi-language caption generation
- Support post loading from other social media platforms
- Add more mood options for captions
- Improve error handling and user feedback

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any questions, suggestions, or contributions, please open an issue on GitHub or contact the project maintainer.
