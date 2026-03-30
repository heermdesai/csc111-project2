"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Description
===============================
This Python module handles the main quiz and functions.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus, or any instructors
grading. All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""


def get_excitement_score(posts: list[str]) -> float:
    """
    Returns the average excitement score, 0.0 for no excitement, 1.0 for maximum excitement, for a user
    given a list of their text posts. The excitement score is calculated as the ratio of "excitement characters," i.e.
    anything outside the defined normal characters to the total number of characters.

    >>> post1 = ['Yellow team for the win 🙊💛💛💛💛💛💛', 'RT @ChelseaFC: 2-2!!! ALONSO! 💪', 'i need sleep']
    >>> post2 = ['i need sleep']
    >>> post3 = ['🙊💛💛YAY']

    >>> get_excitement_score(post1)
    0.32
    >>> get_excitement_score(post2)
    0.0
    >>> get_excitement_score(post3)
    1.0
    """

    # TODO: could decide against this, but would be cool to id if caps characters are actually excitement as
    #  opposed to just grammar or usernames or smthg

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    punctuation = '.,:; '
    socials = '@#$%&*(){}[]-/'

    normal_characters = alphabet + numbers + punctuation + socials

    exclamatory_count = 0
    length_so_far = 0

    for post in posts:
        for i in range(len(post)):
            if post[i] not in normal_characters:
                exclamatory_count += 1
        length_so_far += len(post)

    return round((exclamatory_count / length_so_far), 2)


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
