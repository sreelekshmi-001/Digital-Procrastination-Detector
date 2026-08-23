def classify_activity(window_title):
    """
    Classify the active window as:
    PRODUCTIVE, DISTRACTION, or NEUTRAL.
    """

    title = window_title.lower()

    # -----------------------------
    # PRODUCTIVE APPLICATIONS
    # -----------------------------
    productive_keywords = [
        "visual studio code",
        "ChatGPT Classic"
        "pycharm",
        "jupyter",
        "python",
        "github",
        "stackoverflow",
        "microsoft word",
        "microsoft excel",
        "powerpoint",
        "google docs",
        "google drive",
        "google sheets",
        "google slides",
        "chatgpt",
        "chatgpt classic",
        "gemini",
        "claude",
        "copilot",
        "notion",
        "figma",
        "canva",
        "coursera",
        "udemy",
        "edx",
        "linkedin learning"
    ]

    # -----------------------------
    # DISTRACTION APPLICATIONS
    # -----------------------------
    distraction_keywords = [
        "youtube",
        "instagram",
        "facebook",
        "netflix",
        "tiktok",
        "twitter",
        "x.com",
        "reddit",
        "twitch",
        "prime video",
        "pinterest",
        "snapchat",
        "spotify"
    ]

    # -----------------------------
    # CHECK PRODUCTIVE
    # -----------------------------
    for keyword in productive_keywords:
        if keyword in title:
            return "PRODUCTIVE"

    # -----------------------------
    # CHECK DISTRACTION
    # -----------------------------
    for keyword in distraction_keywords:
        if keyword in title:
            return "DISTRACTION"

    # -----------------------------
    # EVERYTHING ELSE
    # -----------------------------
    return "NEUTRAL"