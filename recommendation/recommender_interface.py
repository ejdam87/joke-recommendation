from abc import ABC, abstractmethod

class AbstractRecommender(ABC):
    @abstractmethod
    def recommend(self, user_id, k):
        pass
    
    
    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def user_ratings(self, user_id):
        pass

    @abstractmethod
    def submit_rating(self, user_id, joke_id, rating):
        pass

    