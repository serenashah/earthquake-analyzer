from jobs import q, rd, jdb, update_job_status, get_job_by_id
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import logging 
logging.basicConfig()

def pts(key: str, val: float):
    '''
    loads all_month.csv and extracts coordinates
    returns dictionary
    '''
    xy = {}
    longitude = []
    latitude = []
    for item in rd.keys():
        if rd.hget(item, 'type') == 'earthquake':
            if float(rd.hget(item, key)) >= float(val):
                longitude.append(rd.hget(item, 'longitude'))
                latitude.append(rd.hget(item, 'latitude'))
    xy['longitude'] = longitude
    xy['latitude'] = latitude
    logging.critical(json.dumps(xy, indent = 1))
    return xy

@q.worker
def execute_job(jid):
    logging.critical('Inside worker.')
    update_job_status(jid, 'in progress')
    
    job = get_job_by_id(jid)
    logging.critical(job)
    mag = job[b'mag']
    logging.critical(f'mag: {mag}')

    df = pd.DataFrame(pts('mag',float(mag)))
    df_geo = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude,df.latitude))
    world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    axis = world_data.plot(color = 'sienna', edgecolor = 'black')
    df_geo.plot(ax = axis, color = 'red', markersize=8, alpha=0.5, edgecolor='thistle', linewidth=0.4)

    axis.set_facecolor('powderblue')
    plt.xticks(np.arange(-180, 190, step=10), rotation = 45)
    plt.yticks(np.arange(-90, 100, step=10))
    plt.title(f'Earthquakes With Magnitude >= {mag}')
    plt.savefig(f'EqwksWthMagGrtrThan{mag}.png',dpi=600)

    with open(f'EqwksWthMagGrtrThan{mag}.png', 'rb') as f:
        img = f.read()
        
    jdb.hset(jid, 'image', img)
    update_job_status(jid, 'complete')
    
    return 
execute_job()
