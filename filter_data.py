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


class User:
    """
    Represents a social media user and their behavioral metrics across platforms (specifically,
    Twitter, Reddit, and miscellaneous text-post platforms)

    Instance Attributes:

        # GENERAL ATTRIBUTES
        - user_id: A unique identifier sourced from Twitter data or generated internally for new users.
        - mbti: The Myers-Briggs Type Indicator used to classify the user's personality.
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
        - mbti in {'ENTJ', 'ENFJ', 'ESFJ', 'ESTJ', 'ENTP', 'ENFP', 'ESFP', 'ESTP',
            'INTJ', 'INFJ', 'ISFJ', 'ISTJ', 'INTP', 'INFP', 'ISFP', 'ISTP'}
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


# def twitter_files(user: str) -> None:
#     # user info
#     with open(user, newline='') as user_info:
#         reader = csv.reader(user_info)
#         for row in reader:
#           followers = row[7]
#         TODO: complete this function
