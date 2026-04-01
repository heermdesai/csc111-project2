"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Module Description
===============================
This module contains the visualisation/UI for the mbti quiz.

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

pygame.init()

# window
W, H = 1000, 750
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("MBTI Personality Quiz")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (118, 156, 188)
HOVER = (101, 144, 180)

# font
font = pygame.font.SysFont('Arial', 25)
font_result = pygame.font.SysFont('Arial', 55)

# ── question + options ─────────────────────────────────
QUESTIONS = {"social_score": "I actively engage with others online by tagging them, using hashtags, or sharing links.",
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

# choice buttons
choices = []
y = 200
for _ in OPTIONS:
    c = pygame.Rect(100, y, 500, 50)
    choices.append(c)
    y += 60

# vars
running = True
curr_question = 0
question_types = list(QUESTIONS)
answers = {
    "social_score": 0.0,
    "complexity_score": 0.0,
    "expressiveness_score": 0.0,
    "structure_score": 0.0,
    "average_post_length": 0.0
}


# CHAT
def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Split text on newlines first, then word-wrap each line to max_width."""
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        current = ''
        for word in words:
            test = (current + ' ' + word).strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


users = (twitter_user_files('mbti_labels.csv', 'user_info.csv', 'user_tweets.csv')
         + reddit_user_files('reddit_post_small.csv')
         + mixed_user_files('misc_text_posts.csv'))

tree = MBTITree()
loaded_tree = tree.build_mbti_tree(users)

current_node = loaded_tree   # pointer that moves down the tree as user answers
result = ''                  # filled in once we hit a leaf


# main loop
while running:
    screen.fill(WHITE)
    mouse_position = pygame.mouse.get_pos()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and curr_question < len(question_types):

            key = question_types[curr_question]
            i = 0
            for rect in choices:
                if rect.collidepoint(mouse_position):
                    answers[key] = OPTIONS[i][1]  # store score
                    curr_question += 1
                    i += 1
                    # if event.type == pygame.MOUSEBUTTONDOWN and curr_question < len(QUESTIONS):
        #     key = question_types[curr_question]
        #     # i = 0
        #     # for rect in choices:
        #     #     if rect.collidepoint(mouse_position):
        #     #         answers[key] = OPTIONS[i][1]
        #     #         curr_question += 1
        #     #     i += 1
        #     for i, rect in enumerate(choices):
        #         if rect.collidepoint(mouse_position):
        #             answers[key] = OPTIONS[i][1]
        #             curr_question += 1
        #             score = OPTIONS[i][1]
        #
        #             # go left if below threshold, right if at or above
        #             if score < current_node.threshold:
        #                 current_node = current_node.get_left
        #             else:
        #                 current_node = current_node.get_right
        #
        #             # check if we've landed on a leaf
        #             if current_node is None or current_node.is_leaf():
        #                 target = current_node if current_node is not None else current_node
        #                 result = (target.get_root or 'unknown').upper()

    if curr_question < len(QUESTIONS):
        key = question_types[curr_question]

        # drawing the question
        # text = font.render(QUESTIONS[key], True, BLACK)
        # screen.blit(text, (100, 100))

        # drawing the choices
        lines = wrap_text(QUESTIONS[key], font, W - 200)
        y_text = 100
        for line in lines:
            text_change = font.render(line, True, BLACK)
            screen.blit(text_change, text_change.get_rect(center=(W//2, y_text)))
            y_text += 30

        i = 0
        for rect in choices:
            label, score = OPTIONS[i]

            color = HOVER if rect.collidepoint(mouse_position) else BLUE
            pygame.draw.rect(screen, color, rect)

            t = font.render(label, True, BLACK)
            screen.blit(t, (rect.x + 10, rect.y + 15))

            i += 1

    else:
        # result screen
        # total = sum(answers[x] for x in answers)
        # result = f"Total score: {round(total, 2)}"

        mbti_type = loaded_tree.predict(answers)
        result = f"Your type: {mbti_type.upper()}"

        text = font_result.render(result, True, BLACK)
        screen.blit(text, (100, 200))

    pygame.display.flip()

pygame.quit()
