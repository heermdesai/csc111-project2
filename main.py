"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Description
===============================
This Python module handles the main quiz and functions.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking CSC111 at the University
of Toronto St. George campus, or any instructors grading. All forms of distribution of this code are
expressly prohibited.

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


from __future__ import annotations
from typing import Any, Optional


class BinaryTree:
    """A binary tree where every node has at most two children: left and right.

    This is the base class. It handles the structure only —
    no MBTI logic here.

    Representation Invariants:
        - self._root is None implies self._left is None and self._right is None
        - self._left is not None implies self._root is not None
        - self._right is not None implies self._root is not None
    """
    _root: Optional[Any]
    _left: Optional[BinaryTree]
    _right: Optional[BinaryTree]

    def __init__(self, root: Optional[Any],
                 left: Optional[BinaryTree] = None,
                 right: Optional[BinaryTree] = None) -> None:
        self._root  = root
        self._left  = left
        self._right = right

    def is_empty(self) -> bool:
        """Return True if this tree has no root (is empty)."""
        return self._root is None

    def is_leaf(self) -> bool:
        """Return True if this node has no children."""
        return self._left is None and self._right is None

class MBTITree(BinaryTree):
    """A decision tree node for MBTI classification.

    Inherits _root, _left, _right from BinaryTree.
    _root stores the split condition as a string like 'emotion_rate < 0.055',
    or the predicted MBTI type if this is a leaf.

    Instance Attributes:
        - feature:    the feature this node splits on, or None if leaf
        - threshold:  the split value, or None if leaf
        - prediction: majority MBTI type among training users at this node
        - mbti_counts: how many of each type reached this node during training

    Representation Invariants:
        - self.is_leaf() implies self.feature is None
        - not self.is_leaf() implies self.feature is not None
        - not self.is_leaf() implies isinstance(self._left, MBTITree)
        - not self.is_leaf() implies isinstance(self._right, MBTITree)
    """
    feature:     str
    threshold:   float
    prediction:  str
    mbti_counts: dict[str, int]

    def __init__(self, mbti_counts: dict[str, int], feature: str, threshold: float) -> None:

        max_so_far = 0
        key_so_far = ''
        for key in mbti_counts:
            if mbti_counts[key] > max_so_far:
                key_so_far = key
                max_so_far = mbti_counts[key]
        majority = key_so_far

        self._root = mbti_counts
        self._left = MBTITree(None)
        self._right = MBTITree(None)

        self.prediction = majority
        self.feature = feature
        self.threshold = threshold


    def add_split(self, feature: str, threshold: float,
                  left: MBTITree, right: MBTITree) -> None:
        """Turn this leaf into an internal node by attaching children.

        Also updates _root to a readable description of the split condition.
        """
        self.feature = feature
        self.threshold = threshold
        self._left = left    # from BinaryTree — now explicit
        self._right = right   # from BinaryTree — now explicit
        # self._root      = f'{feature} < {threshold:.3f}'  # human-readable label

    def predict(self, user_features: dict[str, float]) -> str:
        """Traverse the tree and return predicted MBTI type.

        Uses _left and _right inherited from BinaryTree.
        """
        if self.is_leaf():           # inherited from BinaryTree
            return self.prediction

        if user_features[self.feature] < self.threshold:
            return self._left.predict(user_features)
        else:
            return self._right.predict(user_features)


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
