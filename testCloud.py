from google.cloud import storage
import cv2
import os
import requests
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

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
	
def get_images_urls(bucket_name):
	'''Lists all the blobs in the bucket.'''
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blobs = bucket.list_blobs()
	images=[]
	for blob in blobs:
		#print('Crc32c: {}'.format(blob.crc32c))
		images.append(bucket.blob(blob.name))
		#uri=blob.media_link
		#print(requests.get(uri))
		url=blob.generate_signed_url(999999999999999)
		images.append(url)
		#r=requests.get(url,stream=True)
		#print(r.headers)
		

	return images


def classifyImage(url):
	app = ClarifaiApp(api_key='6bfb288a66c14572ac765df2aac1c764')
	model = app.models.get('general-v1.3')
	image = ClImage(url=url)
	print(model.predict([image]))
def compareImage(im1, im2):
	pass

#create_bucket(BUCKET_NAME)
#upload_blob(BUCKET_NAME,'testImg.jpg',"test-image-2")
images=get_images(BUCKET_NAME)
