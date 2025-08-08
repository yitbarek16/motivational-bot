# run.py
from fetch_quote import get_quote
from find_image import search_image
from enhance_quote import enhance_quote
from compose_post import compose_post
from textblob import TextBlob
from collections import Counter
import re

# Fallback image if Pexels (or other provider) returns nothing
FALLBACK_IMAGE = "https://images.pexels.com/photos/414171/pexels-photo-414171.jpeg"

def extract_keywords(quote, top_n=4):
    """
    Try (in order):
      1) TextBlob noun_phrases
      2) TextBlob nouns (NN*)
      3) Top-frequency words (filtered)
      4) A tiny default list so search_image always gets something
    Returns a list of tokens suitable for an image search (no spaces).
    """
    blob = TextBlob(quote.lower())
    # 1) noun phrases (multi-word)
    noun_phrases = [p.replace(" ", "+") for p in getattr(blob, "noun_phrases", [])]
    if noun_phrases:
        return noun_phrases[:top_n]

    # 2) nouns via POS tags
    nouns = [word for word, tag in blob.tags if tag.startswith("NN")]
    nouns = [n for n in nouns if len(n) > 2]  # filter tiny tokens
    if nouns:
        return [n.replace(" ", "+") for n in nouns[:top_n]]

    # 3) frequency-based fallback
    words = re.findall(r"\b[a-z0-9']+\b", quote.lower())
    stop = {"the","and","for","with","that","this","from","your","you","are","not","but","all","have","will"}
    filtered = [w for w in words if w not in stop and len(w) > 2]
    most_common = [w for w, _ in Counter(filtered).most_common(top_n)]
    if most_common:
        return [w.replace(" ", "+") for w in most_common]

    # 4) final default
    return ["motivation", "growth", "success"]


def main():
    try:
        quote, author = get_quote()
    except Exception as e:
        print(f"[ERROR] Failed to fetch quote: {e}")
        return

    print(f"\n Original Quote:\n\"{quote}\" — {author}")

    # extract keywords for image search
    keywords = extract_keywords(quote)
    print(f"\n Extracted Keywords: {keywords}")

    # search for an image — don't crash if API fails
    try:
        image_url = search_image(keywords)
    except Exception as e:
        print(f"[WARN] Image search raised an exception: {e}")
        image_url = None

    if not image_url:
        print("[INFO] No image found from provider; using fallback image.")
        image_url = FALLBACK_IMAGE

    print(f"\n Image URL: {image_url}")

    # call enhance_quote with only the quote (match your enhance_quote signature)
    try:
        enhanced = enhance_quote(quote)
    except TypeError:
        # If your enhance_quote expects (quote, author), try that
        enhanced = enhance_quote(quote, author)
    except Exception as e:
        print(f"[WARN] Failed to enhance quote with model: {e}")
        enhanced = ""  # allow compose_post to proceed

    print(f"\n✨ Enhanced Quote:\n{enhanced if enhanced else '(no enhancement)'}")

    # Compose the post using the enhanced text when available
    post = compose_post(image_url, quote if not enhanced else enhanced, author)
    print("\n📢 Final Motivational Post:")
    print(post["caption"])
    print("🖼️ Image:", post["image"])


if __name__ == "__main__":
    main()
