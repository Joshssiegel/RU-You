import argparse
import io
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import cv2
import os
import requests
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import urllib
import numpy as np
import cropFaces
import base64

BUCKET_NAME="ru-you"
CAMERA_BUCKET_NAME="ru-you-camera"
CROPPED_BUCKET_NAME="ru-you-cropped"
IMAGE_FILENAME='temporaryImage.jpg'
API_KEY='6bfb288a66c14572ac765df2aac1c764'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_name)
	print('File {} uploaded to {}.'.format(source_file_name,destination_blob_name))

def create_bucket(bucket_name):
	storage_client=storage.Client()
	bucket=storage_client.create_bucket(bucket_name)
	print('Bucket {} created'.format(bucket.name))


def displayImageFromBlob(blob):
	blob.download_to_filename(IMAGE_FILENAME)
	img=cv2.imread(IMAGE_FILENAME)
	cv2.imshow('name',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
def displayImageFromUrl(url):
	cap = cv2.VideoCapture(url)
	if( cap.isOpened() ) :
		ret,img = cap.read()
		cv2.imshow("win",img)
		cv2.waitKey()

def getImageUrls(bucket_name):
	'''Lists all the blobs in the bucket.'''
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blobs = bucket.list_blobs()
	images=[]
	prev=""
	for blob in blobs:
		#print('Crc32c: {}'.format(blob.crc32c))
		#uri=blob.media_link
		#print(requests.get(uri))
		url=blob.generate_signed_url(999999999999999)
		if(prev == url):
			print("uh oh")
		prev=url
		images.append(url)
		#r=requests.get(url,stream=True)
		#print(r.headers)
		

	return images


def classifyImage(url):
	app = ClarifaiApp(api_key=API_KEY)
	model = app.models.get('general-v1.3')
	image = ClImage(url=url)
	print(model.predict([image]))

def compareImages(im1, im2):
	app = ClarifaiApp(api_key='6bfb288a66c14572ac765df2aac1c764')
	model = app.models.get('general-v1.3')
	img1 = ClImage(url=im1)
	app.inputs.bulk_create_images([img1])
	search=app.inputs.search_by_image(url=im2)
	search_result = search[0]
	score=search_result.score
	print("Score:", score)
	app.inputs.delete(search_result.input_id)
	return score

def onCameraTrigger(image):
	thresh=.8
	client = storage.Client()
	filenames=cropFaces.findAndCropFaces(image)#filenames of faces we've found and cropped
	if(len(filenames)==0):
		return "0"
	facesToAdd=[]
	for filename in filenames:
		counter=0
		upload_blob(CROPPED_BUCKET_NAME,filename,filename)
		cropped_bucket=client.get_bucket(CROPPED_BUCKET_NAME)
		cropped_blob=cropped_bucket.get_blob(filename)
		cropped_url=cropped_blob.generate_signed_url(999999999999999)
		#Get latest uploaded image
		#logging.warn("Data is: ",data)
		bucket=client.get_bucket(BUCKET_NAME)
		blobs=bucket.list_blobs()
		for blob in blobs:
			counter+=1
			url=blob.generate_signed_url(999999999999999)
			score=compareImages(cropped_url,url)
			if(score>=thresh):
				cropped_blob.delete()
				return "0"
		name='image'+str(counter)
		facesToAdd.append((filename,name))
		cropped_blob.delete()
	for face in facesToAdd:
		upload_blob(BUCKET_NAME,face[0],face[1])

	return "1"



#create_bucket(CROPPED_BUCKET_NAME)
#upload_blob(CAMERA_BUCKET_NAME,'josh_suit.jpg',"test-image-9")
#upload_blob(BUCKET_NAME,'cropped1.jpg',"test-image-8")
'''images=getImageUrls(BUCKET_NAME)
for img in images:
	image=cropFaces.resizeAndUpdateImage(img)
	cv2.imshow('name',image)
	cv2.waitKey()'''
#	displayImageFromUrl(img)
#displayImageFromUrl(images[6])
#compareImages(images[7],images[6




#imageb64=to_image_string('josh_suit.jpg')
#imageb64=None
#img=stringToImage(imageb64)
#cv2.imshow("anme",img)
#cv2.waitKey()
#print(onCameraTrigger(imageb64))




