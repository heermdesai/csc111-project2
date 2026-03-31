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

    Scoring rationale:
        - Lexical diversity is the dominant signal: a wide and varied vocabulary suggests
          someone who thinks in abstract, nuanced terms rather than plain, literal language.
          It is weighted most heavily as a result.
        - Question density reflects exploratory, speculative thinking. Intuitive types
          are more likely to pose open-ended questions and think out loud about possibilities.
        - Ellipsis density captures trailing, open-ended thoughts ("and then maybe..."),
          which suggests someone comfortable with ambiguity — a hallmark of intuitive types.
          It is weighted least since ellipses can also appear in casual writing unrelated to
          abstract thinking.
    """
    return (
        features['lexical_diversity'] * 10.0 +  # Breadth and variety of vocabulary
        features['question_density'] * 2.0 +    # Exploratory, speculative thinking
        features['ellipsis_density'] * 1.5      # Comfort with open-ended, unresolved thoughts
    )


def calculate_social_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing social engagement and outward orientation.

    Higher scores suggest Extroversion (E); lower scores suggest Introversion (I).

    Scoring rationale:
        - Tag density is weighted most heavily because directly mentioning others (@user)
          is the clearest signal of active, outward social engagement.
        - We-pronoun rate reflects group identity and collective thinking,
          which is characteristic of socially oriented people.
        - Hashtag density captures community participation — joining broader
          conversations rather than posting in isolation.
        - Link density is weighted least: sharing information can indicate engagement,
          but it's a weaker social signal since it doesn't require personal interaction.
    """
    score = (
        features['tag_density'] * 5.0 +      # Direct interaction with others
        features['we_pronoun_rate'] * 3.0 +  # Group-oriented thinking
        features['hashtag_density'] * 2.0 +  # Participation in broader communities
        features['link_density'] * 1.0       # Passive information sharing
    )
    return score


def calculate_expressiveness_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing emotional expressiveness in language.

    Higher scores suggest Feeling (F) traits — decisions guided by empathy and emotion.
    Lower scores suggest Thinking (T) traits — decisions guided by logic and analysis.

    Scoring rationale:
        - Emoji density is the strongest signal since emojis are a deliberate choice to
          communicate emotion visually, which is strongly associated with feeling-oriented types.
        - Exclamation density reflects enthusiasm and emotional intensity in writing —
          feeling types tend to express excitement and warmth more openly.
        - I-pronoun rate captures personal, self-referential language. Feeling types
          are more likely to frame things through personal experience and emotional perspective
          rather than detached, objective statements.
        - Capital density contributes here only when it exceeds the threshold defined in
          _classify_capital_density. High capital density signals ALL CAPS emotional writing,
          which is an expressiveness marker. Below the threshold, it flows to structure_score
          instead.
    """
    expressiveness_from_capitals = _classify_capital_density(features['capital_density'])[0]

    score = (
        features['emoji_density'] * 4.0 +
        features['exclamation_density'] * 3.0 +
        features['i_pronoun_rate'] * 2.0 +
        expressiveness_from_capitals
    )
    return score


def calculate_structure_score(features: dict[str, float]) -> float:
    """
    Calculate a score representing deliberateness and structural control in writing.

    Higher scores suggest Judging (J) traits — preference for order, planning, and closure.
    Lower scores suggest Perceiving (P) traits — preference for spontaneity and flexibility.

    Scoring rationale:
        - Lexical diversity: choosing precise, varied words suggests intentional and controlled expression,
          which aligns with the deliberate nature of judging types. The weight is lower than in complexity
          because diversity alone doesn't confirm structure.
        - Ellipsis density is subtracted with the highest weight because trailing off ("...") is the clearest
          written signal of unresolved, open-ended thinking — the opposite of the closure-oriented mindset of
          judging types.
        - Exclamation density is subtracted because heavy exclamation use signals impulsive, reactive expression,
          which is more characteristic of perceiving types who respond spontaneously rather than deliberately.
        - Capital density contributes here only when it falls below the threshold defined in _classify_capital_density.
          Moderate capitals suggest deliberate emphasis and careful formatting
    """
    structure_from_capitals = _classify_capital_density(features['capital_density'])[1]

    score = (
        features['lexical_diversity'] * 2.0 +
        structure_from_capitals +
        - features['ellipsis_density'] * 4.0 +
        - features['exclamation_density'] * 1.5
    )
    return score


def _classify_capital_density(capital_density: float) -> tuple[float, float]:
    """
    Returns a tuple of (expressiveness_contribution, structure_contribution), where only one value
    is non-zero depending on which side of the threshold the input falls on.
    Moderate use suggests deliberate emphasis and structured writing (J trait), while very high use
    suggests ALL CAPS emotional expression (F trait).

    The threshold of 0.15 reflects that in typical writing, roughly 10-15% capital
    density is expected from proper nouns, sentence starts, and deliberate emphasis.
    Beyond that, all-caps emotional writing becomes the more likely explanation.
    """

    # in most writing, roughly 2-4% capital density is expected for proper grammar
    # analysis of capital density in novels:
    # https://english.stackexchange.com/questions/43563/what-percentage-of-characters-in-...
    # ...normal-english-literature-is-written-in-capital
    capital_threshold = 0.05

    if capital_density >= capital_threshold:
        # High capitals: likely ALL CAPS or heavy emotional emphasis — expressiveness signal
        return capital_density * 2.0, 0.0
    else:
        # Low/moderate capitals: likely deliberate formatting emphasis — structure signal
        return 0.0, capital_density * 2.0


def get_linguistic_features(posts: list[str]) -> dict[str, float]:
    """Extract linguistic traits from a list of posts and return averaged metrics."""
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
        'extra-imports': [],
        'allowed-io': [],
        'max-nested-blocks': 4
    })
