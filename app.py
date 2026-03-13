import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from pytrends.request import TrendReq
import config_ai
import config_links
import config_legal
from model_utils import get_active_gemini_model

# API Setup from Secrets
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize Clients
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)

st.set_page_config(page_title="Ruhani SEO Auditor", layout="wide")
st.title("🧐 Ruhani YouTube SEO Auditor (Expert Mode)")

v_url = st.text_input("Apni video ka link paste karein:")

if st.button("Analyze Video"):
    if "v=" in v_url:
        v_id = v_url.split("v=")[1].split("&")[0]
        
        with st.spinner('Gemini AI aur Trends data fetch kiya ja raha hai...'):
            try:
                # 1. YouTube Data API se info nikalna
                res = youtube.videos().list(part="snippet,statistics", id=v_id).execute()
                snippet = res['items'][0]['snippet']
                stats = res['items'][0]['statistics']
                
                # 2. Google Trends se context lena (Niche ke mutabik)
                main_keyword = snippet['title'].split("|")[0].strip()
                pytrends.build_payload([main_keyword], timeframe='today 3-m', geo='IN', gprop='youtube')
                trends_df = pytrends.interest_over_time()
                trends_context = "Trending well" if not trends_df.empty else "Low search volume currently"

                # 3. External Gemini Model Call
                active_model = get_active_gemini_model()
                model = genai.GenerativeModel(active_model)
                
                # Prompt taiyar karna
                audit_prompt = config_ai.get_audit_prompt(
                    snippet['title'], 
                    snippet.get('tags', []), 
                    snippet['description'], 
                    stats.get('viewCount', 0),
                    trends_context,
                    "Ruhani Jot"
                )
                
                response = model.generate_content(audit_prompt)
                
                # 4. Result Display (Manual View)
                st.divider()
                st.header("📊 Video Audit Report")
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(snippet['thumbnails']['high']['url'], use_container_width=True)
                    st.metric("Views", stats.get('viewCount', 0))
                
                with c2:
                    st.markdown(response.text)

                # Manual Suggestion Section
                st.divider()
                st.subheader("📋 Manual Copy-Paste Section")
                st.info("Aap in suggestions ko copy karke apne YouTube Studio mein manually update kar sakte hain.")
                
                st.write("**Suggested Description End Piece:**")
                st.code(config_links.get_social_links() + config_legal.get_disclaimer())

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Sahi YouTube link dalein.")

st.caption("Developed for @ruhanijot | Manual Audit v1.0")