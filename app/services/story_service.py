def generate_stage_text(history=None):
    text = (
        "The excitement of graduation day still pulses through you as you sit in "
        "your favorite café. Your phone buzzes with congratulations, a reminder of "
        "the milestone you've just achieved. After years of hard work, the world now "
        "stretches before you, full of possibility."
    )
    return text


def generate_option_text(option=None, history=None):
    text = (
        "As you sip your latte, your thoughts drift to your partner of two years. "
        "You picture a future together: a cozy home, shared dreams, the warmth of "
        "family. It's a path promising deep connection and joy. But committing now "
        "would mean shaping your post-graduation life around this relationship. Some "
        "individual aspirations might need to adapt. You wonder: Is it time to "
        "embrace this path of love and family, with all its joys and challenges?"
    )
    return text


def generate_choice_title_text(choice=None, history=None):
    # figs = [
    #     {"choice": "family", "title": "family"},
    #     {"choice": "poet", "title": "poetry"},
    #     {"choice": "professor", "title": "academia"},
    #     {"choice": "adventurer", "title": "adventure"},
    #     {"choice": "athlete", "title": "athletics"},
    # ]

    title = "You choose your relationship."
    text = (
        "You choose to embrace love and family. With nervous excitement, you and your "
        "partner move in together, navigating the challenges of shared space and "
        "finances. Your relationship deepens as you support each other's dreams and "
        "weather life's storms together. Eventually, you exchange vows, surrounded by "
        "loved ones, embarking on a shared journey."
    )

    return (title, text)

def generate_no_choice_title_text(history=None):
    title = "You don't make a choice."
    text = (
        "As opportunities arise, you find yourself hesitating, always waiting for "
        "something better. You take temporary jobs, start and abandon hobbies, and "
        "maintain casual relationships. Days blend into weeks, then months, as you "
        "drift through life, never fully committing to any particular path, always "
        "keeping your options open."
    )

    return (title, text)