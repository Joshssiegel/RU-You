from google.cloud import storage
BUCKET_NAME="ru-you"
import cv2
import os
import requests
def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	print("After")
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.make_public(None)
	blob.upload_from_filename(source_file_name)

	print('File {} uploaded to {}.'.format(
		source_file_name,
		destination_blob_name))

def create_bucket(bucket_name):
	storage_client=storage.Client()
	bucket=storage_client.create_bucket(bucket_name)
	print('Bucket {} created'.format(bucket.name))
	
	
	
	
def get_images(bucket_name):
	'''Lists all the blobs in the bucket.'''
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blobs = bucket.list_blobs()
	images=[]
	for blob in blobs:
		#print('Crc32c: {}'.format(blob.crc32c))
		images.append(bucket.blob(blob.name))
		uri=blob.public_url
		print(requests.get(uri))
		'''
		#blob.download_to_filename('delete.jpg')
		img=cv2.imread(blob)
		cv2.imshow('name',img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()'''
	return images
def download_image(image, bucket_name, destination_file_name):
	'''Downloads a blob from the bucket.'''
	storage_client = storage.Client()
	blob.download_to_filename(destination_file_name)
	cv2.imshow(destination_file_name)
	print('Blob {} downloaded to {}.'.format(
		source_blob_name,
		destination_file_name))

	
#create_bucket(BUCKET_NAME)
upload_blob(BUCKET_NAME,'testImg.jpg',"test-image-1")
images=get_images(BUCKET_NAME)
#download_image(images[0])
#download_blob(BUCKET_NAME,)