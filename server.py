from flask import Flask, request
import urllib
import RU_You
import cropFaces
app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def display():
	print("we've been visited")
	base64=request.form['body']
	print(base64)
	response=RU_You.onCameraTrigger(base64)
	print("response is: ",response)
	if(response == '0'):
		cropFaces.displayImg(base64)
	return response

if __name__ =='__main__':
	app.run()