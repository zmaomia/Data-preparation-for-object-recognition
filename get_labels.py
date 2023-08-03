import os
import shutil

testfolder = './Gamma-test/JPEG/'

testlabel = './test.txt'

for img in os.listdir(testfolder):
	name, ext = os.path.splitext(img)
	with open(testlabel, 'a') as f:
		f.write(name + '\n')

f.close()