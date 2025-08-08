# image_gen.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from fetch_quote import get_quote

load_dotenv()

client = InferenceClient(
    provider="nebius",
    api_key=os.getenv("HF_TOKEN"),
)

def generate_image(quote: str, author: str):
    """
    Generate an image from a prompt that includes the quote text.
    The model embeds the quote as part of the image.
    """
    prompt = f"A clean, artistic motivational poster with the quote: '{quote}' — {author}"
    try:
        print(f"[INFO] Generating image for prompt:\n{prompt}")
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        return image
    except Exception as e:
        print(f"[ERROR] Image generation failed: {e}")
        raise

# For testing directly
if __name__ == "__main__":
    quote, author = get_quote()
    image = generate_image(quote, author)
    image.show()
