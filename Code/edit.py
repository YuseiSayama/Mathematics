###インポート###
from PIL import Image
import os
import re
import shutil

###Splited内のファイルの更新###
###Splitedファイルへのパスを取得###
path = '../Edit/Splited/'
files = os.listdir(path)
files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]

###image*.jpgの数字部分を取り出す###
###image*.jpgファイルを取り出す###
pattern = 'image\d*.jpg'
splited_image = []
for i in range(len(files_list)):
    if re.match(pattern, files_list[i]):
        splited_image.append(files_list[i])

###数字部分を取り出す###
splited_image = [word.lstrip('image') for word in splited_image]
splited_image = [word.rstrip('.jpg') for word in splited_image]
splited_image = [int(word) for word in splited_image]

###/d*.jpgファイルの変更###
pattern = '\d*.jpg'
renew_image = []
for i in range(len(files_list)):
    if re.match(pattern, files_list[i]):
        renew_image.append(files_list[i])

###ファイルの更新###
for l in renew_image:
    shutil.copy('../Edit/Splited/'+l, '../Image/image'+l)
    os.remove('../Edit/Splited/'+l)


###Editファイルへのパスを取得###
path = '../Edit/'
files = os.listdir(path)
files_list = [f for f in files if os.path.isfile(os.path.join(path, f))]

###.DS_Storeを除く###
try:
    files_list.remove('.DS_Store')
except ValueError:
    pass

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
        while True:
            if not num in splited_image:
                image_crop.save('../Edit/Splited/image'+str(num)+'.jpg', quality=100)
                num += 1
                break
            num += 1
    return num

###それぞれのEditファイルに対して分割をする###
file_num = 0
for file in files_list:
    image = Image.open('../Edit/'+file)
    file_num = trimming(image,file_num)
    os.remove('../Edit/'+file)
