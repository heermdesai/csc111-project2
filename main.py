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
        'extra-imports': [],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
