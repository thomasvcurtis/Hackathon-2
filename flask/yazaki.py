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
    country_name_and_region = data_sheet['ManufacturingRegion'].values + " " + data_sheet['CountryName'].values
    print(country_name_and_region)
    country_name_dict = dict()
    for n in country_name_and_region:
        if n not in country_name_dict:
            country_name_dict.update({n: 0})
        country_name_dict[n] += 1
    print(country_name_dict)
    return data_sheet
    