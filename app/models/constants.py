
OPENAI_BASE_PROMPT = (
            "You are a creative social media assistant that helps user to reformulate base captions. "
            "Your goal is to rewrite image captions with a specific style focusing on a given social media.\n\n"
            "Base caption: {}\n"
            "Platform: {}\n"
            "Mood: {}\n"
            "{}\n"
            "Return a single creative caption only."
        )

GEMINI_BASE_PROMPT = OPENAI_BASE_PROMPT