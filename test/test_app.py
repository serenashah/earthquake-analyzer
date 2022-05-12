import json
import os
import re
import time
import pytest
import requests

api_host = 'localhost'
api_port = '5028'
api_prefix = f'http://{api_host}:{api_port}'

def test_data_download():
    route = f'{api_prefix}/data'
    response = requests.post(route)
    assert response.ok == True
    assert response.content == b'Data has been loaded.\n'

def test_data_get():
    route = f'{api_prefix}/feature/mag'
    response = requests.get(route)
    
    assert response.ok == True
    
def test_data_read():
    route = f'{api_prefix}/data'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert isinstance(response.json(), list) == True
    assert isinstance(response.json()[0], dict) == True
    assert 'mag' in response.json()[0].keys()
    assert 'magError' in response.json()[0].keys()
    assert 'latitude' in response.json()[0].keys()
    assert 'longitude' in response.json()[0].keys()


def test_jobs_info():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job, do the following', response.text)) == True

def test_jobs_cycle():
    route = f'{api_prefix}/jobs'
    job_data = {'mag':5.0}
    response = requests.post(route, json=job_data)

    assert response.ok == True
    assert response.status_code == 200

    UUID = response.json()['id']
    assert isinstance(UUID, str) == True
    assert response.json()['status'] == 'submitted'

    time.sleep(15)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert response.json()['status'] == 'complete'

"""
def test_jobs_delete():
    route1 = f'{api_prefix}/jobs'
    job_data = {'mag':6.0}
    response1 = requests.post(route1, json=job_data)
    UUID = response1.json()['id']
    
    time.sleep(15)

    route = f'{api_prefix}/jobs/delete/{UUID}'
    response = requests.delete(route)
    
    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('has been deleted', response.text)) == True
""" 
