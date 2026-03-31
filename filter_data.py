"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Description
===============================
This Python module handles the filtering and refactoring of external data into standard variables
for use across the project.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking CSC111 at the
University of Toronto St. George campus, or any instructors grading. All forms of distribution of
this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

import csv
from typing import Optional

import helper
from main import MBTITree


class User:
    """
    Represents a social media user and their behavioral metrics across platforms (specifically,
    Twitter, Reddit, and miscellaneous text-post platforms)

    Instance Attributes:

        # GENERAL ATTRIBUTES
        - user_id: A unique identifier sourced from Twitter data or generated internally for new users.
        - mbti: The Myers-Briggs Type Indicator used to classify the user's personality; case-sensitive (lower-case).
        - average_post_length: The mean length of the user's published content.
        - excitement_score: The calculated tone of the user's posts.
        - source_platform: The specific social media service where the data originated.

        # TWITTER-SPECIFIC (OPTIONAL) ATTRIBUTES
        - length_of_bio: The total number of characters in the user's profile biography.
        - average_retweet_count: The mean number of times the user's content is shared by others.
        - hashtags_count: The total frequency of hashtag usage within the user's posts.
        - followers: The total count of other accounts following this user.
        - following: The total count of accounts that this user follows.

    Representation Invariants:
        - mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
            'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}
        - 0.0 <= excitement_score <= 1.0
        - source_platform in {'twitter', 'reddit', 'miscellaneous'}

    """

    # General Attributes
    user_id: int  # Twitter data gives userid, otherwise we create a unique user
    mbti: str
    average_post_length: float
    excitement_score: float
    source_platform: str

    # Twitter-Specific Attributes
    length_of_bio: Optional[int] = None
    average_retweet_count: Optional[float] = None
    hashtags_count: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None

    def __init__(self, user_id=0, mbti='', average_post_length=0.0, excitement_score=0.0,
                 source_platform='miscellaneous', length_of_bio=None, average_retweet_count=None, hashtags_count=None,
                 followers=None, following=None):
        """
        Initializes a User
        """
        self.user_id = user_id
        self.mbti = mbti
        self.average_post_length = average_post_length
        self.excitement_score = excitement_score
        self.source_platform = source_platform

        self.length_of_bio = length_of_bio
        self.average_retweet_count = average_retweet_count
        self.hashtags_count = hashtags_count
        self.followers = followers
        self.following = following


def twitter_user_files(mbti: str, info: str, tweets: str) -> list[User]:
    """
    Returns a list of User objects populated by parsing three Twitter-sourced CSV files of the following format:
        - mbti: A file containing user IDs and MBTI personality type classifications.
        - info: A file containing user IDs and profile metrics like bio length, engagement stats, and follower counts.
        - tweets: A file containing user IDs and raw tweet content used for calculating excitement scores.

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
                u = user_registry[uid]
                u.average_post_length = float(row[21])
                u.length_of_bio = len(row[5])
                u.average_retweet_count = float(row[22])
                u.hashtags_count = int(row[24])
                u.followers = int(row[7])
                u.following = int(row[8])

    with open(tweets) as tweets_file:
        reader = csv.reader(tweets_file)
        for row in reader:
            uid = int(row[0])
            if uid in user_registry:
                tweets_list = row[1:]
                user_registry[uid].excitement_score = helper.get_excitement_score(tweets_list)

    return list(user_registry.values())


def reddit_user_files(misc_file: str, reddit_post_file: str) -> list[User]:
    """Returns a list of Users based on the reddit dataset.

    Preconditions:
        - misc_file is the path to a CSV file corresponding to a file with two columns,
            where the left column is mbti type, and right column is the corresponding reddit text post.
        - reddit_post_file is the path to a CSV file corresponding to the reddit posts (small),
            where the leftmost column is the username, middle column is the text post,
            and the rightmost column is the mbti type.
    """
    i = 0
    users_and_post = {}
    user_list = []

    with open(misc_file) as f:
        reader = csv.reader(f)
        for row in reader:
            user = User()
            user.user_id = i
            i += 1
            user.mbti = row[0]
            user.average_post_length = len(row[1])
            user.excitement_score = helper.get_excitement_score([row[1]])
            user.source_platform = 'miscellaneous'

            user_list.append(user)

    with open(reddit_post_file) as f:
        reader = csv.reader(f)
        for row in reader:
            user = User()
            if row[0] not in users_and_post:
                user.user_id = i
                i += 1
                users_and_post[user.user_id][0] += len(row[1])
                users_and_post[user.user_id][1] += 1
            user.mbti = row[2]
            user.average_post_length = users_and_post[user.user_id][0] / users_and_post[user.user_id][1]
            user.excitement_score = helper.get_excitement_score(users_and_post[user.user_id][0])
            user.source_platform = 'reddit'

            user_list.append(user)

    return user_list


def extract_user_features(user: User) -> dict[str, float]:
    """Return a dictionary of numerical features for a given User."""

    features = {
        'average_post_length': float(user.average_post_length),
        'excitement_score': float(user.excitement_score)
    }

    # Twitter-specific stats if they exist, otherwise default to 0.0
    if user.source_platform == 'twitter':
        features['followers'] = float(user.followers or 0)
        features['following'] = float(user.following or 0)
        features['hashtags_count'] = float(user.hashtags_count or 0)
    else:
        features['followers'] = 0.0
        features['following'] = 0.0
        features['hashtags_count'] = 0.0

    return features


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
