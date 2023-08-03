import os
import json 
import cv2


folder = './orig-2/test/'
# check_save = './guangming-data-check/' #foler to save checked img
names = ['lamppostA', 'lamppostB', 'lamppostC', 'lamppostD', 'monitorA', 'monitorB', 'trafficlightA', 'trafficlightB']
# imglist = []
# jsonlist = []

labellist = []

for cato in names:
    print(f'---- statisticing {cato}-----')
    obj_num = 0
    img_num = 0

    for jsonf in os.listdir(folder + 'JSON'):

        img_label = []

        jname, ext = os.path.splitext(jsonf)

        if ext == '.json':      

            with open(folder + 'JSON/' + jsonf, 'r') as f:
                data = json.load(f)
                # print(data)

            for shape in data['shapes']:
                label = shape['label']

                if label[:-1] == cato:  #统计某类别目标的个数
                    obj_num += 1


                if label[:-1] not in img_label:  #统计存在某类别目标的影像数
                    img_label.append(label[:-1])

        if cato in img_label: #统计存在某类别目标的影像数
            img_num += 1

        if label[:-1] not in labellist: 
            labellist.append(label[:-1])

    print(f'{cato} obj_num:', obj_num )
    print(f'{cato} img_num:', img_num )


print(labellist)

# print(list(set(imglist).difference(set(jsonlist)))) 