


from apscheduler.schedulers.blocking import BlockingScheduler

def job_function():
    print("Hello World")

sched = BlockingScheduler()

# 1분마다 실행 스케줄러
sched.add_job(job_function, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute='*', second='0')

sched.start()