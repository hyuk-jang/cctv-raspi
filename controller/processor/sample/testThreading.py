import threading

 
def sum(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print("Subthread", total)
 
t = threading.Thread(target=sum, args=(1, 100000))
t.start()
 
print("Main Thread")

def test():

    return 'aa'



from apscheduler.schedulers.blocking import BlockingScheduler
# Invter val Test 용
sched = BlockingScheduler()
sched.add_job(test, 'interval', seconds=1)
sched.start()



