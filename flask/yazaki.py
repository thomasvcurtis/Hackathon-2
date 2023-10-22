from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np
from sklearn import preprocessing
import json
import constants

app = Flask(__name__)

FILE_NAME = "../HackDearborn_Yazaki_MfgInfo_SECRET.xlsx"

@app.route('/')
def display_map():
    sheet = ingest_data()
    sheet = preprocess_data(sheet)
    return render_template('map.html', css=url_for('static', filename='styles.css'), geojson=url_for('static', filename='data.geojson'))

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
    data_sheet['Availability'] = d
    country_name_and_region = data_sheet['ManufacturingRegion'].values + " " + data_sheet['CountryName'].values
    print(country_name_and_region)
    country_name_dict = dict()
    for n in country_name_and_region:
        if n not in country_name_dict:
            country_name_dict.update({n: 0})
        country_name_dict[n] += 1
    print(country_name_dict)
    test = data_sheet['StateProvince'].str.lower().values.tolist()
    print(convert_abbreviations(test))
    data_sheet['StateProvince'] = test
    data_sheet.to_excel("output.xlsx")
    convert_to_geojson()

    return data_sheet

def convert_abbreviations(array):
    # Abbreviations for MapBox API
    ABBREVIATIONS = {'chihuahua' : 'MX-CHH', 'chi' : 'MX-CHH', 'durango' : 'MX-DUR', 'dgo' : 'MX-DUR', 'nuevo leon' : 'MX-NLE', 
                     'chiapas' : 'MX-CHP', 'chs' : 'MX-CHP', 'sonora' : 'MX-SON', 'son' : 'MX-SON', 'san luis potosi' : 'MX-SLP', 
                     'jalisco' : 'MX-JAL', 'coahuila' : 'MX-COA', 'coa' : 'MX-COA', 'colima' : 'MX-COL', 'col' : 'MX-COL', 
                     'gto' : 'MX-GUA', 'leon' : 'NI', 'mi' : 'US-MI', 'tn' : 'US-TN', 'santa ana' : 'US-CA', 'san marcos' : 'GT',
                     'mx' : 'MX'}
    for i in range(len(array)):
        if type(array[i]) != str:
            array[i] = 'leon'
        array[i] = array[i].lower()
        if array[i] in ABBREVIATIONS:
            array[i] = ABBREVIATIONS[array[i]]
    return array

def convert_to_geojson():
    geojson = {  "type": "FeatureCollection",
            "features": []
    }
    with pd.ExcelFile("output.xlsx") as xls:
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            df = df.drop('Unnamed: 0', axis=1)
            for index, row in df.iterrows():
                # Create a dictionary for each rows
                row_dict = {
                    "type" : "Feature",
                    "properties" : {

                    },
                    "geometry" : {

                    }
                }
                row_dict["properties"] = row.to_dict()
                temp = {
                    "type" : "Point",
                    "coordinates" : constants.COORD_DICT[row_dict["properties"]["StateProvince"]]
                }
                row_dict["geometry"] = temp
                geojson["features"].append(row_dict)

    json_data = json.dumps(geojson, indent=4)

    output_filename = 'static/data.geojson'
    with open(output_filename, 'w') as output_file:
        output_file.write('{}'.format(json_data))
    
    