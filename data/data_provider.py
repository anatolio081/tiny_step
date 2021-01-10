import json
import os

goals_path = "data/goals.json"


def get_goals():
    with open(goals_path, "r", encoding='utf-8') as f:
        goals = json.load(f)
    return goals
