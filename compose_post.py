# compose_post.py
def compose_post(image_url, quote, author):
    caption = f"{quote}\n\n— {author}\n📸 via Pexels"
    return {"image": image_url, "caption": caption}

