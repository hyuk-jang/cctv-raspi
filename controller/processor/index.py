# -*- coding: utf-8 -*- 

from sample import main


'''
    Main Start
'''
mainProcessor = main.MainProcessor()

# mainProcessor.runScheduler()
mainProcessor.main()


'''
    Main Test Code
'''
## TEST Interval
## main Test 용
# mainProcessor.main()

## Invter val Test 용
# sched = BlockingScheduler()
# sched.add_job(mainProcessor.main, 'interval', seconds=2)
# sched.start()
