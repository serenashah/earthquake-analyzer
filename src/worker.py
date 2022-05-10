from jobs import q, rd, jdb, update_job_status
import time

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    print('hello')
    mag_list = []
    for key in rd.keys():
        if key('mag') >= jdb.hget(key, 'min_mag'):
            if key('mag') <= jdb.hget(key, 'max_mag'):
                mag_list.append(key('mag'))
    update_job_status(jid, 'complete')
    rd.hset(job, 'magnitudes in range', mag_list)
    return
execute_job()
