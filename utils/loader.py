import pandas as pd
import numpy as np


def ratings_as_matrix(ratings_path: str, jokes_path: str) -> pd.DataFrame:
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

    # insert non-rated jokes
    for joke_id in non_rated["jokeId"]:
        matrix[joke_id] = np.nan

    # sort by joke ID
    return matrix.sort_index(axis=1)


def save_matrix(ratings_path: str, jokes_path: str, out_path: str) -> None:
    """
    Saves the rating matrix to given <out_path>
    """
    matrix = ratings_as_matrix(ratings_path, jokes_path)
    matrix.to_csv(out_path)
