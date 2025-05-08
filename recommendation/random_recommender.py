import pandas as pd
import numpy as np
import random
from .recommender_interface import AbstractRecommender


class RandomRecommender(AbstractRecommender):
    """ A recommender system that suggests jokes randomly.

        This recommender system provides joke recommendations by randomly selecting from available jokes.
        For existing users, it prioritizes jokes they haven't rated yet. If there aren't enough
        unrated jokes, it falls back to recommending from all available jokes.
        
        Inherits from:
            AbstractRecommender: Interface defining recommender system methods.
    """
    def __init__(self, rating_matrix_path):
        self.rating_matrix = pd.read_csv(rating_matrix_path)

        self.rating_matrix.drop(columns=['userId'], inplace=True)
        self.rating_matrix.columns = [i for i in range(self.rating_matrix.shape[1])]

        # should be empty, only rated jokes used
        self.forbidden_jokes = [
            col for col in self.rating_matrix.columns[self.rating_matrix.isna().all()]
        ]

        self.not_rated_jokes = [
            col for col in self.rating_matrix.columns if col not in self.forbidden_jokes
        ]


    def recommend(self, uid, top_k=6):
        """Generate random joke recommendations for a user.
        
        Args:
            uid (int): User ID to generate recommendations for
            top_k (int, optional): Number of recommendations to return. Defaults to 6.
            
        Returns:
            list[int]: List of recommended joke IDs (length <= top_k)
            
        Behavior:
        - For new users (uid not in matrix): Returns random selection from all jokes
        - For existing users: Returns random selection from unrated jokes
        - If insufficient unrated jokes: Falls back to random selection from all jokes
        """
        if len(self.not_rated_jokes) < top_k:
            return self.not_rated_jokes
        sample = random.sample(self.not_rated_jokes, top_k)
        print(f"Random recommends {sample[0]}")
        return sample
    

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
        if not 0 <= user_id < self.rating_matrix.shape[0]:
            raise ValueError(f"User ID {user_id} not found in rating matrix.")
        user_row = self.rating_matrix.iloc[user_id]
        return user_row.dropna().astype(float).to_dict()

    def submit_rating(self, user_id, joke_id, rating):
        """
        Store a user's rating for a specific joke.

        Args:
            user_id (int): User ID.
            joke_id (int): Joke ID.
            rating (float): Rating value.
        """
        if not 0 <= joke_id < self.rating_matrix.shape[1]:
            raise ValueError(f"Joke ID {joke_id} not found in rating matrix.")
        if not 0 <= user_id < self.rating_matrix.shape[0]:
            raise ValueError(f"User ID {user_id} not found in rating matrix.")
        
        if joke_id in self.not_rated_jokes:
            self.not_rated_jokes.remove(joke_id)
        self.rating_matrix.iloc[user_id, joke_id] = rating