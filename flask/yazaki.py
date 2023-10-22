from flask import Flask
import pandas as pd
import numpy as np
from sklearn import preprocessing

app = Flask(__name__)

FILE_NAME = "../HackDearborn_Yazaki_MfgInfo_SECRET.xlsx"

@app.route('/')
def display_map():
    sheet = ingest_data()
    sheet = preprocess_data(sheet)
    return sheet.to_html()

def ingest_data():
    data_sheet = pd.read_excel(FILE_NAME)
    return data_sheet

def preprocess_data(data_sheet):
    cols = ['Usage', 'Capacity']
    data_sheet['Usage'] = data_sheet['Usage'].interpolate()
    data_sheet['Capacity'] = data_sheet['Capacity'].interpolate()
    availability = data_sheet['Usage'] - data_sheet['Capacity']
    data_sheet = data_sheet.drop(cols, axis=1)
    data_sheet['Availability'] = availability
    scaler = preprocessing.MinMaxScaler()
    array = np.array(data_sheet['Availability'])
    d = scaler.fit_transform(array.reshape(-1,1))
    print("normalized array: ", d)
    return data_sheet
    