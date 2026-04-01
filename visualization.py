"""..."""

import pygame
from main import MBTITree

# colors
WHITE = (255, 255, 255)
BLUE = (118, 156, 188)
BLUE_HOVER = (101, 144, 180)
BLACK = (0, 0, 0)

# values
WIDTH = 800
HEIGHT = 200
MARGIN = 52
BUTTON_HEIGHT = 55
BUTTON_GAP = 10

QUESTIONS = {
        "social_score": "I actively engage with others online by tagging them, using hashtags, or sharing links.",
        "complexity_score": "I prefer using abstract metaphors and a sophisticated vocabulary over simple facts.",
        "expressiveness_score": "My writing is often filled with emotion, exclamation points, and emojis.",
        "structure_score": "I put a lot of effort into making my posts organized and grammatically correct.",
        "average_post_length": "I usually write long, detailed explanations rather than short snippets."
}

OPTIONS = [
    ('Strongly disagree', 0.0),
    ('Disagree', 0.25),
    ('Neutral', 0.5),
    ('Agree', 0.75),
    ('Strongly agree', 1.0),
]


class MBTIQuizWindow:
    """..."""
    tree: MBTITree
    curr_node: MBTITree
    path: list[tuple[str, float, str]]
    result: str
    hovered: int

    def __init__(self, tree: MBTITree):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MBTI Personality Quiz')

        self.font = pygame.font.Font('Georgia', 15)
        self.font_result = pygame.font.Font('Georgia', 55, bold=True)

        self.tree = tree
        self.curr_node = self.tree
        self.path = []
        self.result = ''
        self.hovered = -1

    def _get_depth(self) -> int:
        """Returns how many questions have been answered so far."""
        return len(self.path)


############ DRAWINGS ############
def _option_boxes() -> list[pygame.Rect]:
    """Returns a list of rectangles representing the option boxes."""
    boxes = []
    y = 200
    for x in OPTIONS:
        boxes.append(pygame.Rect(MARGIN, y, WIDTH - MARGIN * 2, BUTTON_HEIGHT))
        y += BUTTON_HEIGHT + BUTTON_GAP

    return boxes


############ EVENTS ############
def handle_click(self, position: tuple[int, int]) -> None:
    """Respond to mouse click"""
    if self.result:
        self._restart()
        return

    choices = self._option_boxes()
    i = 0
    for c in choices:
        if c.collidepoint(position):
            label, score = OPTIONS[i]
            feature = self.current_node.feature

            self.path.append((feature, score, label))
        i += 1

    subtrees = self.current_node.get_subtrees()
    if self.score < self.current_node.threshold:
        next_node = subtrees[0]
    else:
        next_node = subtrees[1]

    if next is None:
        self.result = self._root
    else:
        self.current_node = next_node


def handle_hover(self, position: tuple[int, int]) -> None:
    """Track where the mouse is hovering."""
    if self.result:
        self.hovered = -1
        return
    self.hovered = -1
    i = 0
    for rect in self._option_rects():
        if rect.collidepoint(position):
            self.hovered = i
        i += 1


#### DRAW FRAME ####
def draw(self) -> None:
    """..."""
    self.screen.fill(WHITE)
    if self.result:
        self._draw_result()
    else:
        self._draw_question()


def _draw_question(self) -> None:
    """..."""
    node = self.current_node
    depth = self._get_depth()
    total = 5
    feature = node.feature

    question = QUESTIONS[feature]
    lines = wrap_text(question, self.font_q, W - MARGIN * 2)
