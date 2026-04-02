"""CSC111 Winter 2026 Project 2 Phase 2
Linguistic Pattern Recognition for MBTI Classification: A Data-Driven Decision Tree Analysis of Social Media Posts

Module Description
===============================
This module implements the Graphical User Interface for the MBTI Personality Predictor Quiz
using the Pygame library.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

import pygame
from main import MBTITree
from filter_data import twitter_user_files, reddit_user_files, mixed_user_files

W, H = 1000, 750
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (118, 156, 188)
HOVER_COLOR = (101, 144, 180)

QUESTIONS = {
    "social_score": "I actively engage with others online by tagging them, using hashtags, or sharing links.",
    "complexity_score": "I prefer using abstract metaphors and a sophisticated vocabulary over simple facts.",
    "expressiveness_score": "My writing is often filled with emotion, exclamation points, and emojis.",
    "structure_score": "I put a lot of effort into making my posts organized and grammatically correct.",
    "average_post_length": "I usually write long, detailed explanations rather than short snippets."
}

OPTIONS = [
    ("Strongly disagree", 0.0),
    ("Disagree", 0.25),
    ("Neutral", 0.5),
    ("Agree", 0.75),
    ("Strongly agree", 1.0),
]


def run_quiz() -> None:
    """Initialize the MBTI decision tree from CSV datasets and launch the Pygame event loop
    to conduct the personality quiz. This function handles the initialization of pygame, the data-driven
    tree construction, and the transition between question states.
    """
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("MBTI Personality Quiz")

    font = pygame.font.SysFont('Helvetica', 25)
    font_result = pygame.font.SysFont('Helvetica', 55, bold=True)

    # Initialize Data and Tree
    users = (twitter_user_files('mbti_labels.csv', 'user_info.csv', 'user_tweets.csv')
             + reddit_user_files('reddit_post_small.csv')
             + mixed_user_files('misc_text_posts.csv'))

    tree_manager = MBTITree()
    loaded_tree = tree_manager.build_mbti_tree(users)

    # UI State
    running = True
    curr_q_idx = 0
    question_keys = list(QUESTIONS)
    user_answers = {key: 0.0 for key in QUESTIONS}

    # Create Buttons (Centered)
    button_width = 400
    button_height = 50
    choices_rects = []

    for i in range(len(OPTIONS)):
        # Calculate Y position: start at 250 and move down 70 pixels per button
        rect = pygame.Rect((W // 2 - button_width // 2), 250 + (i * 70),
                           button_width, button_height)
        choices_rects.append(rect)

    # code adapted from Gemini, particularly for conciseness in logic since the original code
    # was unnecessarily complex since it was adapted from a previous pygame high school project
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and curr_q_idx < len(question_keys):
                clicked_idx = handle_mouse_click(mouse_pos, choices_rects)
                if clicked_idx != -1:
                    user_answers[question_keys[curr_q_idx]] = OPTIONS[clicked_idx][1]
                    curr_q_idx += 1

        if curr_q_idx < len(question_keys):
            draw_quiz_ui(screen, font, curr_q_idx, question_keys, choices_rects, mouse_pos)
        else:
            display_results(screen, font_result, font, loaded_tree.predict(user_answers))

        pygame.display.flip()
    pygame.quit()


def handle_mouse_click(mouse_pos: tuple[int, int], choices_rects: list[pygame.Rect]) -> int:
    """Return the index of the Rect in choices_rects that contains mouse_pos. Return -1 if
    mouse_pos is not colliding with any Rect.

    Preconditions:
        - all(isinstance(r, pygame.Rect) for r in choices_rects)
    """
    for i in range(len(choices_rects)):
        if choices_rects[i].collidepoint(mouse_pos):
            return i
    return -1


def draw_quiz_ui(screen: pygame.Surface, font: pygame.font.Font,
                 curr_q_idx: int, question_keys: list[str],
                 choices_rects: list[pygame.Rect], mouse_pos: tuple[int, int]) -> None:
    """"Render the current question and the five Likert-scale response buttons onto the screen.
    Buttons change color to HOVER_COLOR if mouse_pos is hovering over them.

    Preconditions:
        - 0 <= curr_q_idx < len(question_keys)
        - len(choices_rects) == 5
    """
    current_key = question_keys[curr_q_idx]
    wrapped_lines = wrap_text(QUESTIONS[current_key], font, W - 100)

    # Draw Question
    for i in range(len(wrapped_lines)):
        txt_surface = font.render(wrapped_lines[i], True, BLACK)
        screen.blit(txt_surface, txt_surface.get_rect(center=(W // 2, 100 + i * 35)))

    # Draw Buttons
    for i in range(len(choices_rects)):
        rect = choices_rects[i]
        color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, color, rect, border_radius=8)

        label_text = font.render(OPTIONS[i][0], True, BLACK)
        label_rect = label_text.get_rect(center=rect.center)
        screen.blit(label_text, label_rect)


def display_results(screen: pygame.Surface, f_big: pygame.font.Font,
                    f_small: pygame.font.Font, mbti_type: str) -> None:
    """Render the final predicted MBTI type in a large font at the center of the screen and
    display an exit hint.

    Preconditions:
        - len(mbti_type) == 4
    """
    res_str = f"Your Predicted Type: {mbti_type.upper()}"
    res_surface = f_big.render(res_str, True, BLACK)
    screen.blit(res_surface, res_surface.get_rect(center=(W // 2, H // 2)))

    hint_surface = f_small.render("Close window to exit", True, (150, 150, 150))
    screen.blit(hint_surface, hint_surface.get_rect(center=(W // 2, H // 2 + 100)))


def wrap_text(text: str, font_obj: pygame.font.Font, max_width: int) -> list[str]:
    """Break a string into multiple lines such that each line's rendered width
    is less than or equal to max_width.

    Preconditions:
        - max_width > 0
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = (current_line + " " + word).strip()
        if font_obj.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines


if __name__ == '__main__':
    # Uncomment the following lines for code checking/debugging purposes.
    # We recommend commenting out these lines when working with large datasets to reduce runtime.

    run_quiz()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,

        # 'E1101' added to allow pygame method usage,
        # 'R0914' and 'R0913' added because using multiple locals and arguments is required,
        # splitting logic would make code unnecessarily broken up/hard to follow
        'disable': ['static_type_checker', 'E1101', 'R0914', 'R0913'],

        'extra-imports': ['filter_data', 'linguistic_scores', 'mbti_helper', 'main', 'pygame'],
        'allowed-io': ['ask_user', 'run_mbti_test'],
        'max-nested-blocks': 4
    })
