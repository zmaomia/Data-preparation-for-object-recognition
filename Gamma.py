import numpy as np
import cv2
# import math
# from matplotlib import pyplot as plt
from skimage import exposure
import shutil
import os
import json

def gamma_corrected(savefolder, imgfolder, img, para): #Gamma correction
	#pare > 1 Increase brightness
	#pare < 1 Decrease brightness
	imgsavefolder = savefolder + '/JPEG/'
	jsonsavefolder = savefolder + '/JSON/'

	if not os.path.exists(imgsavefolder):
		os.makedirs(imgsavefolder)

	if not os.path.exists(jsonsavefolder):
		os.makedirs(jsonsavefolder)

	jsonfolder = imgfolder.replace('JPEG', 'JSON')
	jsonfile = jsonfolder + img.replace('png', 'json')

	origimgpath = os.path.join(imgfolder,img)

	im = cv2.imread(os.path.join(imgfolder,img))

	h = im.shape[0]
	w = im.shape[1]

	for p in para:
		gamma_img = exposure.adjust_gamma(im, p)

		gamma_imgsavepath = imgsavefolder + 'g' + str(p) + '_' + img
		orig_imgsavepath = imgsavefolder + img

		gamma_jsonsavepath = jsonsavefolder + 'g' + str(p) + '_' + img.replace('png', 'json')
		orig_jsonsavepath = jsonsavefolder + img.replace('png', 'json')
		
		#save gamma image
		cv2.imwrite(gamma_imgsavepath, gamma_img)
	
		# rewrite jsonfile since imagePath is changed
		# shutil.copy (jsonfile, gamma_jsonsavepath)
		new_data = {}

		with open(jsonfile, 'r') as f:
			data = json.load(f)

		imagePath = data['imagePath']
		new_data['imagePath'] = 'g' + str(p) + '_' + img
		new_data['version'] = data['version']
		new_data['flags'] = data['flags']
		new_data['imageHeight'] = h
		new_data['imageWidth'] = w
		new_data['shapes'] = data['shapes']

		with open(gamma_jsonsavepath,"w") as savef:
				json.dump(new_data,savef)

		f.close()
		savef.close()

##Gamma parameters
para = [0.7, 1.5]

img_org_folder = './orig-3/val/JPEG/'
save_folder = './orig-3/val/Gamma/'

if not os.path.exists(save_folder):
	os.makedirs(save_folder)
	os.makedirs(save_folder + 'JPEG')
	os.makedirs(save_folder + 'JSON')

for img in os.listdir(img_org_folder):
	# print('processing img:', img)
	gamma_corrected(save_folder, img_org_folder, img, para)