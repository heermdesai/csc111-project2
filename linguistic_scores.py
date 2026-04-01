"""CSC111 Winter 2026 Project 2 Phase 2
Predicting MBTI Personality Types Using Social Media Activity: A Data-Driven Decision Tree Approach

Module Description
===============================
This module contains independent helper functions used for linguistic analysis and feature calculation.
These functions process raw text data to generate  the numerical metrics required for personality classification.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students taking
CSC111 at the University of Toronto St. George campus, or any instructors grading.
All forms of distribution of this code are expressly prohibited.

This file is Copyright (c) 2026 Heer, Laavanya, Saanvi :)
"""
import emoji


def calculate_complexity_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing abstract thinking and conceptual depth.

    Higher scores suggest iNtuition (N) traits — preference for patterns, ideas, and abstraction.
    Lower scores suggest Sensing (S) traits — preference for concrete facts and practicality.

    Weights:
    - Lexical diversity (10.0): Primary indicator of abstract, nuanced thought.
    - Question density (2.0): Reflects speculative and exploratory thinking.
    - Ellipsis density (1.5): Captures comfort with ambiguity and open-ended ideas.
    """
    return (
        features['lexical_diversity'] * 10.0
        + features['question_density'] * 2.0
        + features['ellipsis_density'] * 1.5
    )


def calculate_social_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing social engagement and outward orientation.

    Higher scores suggest Extroversion (E); lower scores suggest Introversion (I).

    Weights:
    - Tag density (5.0): Primary indicator of direct, outward interaction (@user).
    - We-pronoun rate (3.0): Reflects group-oriented identity and collective thinking.
    - Hashtag density (2.0): Captures active participation in broader communities.
    - Link density (1.0): Represents passive information sharing and engagement.
    """
    score = (
        features['tag_density'] * 5.0
        + features['we_pronoun_rate'] * 3.0
        + features['hashtag_density'] * 2.0
        + features['link_density'] * 1.0
    )
    return score


def calculate_expressiveness_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing emotional expressiveness in language.

    Higher scores suggest Feeling (F) traits — decisions guided by empathy and emotion.
    Lower scores suggest Thinking (T) traits — decisions guided by logic and analysis.

    Weights:
    - Emoji density (4.0): Primary visual indicator of deliberate emotional communication.
    - Exclamation density (3.0): Reflects enthusiasm, warmth, and emotional intensity.
    - I-pronoun rate (2.0): Captures personal, self-referential, and subjective framing.
    - Capital density (Variable): High density signals emotional "all caps" writing
      (via _classify_capital_density).
    """
    expressiveness_from_capitals = _classify_capital_density(features['capital_density'])[0]

    score = (
        features['emoji_density'] * 4.0
        + features['exclamation_density'] * 3.0
        + features['i_pronoun_rate'] * 2.0
        + expressiveness_from_capitals
    )
    return score


def calculate_structure_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing deliberateness and structural control in writing.

    Higher scores suggest Judging (J) traits — preference for order, planning, and closure.
    Lower scores suggest Perceiving (P) traits — preference for spontaneity and flexibility.

    Weights:
    - Lexical diversity (2.0): Suggests intentional, precise, and controlled expression.
    - Capital density (Variable): Moderate use indicates deliberate formatting
      (via _classify_capital_density).
    - Ellipsis density (-4.0): Penalizes trailing, open-ended, or unresolved thoughts.
    - Exclamation density (-1.5): Penalizes impulsive or reactive spontaneity.
    """
    structure_from_capitals = _classify_capital_density(features['capital_density'])[1]

    score = (
        features['lexical_diversity'] * 2.0
        + structure_from_capitals
        - features['ellipsis_density'] * 4.0
        - features['exclamation_density'] * 1.5
    )
    return score


def _classify_capital_density(capital_density: float) -> tuple[float, float]:
    """
    Classify capital density as either an emotional or structural signal.

    Returns:
        (expressiveness_contribution, structure_contribution)

    Logic:
    - High density (>= 0.05): Interpreted as "ALL CAPS" emotional writing (F trait).
    - Low/Moderate density (< 0.05): Interpreted as deliberate, structured formatting (J trait).

    In most writing, 2-4% of capital density is expected for proper grammar.
    https://english.stackexchange.com/questions/43563/what-percentage-of-characters-in-normal-english-literature-
    is-written-in-capital
    """

    capital_threshold = 0.05

    if capital_density >= capital_threshold:
        # High capitals: likely ALL CAPS or heavy emotional emphasis — expressiveness signal
        return capital_density * 2.0, 0.0
    else:
        # Low/moderate capitals: likely deliberate formatting emphasis — structure signal
        return 0.0, capital_density * 2.0


def get_linguistic_features(posts: list[str]) -> dict[str, float]:
    """
    Extract and average linguistic metrics from a list of text posts.

    Returns a dictionary mapping feature names to their mean values across all posts.
    Metrics include punctuation density (exclamations, questions, ellipses),
    formatting (capitals), social markers (tags, hashtags, links, emojis),
    and lexical analysis (diversity, I/We pronoun rates).

    Preconditions:
    - posts is a list of strings; empty strings are skipped in density calculations.
    """
    if not posts:
        return {}

    totals = {
        'exclamation_density': 0.0, 'question_density': 0.0, 'ellipsis_density': 0.0,
        'capital_density': 0.0, 'lexical_diversity': 0.0, 'i_pronoun_rate': 0.0,
        'we_pronoun_rate': 0.0, 'link_density': 0.0, 'hashtag_density': 0.0,
        'tag_density': 0.0, 'emoji_density': 0.0
    }

    i_words = {'i', 'me', 'my', 'mine', 'myself'}
    we_words = {'we', 'us', 'our', 'ours', 'ourselves'}

    for post in posts:
        length = len(post)
        if length == 0:
            continue

        totals['exclamation_density'] += post.count('!') / length
        totals['question_density'] += post.count('?') / length
        totals['ellipsis_density'] += post.count('...') / length
        totals['hashtag_density'] += post.count('#') / length
        totals['tag_density'] += post.count('@') / length
        totals['capital_density'] += sum(1 for ch in post if ch.isupper()) / length
        totals['emoji_density'] += emoji.emoji_count(post) / length

        words = post.lower().split()
        word_count = len(words)

        if word_count > 0:
            totals['lexical_diversity'] += len(set(words)) / word_count
            totals['i_pronoun_rate'] += sum(1 for w in words if w in i_words) / word_count
            totals['we_pronoun_rate'] += sum(1 for w in words if w in we_words) / word_count

        totals['link_density'] += (post.count('http') + post.count('www')) / length

    return {k: v / len(posts) for k, v in totals.items()}


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
        'extra-imports': ['main', 'mbti_helper', 'filter_data', 'emoji'],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
