from dataclasses import dataclass
from datetime import datetime
import os
import pickle
import random

from src.utils import constants as c


def get_random_position() -> list[int]:
    """
    Get a random position on the grid

    Returns:
        list[int]: A list with two integers representing the x and y coordinates
    """
    return [random.randint(50, c.WIDTH - 50), random.randint(50, c.HEIGHT - 50)]


@dataclass
class Score:
    date: str
    score: int


def get_top_five_scores() -> list[Score]:
    """
    Get the top five scores from the scores file

    Returns:
        list[Score]: A list with the top five Score objects
    """
    try:
        if os.path.isfile(c.SCORES_FILE):
            with open(c.SCORES_FILE, "rb") as file:
                scores = pickle.load(file)
                if not scores:
                    return []
                return sorted(scores, key=lambda x: x.score, reverse=True)[:5]
    except (EOFError, FileNotFoundError, pickle.UnpicklingError):
        if os.path.exists(c.SCORES_FILE):
            os.remove(c.SCORES_FILE)
        return []

    return []


def save_current_score(scores: list):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_score_objects = [Score(date=timestamp, score=score) for score in scores]
    existing_scores = []

    os.makedirs(os.path.dirname(c.SCORES_FILE), exist_ok=True)

    try:
        if os.path.isfile(c.SCORES_FILE):
            with open(c.SCORES_FILE, "rb") as file:
                existing_scores = pickle.load(file)
    except EOFError:
        existing_scores = []

    all_scores = existing_scores + new_score_objects

    with open(c.SCORES_FILE, "wb") as file:
        pickle.dump(all_scores, file)
