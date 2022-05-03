#!/usr/bin/env python3
from flask import Flask, request
import json
import csv
app = Flask(__name__)
eq_data = {'all_month':[]}

@app.route('/download_data', methods=['POST'])
def download_data():
    '''
    loads the data to dictionary of list of dict (easier to work w flask than list)
    returns json-formatted
    '''
    global eq_data
    with open('all_month.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            eq_data['all_month'].append(dict(row))
    return 'Data has been loaded.\n'

@app.route('/feature/<feat_string>', methods=['GET'])
def specific_feature(feat_string: str):
    '''
    prints a given feature for all earthquakes
    we probably should make these return lists/strings/dicts in the future
    '''
    string_list = []
    for x in eq_data['all_month']:
        string_list.append('[ID ' + x['id'] + f']: ' + x[feat_string])
    return(f'All Earthquake {feat_string}s\n' + json.dumps(string_list, indent = 1)+ '\n')

@app.route('/earthquake/<id_num>', methods=['GET'])
def specific_earthquake(id_num: str):
    '''
    prints all info abt a specific earthquake given # index
    really we should do one by ID maybe?
    '''
    for x in eq_data['all_month']:
        if x['id'] == id_num:
            return(f'Earthquake {id_num}\n' + json.dumps(x, indent = 1) + '\n')

@app.route('/magnitude/<mag>', methods=['GET'])
def big_earthquake(mag: int):
    '''
    prints earthquakes above some given magnitude
    '''
    magnitude_list = []
    for x in eq_data['all_month']:
        if float(x['mag']) >= int(mag):
            magnitude_list.append('[ID ' + x['id'] + ']: ' + x['mag'])
    return(f'Magnitudes above {mag}\n' + json.dumps(magnitude_list, indent = 1) + '\n')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
