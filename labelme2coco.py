#!/usr/bin/env python

import argparse
import collections
import datetime
import glob
import json
import os
import os.path as osp
import sys
import numpy as np
import PIL.Image
import labelme

try:
	import pycocotools.mask
except ImportError:
	print('Please install pycocotools:\n\n    pip install pycocotools\n')
	sys.exit(1)


def main():

	input_dir_json = './orig-3/test/aug/JSON-test-aug'
	input_dir_JPEG = './orig-3/test/aug/JPEGImage-test-aug'
	output_dir = './orig-3/test/'
	filename = 'test'
	labels = './labels1cls.txt'

	names = ['lamppostA', 'lamppostB', 'lamppostC', 'lamppostD', 'monitorA', 'monitorB', 'trafficlightA', 'trafficlightB']

	# names = ['vpole', 'ppole', 'light', 'timer', 'sign', 'camera', 'flashlight'] 


	if osp.exists(output_dir):
		print('Output directory already exists:', output_dir)
		# sys.exit(1)
	# if not os.path.exists()
	else:
		os.makedirs(output_dir)
		# os.makedirs(osp.join(output_dir, 'JPEGImages'))
	print('Creating dataset:', output_dir)

	now = datetime.datetime.now()

	data = dict(
		info=dict(
			description=None,
			url=None,
			version=None,
			year=now.year,
			contributor=None,
			date_created=now.strftime('%Y-%m-%d %H:%M:%S.%f'),
		),
		licenses=[dict(
			url=None,
			id=0,
			name=None,
		)],
		images=[
			# license, url, file_name, height, width, date_captured, id
		],
		type='instances',
		annotations=[
			# segmentation, area, iscrowd, image_id, bbox, category_id, id
		],
		categories=[
			# supercategory, id, name
		],
	)

	class_name_to_id = {}

	for i, line in enumerate(open(labels).readlines()):
		class_id = i - 1  # starts with -1
		class_name = line.strip()
		if class_id == -1:
			assert class_name == '__ignore__'
			continue
		class_name_to_id[class_name] = class_id
		data['categories'].append(dict(
			supercategory=None,
			id=class_id,
			name=class_name,
		))

	out_ann_file = osp.join(output_dir,  filename+'.json')
	label_files = glob.glob(osp.join(input_dir_json, '*.json')) #'./Gammatest/JSON' + json
	
	totalbboxlist = [] 

	for image_id, label_file in enumerate(label_files):
		
		label_file = label_file.replace('\\', '/')
		print('Generating dataset from:', label_file)
		with open(label_file) as f:
			label_data = json.load(f)

		base = osp.splitext(osp.basename(label_file))[0]
		out_img_file = osp.join(
			output_dir, 'JPEGImages', base + '.png'
		)
		
		# path = label_data['imagePath']
		imagepath = base + '.png'

		img_file = osp.join(input_dir_JPEG, imagepath)
		img_file = img_file.replace('\\', '/')
		# print('img_file:', img_file)
		img = np.asarray(PIL.Image.open(img_file))	
		# PIL.Image.fromarray(img).save(out_img_file)
		
		data['images'].append(dict(
			license=0,
			url=None,
			file_name=osp.relpath(out_img_file, osp.dirname(out_ann_file)),
			height=img.shape[0],
			width=img.shape[1],
			date_captured=None,
			id=image_id,
		))

		masks = {}                                     # for area
		segmentations = collections.defaultdict(list)  # for segmentation
		
		for shape in label_data['shapes']:

			points = shape['points']
			label = shape['label']
			# label = label[5:] ## transfer label to glass+id

			# print('label:', label)
			# exit(0)
			if label[:-1] in names:
				# print('==========:',label[:-1])

				shape_type = shape.get('shape_type', None)
				
				mask = labelme.utils.shape_to_mask(
					img.shape[:2], points, shape_type
				)

				if label in masks:
					masks[label] = masks[label] | mask
				else:
					masks[label] = mask

				points = np.asarray(points).flatten().tolist()
				segmentations[label].append(points)

		for label, mask in masks.items():
			
			cls_name = label[:-1]

			if cls_name not in class_name_to_id:
				continue
			
			cls_id = class_name_to_id[cls_name]

			mask = np.asfortranarray(mask.astype(np.uint8))
			mask = pycocotools.mask.encode(mask)
			area = float(pycocotools.mask.area(mask))
			bbox = pycocotools.mask.toBbox(mask).flatten().tolist()

			totalbboxlist.append(bbox)

			data['annotations'].append(dict(
				id=len(data['annotations']),
				image_id=image_id,
				category_id=cls_id,
				segmentation=segmentations[label],
				area=area,
				bbox=bbox,
				iscrowd=0,
			))

	with open(out_ann_file, 'w') as f:
		json.dump(data, f)
	f.close()


if __name__ == '__main__':
	main()
