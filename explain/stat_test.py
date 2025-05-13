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


def prepare_sample(profile_paths: list[str], do_normalize: bool) -> dict[str, NDArray]:
    res = {"cb": [], "svd": [], "random": []}
    for profile in profile_paths:
        ratings = get_ratings(profile)
        n_ratings = normalize(ratings) if do_normalize else ratings
        for k, rats in n_ratings.items():
            res[k].append(rats)
    
    return { k: np.concatenate(v, axis=0) for k, v in res.items() }

n_samples = prepare_sample( [f"./data/profiles/profile_{p}.json" for p in PROFILES], True )
samples = prepare_sample( [f"./data/profiles/profile_{p}.json" for p in PROFILES], False )


from scipy.stats import shapiro

for system in ["cb", "svd", "random"]:
    stat, p = shapiro(n_samples[system])
    print(p)

import matplotlib.pyplot as plt
# Data
means = [np.mean(samples["cb"]), np.mean(samples["svd"]), np.mean(samples["random"])]
stds = [np.std(samples["cb"]), np.std(samples["svd"]), np.std(samples["random"])]
labels = ["CB", "SVD", "Random"]

x_pos = range(len(means))

# Create dot plot
plt.figure(figsize=(6, 4))
plt.errorbar(x_pos, means, yerr=stds, fmt='o', capsize=5, color='black', ecolor='#C4C4C4')

plt.text(x_pos[0] + 0.1, means[0] + 0.2, f'{means[0]:.2f}±{stds[0]:.2f}', ha='center', va='bottom', fontsize=10, color='blue')
plt.text(x_pos[1], means[1] + 0.2, f'{means[1]:.2f}±{stds[1]:.2f}', ha='center', va='bottom', fontsize=10, color='blue')
plt.text(x_pos[2] - 0.1, means[2] + 0.2, f'{means[2]:.2f}±{stds[2]:.2f}', ha='center', va='bottom', fontsize=10, color='blue')


plt.ylabel("Mean Rating")
plt.xticks(x_pos, labels)
plt.title("Mean rating per system")
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

from scipy.stats import friedmanchisquare, wilcoxon

stat, p = friedmanchisquare(n_samples["cb"], n_samples["svd"], n_samples["random"])
print(p)

stat_12, p_12 = wilcoxon(n_samples["cb"], n_samples["svd"])
stat_13, p_13 = wilcoxon(n_samples["cb"], n_samples["random"])
stat_23, p_23 = wilcoxon(n_samples["svd"], n_samples["random"])

print(p_12)
print(p_13)
print(p_23)
