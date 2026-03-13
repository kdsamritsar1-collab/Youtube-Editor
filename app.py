import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import requests
import config_ai
import config_links
import config_legal
from model_utils import get_active_gemini_model

# API Keys from Streamlit Secrets
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Clients Initialize
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Ruhani SEO & Thumbnail Auditor", layout="wide")
st.title("🧐 Ruhani YouTube SEO & Thumbnail Auditor")
st.write("अपना वीडियो लिंक डालें और AI से उसकी कमियाँ, थंबनेल एनालिसिस और सुधार जानें।")

v_url = st.text_input("अपना वीडियो लिंक पेस्ट करें:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Run Full Audit (SEO + Thumbnail)"):
    if "v=" in v_url:
        v_id = v_url.split("v=")[1].split("&")[0]
        
        with st.status("वीडियो और थंबनेल का विश्लेषण किया जा रहा है...", expanded=True) as status:
            try:
                # 1. YouTube Data Fetch
                res = youtube.videos().list(part="snippet,statistics", id=v_id).execute()
                snippet = res['items'][0]['snippet']
                stats = res['items'][0]['statistics']
                
                # Thumbnails में से सबसे हाई क्वालिटी वाली इमेज का URL लें
                thumb_url = snippet['thumbnails'].get('maxres', snippet['thumbnails']['high'])['url']
                
                # 2. थंबनेल इमेज को डाउनलोड करना (Gemini को भेजने के लिए)
                img_data = requests.get(thumb_url).content
                image_parts = [{"mime_type": "image/jpeg", "data": img_data}]

                # 3. Gemini Audit Call with Vision
                # नोट: थंबनेल देखने के लिए हमें 'gemini-1.5-pro' या 'flash' मॉडल चाहिए
                active_model = get_active_gemini_model()
                model = genai.GenerativeModel(active_model)
                
                prompt = config_ai.get_audit_prompt(
                    snippet['title'], 
                    snippet.get('tags', []), 
                    snippet['description'], 
                    stats.get('viewCount', 0),
                    "Ruhani Jot"
                )
                
                # प्रॉम्ट और इमेज दोनों एक साथ भेजें
                response = model.generate_content([prompt, image_parts[0]])
                report_text = response.text
                
                status.update(label="ऑडिट पूरा हुआ!", state="complete")

                # --- Results Display ---
                st.divider()
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(thumb_url, caption="Current Video Thumbnail", use_container_width=True)
                    st.metric("Total Views", stats.get('viewCount', 0))
                    
                    # Report Download Button
                    st.download_button(
                        label="📄 पूरी रिपोर्ट डाउनलोड करें (.txt)",
                        data=report_text,
                        file_name=f"full_audit_report_{v_id}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:
                    # यहाँ AI की पूरी रिपोर्ट दिखेगी जिसमें थंबनेल एनालिसिस भी शामिल है
                    st.markdown(report_text)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("कृपया सही YouTube लिंक डालें।")

st.divider()
st.caption("Developed for @ruhanijot | SEO + Thumbnail Modular Suite")
