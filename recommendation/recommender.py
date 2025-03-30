import pandas as pd

from recommendation.filler import Filler


class Recommender:

    def __init__(self, filler: Filler) -> None:
        self.filler = filler

    def fit(self, data: pd.DataFrame) -> None:
        self.filler.fit(data)

    def predict(self, row: pd.Series) -> pd.Series:
        missing = row.isna()
        filled = self.filler.fill(row)
        new_scores = filled[missing]
        return new_scores.sort_values(ascending=False)
