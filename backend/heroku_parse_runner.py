import schedule
import time
import os
import config


def job():
    os.system("bash parse.sh")


schedule.every(config.UPDATE_EVERY).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
