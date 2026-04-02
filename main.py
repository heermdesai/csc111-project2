"""CSC111 Winter 2026 Project 2 Phase 2:
Linguistic Pattern Recognition for MBTI Classification: A Data-Driven Decision Tree Analysis of Social Media Posts

Module Description
===============================
This module implements the core MBTITree class, a recursive decision tree structure designed to classify
personality types based on digital linguistic markers. The module uses an algorithm to build a predictive model
from processed social media data (Twitter, Reddit, and miscellaneous text), traverses the tree based on
numerical feature scores to reach a leaf node representing a specific MBTI type. It provides a basic console
interface that allows users to "quiz" themselves against the trained model by providing self-assessment scores
for specific linguistic behaviors.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

from __future__ import annotations
from typing import Optional, Any

from filter_data import User, twitter_user_files, reddit_user_files, mixed_user_files
from mbti_helper import find_best_split, get_count, extract_user_features


class MBTITree:
    """ A decision tree for MBTI classification where each node represents either a decision point (split) or a
    final personality prediction (leaf).

    Instance Attributes:
        - feature: The attribute name this node splits on (e.g., 'excitement_score'). Set to None
            if this node is a leaf.
        - threshold: The median value used to divide users at this node. Set to None if this node
            is a leaf.
        - mbti_counts: A dictionary mapping MBTI types to the frequency of training users of that
            type who reached this node. Set to None if this node is a leaf.

    Private Instance Attributes
        - _root: Stores the current predicted MBTI string (e.g., 'INTJ').
        - _left: The child tree containing users with feature values < threshold.
        - _right: The child tree containing users with feature values >= threshold.

    Representation Invariants:
        - all(mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
                       'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}
              for mbti in self.mbti_counts)
        - self.threshold is None or 0.0 <= self.threshold <= 1.0
    """
    feature: Optional[str]
    threshold: Optional[float]
    mbti_counts: Optional[dict[str, int]]
    _left: Optional[MBTITree]
    _right: Optional[MBTITree]
    _root: Optional[Any]

    def __init__(self, mbti_counts: dict[str, int] = None, feature: str = None, threshold: float = 0.0) -> None:
        """
        Initializes an MBTI Tree

        Sets the root to the most frequent MBTI type in mbti_counts,
        or None if mbti_counts is empty or not given. Left and right subtrees are
        initialized to None.
        """
        if not mbti_counts:
            self._root = None
        else:
            max_so_far = -1
            key_so_far = ''
            for key in mbti_counts:
                if mbti_counts[key] > max_so_far:
                    key_so_far = key
                    max_so_far = mbti_counts[key]

            self._root = key_so_far

        self._left = None
        self._right = None
        self.feature = feature
        self.threshold = threshold
        self.mbti_counts = mbti_counts

    def get_subtrees(self) -> tuple[Optional[MBTITree], Optional[MBTITree]]:
        """Returns a tuple of the left and right subtrees of the current node"""
        return self._left, self._right

    def build_mbti_tree(self, users: list[User], features: list[str] = None,
                        depth: int = 0, max_depth: int = 5) -> MBTITree:
        """
        Recursively builds and returns an MBTITree trained on the given list of users.

        At each node, the best feature and median threshold are selected using
        find_best_split. Users are partitioned into left (feature < threshold) and
        right (feature >= threshold) subsets, and the tree is built recursively.
        Recursion stops when any of the following base cases are met:
            - All users share the same MBTI type (len(counts) <= 1)
            - No features remain to split on
            - The current depth has reached max_depth

        Preconditions:
            - len(users) != 0
            - depth >= 0
            - all features in features (if provided) are valid keys returned by extract_user_features
        """

        if features is None:
            features = ['average_post_length', 'social_score', 'expressiveness_score',
                        'complexity_score', 'structure_score']

        counts = get_count(users)

        if len(counts) <= 1 or not features or depth >= max_depth:
            return MBTITree(counts)

        feature, threshold = find_best_split(users, features)
        node = MBTITree(counts, feature, threshold)

        # Split the data into two halves
        left_users = [v for v in users if extract_user_features(v)[feature] < threshold]
        right_users = [v for v in users if extract_user_features(v)[feature] >= threshold]

        remaining_features = [f for f in features if f != feature]

        # Recursively build the left and right subtrees
        node._left = self.build_mbti_tree(left_users, remaining_features, depth + 1, max_depth)
        node._right = self.build_mbti_tree(right_users, remaining_features, depth + 1, max_depth)

        return node

    def predict(self, answers: Optional[dict[str, float]] = None) -> str:
        """
        Traverses the tree and return predicted MBTI type based on user input.
        """
        if self._left is None and self._right is None:
            return self._root

        if answers is None:
            user_score = ask_user(self)
        else:
            user_score = answers[self.feature]

        if user_score < self.threshold:
            return self._left.predict(answers)
        else:
            return self._right.predict(answers)


def ask_user(tree: MBTITree) -> float:
    """
    Prompt the user to answer a question for a specific feature.

    Preconditions:
    - tree.feature in questions

    """
    questions = {
        "social_score": "I actively engage with others online by tagging them, using hashtags, or sharing links.",
        "complexity_score": "I prefer using abstract metaphors and a sophisticated vocabulary over simple facts.",
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

    user_input = input("Enter 1–5: ").strip()
    while user_input not in scale:
        print("Invalid input. Please enter a number from 1 to 5.")
        user_input = input("Enter 1–5: ").strip()

    return scale[user_input]


def run_mbti_test() -> None:
    """Runs the MBTI test"""
    users = (twitter_user_files('mbti_labels.csv', 'user_info.csv', 'user_tweets.csv')
             + reddit_user_files('reddit_post_small.csv')
             + mixed_user_files('misc_text_posts.csv'))

    tree = MBTITree()
    loaded_tree = tree.build_mbti_tree(users)

    print("Welcome to the MBTI Personality Predictor Quiz!")
    # Start the prediction process from the root
    final_type = loaded_tree.predict()

    print(f"\nYour predicted MBTI type is: {final_type.upper()}")


if __name__ == '__main__':
    # Uncomment the following lines for code checking/debugging purposes.
    # We recommend commenting out these lines when working with large datasets to reduce runtime.

    run_mbti_test()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['filter_data', 'linguistic_scores', 'mbti_helper'],
        'allowed-io': ['ask_user', 'run_mbti_test'],
        'max-nested-blocks': 4
    })
