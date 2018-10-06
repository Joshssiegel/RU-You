from google.cloud import storage
import cv2
import os
import requests
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import urllib
import numpy as np


BUCKET_NAME="ru-you"
IMAGE_FILENAME='temporaryImage.jpg'
def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_name)
	print('File {} uploaded to {}.'.format(
		source_file_name,
		destination_blob_name))

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
	app = ClarifaiApp(api_key='6bfb288a66c14572ac765df2aac1c764')
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


#create_bucket(BUCKET_NAME)
#upload_blob(BUCKET_NAME,'testImg.jpg',"test-image-2")
images=getImageUrls(BUCKET_NAME)
displayImageFromUrl(images[1])
displayImageFromUrl(images[1])
compareImages(images[1],images[1])
