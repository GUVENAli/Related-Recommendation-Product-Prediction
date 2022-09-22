import matplotlib.pyplot as plt
import pandas as pd
import json
import tqdm
from argparse import ArgumentParser

def read_events(file_Path):
    with open(file_Path) as jFile:
        jeString = jFile.read()
    return jeString

def load_data(json_String) :
    jeData = json.loads(json_String)
    data = pd.DataFrame.from_dict(jeData["events"])
    return data

def count_Elements_In_Charts(data, data_column_name, step_size=100):
    sess_ids = data[data_column_name]
    sess_ids_uniques = sess_ids.unique()
    count_uniques = []

    for i in tqdm.tqdm(range(0, len(sess_ids_uniques), 100)):
        count_uniques.append(len(data[data[data_column_name] == data[data_column_name].unique()[i]]))
    return count_uniques

def plot_distribution(count_uniques, num_bins=50):
    plt.hist(count_uniques, bins=num_bins)
    plt.title("Element Distribution in Charts")
    plt.xlabel("Element Numbers")
    plt.ylabel("Amount")
    plt.show()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--events", type=str, default="../data/events.json", help="paht to event.json")
    opt = parser.parse_args()

    jeString = read_events(opt.events)
    data = load_data(jeString)
    count_uniques = count_Elements_In_Charts(data, "sessionid")
    plot_distribution(count_uniques)


