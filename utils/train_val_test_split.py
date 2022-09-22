import numpy as np
import json
import pandas as pd
np.random.seed(42)

def split(sess_ids_uniques, data, event_path):
    with open(event_path) as jFile:
        jeString = jFile.read()
    jeData = json.loads(jeString)
    data_event = pd.DataFrame.from_dict(jeData["events"])
    data_event = data_event.dropna()
    ids = np.arange(len(sess_ids_uniques))
    np.random.shuffle(ids)
    train_inds = ids[0:len(sess_ids_uniques) - 10] # 10 of the data for test
    count = 1
    for i in ids[len(sess_ids_uniques) - 10: len(sess_ids_uniques)]:
        data_event[data_event["sessionid"] == sess_ids_uniques[i]].to_json("../data/test{:d}.json".format(count), orient="records")
        count += 1

    train_data = data.iloc[train_inds, :]

    return train_data
