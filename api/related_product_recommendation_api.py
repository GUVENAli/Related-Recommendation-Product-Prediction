from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
import collections
import sys

app = Flask(__name__)
api = Api(app)

class Clusterer(Resource):
    def recommendation(self, predictions):
        with open("../data/events.json") as jFile:
            jeString = jFile.read()

        with open("../data/meta.json", encoding="utf-8") as jFile:
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

        dataset = pd.read_csv("../data/dataset.csv")
        sess_ids_uniques = dataset["sessionid"]
        dataset.drop(columns=["Unnamed: 0", "sessionid"], inplace=True)

        scaler = StandardScaler()
        pre_d = scaler.fit_transform(dataset)
        preds = model.predict(pre_d)

        preds_df = pd.DataFrame(preds, columns=["preds"])
        chosen_carts = sess_ids_uniques[preds_df["preds"] == predictions[0]]
        app.logger.warning(predictions)

        product_names = []
        ids = np.arange(len(chosen_carts))
        np.random.shuffle(ids)
        loop = chosen_carts.values[ids[0:np.min([100, len(ids)//10])]]
        for i in range(len(loop)):
            products = data[data["sessionid"] == loop[i]]["productid"]
            for j in range(len(products)):
                temp = data_m[data_m["productid"] == products.values[j]]["name"]
                if temp.empty:
                    pass
                else:
                    product_names.append(temp.values[0])
        dd = collections.Counter(product_names)
        mm = dd.most_common(10)
        mm_df = pd.DataFrame(mm)
        sum_mm = np.sum(mm_df.iloc[:, 1].values)
        mm_df.iloc[:, 1] /= sum_mm
        results = mm_df.to_numpy().tolist()
        return results

    def post(self):
        args = parser.parse_args()
        test = np.array(json.loads(args['data']))
        scaler1 = StandardScaler()
        pre_d = scaler1.fit_transform(test)
        prediction = model.predict(pre_d)
        result = self.recommendation(prediction)
        print(prediction)
        return jsonify(result)

api.add_resource(Clusterer, '/recommendation')

if __name__ == '__main__':
    parser = reqparse.RequestParser()
    parser.add_argument('data')

    with open('../model/kmeans_model.pickle', 'rb') as f:
        model = pickle.load(f)

    app.run(debug=True)


