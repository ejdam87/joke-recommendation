import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from utils.paths import V, JOKE_CONTENT

jokes = pd.read_csv(JOKE_CONTENT)
jokes = jokes[~jokes["jokeId"].isin([1,2,3,4,6,9,10,11,12,14])].reset_index(drop=True)

V = np.loadtxt(V, delimiter=',')

scaler = StandardScaler()
V_scaled = scaler.fit_transform(V)

kmeans = KMeans(n_clusters=20, random_state=42)
labels = kmeans.fit_predict(V_scaled)


indices = np.where(labels == 8)[0]
for i in indices:
    print( jokes.iloc[i]["jokeText"] )
    print("---")
