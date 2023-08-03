# coding:utf-8

import cv2
import os
import numpy as np
import math
import copy
import json

def enhancement_using_mirror(modes, ImagePath,AnnotationsPath,ImageSavePath,AnnotationsSavePath):

	#mirror
	for mode in modes:
		for imgfile in os.listdir(ImagePath):
			print('processing img:', imgfile)
			img = cv2.imread(os.path.join(ImagePath,imgfile))

			h = img.shape[0]
			w = img.shape[1]

			new_data = {}

			Annotations = os.path.join(AnnotationsPath, imgfile[:-4]+'.json')

			new_name = 'm' + mode + '_' + imgfile 
			saveAnnotations = os.path.join(AnnotationsSavePath,new_name[:-4]+'.json')
			
			with open(Annotations, 'r') as f:
				data = json.load(f)

			imagePath = data['imagePath']
			new_data['imagePath'] = 'm'+ mode + '_' + imagePath
			new_data['version'] = data['version']
			new_data['flags'] = data['flags']
			new_data['imageHeight'] = h
			new_data['imageWidth'] = w

			new_shapes = []
			
			# horizontal mirror
			if mode == 'h':
				mirror_img_h  = mirror_h(img)
				cv2.imwrite(os.path.join(ImageSavePath,new_name),mirror_img_h)
				
				for shape in data['shapes']:

					new_info = {}

					new_info['label'] = shape['label']
					new_info['group_id'] = shape['group_id']
					new_info['shape_type'] = shape['shape_type']
					new_info['flags'] = shape['flags']
			
					points = shape['points']
					new_points = []

					for point in points:

						temp_list = []
						p_x = point[0]
						p_y = point[1]
						mh_p_x = abs(w - p_x)

						temp_list.append(mh_p_x)
						temp_list.append(p_y)

						if len(temp_list) > 0:
							new_points.append(temp_list)

					#draw polugon to check data
					# pts = np.array(new_points, np.int32)
					# pts = pts.reshape((-1,1,2))
					# new_mirror_img_h = cv2.polylines(mirror_img_h,[pts],True,(0,255,255))
					# cv2.imwrite(os.path.join(ImageSavePath,new_name),new_mirror_img_h)

					new_info['points'] = new_points
					new_shapes.append(new_info)

			elif mode == 'v':
				# vertical mirror
				mirror_img_v = mirror_v(img)
				cv2.imwrite(os.path.join(ImageSavePath,new_name),mirror_img_v)

				Annotations = os.path.join(AnnotationsPath, imgfile[:-4]+'.json')
				saveAnnotations = os.path.join(AnnotationsSavePath,new_name[:-4]+'.json')

				for shape in data['shapes']:
					new_info = {}
					new_info['label'] = shape['label']
					new_info['group_id'] = shape['group_id']
					new_info['shape_type'] = shape['shape_type']
					new_info['flags'] = shape['flags']
			
					points = shape['points']

					new_points = []

					for point in points:

						temp_list = []
						p_x = point[0]
						p_y = point[1]
						# mh_p_x = abs(w - p_x)
						mh_p_y = abs(h - p_y)

						temp_list.append(p_x)
						temp_list.append(mh_p_y)

						if len(temp_list) > 0:
							new_points.append(temp_list)

					# pts = np.array(new_points, np.int32)
					# pts = pts.reshape((-1,1,2))
					# new_mirror_img_v = cv2.polylines(mirror_img_v,[pts],True,(0,255,255))
					# cv2.imwrite(os.path.join(ImageSavePath,new_name),new_mirror_img_v)

					new_info['points'] = new_points
					new_shapes.append(new_info)

			elif mode == 'd':
				# vertical mirror
				mirror_img_d = mirror_d(img)
				cv2.imwrite(os.path.join(ImageSavePath,new_name),mirror_img_d)

				Annotations = os.path.join(AnnotationsPath, imgfile[:-4]+'.json')
				saveAnnotations = os.path.join(AnnotationsSavePath,new_name[:-4]+'.json')

				imagePath = data['imagePath']
				new_data['imagePath'] = 'md_' + imagePath

				for shape in data['shapes']:
					new_info = {}
					new_info['label'] = shape['label']
					new_info['group_id'] = shape['group_id']
					new_info['shape_type'] = shape['shape_type']
					new_info['flags'] = shape['flags']
			
					points = shape['points']

					new_points = []

					for point in points:

						temp_list = []
						p_x = point[0]
						p_y = point[1]
						mh_p_x = abs(w - p_x)
						mh_p_y = abs(h - p_y)

						temp_list.append(mh_p_x)
						temp_list.append(mh_p_y)

						if len(temp_list) > 0:
							new_points.append(temp_list)

					# pts = np.array(new_points, np.int32)
					# pts = pts.reshape((-1,1,2))
					# new_mirror_img_d = cv2.polylines(mirror_img_d,[pts],True,(0,255,255))
					# cv2.imwrite(os.path.join(ImageSavePath,new_name),new_mirror_img_d)
					# print('new_points:', new_points)

					new_info['points'] = new_points
					new_shapes.append(new_info)

			new_data['shapes'] = new_shapes

			with open(saveAnnotations,"w") as savef:
				json.dump(new_data,savef)

			savef.close()

#水平镜像
def mirror_h(src):
# def mirror_h(src):
	w = src.shape[1]
	h = src.shape[0]

	ll = src.shape[2]
	mirror_img = copy.deepcopy(src)
	
	for wi in range(w):
		mirror_img[:,w-wi-1] = src[:,wi]
	
	return mirror_img

#垂直镜像
def mirror_v(src):
	w = src.shape[1]
	h = src.shape[0]

	ll = src.shape[2]
	mirror_img = copy.deepcopy(src)
	
	for hi in range(h):
		mirror_img[h-hi-1, :] = src[hi, :]
	return mirror_img

#对角线镜像
def mirror_d(src):
	w = src.shape[1]
	h = src.shape[0]

	ll = src.shape[2]
	mirror_img = copy.deepcopy(src)
	
	for hi in range(h):
		for wi in range(w):
			mirror_img[h-hi-1, w-wi-1] = src[hi, wi]
	return mirror_img

def main(modes):

	print('mirroring...') 
	mir_ImagePath = './all-anno/test/Gamma/JPEG/'
	mir_AnnotationsPath = './all-anno/test/Gamma/JSON/'
	mir_savepath = './all-anno/test/mirror/'
	mir_AnnotationsSavePath = mir_savepath + 'JSON/'
	mir_imgsavepath = mir_savepath + 'JPEG/'

	if not os.path.exists(mir_savepath):
		os.makedirs(mir_savepath)   
	if not os.path.exists(mir_imgsavepath):
		os.makedirs(mir_imgsavepath) 
	if not os.path.exists(mir_AnnotationsSavePath):
		os.makedirs(mir_AnnotationsSavePath)

	enhancement_using_mirror(modes, mir_ImagePath,mir_AnnotationsPath,mir_imgsavepath,mir_AnnotationsSavePath)

if __name__ == '__main__':
	global annotation_file, ifshow
	annotation_file = 'json'#'txt',xml'
	ifshow = 0
	modes = ['h', 'v', 'd']
	main(modes)

