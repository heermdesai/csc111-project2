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

class User:
    """
    TODO: add docstring
    """
    user_id: int
    mbti_type: str
    followers: int
    following: int
    length_of_bio: int

    # TODO: should we use averages or the count -- what is the difference
    retweets: int
    hashtags_count: int
    average_tweet_length: int


# def twitter_files(user: str) -> None:
#     # user info
#     with open(user, newline='') as user_info:
#         reader = csv.reader(user_info)
#         for row in reader:
#           followers = row[7]
#         TODO: complete this function
