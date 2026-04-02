"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Module Description
===============================
This module implements the core algorithm logic for the project. It defines
the MBTITree class, which is a specialized decision tree for MBTI classification, and
provides functions to train the model using recursion and median-based feature splitting.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""
from filter_data import User


def find_best_split(users: list[User], features_to_test: list[str]) -> tuple[str, float]:
    """Determine which feature provides the most accurate split using the median.

    For each feature, computes the median threshold and splits users into two groups.
    The feature whose median split correctly predicts the most users (based on majority
    MBTI label in each group) is selected. Returns the best feature name and its
    corresponding median threshold.

    Preconditions:
        - len(users) >= 1
        - all(f in {'average_post_length', 'social_score', 'expressiveness_score',
              'complexity_score', 'structure_score'} for f in features_to_test)
        - all(u.mbti is not None for u in users)
    """

    best_feature = features_to_test[0]
    best_threshold = get_median_threshold(users, best_feature)
    max_correct_predictions = -1

    for feature in features_to_test:
        # Find the median threshold for this feature
        threshold = get_median_threshold(users, feature)

        # Split users into two groups based on the median
        left_group = [u for u in users if extract_user_features(u)[feature] < threshold]
        right_group = [u for u in users if extract_user_features(u)[feature] >= threshold]

        # Count how many users each group's majority label would correctly predict
        left_correct = _get_majority_count(left_group)
        right_correct = _get_majority_count(right_group)
        total_correct = left_correct + right_correct

        # Update best split if this feature performs better
        if total_correct > max_correct_predictions:
            max_correct_predictions = total_correct
            best_feature = feature
            best_threshold = threshold

    return best_feature, best_threshold


def get_count(users: list[User]) -> dict[str, int]:
    """Return a dictionary mapping each MBTI type to the number of users with that type.

    Preconditions:
        - all(u.mbti is not None for u in users)
        - all(u.mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
                         'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}
              for u in users)
    """
    counts = {}
    for u in users:
        if u.mbti in counts:
            counts[u.mbti] += 1
        else:
            counts[u.mbti] = 1

    return counts


def _get_majority_count(users: list[User]) -> int:
    """Return the count of the most common MBTI type among the given users.

    Returns 0 if the list is empty.
    """
    if not users:
        return 0
    counts = get_count(users)
    return max(counts.values())


def extract_user_features(user: User) -> dict[str, float]:
    """Return a dictionary mapping feature names
    to their corresponding numerical values for a given User."""
    return {
        'average_post_length': user.average_post_length,
        'social_score': user.social_score,
        'expressiveness_score': user.expressiveness_score,
        'complexity_score': user.complexity_score,
        'structure_score': user.structure_score,
    }


def get_median_threshold(users: list[User], feature: str) -> float:
    """Return the median value of the given feature across all users. Returns 0.0 if users is empty.

    Preconditions:
        - feature in {'average_post_length', 'social_score', 'expressiveness_score',
              'complexity_score', 'structure_score'}
        - all(0.0 <= extract_user_features(u)[feature] <= 1.0 for u in users)
    """
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
        'extra-imports': ['csv', 'main', 'linguistic_scores', 'filter_data'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
