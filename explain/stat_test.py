import json

import numpy as np
from numpy.typing import NDArray


PROFILES = ["adam", "david", "elza", "majo", "mato", "miso", "terezka", "zuzka"]


def get_ratings(profile_path: str) -> dict[str, NDArray]:
    """ system -> vector of ratings """
    with open(profile_path, "r") as f:
        profile = json.load(f)

    sys_to_rating = {"cb": [], "svd": [], "random": []}
    for k, rating in profile.items():
        _, system = k.split()
        sys_to_rating[system].append(rating)
    
    return {k: np.array(v) for k, v in sys_to_rating.items()}


def normalize(ratings: dict[str, NDArray]) -> dict[str, NDArray]:
    """ system -> normalized vector of ratings """
    all_ratings = []
    stds = []
    for system, vals in ratings.items():
        all_ratings.append(vals)
        stds.append(np.std(vals))

    global_mean = np.mean( np.array(all_ratings) )
    return {s: (vals - global_mean) / stds[i] for i, (s, vals) in enumerate(ratings.items()) }


def prepare_sample(profile_paths: list[str]) -> dict[str, NDArray]:
    res = {"cb": [], "svd": [], "random": []}
    for profile in profile_paths:
        ratings = get_ratings(profile)
        n_ratings = normalize(ratings)
        n_ratings = ratings
        for k, rats in n_ratings.items():
            res[k].append(rats)
    
    return { k: np.concatenate(v, axis=0) for k, v in res.items() }

samples = prepare_sample( [f"./data/profiles/profile_{p}.json" for p in PROFILES] )

"""
from scipy.stats import shapiro
stat, p = shapiro(samples["random"])
print(p)
"""

from scipy.stats import friedmanchisquare, wilcoxon

stat, p = friedmanchisquare(samples["cb"], samples["svd"], samples["random"])
print(p)

stat_12, p_12 = wilcoxon(samples["cb"], samples["svd"])
stat_13, p_13 = wilcoxon(samples["cb"], samples["random"])
stat_23, p_23 = wilcoxon(samples["svd"], samples["random"])

print(p_12)
print(p_13)
print(p_23)
