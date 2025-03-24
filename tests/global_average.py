from recommender import GlobalAverageRecommender

import pandas as pd

ratings = pd.read_csv("data/rating_matrix_clean_uidless.csv")

recsys = GlobalAverageRecommender()
recsys.fit(ratings)

print( recsys.predict( ratings.iloc[1] ) )
