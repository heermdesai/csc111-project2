"""CSC111 Winter 2026 Project 2 Phase 2: MBTI Personality Predictor

Module Description
===============================
This module serves as the primary entry point and user interface for the MBTI  Prediction system.
It orchestrates the flow of data between the filtering  and tree-building modules to initialize
the model and conduct interactive  personality assessments.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

from filter_data import twitter_user_files, reddit_user_files, mixed_user_files
from mbti_tree import MBTITree

def ask_user(tree: MBTITree) -> dict[str, float]:
    questions = {
        "social_score": "I actively engage with others online by tagging them, using hashtags, or sharing links.",
        "complexity_score": "I prefer using abstract metaphors and a sophisticated vocabulary rather than simple facts.",
        "expressiveness_score": "My writing is often filled with emotion, exclamation points, and emojis.",
        "structure_score": "I put a lot of effort into making my posts organized and grammatically correct.",
        "average_post_length": "I usually write long, detailed explanations rather than short snippets."
    }

    scale = {
        "1": 0.0,
        "2": 0.25,
        "3": 0.5,
        "4": 0.75,
        "5": 1.0,
    }

    question = questions[tree.feature]

    print(f"\n{question}")
    print("  1 - Strongly Disagree")
    print("  2 - Disagree")
    print("  3 - Neutral")
    print("  4 - Agree")
    print("  5 - Strongly Agree")

    while True:
        user_input = input("Enter 1–5: ").strip()
        if user_input in scale:
            score = scale[user_input]
            return {tree.feature: score}
        print("  Invalid input. Please enter a number from 1 to 5.")


def run_mbti_test():

    users = twitter_user_files() + reddit_user_files() + mixed_user_files()
    tree = MBTITree()

    tree.build_mbti_tree(users)
    # Function of asking questions and returning a dict which can be passed into predict
    # return tree.predict()


if __name__ == '__main__':
    # Uncomment the following lines for code checking/debugging purposes.
    # We recommend commenting out these lines when working with large datasets to reduce runtime.

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['csv', 'linguistic_scores', 'mbti_tree', 'filter_data'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
