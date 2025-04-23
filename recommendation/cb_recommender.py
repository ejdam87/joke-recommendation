import os
import json
from collections import defaultdict
import pandas as pd
import numpy as np

JOKE_LABELS = "/data/jokes_labels.csv"
JOKES_LABELED = "data/jokes_labeled.csv"
RATING_MATRIX = "data/rating_matrix.csv"

class ContentBasedSystem:
    def __init__(self):
        """
        Initializes the Content-Based Recommendation System.
        Loads jokes and labels from the specified data folder.
        """
        self.jokes_labeled = pd.read_csv(JOKES_LABELED)
        self.joke_labels = pd.read_csv(JOKE_LABELS)

        # Ensure label_ids are lists (from string like "[1,2]" to list [1,2])
        self.jokes_labeled['label_ids'] = self.jokes_labeled['label_ids'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )

        # joke_id -> label_ids map
        self.joke_to_labels = self.jokes_labeled.set_index('joke_id')['label_ids'].to_dict()

    def recommend(self, path_to_profile, top_k=6):
        """
        Recommends top_k jokes for the user based on their profile.

        Args:
            path_to_profile (str): Path to JSON file with joke ratings (joke_id -> rating).
            top_k (int): Number of recommendations to return.

        Returns:
            List[int]: List of recommended joke_ids.
        """
        with open(path_to_profile, 'r') as f:
            user_ratings = {int(k): float(v) for k, v in json.load(f).items()}

        # Build label importance from rated jokes
        label_scores = defaultdict(float)
        for joke_id, rating in user_ratings.items():
            labels = self.joke_to_labels.get(joke_id, [])
            for label in labels:
                label_scores[label] += rating

        # Score all unrated jokes
        scores = []
        for joke_id, labels in self.joke_to_labels.items():
            if joke_id in user_ratings:
                continue
            score = sum(label_scores.get(label, 0.0) for label in labels)
            scores.append((joke_id, score))

        # Sort and return top K
        scores.sort(key=lambda x: x[1], reverse=True)
        return [joke_id for joke_id, _ in scores[:top_k]]
