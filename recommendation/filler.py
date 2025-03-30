from abc import ABC, abstractmethod

import pandas as pd


class Filler(ABC):

    @abstractmethod
    def fit(self, data: pd.DataFrame) -> None:
        """
        A method to train a recommender system from rating matrix <data>.

        params:
            - <data> - rating matrix (rows ~ users, columns ~ jokes)
        """
        ...

    @abstractmethod
    def fill(self, row: pd.Series) -> pd.Series:
        """
        A method to predict (fill) missing ratings in given <row> of rating matrix.

        (Assuming the same order of jokes as given to <fit>.)

        params:
            - <row> a single row of rating matrix
        
        returns:
            - The same row with filled all missing ratings
        """
        ...
