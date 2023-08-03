

import os
import random
import shutil

orgdatapath = './all-anno/JPEG/'
imgsavefolder = './all-anno/test/JPEG/'
jsonsavefolder = './all-anno/test/JSON/'


if not os.path.exists(jsonsavefolder):
	os.makedirs(jsonsavefolder)

if not os.path.exists(imgsavefolder):
	os.makedirs(imgsavefolder)

imglist = os.listdir(orgdatapath)
ImgNum = len(imglist)

random.shuffle(imglist)
testnum = int(ImgNum * 0.25)

print(f'test num is {testnum}.')

N = 1

for img in imglist:

	imgfile = orgdatapath + img
	name, format_ = os.path.splitext(img)

	jsonfile = './all-anno/JSON/' + name + '.json'

	imgsave = imgsavefolder + img
	jsonsave = jsonsavefolder + name + '.json'

	#### Test data
	if N <= testnum:
		shutil.move(imgfile, imgsave)
		shutil.move(jsonfile, jsonsave)
		N += 1

	# #TEST DATA
	# else:
	# 	shutil.copyfile(imgfile, img_save_test)
	# 	shutil.copyfile(jsonfile, json_save_test)
	# 	N += 1





