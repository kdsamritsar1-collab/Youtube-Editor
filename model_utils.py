import google.generativeai as genai
import streamlit as st

def get_active_gemini_model():
    try:
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        for m in available_models:
            if "gemini-1.5-flash" in m.lower():
                return m
        return "models/gemini-1.5-flash"
    except:
        return "models/gemini-1.5-flash"