"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Description
===============================
This Python module handles helper functions for main.py and filter_data.py.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking CSC111 at the University
of Toronto St. George campus, or any instructors grading. All forms of distribution of this code are
expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""

# TODO: Add get_excitement_score

if __name__ == '__main__':

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': [],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
