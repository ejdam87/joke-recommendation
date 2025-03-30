from recommendation import Recommender, GlobalAverageFiller

import pandas as pd

ratings = pd.read_csv("data/rating_matrix_clean_uidless.csv")

recsys = Recommender( GlobalAverageFiller() )
recsys.fit(ratings)

print( recsys.predict( ratings.iloc[1] ) )
