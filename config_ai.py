def get_audit_prompt(title, tags, desc, views, channel_name):
    prompt = f"""
    You are a Senior YouTube Growth Consultant and Thumbnail Designer.
    Analyze the provided Video Metadata and Thumbnail Image to create a critical Audit Report.

    VIDEO DETAILS:
    - Title: {title}
    - Current Tags: {tags}
    - Views: {views}
    - Channel: {channel_name}

    YOUR AUDIT TASK (Manual Suggestion Mode):
    1. **Title & Tags:** Score the Title (0-10), suggest 3 high-CTR alternatives, and 10 viral tags.
    2. **Description:** Audit for keyword placement and structure.

    YOUR THUMBNAIL TASK:
    1. **Critical Analysis:** Analyze the current thumbnail. Is the text readable? Are the colors engaging? Does it convey emotion? Give it a score (0-10).
    2. **AI-Based Suggestion:** Provide 2 complete concepts for a NEW, high-CTR thumbnail.
       - Concept 1: Focal point (e.g., specific expression), Colors, Text overlay.
       - Concept 2: Story-based or Curiosity-based design.

    Format your output in a professional 'Audit Report Card' style using Markdown.
    """
    return prompt
