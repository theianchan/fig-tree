from ..services.player_service import get_player_age
from ..services.choice_service import compile_player_history
from ..config import ANTHROPIC_API_KEY
import anthropic
import logging

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_claude_response(prompt):
    system = """
    Please generate text for a text-based game. The game is based on the protagonist's 
    vision of a fig tree from The Bell Jar by Sylvia Plath, and allows players to simulate 
    different paths they might take in a lifetime. 

    Writing guidelines:

    1. Write in the second person.
    2. Write in the present tense.
    3. Avoid stretching out the text with abstractions. Prefer details, and be imaginative.
    4. The one exception is names - you can introduce characters ("your best friend", 
    "your son", "someone you're casually dating"), but don't create names for them.
    5. When describing the player or their romantic relationships, use gender-neutral 
    terminology (ie. "partner" instead of "wife/boyfriend", "they" instead of "he/she").
    6. Stylistically, mimic Sylvia Plath in The Bell Jar - be introspective, personal, 
    crisp, and vivid, blending realistic detail with poetic imagery. 
    7. Do not use literal fig tree imagery in your writing.
    8. Use the player's journey so far to inform the narrative.
        """
    
    logging.debug(f"""Prompting Claude with: 
        System:
        {system}
        ---
        Prompt:
        {prompt}
        """)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.5,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    logging.debug(f"Received: {message.content[0].text}")
    return message.content[0].text


def generate_stage_text(player_id):
    if get_player_age(player_id) == 21:
        return (
            "The excitement of graduation day still pulses through you as you sit in "
            "your favorite coffeeshop. Your phone buzzes with congratulations, a reminder "
            "of the milestone you've just achieved. After years of hard work, the world now "
            "stretches before you, full of possibility."
        )

    history = compile_player_history(player_id)
    prompt = """
        The player is arriving at a new stage in life. 
        """
    text = prompt
    return text


def generate_option_text(player_id, option):
    history = compile_player_history(player_id)
    prompt = f"""
        Here's the player's journey so far:
        ```
        {history}
        ```

        The player is currently considering this path:
        ```
        {option}
        ```

        Instructions:

        1. Return your response as two paragraphs, separated by a newline character \n.
        2. The first paragraph should describe in 30-50 words the concrete experiences that 
        are leading the player to consider this path. Invoke detailed settings and people.
        If the player's journey has ended in a specific setting, continue from there.
        3. The second paragraph should sketch out in 20-40 words the allure of the path, 
        while hinting at its trade-offs. Refer to the player's journey if possible.
        4. We provide some default values for paths (family, poet, professor, adventurer, athlete)
        but the player can type in anything they want, so be prepared to handle unexpected inputs.

        IMPORTANT: Your response should include ONLY TWO STORY TEXT PARAGRAPHS AND \n. 
        It will be consumed by a data pipeline expecting this format, so do not precede or 
        follow the response with any comments. 
        """
    text = get_claude_response(prompt)

    return text


def generate_choice_title_text(choice=None, history=None):
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
