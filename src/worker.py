from jobs import q, update_job_status
import time

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    time.sleep(15)
    update_job_status(jid, 'complete')

execute_job()
