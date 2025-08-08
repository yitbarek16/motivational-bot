# runimage.py

from fetch_quote import get_quote
from find_image import search_image
from textblob import TextBlob
from collections import Counter
import re

FALLBACK_IMAGE = "https://images.pexels.com/photos/414171/pexels-photo-414171.jpeg"

def extract_keywords(quote, top_n=4):
    """
    Improved keyword extraction for better image matching.
    """
    blob = TextBlob(quote.lower())

    noun_phrases = [p.replace(" ", "+") for p in blob.noun_phrases]
    nouns = [word for word, tag in blob.tags if tag.startswith("NN") and len(word) > 2]
    adjectives = [word for word, tag in blob.tags if tag.startswith("JJ") and len(word) > 2]

    words = re.findall(r"\b[a-z0-9']+\b", quote.lower())
    stop = {"the", "and", "for", "with", "that", "this", "from", "your", "you", "are", "not", "but", "all", "have", "will"}
    filtered = [w for w in words if w not in stop and len(w) > 2]
    freq_words = [w for w, _ in Counter(filtered).most_common(top_n)]

    # Combine and deduplicate
    candidates = noun_phrases + nouns + adjectives + freq_words
    seen = set()
    final_keywords = []
    for word in candidates:
        token = word.replace(" ", "+")
        if token not in seen:
            seen.add(token)
            final_keywords.append(token)
        if len(final_keywords) >= top_n:
            break

    if not final_keywords:
        final_keywords = ["motivation", "growth", "success"]

    return final_keywords


def main():
    try:
        quote, author = get_quote()
    except Exception as e:
        print(f"[ERROR] Failed to fetch quote: {e}")
        return

    print(f"\n📝 Quote:\n\"{quote}\" — {author}")

    keywords = extract_keywords(quote)
    print(f"\n🔍 Extracted Keywords: {keywords}")

    try:
        image_url = search_image(keywords)
    except Exception as e:
        print(f"[WARN] Image search failed: {e}")
        image_url = None

    if not image_url:
        print("[INFO] Using fallback image.")
        image_url = FALLBACK_IMAGE

    print(f"\n🖼️ Image URL: {image_url}")


if __name__ == "__main__":
    main()
