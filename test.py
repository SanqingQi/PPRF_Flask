import datetime

now_time = str(datetime.datetime.now())
now_time=now_time.split(' ')[0].split('-')
print(int(now_time[1]))