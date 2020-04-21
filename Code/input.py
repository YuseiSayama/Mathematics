###インポート###
import datetime
import os
import glob
from PIL import Image

###ファイルへのパスを取得###
path = '../'
files = os.listdir(path)
files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]

###.DS_Storeを除く###
try:
    files_list.remove('.DS_Store')
except ValueError:
    pass

###name.txtを読み込み###
with open('../data/name.txt') as f:
    name_list = [s.strip() for s in f.readlines()]

###ファイルナンバーの取得###
file_num = int(name_list[len(name_list)-1])

###今日の日付の設定###
dt_today = datetime.datetime.now()

###画像の分割###
def trimming(image,num):
    width, height = image.size

    img_pixels = [image.getpixel((width//2,j)) for j in range(height)]

    blue_posi = []
    for i in range(height):
        if 0 <= img_pixels[i][0] <= 15:
            if 120 <= img_pixels[i][1] <= 135:
                if 240 <= img_pixels[i][2] <= 255:
                    blue_posi.append((i-44)//60)

    blue_posi = list((set(blue_posi)))

    blue_posi.sort()

    trim_posi = []
    for i in range(len(blue_posi)):
        trim_posi.append(48+60*blue_posi[i])
        trim_posi.append(100+60*blue_posi[i])
    del trim_posi[len(trim_posi)-1]
    del trim_posi[0]

    for i in range(len(trim_posi)//2):
        image_crop = image.crop((0,trim_posi[2*i]+1,width,trim_posi[2*i+1]))
        image_crop.save('../Image/image'+str(num)+'.jpg', quality=100)
        ###date.txtの書き込み###
        with open('../data/date.txt', mode='a') as f:
            f.write(str(dt_today.date())+'\n')
        ###time.txtの書き込み###
        with open('../data/time.txt', mode='a') as f:
            f.write('0'+'\n')
        ###renew_times.txtの書き込み###
        with open('../Renew/renew_times.txt', mode='a') as f:
            f.write('0'+'\n')
        ###renew_date.txtの書き込み###
        with open('../Renew/renew_date.txt', mode='a') as f:
            f.write(str(dt_today.date())+'\n')
        num += 1
        ###nume.txtの書き込み###
        with open('../data/name.txt', mode='a') as f:
            f.write(str(num)+'\n')

    return num

for file in files_list:
    image = Image.open('../'+file)
    file_num = trimming(image,file_num)
    os.remove('../'+file)
