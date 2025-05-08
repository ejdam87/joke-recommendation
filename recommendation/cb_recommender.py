import json
import pandas as pd
import numpy as np
from collections import Counter
from .recommender_interface import AbstractRecommender


class ContentBasedRecommender(AbstractRecommender):
    def __init__(self, joke_labels_path, jokes_labeled_path, rating_matrix_path):
        """
        Initializes the Content-Based Recommender System.
        Loads labeled jokes, joke labels, and user ratings.
        """
        self.joke_labels = pd.read_csv(joke_labels_path)
        self.jokes_labeled = pd.read_csv(jokes_labeled_path)
        self.rating_matrix = pd.read_csv(rating_matrix_path)

        self.rating_matrix.drop(columns=['userId'], inplace=True)
        self.rating_matrix.columns = [i for i in range(self.rating_matrix.shape[1])]

        # Parse label_ids from strings to actual lists
        self.jokes_labeled['label_ids'] = self.jokes_labeled['label_ids'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )

        # should be empty, only rated jokes used
        self.forbidden_jokes = [
            col for col in self.rating_matrix.columns[self.rating_matrix.isna().all()]
        ]

        self.not_rated_jokes = [
            col for col in self.rating_matrix.columns if col not in self.forbidden_jokes
        ]

        # Create joke_id -> label_ids mapping
        self.jokes_labeled['joke_id'] = self.jokes_labeled['joke_id'] - 1 # start from 0
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
        
        if not 0 <= uid < self.rating_matrix.shape[0]:
            rated_jokes = []
        else:
            user_ratings = self.rating_matrix.iloc[uid]
            print("uid", uid)
            print(user_ratings)
            rated_jokes = user_ratings[user_ratings.notna()].index.astype(int).tolist()

        if len(rated_jokes) < 5:
            return self.best_jokes(uid, top_k)
        
        if len(self.not_rated_jokes) < top_k:
            return self.not_rated_jokes
        
        suitable_labels = {}
        for joke_id in rated_jokes:
            joke_labels = self.joke_to_labels.get(joke_id, [])
            for label in joke_labels:
                if label not in suitable_labels:
                    suitable_labels[label] = 0
                suitable_labels[label] += self.rating_matrix.iloc[uid, joke_id]
        suitable_labels = dict(sorted(suitable_labels.items(), key=lambda item: item[1], reverse=True))

        jokes_score = {}
        for joke_id in self.not_rated_jokes:
            for label in self.joke_to_labels.get(joke_id, []):
                if label in suitable_labels:
                    jokes_score[joke_id] = jokes_score.get(joke_id, 0) + suitable_labels[label]

        res = sorted(
            jokes_score,
            key=lambda k: 0 if pd.isna(jokes_score[k]) else jokes_score[k],
            reverse=True
        )
        print(f"CB recommends {res[0]}")
        return res[:top_k]

                    

    def add_user(self):
        """
        Add a new user to the rating matrix with unrated (NaN) jokes.

        Returns:
            int: ID of the newly added user.
        """
        new_user = pd.Series([np.nan] * self.rating_matrix.shape[1], index=self.rating_matrix.columns)
        self.rating_matrix = pd.concat([self.rating_matrix, new_user.to_frame().T], ignore_index=True)
        return self.rating_matrix.shape[0] - 1


    def best_jokes(self, user_id, top_k=6):
        """
        Get the top K jokes the user has not seen, based on average ratings.

        Args:
            user_id (int): The user ID.
            top_k (int): Number of top jokes to return.

        Returns:
            list[int]: List of top K unseen joke IDs.
        """
        if not 0 <= user_id < self.rating_matrix.shape[0]:
            seen_jokes = set()
        else:
            seen_jokes = set(self.rating_matrix.iloc[user_id].dropna().index)
            # print(f"Seen jokes for user {user_id}: {seen_jokes}")

        avg_ratings = self.rating_matrix.mean()
        print("AVG", avg_ratings)
        unseen_ratings = avg_ratings[~avg_ratings.index.isin(seen_jokes)]
        top_jokes = unseen_ratings.sort_values(ascending=False).head(top_k)
        print("TOP",top_jokes)
        res = top_jokes.index.tolist()
        print(f"CB recommends top overall {res[0]}")
        return res


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
        # joke_id_str = str(joke_id)
        if not 0 <= joke_id < self.rating_matrix.shape[1]:
            raise ValueError(f"Joke ID {joke_id} not found in rating matrix.")
        if not 0 <= user_id < self.rating_matrix.shape[0]:
            raise ValueError(f"User ID {user_id} not found in rating matrix.")
        
        if joke_id in self.not_rated_jokes:
            self.not_rated_jokes.remove(joke_id)
        self.rating_matrix.iloc[user_id, joke_id] = rating

    def safe_state(self):
        """
        Save the current state of the recommender system.

        Returns:
            dict: State of the recommender system.
        """
        pd.to_csv(self.rating_matrix, "rating_matrix_new.csv", index=True)
