from pathlib import Path

import pandas as pd
import numpy as np


def ratings_as_matrix(ratings_path: str, jokes_path: str, include_non_rated: bool=True) -> pd.DataFrame:
    """
    Loads joke ratings in a form of matrix where:
        column ~ joke
        row    ~ user
        value on matrix[i][j] corresponds to the rating of joke <j> of user <i> 
    """
    rdf = pd.read_csv(ratings_path)
    jdf = pd.read_csv(jokes_path)
    non_rated = jdf[ ~jdf["jokeId"].isin( rdf["jokeId"] ) ]
    matrix = rdf.pivot(index='userId', columns='jokeId', values='rating')

    if include_non_rated:
        # insert non-rated jokes
        for joke_id in non_rated["jokeId"]:
            matrix[joke_id] = np.nan

    # sort by joke ID
    return matrix.sort_index(axis=1)


def save_matrix(ratings_path: str, jokes_path: str, out_path: str, include_non_rated: bool=True) -> None:
    """
    Saves the rating matrix to given <out_path>
    """
    matrix = ratings_as_matrix(ratings_path, jokes_path, include_non_rated)
    matrix.to_csv(out_path)


def remove_uid(rating_matrix_path: str) -> None:
    """
    Drops User ID from the rating matrix and stores it in the same directory
    """
    ratings = pd.read_csv(rating_matrix_path)
    ratings.drop("userId", axis=1, inplace=True)
    ratings.to_csv( Path(rating_matrix_path).with_name("rating_matrix_clean_uidless.csv"), index=False )
