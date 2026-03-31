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
from typing import Optional

import helper
from mbti_tree import MBTITree


class User:
    """
    Represents a social media user and their behavioral metrics across platforms (specifically,
    Twitter, Reddit, and miscellaneous text-post platforms)

    Instance Attributes:
        - user_id: A unique identifier sourced from Twitter data or generated internally for other users.
        - mbti: The Myers-Briggs Type Indicator used to classify the user's personality; case-sensitive (lower-case).
        - source_platform: The specific social media service where the data originated.
        - average_post_length: The mean length of the user's published content.
        - social_score: A measure of outward social engagement, reflecting the E/I axis.
        - expressiveness_score: A measure of emotional expressiveness in language, reflecting the F/T axis.
        - complexity_score: A measure of abstract thinking and conceptual depth, reflecting the N/S axis.
        - structure_score: A measure of deliberateness and structural control in writing, reflecting the J/P axis.

    Representation Invariants:
        - mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
            'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}
        - source_platform in {'twitter', 'reddit', 'miscellaneous'}

    """

    user_id: int
    mbti: str
    source_platform: str
    average_post_length: float
    social_score: float
    expressiveness_score: float
    complexity_score: float
    structure_score: float

    def __init__(self, user_id: int = 0, mbti: str = '', average_post_length: float = 0.0,
                 social_score: float = 0.0, expressiveness_score: float = 0.0, complexity_score: float = 0.0,
                 structure_score: float = 0.0, source_platform: str = 'miscellaneous') -> None:
        """Initializes a User."""
        self.user_id = user_id
        self.mbti = mbti
        self.average_post_length = average_post_length
        self.social_score = social_score
        self.expressiveness_score = expressiveness_score
        self.complexity_score = complexity_score
        self.structure_score = structure_score
        self.source_platform = source_platform


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

    with open(mbti) as mbti_file:
        reader = csv.reader(mbti_file)
        for row in reader:
            uid = int(row[0])
            new_user = User()
            new_user.user_id = uid
            new_user.mbti = row[1]
            new_user.source_platform = 'twitter'
            user_registry[uid] = new_user

    with open(info) as info_file:
        reader = csv.reader(info_file)
        for row in reader:
            uid = int(row[0])
            if uid in user_registry:
                user_registry[uid].average_post_length = float(row[21])

    with open(tweets) as tweets_file:
        reader = csv.reader(tweets_file)
        for row in reader:
            uid = int(row[0])
            if uid in user_registry:
                tweets_list = [t for t in row[1:] if t]  # filter empty strings
                features = helper.get_linguistic_features(tweets_list)
                user_registry[uid].social_score = helper.calculate_social_score(features)
                user_registry[uid].expressiveness_score = helper.calculate_expressiveness_score(features)
                user_registry[uid].complexity_score = helper.calculate_complexity_score(features)
                user_registry[uid].structure_score = helper.calculate_structure_score(features)

    return list(user_registry.values())


def mixed_data(misc_file: str) -> list[User]:
    """Returns a list of Users based on a dataset with miscellaneous textposts.

    Preconditions:
        - misc_file is the path to a CSV file with two columns, where the left column is mbti type,
          and right column is the corresponding text post.
    """
    user_list = []

    with open(misc_file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            post = row[1]
            features = helper.get_linguistic_features([post])

            user = User(
                user_id=i,
                mbti=row[0],
                average_post_length=float(len(post)),
                social_score=helper.calculate_social_score(features),
                expressiveness_score=helper.calculate_expressiveness_score(features),
                complexity_score=helper.calculate_complexity_score(features),
                structure_score=helper.calculate_structure_score(features),
                source_platform='miscellaneous'
            )
            user_list.append(user)

    return user_list


def reddit_user_files(reddit_post_file: str) -> list[User]:
    """Returns a list of Users based on the reddit dataset.

    Preconditions:
        - reddit_post_file is the path to a CSV file where the leftmost column is the username,
          the middle column is the text post, and the rightmost column is the mbti type.
    """
    # Maps username -> [total_post_length, post_count, mbti, list_of_posts]
    username_data = {}

    with open(reddit_post_file) as f:
        reader = csv.reader(f)
        for row in reader:
            username, post, mbti = row[0], row[1], row[2]
            if username not in username_data:
                username_data[username] = [0, 0, mbti, []]
            username_data[username][0] += len(post)
            username_data[username][1] += 1
            username_data[username][3].append(post)

    user_list = []
    for i, (username, data) in enumerate(username_data.items()):
        total_length, post_count, mbti, posts = data
        features = helper.get_linguistic_features(posts)

        user = User(
            user_id=i,
            mbti=mbti,
            average_post_length=float(total_length / post_count),
            social_score=helper.calculate_social_score(features),
            expressiveness_score=helper.calculate_expressiveness_score(features),
            complexity_score=helper.calculate_complexity_score(features),
            structure_score=helper.calculate_structure_score(features),
            source_platform='reddit'
        )
        user_list.append(user)

    return user_list


def extract_user_features(user: User) -> dict[str, float]:
    """Return a dictionary of numerical features for a given User."""
    return {
        'average_post_length': user.average_post_length,
        'social_score': user.social_score,
        'expressiveness_score': user.expressiveness_score,
        'complexity_score': user.complexity_score,
        'structure_score': user.structure_score,
    }


def get_median_threshold(users: list[User], feature: str) -> float:
    """Find the median value of a specific feature across a list of users."""
    values = []
    for u in users:
        u_feats = extract_user_features(u)
        values.append(u_feats[feature])

    if not values:
        return 0.0

    sorted_values = sorted(values)
    size = len(sorted_values)

    if size % 2 == 1:
        # Odd number of elements: take the middle one
        return float(sorted_values[size // 2])
    else:
        # Even number: average the two middle elements
        mid1 = sorted_values[size // 2 - 1]
        mid2 = sorted_values[size // 2]
        return (mid1 + mid2) / 2


def find_best_split(users: list[User]) -> tuple[str, float]:
    """Determine which feature provides the most accurate split using the median."""
    features_to_test = ['average_post_length', 'excitement_score', 'followers', 'hashtags_count']

    best_feature = features_to_test[0]
    best_threshold = 0.0
    max_correct_predictions = -1

    for feature in features_to_test:
        # 1. Get the median for this specific feature
        threshold = get_median_threshold(users, feature)

        # TODO Find a way for the best split -- what personalities are correlated w what features
        # 2. Split the users into two groups based on that median
        # left_group = [u for u in users if extract_user_features(u)[feature] < threshold]
        # right_group = [u for u in users if extract_user_features(u)[feature] >= threshold]

        # 3. Calculate how many correct predictions we'd make if we stopped here
        # (Accuracy = Majority count in Left + Majority count in Right)
        # current_correct = (get_majority_mbti_count(left_group) + get_majority_mbti_count(right_group))

    raise NotImplementedError


def build_mbti_tree(users: list[User], depth: int = 0, max_depth: int = 5) -> MBTITree:
    """
    Recursively builds an MBTITree using the median-split logic.
    """
    # Count MBTI types for this specific group of users
    counts = {}
    for u in users:
        counts[u.mbti] = counts.get(u.mbti, 0) + 1

    # 2. Check STOPPING CONDITIONS (Base Cases)
    # Stop if: all users are the same type, list is too small, or we hit max depth
    if len(counts) <= 1 or depth >= max_depth:
        # Create a leaf node (feature and threshold are None)
        return MBTITree(counts, '', 0.0)

    # 3. Find the best feature to split on using the median
    # This calls the function we wrote in the filtering file
    feature, threshold = find_best_split(users)

    # 4. Create the current node
    node = MBTITree(counts, feature, threshold)

    # 5. Split the data into two halves
    left_users = [u for u in users if extract_user_features(u)[feature] < threshold]
    right_users = [u for u in users if extract_user_features(u)[feature] >= threshold]

    # Handle the edge case where a split doesn't actually divide the data
    if not left_users or not right_users:
        return MBTITree(counts, None, None)

    # 6. Recursively build the left and right subtrees
    node._left = build_mbti_tree(left_users, depth + 1, max_depth)
    node._right = build_mbti_tree(right_users, depth + 1, max_depth)

    return node


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
        'extra-imports': ['csv'],
        'allowed-io': ['twitter_user_files', 'reddit_user_files'],
        'max-nested-blocks': 4
    })
