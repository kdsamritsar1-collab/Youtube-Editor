def get_social_links():
    """
    यह फंक्शन आपके सभी सोशल मीडिया हैंडल्स को एक सुंदर और प्रोफेशनल 
    फॉर्मेट में वापस (return) करता है।
    """
    
    # 1. अपने सोशल मीडिया लिंक्स यहाँ बदलें
    links = {
        "instagram": "https://www.instagram.com/ruhanijot",
        "facebook": "https://www.facebook.com/ruhani.saanjh",
        "podcast": "https://www.youtube.com/@SikhiSidakPodcast",
        "main_channel": "https://www.youtube.com/@RuhaniJot",
        "kids_channel": "https://www.youtube.com/@hindi-fun-tv"
    }
    
    # 2. टेक्स्ट फॉर्मेट तैयार करना जो वीडियो डिस्क्रिप्शन के अंत में जुड़ेगा
    formatted_text = f"""
🔗 Connect with us for more Spiritual & Educational Content:

📸 Instagram: {links['instagram']}
👤 Facebook: {links['facebook']}
🎙️ Sikhi Sidak Podcast: {links['podcast']}
📺 Subscribe our Main Channel: {links['main_channel']}
👶 Kids Stories & Rhymes: {links['kids_channel']}

🙏 Like, Share & Subscribe to support our mission!
    """
    
    return formatted_text

def get_raw_links():
    """
    अगर आपको कभी सिर्फ कच्चे (raw) लिंक्स की डिक्शनरी चाहिए हो, 
    तो आप इस फंक्शन का उपयोग कर सकते हैं।
    """
    return {
        "IG": "https://www.instagram.com/ruhanijot",
        "FB": "https://www.facebook.com/ruhani.saanjh"
    }