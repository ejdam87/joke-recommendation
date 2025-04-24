import os
import json
from collections import defaultdict, Counter
import pandas as pd
import numpy as np
from .recommender_interface import AbstractRecommender
JOKE_LABELS = "../data/joke_labels.csv"
JOKES_LABELED = "../data/jokes_labeled.csv"
RATING_MATRIX = "../data/rating_matrix.csv"

class ContentBasedRecommender(AbstractRecommender):
    def __init__(self):
        """
        Initializes the Content-Based Recommendation System.
        Loads jokes and labels from the specified data folder.
        """
        self.jokes_labeled = pd.read_csv(JOKES_LABELED)
        self.joke_labels = pd.read_csv(JOKE_LABELS)
        self.rating_matrix = pd.read_csv(RATING_MATRIX)

        # Ensure label_ids are lists (from string like "[1,2]" to list [1,2])
        self.jokes_labeled['label_ids'] = self.jokes_labeled['label_ids'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )

        # joke_id -> label_ids map
        self.joke_to_labels = self.jokes_labeled.set_index('joke_id')['label_ids'].to_dict()

    def recommend(self, uid, top_k=6):
        """
        Recommend jokes to a user based on content similarity (shared labels).
        
        Args:
            uid (int): User ID (row index in rating_matrix).
            top_k (int): Number of jokes to recommend.

        Returns:
            List of recommended joke IDs.
        """
        # Get user ratings
        user_ratings = self.rating_matrix.loc[uid]
        rated_jokes = user_ratings[user_ratings.notna()].index.astype(int)

        if len(rated_jokes) > 0:
            # TODO
            return []

        # Build user profile: label preferences weighted by rating
        label_scores = Counter()
        for joke_id in rated_jokes:
            rating = user_ratings[str(joke_id)]
            for label in self.joke_to_labels.get(joke_id, []):
                label_scores[label] += rating

        # Score all jokes based on overlap with user label preferences
        joke_scores = {}
        for joke_id, labels in self.joke_to_labels.items():
            if str(joke_id) in rated_jokes:
                continue  # Skip already rated jokes
            score = sum(label_scores.get(label, 0) for label in labels)
            if score != 0:
                joke_scores[joke_id] = score

        # Return top_k jokes sorted by score
        top_jokes = sorted(joke_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [joke_id for joke_id, _ in top_jokes]
    
    def add_user(self):
        """
        Add a new user to the system by appending a row of NaNs (unrated) to the rating matrix.
        
        Returns:
            int: The ID of the newly added user (row index).
        """
        new_user = pd.Series([np.nan] * self.rating_matrix.shape[1], index=self.rating_matrix.columns)
        self.rating_matrix = pd.concat([self.rating_matrix, new_user.to_frame().T], ignore_index=True)
        return self.rating_matrix.shape[0] - 1

    def user_ratings(self, user_id):
        """
        Get all the user's ratings as a dictionary: {joke_id: rating}.
        
        Args:
            user_id (int): ID of the user (row index in rating_matrix).
        
        Returns:
            dict: Joke ID -> Rating for the user.
        """
        user_row = self.rating_matrix.loc[user_id]
        return user_row.dropna().astype(float).to_dict()

    def submit_rating(self, user_id, joke_id, rating):
        """
        Save a new rating into the matrix.
        
        Args:
            user_id (int): The user ID.
            joke_id (int): The joke ID (must match column name in rating_matrix).
            rating (float): The rating to assign.
        """
        joke_id_str = str(joke_id)
        if joke_id_str not in self.rating_matrix.columns:
            raise ValueError(f"Joke ID {joke_id} not found in rating matrix columns.")
        self.rating_matrix.at[user_id, joke_id_str] = rating