"""filter data"""

import csv


def load_reddit_psychometric(mbti_file: str) -> None:
    with open(mbti_file, newline='') as file:
        csv_reader = csv.reader(file)



