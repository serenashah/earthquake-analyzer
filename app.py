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
    return json.dumps(eq_data, indent = 1)

@app.route('/<id_string>', methods=['GET'])
def specific_feature(id_string: str):
    '''
    prints a given feature for all earthquakes
    we probably should make these return lists/strings/dicts in the future
    '''
    print(f'All Earthquake {str}s')
    for x in eq_data['all_month']:
        print('[ID ' + x['id'] + f']: ' + x[id_string])

@app.route('/earthquake/<num>', methods=['GET'])
def specific_earthquake(num: int):
    '''
    prints all info abt a specific earthquake given # index
    really we should do one by ID maybe?
    '''
    print(json.dumps(eq_data['all_month'][num], indent = 1))

@app.route('/magnitude/<mag>', methods=['GET'])
def big_earthquake(mag: int):
    '''
    prints earthquakes above some given magnitude
    '''
    print(f'Magnitudes above {mag}\n')
    for x in eq_data['all_month']:
        if float(x['mag']) >= mag:
            print('[ID ' + x['id'] + ']: ' + x['mag'])
        
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
