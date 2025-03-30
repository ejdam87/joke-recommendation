from recommendation.filler import Filler

import pandas as pd
import numpy as np


class GlobalAverageFiller(Filler):
    def __init__(self) -> None:
        self.means = None

    def fit(self, data: pd.DataFrame) -> None:
        # not considering mean values in the mean
        self.means = np.nanmean(data.values, axis=0)

    def fill(self, row: pd.Series) -> pd.Series:
        assert self.means is not None, "Assuming trained filler"

        row_c = row.copy()
        # input the mean on all empty positions
        row_c[ row.isna() ] = self.means[ row.isna() ]
        return row_c
