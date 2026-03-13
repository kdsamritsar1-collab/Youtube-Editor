def get_audit_prompt(title, tags, desc, views, trending_data, channel_name):
    prompt = f"""
    You are a Professional YouTube Growth Auditor.
    
    Current Video Performance:
    - Title: {title}
    - Views: {views}
    - Current Tags: {tags}
    - Channel: {channel_name}
    
    Market Context (Google Trends):
    {trending_data}

    YOUR MISSION (Manual Suggestion Mode):
    1. Score the Title (0-10) and explain WHY. Provide 3 High-CTR alternatives.
    2. Audit the Tags: Identify weak tags and suggest 10 viral tags based on Trends.
    3. Description Check: Suggest where to naturally place keywords and social links.
    4. Action Plan: Give 3 specific steps the creator should do MANUALLY to improve reach.

    Format the output in a clean 'Audit Report Card' style using Markdown.
    """
    return prompt