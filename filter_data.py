"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Description
===============================
This Python module handles the filtering and refactoring of external data into standard variables
for use across the project.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus, or any instructors
grading. All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

import csv
from typing import Optional

import main


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

    def __init__(self, user_id, mbti, average_post_length, excitement_score, source_platform,
                 length_of_bio=None, average_retweet_count=None, hashtags_count=None,
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
        - tweets: A file containing user IDs and raw tweet content used for calculating sentiment scores.

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
                user_registry[uid].post_sentiment = main.get_excitement_score(tweets_list)

    return list(user_registry.values())


def reddit_user_files(mbti_file: str, reddit_post_file: str) -> list[User]:
    """Returns a list of Users based on the reddit dataset.

    Preconditions:
        - mbti_file is the path to a CSV file corresponding to a file with two columns,
            where the left column is mbti type, and right column is the corresponding reddit text post.
        - reddit_post_file is the path to a CSV file corresponding to the reddit posts (small),
            where the leftmost column is the username, middle column is the text post,
            and the rightmost column is the mbti type.
    """
    i = 0
    users_and_post = {}
    user_list = []

    with open(mbti_file) as f:
        reader = csv.reader(f)
        user = User()
        for row in reader:
            user.user_id = i
            i += 1
            user.mbti = row[0]
            user.average_post_length = len(row[1])
            user.excitement_score = main.get_excitement_score(list(row[1]))
            user.source_platform = 'reddit'

            user_list.append(user)

    with open(reddit_post_file) as f:
        reader = csv.reader(f)
        user = User()
        for row in reader:
            if row[0] not in users_and_post:
                user.user_id = i
                i += 1
                users_and_post[user.user_id][0] += len(row[1])
                users_and_post[user.user_id][1] += 1
            user.mbti = row[2]
            user.average_post_length = users_and_post[user.user_id][0] / users_and_post[user.user_id][1]
            user.excitement_score = main.get_excitement_score(users_and_post[user.user_id][0])
            user.source_platform = 'reddit'

            user_list.append(user)

    return user_list


if __name__ == '__main__':

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['twitter_user_files', 'reddit_user_files'],
        'max-nested-blocks': 4
    })
