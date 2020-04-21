###インポート###
import datetime
from PIL import Image
import numpy as np
import copy
import math
import os
import random
import PyPDF2
import shutil

###今日の日付を設定###
dt_today = datetime.datetime.now()

###dataファイルの読み込み###
with open('../data/date.txt') as f:
    date_list = [s.strip() for s in f.readlines()]
with open('../data/time.txt') as f:
    time_list = [s.strip() for s in f.readlines()]

###更新###
if os.path.exists('../Renew/renew_trigger.txt'):
    with open('../Renew/renew_trigger.txt') as f:
        Renew_Trigger = [s.strip() for s in f.readlines()]
    with open('../Renew/renew_times.txt') as f:
        Renew_Times = [s.strip() for s in f.readlines()]
    with open('../Renew/renew_date.txt') as f:
        Renew_Date = [s.strip() for s in f.readlines()]
    trigger_date = datetime.datetime.strptime(Renew_Trigger[0], '%Y-%m-%d') - dt_today
    if trigger_date.total_seconds() <= 0:
        for i in range(len(Renew_Date)):
            date_list[i] = Renew_Date[i]
            time_list[i] = Renew_Times[i]

###date,timeファイルの書き込み###
with open('../data/time.txt', mode='w') as f:
    f.write('\n'.join(time_list))
    f.write('\n')
with open('../data/date.txt', mode='w') as f:
    f.write('\n'.join(date_list))
    f.write('\n')

###date_listをdatetime型にする###
date_list = [datetime.datetime.strptime(l,'%Y-%m-%d') for l in date_list]

###問題番号を設定###
exam_num_list = []
for i in range(len(date_list)):
    dt_diff = dt_today - date_list[i]
    if dt_diff.total_seconds() > 0:
        exam_num_list.append(str(i))

###問題番号と日付を記録しておく###
with open('../Question/recent_exam_posi.txt', mode='w') as f:
    f.write('\n'.join(exam_num_list))
with open('../Question/recent_exam_date.txt', mode='w') as f:
    f.write(str(dt_today.date())+'\n')

###問題番号をランダムソート###
random.shuffle(exam_num_list)

###問題番号の画像表示###
def num_gen(str):
    dst = Image.open('../Number/問題下地.jpg')
    dst.putalpha(0)
    dst.paste(num_list[10], (0,0), num_list[10])
    digi = list(str)
    x_posi = num_list[10].width
    for l in digi:
        dst.paste(num_list[int(l)], (x_posi,0), num_list[int(l)])
        x_posi += num_list[int(l)].width
    return dst

###画像の生成###
def join(im_list,st_num_list, resample=Image.BICUBIC):
    dst = Image.new('RGB', (2183,3086))
    dst.paste(foundation, (0,0))
    pos_y = 44
    for i in range(len(im_list)):
        dst.paste(num_gen(st_num_list[i]), (0,pos_y))
        pos_y += 116
        dst.paste(im_list[i], (0, pos_y))
        pos_y += im_list[i].height-4
    return dst

###元になる画像を開く###
exam_list = []
for l in exam_num_list:
    exam_list.append(Image.open('../Image/image'+l+'.jpg'))

###数字の画像を開く###
num_list = []
for i in range(10):
    num_list.append(Image.open('../Number/'+str(i)+'.png'))
num_list.append(Image.open('../Number/No.png'))
num_list = [im.resize((int(im.width * 110 / im.height), 110))for im in num_list]

###下地を開く###
foundation = Image.open('../Number/下地.jpg')

###ページ長との調整###
comp_height = 0
exam_in_page = [0]
for i in range(len(exam_list)):
    comp_height += exam_list[i].height+110
    if comp_height >= 3000:
        exam_in_page.append(i)
        comp_height = exam_list[i].height+110
exam_in_page.append(len(exam_list)+1)

###画像(PDF)生成###
merger = PyPDF2.PdfFileMerger()
page_num = 0
for i in range(len(exam_in_page)-1):
    join(exam_list[exam_in_page[i]:exam_in_page[i+1]],exam_num_list[exam_in_page[i]:exam_in_page[i+1]]).save('../Storage/exam'+str(page_num), "PDF", resolution = 100.0)
    merger.append('../Storage/exam'+str(page_num))
    os.remove('../Storage/exam'+str(page_num))
    page_num += 1

###pdf作成###
desktop_path = os.path.expanduser('~') + '/desktop/'
merger.write(desktop_path + 'exam.pdf')
merger.close()

###バックナンバーを保存###
shutil.copy(desktop_path + 'exam.pdf', '../BackNumber/exam'+str(dt_today.date())+'.pdf')
