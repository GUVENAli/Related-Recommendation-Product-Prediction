import matplotlib.pyplot as plt
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default="../data/sc_scores.txt", help="file path to silhouette coff.")

    opt = parser.parse_args()

    sc_score = []
    k_param = []
    with open(opt.data) as scores:
        for line in scores:
            score = line.rstrip("\n")
            score = score.split(" ")
            k_param.append(float(score[0]))
            sc_score.append(float(score[1]))

    plt.plot(k_param, sc_score)
    plt.title("Silhouette Scores")
    plt.ylabel("Silhouette Coefficient")
    plt.xlabel("Number of Clusters")
    plt.show()
