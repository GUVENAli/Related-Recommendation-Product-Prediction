# Related Products Recommendation API

It was created for recommendation of products according to the products in a cart of a person.

## Environment
* Windows 10, 64-bit, Intel Core i7-8750H CPU @2.20GHz, 16 GB RAM
* PyCharm Community 2020.3
* Python 3.7

## Necessary Libraries

Using "requirements.txt" file and script below, you can get the libraries for your environment.

```python
pip install -r requirements.txt
```

## Data Preparation

You will need the data, "events.json" and "meta.json" files. After getting the files you can run the script below on terminal.
The files is considered to put in the folder of "data".

```python
python plot_distribution.py --events ../data/events.json
```

For generate csv dataset from events and meta run the below script.
```python
python data_prep.py --events ../data/events.json --meta ../data/meta.json --dataset ../data/dataset.csv
```
Note: It can be take 5 hours or more.
If you do not want to wait, just download the dataset with the code. Dataset is in data folder.

## Model
K-means++ is used. The script is below to run it with dataset.csv and default parameters

```python
python kmeans_model.py
```

## Run the API
First run the code below for the server side.
```python
python related_product_recommendation_api.py
```

Then for requesting related products from the server, run the below script:
```python
python main.py
```

## IMPORTANT NOTE
events.json and meta.json can not be shared because of they are private data. If you want to run this codes, you will need to add the files to data folder.
dataset.csv is anonymized so if you want to download just click [here](https://drive.google.com/drive/folders/1WWmEevA3Yj4UzP5vfKt6G502w0IZybxm?usp=sharing)

In the data folder, there are 10 samples each has one cart and related products. Assuming that the inputs of the server would be like this.
