import argparse
import io	
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
#import cv2
import os
import requests
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

BUCKET_NAME="ru-you"
IMAGE_FILENAME='temporaryImage.jpg'
API_KEY='6bfb288a66c14572ac765df2aac1c764'
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
	
def getImageUrls(bucket_name):
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
	app = ClarifaiApp(api_key=API_KEY)
	model = app.models.get('general-v1.3')
	image = ClImage(url=url)
	print(model.predict([image]))
def compareImage(im1, im2):
	pass
	

def get_crop_hint(path):
	"""Detect crop hints on a single image and return the first result."""
	client = vision.ImageAnnotatorClient()

	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)

	crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
	image_context = types.ImageContext(crop_hints_params=crop_hints_params)

	response = client.crop_hints(image=image, image_context=image_context)
	hints = response.crop_hints_annotation.crop_hints

	# Get bounds for the first crop hint using an aspect ratio of 1.77.
	vertices = hints[0].bounding_poly.vertices

	return vertices


def draw_hint(image_file):
	"""Draw a border around the image using the hints in the vector list."""
	vects = get_crop_hint(image_file)

	im = Image.open(image_file)
	draw = ImageDraw.Draw(im)
	draw.polygon([
		vects[0].x, vects[0].y,
		vects[1].x, vects[1].y,
		vects[2].x, vects[2].y,
		vects[3].x, vects[3].y], None, 'red')
	im.save('output-hint.jpg', 'JPEG')


def crop_to_hint(image_file):
	"""Crop the image using the hints in the vector list."""
	vects = get_crop_hint(image_file)

	im = Image.open(image_file)
	im2 = im.crop([vects[0].x, vects[0].y,
				  vects[2].x - 1, vects[2].y - 1])
	im2.save('output-crop.jpg', 'JPEG')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('image_file', help='The image you\'d like to crop.')
	parser.add_argument('mode', help='Set to "crop" or "draw".')
	args = parser.parse_args()

	parser = argparse.ArgumentParser()

	if args.mode == 'crop':
		crop_to_hint(args.image_file)
	elif args.mode == 'draw':
		draw_hint(args.image_file)

#create_bucket(BUCKET_NAME)
#upload_blob(BUCKET_NAME,'testImg.jpg',"test-image-2")
images=getImageUrls(BUCKET_NAME)
