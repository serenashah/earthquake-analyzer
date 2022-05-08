#!/usr/bin/env python3
from flask import Flask, request
import json
import csv
from jobs import rd, q, add_job, get_job_by_id
app = Flask(__name__)
eq_data = {'all_month':[]}

@app.route('/data', methods=['POST', 'GET'])
def download_data():
    '''
    loads the data to dictionary of list of dict (easier to work w flask than list)
    returns json-formatted
    '''
    global eq_data
    
    if request.method == 'POST':
        rd.flushdb()

        with open('all_month.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                eq_data['all_month'].append(dict(row))
            
        for item in eq_data['all_month']:
            rd.hset(item['id'], mapping = item)

        return 'Data has been loaded.\n'

    elif request.method == 'GET':
        
        eq_list = []
        
        for item in rd.keys():
            eq_list.append(rd.hgetall(item))
        
        return (json.dumps(eq_list, indent = 2) + '\n')

    else:
        return "Only supports POST and GET methods.\n"

@app.route('/feature/<feat_string>', methods=['GET'])
def specific_feature(feat_string: str):
    '''
    prints a given feature for all earthquakes
    we probably should make these return lists/strings/dicts in the future
    '''
    string_list = []
    for item in rd.keys():
        string_list.append('[ID ' + rd.hget(item, 'id') + ']: ' + rd.hget(item, feat_string))
    return(f'All Earthquake {feat_string}s\n' + json.dumps(string_list, indent = 1)+ '\n')

@app.route('/earthquake/<id_num>', methods=['GET'])
def specific_earthquake(id_num: str):
    '''
    prints all info abt a specific earthquake given # index
    really we should do one by ID maybe?
    '''
    for item in rd.keys():
        if rd.hget(item, 'id') == id_num:
            return(f'Earthquake {id_num}\n' + json.dumps(rd.hgetall(item), indent = 1) + '\n')

@app.route('/magnitude/<mag>', methods=['GET'])
def big_earthquake(mag: int):
    '''
    prints earthquakes above some given magnitude
    '''
    magnitude_list = []
    for item in rd.keys():
        if float(rd.hget(item, 'mag')) >= int(mag):
            magnitude_list.append('[ID ' + rd.hget(item, 'id') + ']: ' + rd.hget(item, 'mag'))
    return(f'Magnitudes above {mag}\n' + json.dumps(magnitude_list, indent = 1) + '\n')

@app.route('/delete/<id_num>/<feature_string>', methods =['DELETE'])
def delete_feature(id_num: str, feature_string:str):
    feature_list = []
    for item in rd.keys():
        if rd.hget(item, 'id') == id_num:
            rd.delete(item, feature_string)
    return (f'Earthquake {id_num}-> {feature_string} DELETED.\n')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
