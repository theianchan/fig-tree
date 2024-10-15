from ..services.player_service import get_player_age
from ..services.choice_service import compile_player_history
from ..config import ANTHROPIC_API_KEY
import anthropic
import logging
import ast

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

    The message of the game is this: we live in an age of miracles, and you can have it
    all. Through commitment, community, and technology, you can walk down more paths in
    life than you can imagine when you're young. Take the player on an arc - when
    considering a path, the player can be hesitant about the sacrifices required.
    But as they age and commit, they find more and more creative ways to explore varied
    interests, or dive ever deeper into one. 
    
    DO NOT moralize the player's choices, make them feel like they made the wrong choice,
    or like they have spread themselves too thin. The player should have an overwhelmingly 
    rich life by the end of their journey.
    """

    logging.debug(
        f"""Prompting Claude with: 
        System:
        {system}
        ---
        Prompt:
        {prompt}
        """
    )

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
    prompt = f"""
        Here's the player's journey so far:
        ```
        {history}
        ```

        7 years have passed, and the player is arriving at a new crossroads.

        Instructions:

        1. Extend the story, returning your response as one paragraph of ~30 words.

        2. Describe the last 7 years as a consequence of the player's choice. You can
        describe ups, downs both. Draw from the player's journey and previously
        referenced events, choices, relationships.

        3. The player has grown, and is in a reflective state, but don't present any 
        new options yet.

        IMPORTANT: Your response should include ONLY THE STORY TEXT PARAGRAPH. It will 
        be consumed by a data pipeline expecting this format, so do not precede or 
        follow the response with any comments. 
        """
    text = get_claude_response(prompt)

    return text


def generate_option_text(player_id, option):
    history = compile_player_history(player_id)
    prompt = f"""
        Here's the player's journey so far:
        ```
        {history}
        ```

        The player is considering this path:
        ```
        {option}
        ```

        Instructions:

        1. Extend the story, returning your response as two paragraphs, separated by a 
        newline character "\n".

        2. The first paragraph should describe in ~30 words the concrete experiences that 
        are leading the player to consider this path. Invoke detailed settings and people.
        If the player's journey has ended in a specific setting, continue from there.

        3. The second paragraph should sketch out in ~30 words the allure of the path, 
        while hinting at its trade-offs. Refer to the player's journey if possible.
        It's possible for the player to dive deeper into a path already chosen.

        4. We provide some default values for paths (family, poet, professor, adventurer, 
        athlete) but the player can type in anything they want, so be prepared to handle 
        unexpected inputs.

        IMPORTANT: Your response should include ONLY TWO STORY TEXT PARAGRAPHS AND \n. 
        It will be consumed by a data pipeline expecting this format, so do not precede or 
        follow the response with any comments. 
        """
    text = get_claude_response(prompt)

    return text


def generate_choice_title_text(player_id, choice):
    history = compile_player_history(player_id, include_current_option=True)
    prompt = f"""
        Here's the player's journey so far:
        ```
        {history}
        ```

        The player has chosen this path:
        ```
        {choice}
        ```

        Instructions:

        1. Extend the story, returning your response as a dictionary with two keys 
        "title" and "text".

        2. The value of "title" should be a short title describing the choice ie.
        "You choose family." or "You choose poetry." or "You choose academia."

        3. The value of "text" should be a paragraph of ~30 words describing how 
        the player committed to their choice. Invoke detailed settings and people.

        4. We provide some default values for choices (family, poet, professor, adventurer, 
        athlete) but the player can type in anything they want, so be prepared to handle 
        unexpected inputs.

        IMPORTANT: Your response must be a dictionary with two keys "title" and "text". 
        It will be consumed by a data pipeline expecting this format, so do not precede or 
        follow the response with any comments. 
        """
    response = get_claude_response(prompt)
    response = ast.literal_eval(response)

    return response["title"], response["text"]


def generate_no_choice_title_text(player_id):
    title = "You don't make a choice."
    history = compile_player_history(player_id)
    prompt = f"""
        Here's the player's journey so far:
        ```
        {history}
        ```

        The player did not make a choice for their current stage.

        Instructions:

        1. Extend the story, returning your response as one paragraph of ~30 words.

        2. Describe how the player was indecisive, distracted, or otherwise unable to make 
        a choice. As the player ages, this should sound more like they're enjoying their
        life and less like they're wasting it.

        IMPORTANT: Your response should include ONLY THE STORY TEXT PARAGRAPH. It will 
        be consumed by a data pipeline expecting this format, so do not precede or 
        follow the response with any comments. 
        """
    text = get_claude_response(prompt)

    return (title, text)
