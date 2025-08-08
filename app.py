# app.py
import streamlit as st
from fetch_quote import get_quote
from enhance_quote import enhance_quote
from image import generate_image
from PIL import Image

st.set_page_config(page_title="Motivational Bot", layout="centered")

st.title("Motivational Quote Generator")

if st.button("Generate Post"):
    with st.spinner("Creating your motivational post..."):
        try:
            # Step 1: Fetch Quote
            quote, author = get_quote()

            # Step 2: Enhance Quote
            enhanced = enhance_quote(quote, author)
            if not enhanced:
                enhanced = quote  # fallback

            # Step 3: Generate Image
            image = generate_image(quote, author)

            # Display: Image first, then quotes
            st.image(image, use_column_width=True)
            st.markdown(f"**“{quote}” — {author}**")
            st.write(enhanced)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
