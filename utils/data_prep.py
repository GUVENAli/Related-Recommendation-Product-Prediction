import pandas as pd
import json
import tqdm
import numpy as np
from argparse import ArgumentParser

def time_zone(order_time_zone):
    time_zone_morning = 0
    time_zone_afternoon = 0
    time_zone_evening = 0
    time_zone_night = 0
    if order_time_zone >= 6 and order_time_zone <= 12:
        time_zone_morning = 1
    elif order_time_zone > 12 and order_time_zone <= 18:
        time_zone_afternoon = 1
    elif order_time_zone > 18 and order_time_zone <= 24:
        time_zone_evening = 1
    else:
        time_zone_night = 1
    return time_zone_morning, time_zone_afternoon, time_zone_evening, time_zone_night

def categories_coding(categories, cat_uniques):
    out = np.zeros(len(cat_uniques))
    for i in range(len(categories)):
        for j in range(len(cat_uniques)):
            if categories[i] == cat_uniques[j]:
                out[j] = out[j] + 1
                break
    return out

def subcategories_coding(subcategories, subcat_uniques):
    out = np.zeros(len(subcat_uniques))
    for i in range(len(subcategories)):
        for j in range(len(subcat_uniques)):
            if subcategories[i] == subcat_uniques[j]:
                out[j] = out[j] + 1
                break
    return out

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--events", type=str, default="../data/events.json", help="path to event.json")
    parser.add_argument("--meta", type=str, default="../data/meta.json", help="path to meta.json")
    parser.add_argument("--dataset", type=str, default="../data/dataset.csv", help="path to write the dataset as csv")
    opt = parser.parse_args()

    with open(opt.events) as jFile:
        jeString = jFile.read()

    with open(opt.meta, encoding="utf-8") as jFile:
        jmString = jFile.read()

    jeData = json.loads(jeString)
    data = pd.DataFrame.from_dict(jeData["events"])
    data = data.dropna()
    sess_ids = data["sessionid"]
    sess_ids_uniques = sess_ids.unique()
    count_uniques = []

    jmData = json.loads(jmString)
    data_m = pd.DataFrame.from_dict(jmData["meta"])
    data_m = data_m.dropna()
    cat_uniques = data_m["category"].unique()
    subcat_uniques = data_m["subcategory"].unique()

    columns = ["sessionid", "sum_products", "sum_price", "morning", "afternoon", "evening", "night"]
    columns.extend(cat_uniques)
    columns.extend(subcat_uniques)
    dataset = pd.DataFrame(columns=columns)
    for i in tqdm.tqdm(range(0, len(sess_ids_uniques))):
        features = []
        sum_products = len(data[data["sessionid"] == sess_ids_uniques[i]])
        sum_price = np.sum(data[data["sessionid"] == sess_ids_uniques[i]]["price"].values.astype(np.float))
        dates = data[data["sessionid"] == sess_ids_uniques[i]]["eventtime"].values
        order_time_zone = np.max([int(dates[j][11:13]) for j in range(len(dates))])
        time_zone_morning, time_zone_afternoon, time_zone_evening, time_zone_night = time_zone(order_time_zone)
        product_ids = data[data["sessionid"] == sess_ids_uniques[0]]["productid"].values
        categories = [data_m[data_m["productid"] == product_ids[k]]["category"].values[0]
                      if not data_m[data_m["productid"] == product_ids[k]].empty else "Other" for k in
                      range(len(product_ids))]
        subcategories = [data_m[data_m["productid"] == product_ids[k]]["subcategory"].values[0]
                         if not data_m[data_m["productid"] == product_ids[k]].empty else "Other" for k in
                         range(len(product_ids))]
        cat_features = categories_coding(categories, cat_uniques)
        subcat_feautes = subcategories_coding(subcategories, subcat_uniques)
        features.append(sess_ids_uniques[i])
        features.append(sum_products)
        features.append(sum_price)
        features.extend([time_zone_morning, time_zone_afternoon, time_zone_evening, time_zone_night])
        features.extend(list(cat_features))
        features.extend(list(subcat_feautes))
        dataset.loc[i] = features
    dataset.to_csv(opt.dataset)
