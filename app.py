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

st.set_page_config(page_title="Ruhani SEO & Thumbnail Lab", layout="wide")
st.title("🧐 Ruhani SEO & Thumbnail Designer Lab")

v_url = st.text_input("YouTube लिंक डालें:")

if st.button("Run Deep Audit"):
    if "v=" in v_url:
        v_id = v_url.split("v=")[1].split("&")[0]
        
        with st.status("Analyzing SEO & Visuals...", expanded=True):
            # 1. Fetch Data
            res = youtube.videos().list(part="snippet,statistics", id=v_id).execute()
            snippet = res['items'][0]['snippet']
            stats = res['items'][0]['statistics']
            thumb_url = snippet['thumbnails'].get('maxres', snippet['thumbnails']['high'])['url']
            
            # 2. Vision Analysis
            img_response = requests.get(thumb_url)
            img_data = img_response.content
            
            active_model = get_active_gemini_model()
            model = genai.GenerativeModel(active_model)
            prompt = config_ai.get_audit_prompt(snippet['title'], snippet.get('tags', []), snippet['description'], stats.get('viewCount', 0), "Ruhani Jot")
            
            response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
            
            # Save data in session for the Overlay Tool
            st.session_state['current_img'] = Image.open(io.BytesIO(img_data))
            st.session_state['report'] = response.text
            st.session_state['v_id'] = v_id

if 'report' in st.session_state:
    st.divider()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(st.session_state['current_img'], caption="Original Thumbnail", use_container_width=True)
        st.markdown("### 🛠️ Thumbnail Overlay Tool")
        overlay_text = st.text_input("थंबनेल पर नया टेक्स्ट लिख कर देखें:", "Best Gurbani 2026")
        
        if st.button("Apply Overlay Preview"):
            img = st.session_state['current_img'].copy()
            draw = ImageDraw.Draw(img)
            # बेसिक फॉन्ट सेटअप (Streamlit Cloud पर डिफॉल्ट फॉन्ट लोड होता है)
            draw.text((50, 50), overlay_text, fill="white", stroke_fill="black", stroke_width=2)
            st.image(img, caption="New Concept Preview", use_container_width=True)
            st.info("यह सिर्फ एक प्रीव्यू है ताकि आप डिज़ाइन का अंदाज़ा लगा सकें।")

    with col2:
        st.markdown(st.session_state['report'])

st.divider()
st.caption("Developed for @ruhanijot | SEO + Vision + Design Tool")
