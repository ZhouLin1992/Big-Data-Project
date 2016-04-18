import sys
from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import model_from_json
import os
from PIL import Image
import numpy as np
from resizeimage import resizeimage

print('loading data...')
data = np.empty((1,1,256,256),dtype="float32")
label = np.empty((1,),dtype="float32")
imgs = os.listdir("/var/www/html/jQuery_upload/uploads/")
num = len(imgs)
for i in range(num):
	img = Image.open("/var/www/html/jQuery_upload/uploads/"+imgs[i])
	img = img.convert('L')
	img = resizeimage.resize_cover(img, [256,256])
	arr = np.asarray(img,dtype="float32")
	data[i,0,:,:] = arr
#	label[i] = int(imgs[i].split('_')[0])
	
scale = np.max(data)
data /= scale
mean = np.std(data)
data -= mean
print('loading model...')
model = model_from_json(open('/home/xinsongdu/Desktop/bigdata/project/data/my_model_architecture2.json').read())
model.load_weights('/home/xinsongdu/Desktop/bigdata/project/data/my_model_weights2.h5')
pdct=model.predict_classes(data, batch_size=1, verbose=1)
pdct2=model.predict_proba(data, batch_size=1, verbose=1)

file=open('/var/www/html/jQuery_upload/log/log.txt','w+')

print('*result*')
print('<tr>')
if(pdct[0]==0):
	print('<td>Alley</td>')
elif(pdct[0]==1):
	print('<td>Amusement Park</td>');
elif(pdct[0]==2):
	print('<td>Aquarium</td>');
elif(pdct[0]==3):
	print('<td>Bedroom</td>');
elif(pdct[0]==4):
	print('<td>Bookstore</td>');
elif(pdct[0]==5):
	print('<td>Bridge</td>');
print('</tr>')
print('<tr><td>Alley</td><td>',pdct2[0][0],'</td></tr>');
print('<tr><td>Amusement Park</td><td>',pdct2[0][1],'</td></tr>');
print('<tr><td>Bedroom</td><td>',pdct2[0][3],'</td></tr>');
print('<tr><td>Bookstore</td><td>',pdct2[0][4],'</td></tr>');
print('<tr><td>Bridge</td><td>',pdct2[0][5],'</td></tr>');

file.write('*result*')
file.write('<tr>')
if(pdct[0]==0):
	file.write('<td>Alley</td>')
elif(pdct[0]==1):
	file.write('<td>Amusement Park</td>');
elif(pdct[0]==2):
	file.write('<td>Aquarium</td>');
elif(pdct[0]==3):
	file.write('<td>Bedroom</td>');
elif(pdct[0]==4):
	file.write('<td>Bookstore</td>');
elif(pdct[0]==5):
	file.write('<td>Bridge</td>');
file.write('</tr>')
file.write('<tr><td>Alley</td><td>'+str(pdct2[0][0])+'</td></tr>');
file.write('<tr><td>Amusement Park</td><td>'+str(pdct2[0][1])+'</td></tr>');
file.write('<tr><td>Bedroom</td><td>'+str(pdct2[0][3])+'</td></tr>');
file.write('<tr><td>Bookstore</td><td>'+str(pdct2[0][4])+'</td></tr>');
file.write('<tr><td>Bridge</td><td>'+str(pdct2[0][5])+'</td></tr>');
file.close







# if(pdct[0]==0):
# 	print('*Alley*');
# elif(pdct[0]==1):
# 	print('*Amusement Park*');
# elif(pdct[0]==2):
# 	print('*Aquarium*');
# elif(pdct[0]==3):
# 	print('*Bedroom*');
# elif(pdct[0]==4):
# 	print('*Bookstore*');
# elif(pdct[0]==5):
# 	print('*Bridge*');

# print('*Alley:',pdct2[0][0],'*');
# print('*Amusement Park:',pdct2[0][1],'*');
# print('*Aquarium:',pdct2[0][2],'*');
# print('*Bedroom:',pdct2[0][3],'*');
# print('*Bookstore:',pdct2[0][4],'*');
# print('*Bridge:',pdct2[0][5],'*');
#print(label)
#print(pdct-label)







