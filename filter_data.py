"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Module Description
===============================
This module serves as the data processing pipeline for the project. It handles the
ingestion, cleaning, and transformation of raw social media datasets into a standardized format
for analysis using a new defined User class.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

import csv
# from typing import Optional

import linguistic_scores


class User:
    """
    Represents a social media user and their behavioral metrics across platforms (specifically,
    Twitter, Reddit, and miscellaneous text-post platforms)

    Instance Attributes:
        - user_id: A unique identifier sourced from Twitter data or generated internally for other users.
        - mbti: The Myers-Briggs Type Indicator used to classify the user's personality; case-sensitive (lower-case).
        - average_post_length: The mean length of the user's published content.
        - social_score: A measure of outward social engagement, reflecting the E/I axis.
        - expressiveness_score: A measure of emotional expressiveness in language, reflecting the F/T axis.
        - complexity_score: A measure of abstract thinking and conceptual depth, reflecting the N/S axis.
        - structure_score: A measure of deliberateness and structural control in writing, reflecting the J/P axis.

    Representation Invariants:
        - self.mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
            'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}

    """

    user_id: int
    mbti: str
    average_post_length: float
    social_score: float
    expressiveness_score: float
    complexity_score: float
    structure_score: float

    def __init__(self, user_id: int = 0, mbti: str = '', average_post_length: float = 0.0,
                 scores: dict[str, float] = None) -> None:
        """Initializes a User.
        The scores dict is expected to contain the keys: 'social_score', 'expressiveness_score',
        'complexity_score', and 'structure_score'. Any missing keys default to 0.0."""

        self.user_id = user_id
        self.mbti = mbti
        self.average_post_length = average_post_length

        scores = scores or {}
        self.social_score = scores.get('social_score', 0.0)
        self.expressiveness_score = scores.get('expressiveness_score', 0.0)
        self.complexity_score = scores.get('complexity_score', 0.0)
        self.structure_score = scores.get('structure_score', 0.0)


# ===============================
# CSV FILES PROCESSING
# ===============================
def twitter_user_files(mbti: str, info: str, tweets: str) -> list[User]:
    """
    Returns a list of User objects populated by parsing three Twitter-sourced CSV files:
        - mbti: A file containing user IDs and MBTI personality type classifications.
        - info: A file containing user IDs and profile metrics including average post length.
        - tweets: A file containing user IDs and raw tweet content for linguistic analysis.

    Preconditions:
        - All input files must be in CSV format.
        - The User ID must be located in the first column (index 0) of every input file.
        - The MBTI file serves as the master record, containing a comprehensive list of all User IDs.
          No new User IDs may appear in subsequent files that are not already present in the MBTI file.
    """
    user_registry = {}

    with open(mbti, encoding="utf-8") as mbti_file:
        reader = csv.reader(mbti_file)
        next(reader)
        for row in reader:
            uid = int(row[0])
            new_user = User()
            new_user.user_id = uid
            new_user.mbti = row[1]
            user_registry[uid] = new_user

    with open(info, encoding="utf-8") as info_file:
        reader = csv.reader(info_file)
        next(reader)
        for row in reader:
            uid = int(row[0])
            if uid in user_registry:
                user_registry[uid].average_post_length = float(row[21])

    with open(tweets, encoding="utf-8") as tweets_file:
        reader = csv.reader(tweets_file)
        next(reader)
        for row in reader:
            if not row:
                continue
            try:
                uid = int(row[0])
                if uid in user_registry:
                    tweets_list = [t for t in row[1:] if t]

                    scores = linguistic_scores.compute_scores(tweets_list)
                    user = user_registry[uid]
                    user.social_score = scores['social_score']
                    user.expressiveness_score = scores['expressiveness_score']
                    user.complexity_score = scores['complexity_score']
                    user.structure_score = scores['structure_score']
            except ValueError:
                continue

    return list(user_registry.values())


def reddit_user_files(reddit_post_file: str) -> list[User]:
    """Returns a list of Users based on the reddit dataset.

    Preconditions:
        - reddit_post_file is the path to a CSV file where the leftmost column is the username,
          the middle column is the text post, and the rightmost column is the mbti type.
    """
    user_registry = {}
    user_posts = {}  # Track posts separately to compute scores at the end
    uid = 0

    with open(reddit_post_file, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            username, post, mbti = row[0], row[1], row[2]

            if username not in user_registry:
                new_user = User()
                new_user.user_id = uid
                new_user.mbti = mbti
                new_user.average_post_length = 0.0

                user_registry[username] = new_user
                user_posts[username] = []
                uid += 1

            user = user_registry[username]
            user_posts[username].append(post)

            # temporarily store total length in average_post_length; divide by count later
            user.average_post_length += len(post)

    for username, user in user_registry.items():
        posts = user_posts[username]
        user.average_post_length = user.average_post_length / len(posts)

        scores = linguistic_scores.compute_scores(posts)
        user.social_score = scores['social_score']
        user.expressiveness_score = scores['expressiveness_score']
        user.complexity_score = scores['complexity_score']
        user.structure_score = scores['structure_score']

    return list(user_registry.values())


def mixed_user_files(misc_file: str) -> list[User]:
    """Returns a list of Users based on a dataset with miscellaneous textposts.

    Preconditions:
        - misc_file is the path to a CSV file with two columns, where the left column is mbti type,
          and right column is the corresponding text post.
    """
    user_list = []
    uid = 0

    with open(misc_file, encoding="utf-8") as misc:
        reader = csv.reader(misc)
        for row in reader:
            mbti_type = row[0]
            post = row[1]

            new_user = User()
            new_user.user_id = uid
            new_user.mbti = mbti_type
            new_user.average_post_length = float(len(post))

            scores = linguistic_scores.compute_scores([post])
            new_user.social_score = scores['social_score']
            new_user.expressiveness_score = scores['expressiveness_score']
            new_user.complexity_score = scores['complexity_score']
            new_user.structure_score = scores['structure_score']

            user_list.append(new_user)
            uid += 1

    return user_list


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
        'extra-imports': ['csv', 'main', 'linguistic_scores', 'mbti_helper'],
        'allowed-io': ['twitter_user_files', 'reddit_user_files', 'mixed_user_files'],
        'max-nested-blocks': 4
    })
