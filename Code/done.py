###インポート###
import datetime
import numpy as np
import math

###renewファイルの読み込み###
with open('../Renew/renew_date.txt') as f:
    renew_date = [s.strip() for s in f.readlines()]
with open('../Renew/renew_times.txt') as f:
    renew_times = [s.strip() for s in f.readlines()]

###recentファイルの読み込み###
with open('../Question/recent_exam_posi.txt') as f:
    recent_exam_posi_list = [s.strip() for s in f.readlines()]
with open('../Question/recent_exam_date.txt') as f:
    recent_exam_date_list = [s.strip() for s in f.readlines()]
    recent_exam_date = datetime.datetime.strptime(recent_exam_date_list[0],'%Y-%m-%d')
with open('../Question/recent_done_posi.txt') as f:
    recent_done_posi_list = [s.strip() for s in f.readlines()]
with open('../Question/recent_done_date.txt') as f:
    recent_done_date_list = [s.strip() for s in f.readlines()]
    recent_done_date = datetime.datetime.strptime(recent_done_date_list[0],'%Y-%m-%d')

###更新データの作成###
renew_date = [datetime.datetime.strptime(l,'%Y-%m-%d') for l in renew_date]
if recent_exam_date == recent_done_date:
    renew_posi = list(set(recent_exam_posi_list) - set(recent_done_posi_list))
    renew_trigger_date = recent_exam_date + datetime.timedelta(days=1)
    renew_trigger = [str(renew_trigger_date.date())]
    for k in range(len(renew_times)):
        if str(k) in renew_posi:
            renew_times[k] = int(renew_times[k])
            n = np.random.normal(loc=2,scale=0.2)
            day_num = math.floor(renew_times[int(k)]**n+1)
            if day_num >= 90:
                limit = np.random.normal(loc=90,scale=1.5)
                new_date = recent_exam_date + datetime.timedelta(days=limit)
            else:
                new_date = recent_exam_date + datetime.timedelta(days=day_num)
            renew_times[k] += 1
            renew_times[k] = str(renew_times[k])
            renew_date[k] = new_date
else:
    renew_posi = recent_exam_posi_list
    renew_trigger_date = recent_exam_date + datetime.timedelta(days=1)
    renew_trigger = [str(renew_trigger_date.date())]
    for k in range(len(renew_times)):
        if str(k) in renew_posi:
            renew_times[k] = int(renew_times[k])
            n = np.random.normal(loc=2,scale=0.2)
            day_num = math.floor(renew_times[k]**n+1)
            if day_num >= 90:
                limit = np.random.normal(loc=90,scale=1.5)
                new_date = recent_exam_date + datetime.timedelta(days=limit)
            else:
                new_date = recent_exam_date + datetime.timedelta(days=day_num)
            renew_times[k] += 1
            renew_times[k] = str(renew_times[k])
            renew_date[k] = new_date
renew_date = [str(l.date()) for l in renew_date]
with open('../Renew/renew_trigger.txt', mode='w') as f:
    f.write('\n'.join(renew_trigger))
with open('../Renew/renew_times.txt', mode='w') as f:
    f.write('\n'.join(renew_times))
    f.write('\n')
with open('../Renew/renew_date.txt', mode='w') as f:
    f.write('\n'.join(renew_date))
    f.write('\n')

###recentファイルの更新###
with open('../Question/recent_done_posi.txt', mode='w') as f:
    f.write('\n'.join(recent_exam_posi_list))
with open('../Question/recent_done_date.txt', mode='w') as f:
    f.write('\n'.join(recent_exam_date_list))
