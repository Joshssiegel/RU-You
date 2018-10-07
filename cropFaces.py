from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import cv2
client = vision.ImageAnnotatorClient()

def detect_face(face_file, max_results=4):
	'''Uses the Vision API to detect faces in the given file.

	Args:
		face_file: A file-like object containing an image with faces.

	Returns:
		An array of Face objects with information about the picture.
	'''
	client = vision.ImageAnnotatorClient()

	content = face_file.read()
	image = types.Image(content=content)

	return client.face_detection(image=image).face_annotations

def highlight_faces(image, faces, output_filename):
	"""Draws a polygon around the faces, then saves to output_filename.

	Args:
	  image: a file containing the image with the faces.
	  faces: a list of faces found in the file. This should be in the format
		  returned by the Vision API.
	  output_filename: the name of the image file to be created, where the
		  faces have polygons drawn around them.
	"""
	im = Image.open(image)
	draw = ImageDraw.Draw(im)
	im2=Image.open(image)
	i=0
	for face in faces:
		i+=1
		box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
		im2=crop(im,face.bounding_poly.vertices)
		draw.line(box + [box[0]], width=5, fill='#00ff00')
		im2.save("cropped"+str(i)+".jpg")#instead of save, write it to the cloud
		
	im.save(output_filename)

def crop(image_file, box):
	vects = box
	im = image_file
	im2 = im.crop([vects[0].x, vects[0].y,
				  vects[2].x - 1, vects[2].y - 1])
	return im2
def resizeAndUpdateImage(filename):
	image=cv2.imread(input_filename)
	scale=(image.shape[1]+image.shape[0])/(1600+1200)
	print("Scale is: ",scale)
	image=cv2.resize(image,(int(image.shape[1]/scale),int(image.shape[0]/scale)))
	cv2.imwrite("resized.jpg",image)
	return image
def findAndCropFaces(input_filename, output_filename, max_results):
	resizeAndUpdateImage(input_filename)
	with open('resized.jpg', 'rb') as image:
		faces = detect_face(image, max_results)
		print('Found {} face{}'.format(
			len(faces), '' if len(faces) == 1 else 's'))
		print('Writing to file {}'.format(output_filename))
		# Reset the file pointer, so we can read the file again
		image.seek(0)
		highlight_faces(image, faces, output_filename)
#main('temporaryImage.jpg','output.jpg',5)
#main('person.jpg','person-updated.jpg',5)