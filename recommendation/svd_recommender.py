import numpy as np
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity

class SVDRecommender:
    def __init__(self, u_path, v_path, ratings_path, retraining_patience):
        self.V = np.loadtxt(v_path, delimiter=',')
        self.U = np.loadtxt(u_path, delimiter=',')

        self.R = np.loadtxt(ratings_path, delimiter=',')

        self.ratings_since_training = {}
        self.retraining_patience = retraining_patience

        # jokes = pd.read_csv("data/jester_items.csv")
        # self.jokes = jokes[~jokes["jokeId"].isin([1,2,3,4,6,9,10,11,12,14])].reset_index(drop=True)
    
    def seen_jokes(self, user_id):
        seen = np.where(~np.isnan(self.R[user_id]))[0]
        return seen
    
    def overall_top_k(self, user_id, k):
        jokes_sorted = np.nanmean(self.R, axis=0).argsort()[::-1]
        seen = self.seen_jokes(user_id)
        jokes_filtered = jokes_sorted[~np.isin(jokes_sorted, seen)][:k]

        # for idx in jokes_filtered:
            # print(f"Joke {idx} - score {np.nanmean(self.R[:,idx])}: {self.jokes.iloc[idx]['jokeText']}")
        
        return jokes_filtered

    def recommend(self, user_id, k):
        if user_id == -1:
            return [1, 1, 1, 1, 1, 1]

        seen = self.seen_jokes(user_id)

        if len(seen) <= 5:
            top = self.overall_top_k(user_id, k)
            return top

        preds = np.dot(self.V, self.U[user_id]).argsort()[::-1]
        top_k_filtered = preds[~np.isin(preds, seen)][:k]

        # for idx in top_k_filtered:
            # print(self.jokes.iloc[idx]["jokeText"])

        return top_k_filtered

    def recommend_weighted_mean(self, user_id, k):
        if len(self.seen_jokes(user_id)) <= 5:
            top = self.overall_top_k(user_id, k)
            return top

        seen = self.seen_jokes(user_id)
        print(f"Seen: {seen}")
        ratings = self.R[user_id][seen]

        similarities = cosine_similarity(self.V[seen], self.V)
        weighted_similarities = similarities * ratings[:, None]
        summed_similarities = np.sum(weighted_similarities, axis=0)
        similarities_indices = summed_similarities.argsort()[::-1]
        similarities_filtered = similarities_indices[~np.isin(similarities_indices, seen)][:k]

        # for idx in similarities_filtered:
            # print(f"Joke {idx} - score {summed_similarities[idx]}: {self.jokes.iloc[idx]['jokeText']}")

        return similarities_filtered

    def submit_rating(self, user_id, joke_id, rating):
        self.R[user_id][joke_id] = rating
        self.trigger_training(user_id)

    def add_user(self):
        u = [np.nan] * self.U.shape[1]
        r = [np.nan] * self.R.shape[1]
        self.U = np.vstack([self.U, u])
        self.R = np.vstack([self.R, r])

        return self.U.shape[0] - 1

    def trigger_training(self, user_id):
        since_training = self.ratings_since_training.get(user_id, 0)
        print(f"Ratings since training: {since_training}")
        if since_training >= self.retraining_patience:
            self.U[user_id] = self.train_user(user_id)
            self.ratings_since_training[user_id] = 0
        else:
            self.ratings_since_training[user_id] = since_training + 1         
    
    def train_user(self, user_id):
        num_factors = self.U.shape[1]
        lr = 0.005
        reg = 0.02
        epochs = 50

        u = np.random.normal(scale=0.01, size=num_factors)

        rated_indices = np.where(~np.isnan(self.R[user_id]))[0]
        ratings = self.R[user_id, rated_indices]

        for epoch in range(epochs):
            total_loss = 0
            print(f"Training epoch {epoch}")
            for j_idx, r in zip(rated_indices, ratings):
                v = self.V[j_idx]
                pred = np.dot(u, v)
                err = r - pred
                u += lr * (err * v - reg * u)
                total_loss += err**2 + reg * np.sum(u**2)
            print(f"Loss: {total_loss / len(rated_indices)}")

        return u
    
    def import_profile(self, in_path, user_id = None):
        with open(in_path, 'r') as file:
            profile = json.load(file)

        if user_id is None:
            user_id = self.add_user()

        for joke_id, rating in profile.items():
            self.R[user_id][int(joke_id)] = rating
        
        return user_id
    
    def export_profile(self, out_path, user_id):
        rating_indices = np.where(~np.isnan(self.R[user_id]))[0]
        print(rating_indices)
        ratings_dict = {}

        for idx in rating_indices:
            ratings_dict[str(idx)] = self.R[user_id][idx]
        
        with open(out_path, 'w') as file:
            json.dump(ratings_dict, file)
    
    def user_ratings(self, user_id):
        if user_id >= self.U.shape[0]:
            return None

        ratings = self.R[user_id]
        valid_mask = ~np.isnan(ratings)
        valid_indices = np.where(valid_mask)[0]
        valid_ratings = ratings[valid_mask]

        rating_dict = dict(zip(valid_indices, valid_ratings))

        return rating_dict
    
    def save_matrices(self, u_path, v_path, r_path):
        np.savetxt(u_path, self.U, delimiter=",")
        np.savetxt(v_path, self.V, delimiter=",")
        np.savetxt(r_path, self.R, delimiter=",")