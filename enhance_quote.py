# enhance_quote.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

def enhance_quote(quote, author):
    prompt = f"""Here's a motivational quote:
"{quote} — {author}"

Now expand on it with a short, uplifting message that inspires action and hope."""
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:novita",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] Failed to enhance quote: {e}")
        return None
