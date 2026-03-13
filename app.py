import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import config_ai
import config_links
import config_legal
from model_utils import get_active_gemini_model

# API Setup
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Ruhani Design Lab", layout="wide")
st.title("🎨 Ruhani YouTube Design & SEO Lab")

v_url = st.text_input("अपना वीडियो लिंक डालें:")

# Sidebar for Font & Style Controls
with st.sidebar:
    st.header("🖌️ Text Styling")
    text_color = st.color_picker("Text Color", "#FFFFFF")
    font_size = st.slider("Font Size", 20, 200, 80)
    # आप GitHub में 'fonts' नाम का फोल्डर बनाकर उसमें .ttf फाइलें रख सकते हैं
    uploaded_font = st.file_uploader("Custom Font (.ttf) अपलोड करें (Optional)", type="ttf")

if st.button("Start Deep Audit & Design"):
    if "v=" in v_url:
        v_id = v_url.split("v=")[1].split("&")[0]
        
        with st.status("Fetching SEO & Visual Data..."):
            res = youtube.videos().list(part="snippet,statistics", id=v_id).execute()
            item = res['items'][0]
            thumb_url = item['snippet']['thumbnails'].get('maxres', item['snippet']['thumbnails']['high'])['url']
            
            img_data = requests.get(thumb_url).content
            
            # Gemini Vision Analysis
            active_model = get_active_gemini_model()
            model = genai.GenerativeModel(active_model)
            prompt = config_ai.get_audit_prompt(item['snippet']['title'], item['snippet'].get('tags', []), item['snippet']['description'], item['statistics'].get('viewCount', 0), "Ruhani Jot")
            
            response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
            
            st.session_state['img'] = Image.open(io.BytesIO(img_data))
            st.session_state['report'] = response.text

if 'report' in st.session_state:
    st.divider()
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 🖼️ Thumbnail Editor")
        overlay_text = st.text_area("थंबनेल टेक्स्ट (हिंदी/पंजाबी में भी लिख सकते हैं):", "ਨਵਾਂ ਕੀਰਤਨ 2026")
        
        # Position Controls
        pos_x = st.slider("Horizontal Position (X)", 0, st.session_state['img'].width, 50)
        pos_y = st.slider("Vertical Position (Y)", 0, st.session_state['img'].height, 50)

        img_preview = st.session_state['img'].copy()
        draw = ImageDraw.Draw(img_preview)
        
        # Font Loading Logic
        try:
            if uploaded_font:
                font = ImageFont.truetype(uploaded_font, font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Text Overlay with Shadow for readability
        draw.text((pos_x+2, pos_y+2), overlay_text, fill="black", font=font) # Shadow
        draw.text((pos_x, pos_y), overlay_text, fill=text_color, font=font)
        
        st.image(img_preview, use_container_width=True)
        
        # Download the new design
        buf = io.BytesIO()
        img_preview.save(buf, format="PNG")
        st.download_button("Download New Concept", buf.getvalue(), "new_thumbnail.png", "image/png")

    with col2:
        st.markdown(st.session_state['report'])

st.divider()
st.caption("Custom Font Support Enabled | Powered by Ruhani Jot Tech Stack")
