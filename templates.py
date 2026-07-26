"""
Use-case templates for PromptWriterBot.

Each template defines:
- name: display name shown in menus
- category: which category button it lives under
- needs_tone: whether the tone-selection step should be shown
- prompt: instruction sent to the LLM, with {input} and {tone} placeholders
"""

CATEGORIES = {
    "writing": "✍️ Writing",
    "business": "💼 Business",
    "marketing": "📢 Marketing",
    "social": "🎬 Social & Video",
    "utility": "🔧 Rewrite & Utility",
}

TEMPLATES = {
    # ---- Writing ----
    "blog_idea": {
        "name": "Blog Idea & Outline",
        "category": "writing",
        "needs_tone": False,
        "prompt": (
            "Generate a compelling blog post idea (title) and a short outline "
            "(4-6 bullet points) for a blog about: {input}. "
            "Keep it practical and specific."
        ),
    },
    "blog_intro": {
        "name": "Blog Section Intro",
        "category": "writing",
        "needs_tone": True,
        "prompt": (
            "Write an engaging introduction paragraph (3-5 sentences) for a blog post "
            "about: {input}. Tone: {tone}. Hook the reader in the first sentence."
        ),
    },
    "blog_section": {
        "name": "Blog Section Writing",
        "category": "writing",
        "needs_tone": True,
        "prompt": (
            "Write a well-structured blog section (150-250 words) covering: {input}. "
            "Tone: {tone}. Use clear paragraphs, no headings needed."
        ),
    },
    "song_lyrics": {
        "name": "Song Lyrics",
        "category": "writing",
        "needs_tone": True,
        "prompt": (
            "Write original song lyrics (verse + chorus) inspired by the theme: {input}. "
            "Tone/mood: {tone}. Make it rhythmic and evocative, and make clear this is an original composition."
        ),
    },
    # ---- Business ----
    "product_description": {
        "name": "Product Description",
        "category": "business",
        "needs_tone": True,
        "prompt": (
            "Write a persuasive e-commerce product description for: {input}. "
            "Tone: {tone}. Highlight key benefits and include a short closing hook. "
            "Keep it under 120 words."
        ),
    },
    "email": {
        "name": "Email",
        "category": "business",
        "needs_tone": True,
        "prompt": (
            "Write a clear, well-structured email about: {input}. "
            "Tone: {tone}. Include a subject line, greeting, body, and sign-off."
        ),
    },
    "cold_email": {
        "name": "Cold Outreach Email",
        "category": "business",
        "needs_tone": True,
        "prompt": (
            "Write a short, high-converting cold outreach email for this context: {input}. "
            "Tone: {tone}. Keep it under 120 words, personal-sounding, with a clear single call-to-action."
        ),
    },
    "business_idea_pitch": {
        "name": "Business Idea Pitch",
        "category": "business",
        "needs_tone": True,
        "prompt": (
            "Write a concise elevator pitch (under 100 words) for this business idea: {input}. "
            "Tone: {tone}. Cover the problem, the solution, and why now."
        ),
    },
    "job_description": {
        "name": "Job Description",
        "category": "business",
        "needs_tone": False,
        "prompt": (
            "Write a professional job description for: {input}. "
            "Include a short intro, 5-6 responsibilities, and 4-5 requirements."
        ),
    },
    "interview_questions": {
        "name": "Interview Questions",
        "category": "business",
        "needs_tone": False,
        "prompt": (
            "Generate 8 thoughtful interview questions for this role/topic: {input}. "
            "Mix behavioral and technical/practical questions."
        ),
    },
    "testimonial": {
        "name": "Customer Testimonial (sample)",
        "category": "business",
        "needs_tone": True,
        "prompt": (
            "Write a realistic sample customer testimonial for: {input}. "
            "Tone: {tone}. Keep it under 60 words and specific, not generic. "
            "Clearly this is a sample/template testimonial, not a real quote from a real person."
        ),
    },
    # ---- Marketing ----
    "fb_ad": {
        "name": "Facebook/Instagram Ad Copy",
        "category": "marketing",
        "needs_tone": True,
        "prompt": (
            "Write a scroll-stopping Facebook/Instagram ad (primary text + headline) for: {input}. "
            "Tone: {tone}. Keep primary text under 90 words, headline under 8 words."
        ),
    },
    "google_ad": {
        "name": "Google Search Ad Copy",
        "category": "marketing",
        "needs_tone": True,
        "prompt": (
            "Write Google Search ad copy for: {input}. "
            "Tone: {tone}. Provide 3 headlines (under 30 characters each) and 2 descriptions "
            "(under 90 characters each)."
        ),
    },
    "tagline": {
        "name": "Tagline / Slogan",
        "category": "marketing",
        "needs_tone": True,
        "prompt": (
            "Generate 8 punchy tagline/slogan options for: {input}. Tone: {tone}. "
            "Keep each under 8 words."
        ),
    },
    "cta": {
        "name": "Call To Action",
        "category": "marketing",
        "needs_tone": True,
        "prompt": (
            "Generate 8 short call-to-action phrases for: {input}. Tone: {tone}. "
            "Each under 6 words."
        ),
    },
    "seo_meta": {
        "name": "SEO Meta Title & Description",
        "category": "marketing",
        "needs_tone": False,
        "prompt": (
            "Write an SEO-optimized meta title (under 60 characters) and meta description "
            "(under 155 characters) for a page about: {input}."
        ),
    },
    # ---- Social & Video ----
    "instagram_caption": {
        "name": "Instagram Caption",
        "category": "social",
        "needs_tone": True,
        "prompt": (
            "Write an Instagram caption for: {input}. Tone: {tone}. "
            "Include 5 relevant hashtags at the end."
        ),
    },
    "linkedin_post": {
        "name": "LinkedIn Post",
        "category": "social",
        "needs_tone": True,
        "prompt": (
            "Write a LinkedIn post about: {input}. Tone: {tone}. "
            "Use short paragraphs/line breaks for readability, end with a soft question to drive engagement."
        ),
    },
    "tweet": {
        "name": "Tweet / X Post",
        "category": "social",
        "needs_tone": True,
        "prompt": (
            "Write 3 alternative tweet/X post options (under 280 characters each) about: {input}. "
            "Tone: {tone}."
        ),
    },
    "youtube_title_desc": {
        "name": "YouTube Title & Description",
        "category": "social",
        "needs_tone": True,
        "prompt": (
            "Write a clickable YouTube video title (under 60 characters) and a description "
            "(2-3 sentences plus 3 hashtags) for a video about: {input}. Tone: {tone}."
        ),
    },
    # ---- Utility / Rewrite ----
    "text_improver": {
        "name": "Rewrite / Improve Text",
        "category": "utility",
        "needs_tone": True,
        "prompt": (
            "Rewrite and improve the following text for clarity and flow. Tone: {tone}. "
            "Keep the original meaning intact.\n\nText:\n{input}"
        ),
    },
    "grammar_fix": {
        "name": "Fix Grammar & Spelling",
        "category": "utility",
        "needs_tone": False,
        "prompt": (
            "Correct the grammar, spelling, and punctuation in the following text. "
            "Return only the corrected text.\n\nText:\n{input}"
        ),
    },
    "summarize": {
        "name": "Summarize Text",
        "category": "utility",
        "needs_tone": False,
        "prompt": (
            "Summarize the following text into 3-4 concise bullet points.\n\nText:\n{input}"
        ),
    },
    "expand": {
        "name": "Expand Text",
        "category": "utility",
        "needs_tone": True,
        "prompt": (
            "Expand the following text with more detail and supporting points, roughly doubling "
            "its length. Tone: {tone}.\n\nText:\n{input}"
        ),
    },
}

TONES = [
    "Convincing", "Casual", "Enthusiastic", "Formal", "Funny",
    "Professional", "Witty", "Informative", "Friendly", "Bold",
]


def templates_in_category(category_id: str):
    return {tid: t for tid, t in TEMPLATES.items() if t["category"] == category_id}
