import streamlit as st
import requests
import os
from dotenv import load_dotenv
import base64

# Load API key
load_dotenv()
API_KEY = os.getenv("STABILITY_API_KEY")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🖼️ AI Image Generator")

# Inputs
prompt = st.text_input("Enter your image prompt:")
size = st.selectbox("Select Image Size", ["512x512", "768x768", "1024x1024"])
style = st.selectbox("Select Image Style", ["photorealistic", "cartoon", "fantasy", "cyberpunk", "oil painting", "none"])

# Clear history
if st.button("🧹 Clear History"):
    st.session_state.history = []
    st.success("History cleared.")

# Function to call Stability API
def get_image(prompt, size, style):
    width, height = map(int, size.split("x"))
    full_prompt = f"{prompt}, style: {style}" if style != "none" else prompt

    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, full_prompt),
        "output_format": (None, "jpeg"),
        "width": (None, str(width)),
        "height": (None, str(height))
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Generate image
if st.button("🎨 Generate Image"):
    if prompt:
        image_bytes = get_image(prompt, size, style)
        if image_bytes:
            st.image(image_bytes, caption="Generated Image")
            st.session_state.history.append({
                "prompt": prompt,
                "size": size,
                "style": style,
                "image": image_bytes
            })
    else:
        st.warning("Please enter a prompt.")

# Show history
if st.session_state.history:
    st.subheader("🕘 Image History")
    for i, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**{i}. Prompt:** {item['prompt']} | **Size:** {item['size']} | **Style:** {item['style']}")
        st.image(item["image"], width=300)

        # Download button
        b64 = base64.b64encode(item["image"]).decode()
        href = f'<a href="data:file/jpeg;base64,{b64}" download="generated_image_{i}.jpg">📥 Download Image</a>'
        st.markdown(href, unsafe_allow_html=True)
