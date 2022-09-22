import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from utils.train_val_test_split import split
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pickle

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--events", type=str, default="../data/events.json", help="path to event.json")
    parser.add_argument("--dataset", type=str, default="../data/dataset.csv", help="path to dataset created in csv")
    parser.add_argument("--nclusters", type=int, default=5, help="number of clusters used in KMeans")
    parser.add_argument("--ninit", type=int, default=50, help="number of runs in an iteration used in KMeans")
    parser.add_argument("--maxiter", type=int, default=500, help="number of iterations used in KMeans")

    opt = parser.parse_args()

    data = pd.read_csv(opt.dataset)
    sess_ids_uniques = data["sessionid"]
    data.drop(columns=["Unnamed: 0", "sessionid"], inplace=True)

    train_data = split(sess_ids_uniques, data, opt.events)

    preprocessor = Pipeline(
        [
            ("scaler", StandardScaler()),
        ]
    )
    clusterer = Pipeline(
        [
            (
                "kmeans",
                KMeans(
                    n_clusters=opt.nclusters,
                    init="k-means++",
                    n_init=opt.ninit,
                    max_iter=opt.maxiter,
                    random_state=42,
                    verbose=1
                ),
            ),
        ]
    )
    pipe = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("clusterer", clusterer)
        ]
    )

    """"
    # Uncomment this line if you want to see the silhouette coefficient scores, 5 for the best (0.71)
    scores = []
    kmeans_kwargs = {
          "init": "k-means++",
          "n_init": 30,
          "max_iter": 100,
          "random_state": 42,
          }
    scaler = StandardScaler()
    count = 0
    for i in range(3, 122, 2):
        pre_d = scaler.fit_transform(train_data)
        kmeans = KMeans(n_clusters=i, **kmeans_kwargs)
        kmeans.fit(pre_d)
        preds = kmeans.labels_
        scores.append(silhouette_score(pre_d, preds))
        print(i, scores[count])
        count += 1
    plt.plot(scores)
    plt.show()
    """
    pipe.fit(train_data)
    preprocessed_data = pipe["preprocessor"].transform(train_data)
    predicted_labels = pipe["clusterer"]["kmeans"].labels_
    print("Silhouette Score: ", silhouette_score(preprocessed_data, predicted_labels))

    with open("kmeans_model.pickle", "wb") as f:
        pickle.dump(pipe["clusterer"]["kmeans"], f)