import json

def get_avg(profile_path: str) -> dict[str, float]:
    with open(profile_path, "r") as f:
        profile = json.load(f)
    
    sys_to_rating = {"cb": [], "svd": [], "random": []}
    for k, rating in profile.items():
        joke, system = k.split()
        sys_to_rating[system].append(rating)
    
    return { sys : sum(v) / len(v) for sys, v in sys_to_rating.items() }

for system, avg_r in get_avg("./data/profiles/profile_elza.json").items():
    print(system, f": {avg_r:.3f}")
