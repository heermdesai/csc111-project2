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

from __future__ import annotations
from typing import Any, Optional


class MBTITree:
    """A decision tree node for MBTI classification that functions both as data-driven classifier
    and an interactive quiz structure. Each node represents either a decision point (split) or a
    final personality prediction (leaf).

    Instance Attributes:
        - feature: The attribute name this node splits on (e.g., 'excitement_score'). Set to None
            if this node is a leaf.
        - threshold: The median value used to divide users at this node.  Set to None if this node
            is a leaf.
        - mbti_counts: A dictionary mapping MBTI types to the frequency of training users of that
            type who reached this node.

    Private Instance Attributes
        - _root:
            - If is_leaf(): Stores the predicted MBTI string (e.g., 'INTJ').
            - If not is_leaf(): Stores a human-readable string of the split condition
                (e.g., 'excitement_score < 0.15').
        - _left: The child tree containing users with feature values < threshold.
        - _right: The child tree containing users with feature values >= threshold.

    Representation Invariants:
        - self.is_leaf() == (self.feature is None)
        - self.is_leaf() == (self.threshold is None)
        - not self.is_leaf() ==> isinstance(self._left, MBTITree)
        - not self.is_leaf() ==> isinstance(self._right, MBTITree)
        - all(mbti in {'entj', 'enfj', 'esfj', 'estj', 'entp', 'enfp', 'esfp', 'estp',
                       'intj', 'infj', 'isfj', 'istj', 'intp', 'infp', 'isfp', 'istp'}
              for mbti in self.mbti_counts)
    """
    feature: Optional[str]
    threshold: Optional[float]
    mbti_counts: dict[str, int]
    _left: Optional[MBTITree]
    _right: Optional[MBTITree]

    def __init__(self, mbti_counts: dict[str, int], feature: str = '', threshold: float = 0.0) -> None:
        """
        Initializes an MBTI Tree
        """
        if not mbti_counts:
            self._root = None
        else:
            max_so_far = -1
            key_so_far = ''
            for key in mbti_counts:
                if mbti_counts[key] > max_so_far:
                    key_so_far = key
                    max_so_far = mbti_counts[key]

            self._root = key_so_far

        self._left = None
        self._right = None
        self.feature = feature
        self.threshold = threshold
        self.mbti_counts = mbti_counts

    def is_leaf(self) -> bool:
        """Return True if this node has no children."""
        return self._left is None and self._right is None

    def add_split(self, feature: str, threshold: float,
                  left: MBTITree, right: MBTITree) -> None:
        """Turn this leaf into an internal node by attaching children and pdates _root to a
        readable description of the split condition.
        """
        # TODO root kya hai
        # self._root      = f'{feature} < {threshold:.3f}'  # human-readable label

        self._left = left
        self._right = right
        self.feature = feature
        self.threshold = threshold

    def predict(self, user_features: dict[str, float]) -> str:
        """
        Traverses the tree and return predicted MBTI type.
        """
        if self.is_leaf():
            return self._root

        if user_features[self.feature] < self.threshold:
            return self._left.predict(user_features)
        else:
            return self._right.predict(user_features)


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
