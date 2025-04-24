import json
import pandas as pd
import numpy as np
from collections import Counter
from .recommender_interface import AbstractRecommender

JOKE_LABELS = "../data/joke_labels.csv"
JOKES_LABELED = "../data/jokes_labeled.csv"
RATING_MATRIX = "../data/rating_matrix.csv"

class ContentBasedRecommender(AbstractRecommender):
    def __init__(self, joke_labels_path, jokes_labeled_path, rating_matrix_path):
        """
        Initializes the Content-Based Recommender System.
        Loads labeled jokes, joke labels, and user ratings.
        """
        self.joke_labels = pd.read_csv(joke_labels_path)
        self.jokes_labeled = pd.read_csv(jokes_labeled_path)
        self.rating_matrix = pd.read_csv(rating_matrix_path)

        self.rating_matrix.set_index('userId', inplace=True)
        self.rating_matrix.index = self.rating_matrix.index.astype(int)
        self.rating_matrix = self.rating_matrix.loc[:, self.rating_matrix.columns.str.isdigit()]

        # Parse label_ids from strings to actual lists
        self.jokes_labeled['label_ids'] = self.jokes_labeled['label_ids'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )

        # Create joke_id -> label_ids mapping
        self.joke_to_labels = self.jokes_labeled.set_index('joke_id')['label_ids'].to_dict()

    def recommend(self, uid, top_k=6):
        """
        Recommend jokes to a user based on content similarity via shared labels.

        Args:
            uid (int): User ID.
            top_k (int): Number of jokes to recommend.

        Returns:
            list[int]: List of recommended joke IDs.
        """
        if uid not in self.rating_matrix.index:
            raise ValueError(f"User ID {uid} not found in rating matrix.")

        user_ratings = self.rating_matrix.loc[uid]
        rated_jokes = user_ratings[user_ratings.notna()].index.astype(int).tolist()

        if not rated_jokes:
            return [1,2,3,4,5,6] # placeholder 

        label_scores = Counter()
        for joke_id in rated_jokes:
            rating = user_ratings[str(joke_id)]
            for label in self.joke_to_labels.get(joke_id, []):
                label_scores[label] += rating

        joke_scores = {}
        for joke_id, labels in self.joke_to_labels.items():
            if joke_id in rated_jokes:
                continue  # Skip jokes already rated
            score = sum(label_scores.get(label, 0) for label in labels)
            if score > 0:
                joke_scores[joke_id] = score

        top_jokes = sorted(joke_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [joke_id for joke_id, _ in top_jokes]

    def add_user(self):
        """
        Add a new user to the rating matrix with unrated (NaN) jokes.

        Returns:
            int: ID of the newly added user.
        """
        new_user = pd.Series([np.nan] * self.rating_matrix.shape[1], index=self.rating_matrix.columns)
        self.rating_matrix = pd.concat([self.rating_matrix, new_user.to_frame().T], ignore_index=True)
        return self.rating_matrix.shape[0] - 1

    def user_ratings(self, user_id):
        """
        Get all the user's ratings.

        Args:
            user_id (int): User ID.

        Returns:
            dict: {joke_id: rating}
        """
        if user_id not in self.rating_matrix.index:
            raise ValueError(f"User ID {user_id} not found in rating matrix.")
        user_row = self.rating_matrix.loc[user_id]
        return user_row.dropna().astype(float).to_dict()

    def submit_rating(self, user_id, joke_id, rating):
        """
        Store a user's rating for a specific joke.

        Args:
            user_id (int): User ID.
            joke_id (int): Joke ID.
            rating (float): Rating value.
        """
        joke_id_str = str(joke_id)
        if joke_id_str not in self.rating_matrix.columns:
            raise ValueError(f"Joke ID {joke_id} not found in rating matrix.")
        if user_id not in self.rating_matrix.index:
            raise ValueError(f"User ID {user_id} not found in rating matrix.")
        self.rating_matrix.at[user_id, joke_id_str] = rating
