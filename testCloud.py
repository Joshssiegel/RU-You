from google.cloud import storage

BUCKET_NAME="ru-you"
def upload_blob(bucket_name, source_file_name, destination_blob_name):
	"""Uploads a file to the bucket."""
	storage_client = storage.Client()
	print("After")
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

#create_bucket(BUCKET_NAME)
upload_blob(BUCKET_NAME,'testImg.jpg',"test-image-1")