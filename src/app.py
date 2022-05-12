#!/usr/bin/env python3
from flask import Flask, request, send_file
import json
import logging
import csv
from jobs import rd, q, add_job, get_job_by_id, jdb
logging.basicConfig()
app = Flask(__name__)
eq_data = {'all_month':[]}

@app.route('/help', methods=['GET'])
def help() -> str:
    '''
    Information on how to interact with the application
    Returns: A string describing what paths to use for each function.
    '''
    return '''\nFIRST LOAD DATA USING THE FOLLOWING PATH: /data -X POST\n
    IF THERE ARE ERROR LOAD THE DATA ONCE MORE\n\n
    Navigation:\n
    Use the following routes to access the data:
      1.  /feature/<feat_string>
          #posts data for a specific column in the csv
      2.  /earthquake/<id_num>
          #posts data from all columns for one earthquake
      3.  /magnitude/<mag>
          #all the earthquakes for a given magnitude
      4.  /delete/<id_num>
          #deletes an entry on the list based on id, or use 'all' to delete all jobs
      5.  /update/<id_num>/<feature_string>/<new_value>
          #changes the value of a feature for an earthquake
      6.  /jobs
          #uses a JSON to create a job
      7.  /jobs/delete/<job_uuid>
          #deletes one of the jobs that has been created
      8.  /jobs/<job_uuid>
          #API route for checking on the status of a submitted job
      9.  /download_map/<jobuuid>
          #plots map of earthquake magnitudes and downloads as png
          [pipe image i.e. "/download/<jobuuid> > map.png" to use
      10. /download_plot/<jobuuid>
          #plots scatter plot of # sensors vs error and downloads as png
          [pipe image i.e. "/download_plot/<jobuuid> > plot.png" to use\n\n'''

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
    '''
    string_list = []
    for item in rd.keys():
        string_list.append('[ID ' + rd.hget(item, 'id') + ']: ' + rd.hget(item, feat_string))
    return(f'All Earthquake {feat_string}s\n' + json.dumps(string_list, indent = 1)+ '\n')

@app.route('/earthquake/<id_num>', methods=['GET'])
def specific_earthquake(id_num: str):
    '''
    prints all info abt a specific earthquake given its id
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

@app.route('/delete/<id_num>', methods =['DELETE'])
def delete_id(id_num: str):
    '''
    deletes an earthquake from data given its id
    ''' 
    feature_list = []
    for item in rd.keys():
        if rd.hget(item, 'id') == id_num:
            rd.delete(item)
            return (f'Earthquake {id_num} DELETED.\n')

@app.route('/update/<id_num>/<feature_string>/<new_value>', methods =['PUT'])
def update_feature(id_num: str, feature_string:str, new_value:str):
    '''
    updates a specific earthquake's feature given the id and the desired feature
    '''
    feature_list = []
    for item in rd.keys():
        if rd.hget(item, 'id') == id_num:
            rd.hset(item, feature_string, new_value)
            return (f'Earthquake {id_num}-> {feature_string} UPDATED to {new_value}.\n')

@app.route('/jobs', methods=['POST', 'GET'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created. Also returns the jobs requested with GET.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['mag']), indent=2) + '\n'

    elif request.method == 'GET':
        redis_list = []
        logging.critical(jdb)
        for key in jdb.keys():
            if not key.startswith(b'job.'):
                continue
            job_uuid = key.strip(b'job.').decode('utf-8')
            job_dict = byte_to_str(job_uuid)
            redis_list.append(job_dict)
        return json.dumps(redis_list, indent=1) + '\n' + """
  To submit a job, do the following:
        curl <ip_address>:<flask_port>/jobs -X POST -d '{"mag":<mag_num>}' -H "Content-Type: application/json"
"""

@app.route('/jobs/delete/<job_uuid>', methods=['DELETE'])
def delete_job(job_uuid:str):
    """
    API route to delete a specific job, or all.
    """
    if request.method == 'DELETE':
        if job_uuid == 'all':
            for key in jdb.keys():
                jdb.delete(key)
            return f'All jobs deleted.\n'
        else:
            str_id = 'job.' + job_uuid
            logging.critical("changing input:" + str_id)
            for key in jdb.keys():
                logging.critical("jdb key: " + key.decode('utf-8'))
                if key.decode('utf-8') == str_id:
                    jdb.delete(key)
                    return f'{job_uuid} has been deleted.\n'
        
    else:
        return """
    This is a route for DELETE-ing former jobs. Use the form:
    curl -X DELETE <ip_address>:<flask_port>/jobs/delete/<job>
    Or to delete all jobs, use the form:
    curl -X DELETE <ip_address>:<flask_port>/jobs/delete/all
    """ 

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid: str):
    """
    API route for checking on the status of a submitted job.
    """
    job_dict = byte_to_str(job_uuid)
    return json.dumps(job_dict, indent=0) + '\n'

def byte_to_str(job_uuid:str):
    """
    Converts specific job's dict of bytes to dict of strings given the job id.
    """
    job_dict = {}
    job_bytes = get_job_by_id(job_uuid)
    for key in job_bytes:
        str_key = key.decode('utf-8')
        str_val = job_bytes[key].decode('utf-8')
        job_dict[str_key] = str_val
    return job_dict

@app.route('/download_map/<job_uuid>', methods=['GET'])
def download(job_uuid):
    '''
    downloads the map to the user's local machine. 
    '''
    path = f'/app/{job_uuid}.png'
    with open(path, 'wb') as f:
        f.write(jdb.hget(job_uuid, 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

@app.route('/download_plot/<job_uuid>', methods=['GET'])
def downloadplot(job_uuid):
    '''
    downloads the plot to the user's local machine.
    '''
    path = f'/app/{job_uuid}2.png'
    with open(path, 'wb') as f:
        f.write(jdb.hget(job_uuid, 'image_plot'))
    return send_file(path, mimetype='image_plot/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
