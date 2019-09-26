from flask import Flask, request, jsonify, abort, render_template, url_for, request, send_from_directory, redirect
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import json
import requests

df = pd.read_json('digimon.json')
def comb(i):
    return str(i['stage']) + '#' + str(i['type']) + '#' + str(i['attribute'])

df['target'] = df.apply(
    comb, axis=1
)
df['digimon'] = df['digimon'].apply(
    lambda i: i.lower()
)
listNama = list(df['digimon'])
covz = CountVectorizer(
    tokenizer= lambda i: i.split('#')
)
dfMod = covz.fit_transform(df['target'])
simScore = cosine_similarity(dfMod)
# print(simScore)
# print(len(simScore))

# print(df.head())
# print(df.columns)
#['no', 'digimon', 'image', 'stage', 'type', 'attribute', 'memory',
#       'equip', 'HP', 'SP', 'atk', 'def', 'int', 'spd', 'target']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homedigi.html')

@app.route('/FindRecom', methods=['GET', 'POST'])
def FindRec():
    body = request.form
    digi_name = body['namadigi']
    digi_name = digi_name.lower()
    if digi_name not in listNama:
        return redirect('/notfound')
    index_digi = df[df['digimon'] == digi_name].index.values[0]
    userFave = df.iloc[index_digi][['digimon', 'stage', 'type', 'attribute', 'image']]
    skorDigi = list(enumerate(simScore[index_digi]))
    sortDigi = sorted(
        skorDigi, key = lambda item: item[1], reverse= True)
    recForUser = []
    for item in sortDigi[0:7]:
        data_temp = {}
        if df.iloc[item[0]]['digimon'] != digi_name:
            name = df.iloc[item[0]]['digimon'].capitalize()
            stage = df.iloc[item[0]]['stage']
            image = df.iloc[item[0]]['image']
            dtype = df.iloc[item[0]]['type']
            attr = df.iloc[item[0]]['attribute']
            data_temp['name'] = name
            data_temp['stage'] = stage
            data_temp['image'] = image
            data_temp['type'] = dtype
            data_temp['attribute'] =attr
            recForUser.append(data_temp)
    return render_template('results.html', recForUser = recForUser, userFave= userFave)

@app.route('/notfound')
def notfound():
    return render_template('error.html')


if __name__=='__main__':
    app.run(debug=True)

