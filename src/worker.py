from jobs import q, rd, jdb, update_job_status
import time

@q.worker
def execute_job(jid):
    print('hello')
    update_job_status(jid, 'in progress')
    mag_list = []
    for item in rd.keys():
        if float(rd.hget(item, 'mag')) >= float(jdb.hget(item, 'min_mag')):
            if float(rd.hget(item, 'mag')) <= float(jdb.hget(item, 'max_mag')):
                mag_list.append(rd.hget(item, 'mag'))
    update_job_status(jid, 'complete')
    rd.hset(job, 'magnitudes in range', mag_list)
    return
execute_job()
