from flask import Flask, render_template, request, send_file
from random import choice
import subprocess
import os

app = Flask(__name__)

def is_image(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ['png','jpg','jpeg','gif']

def makeID():
	return ''.join(choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))

@app.route("/", methods=['GET','POST'])
def root():
	if request.method == 'POST':
		img = request.files['file']
		if is_image(img.filename):
			stem = str(makeID())
			path = os.path.join('./images/', stem + '.' + img.filename.split('.')[-1])
			img.save(path)
			subprocess.call(['python', 'intensifies.py',
				'--image', path,
				'--text', request.form['text'],
				'--outfile', './gifs/' + stem + '.gif',
				'--intensity', '5',
				'--flash-text'])
			return "<img src=\"/i/" + stem + "\">"
	else:
		return render_template("index.html")

@app.route("/i/<stem>/")
def getfile(stem):
	return send_file("./gifs/" + stem + ".gif", mimetype="image/gif")

if __name__ == "__main__":
	app.debug = True
	app.run()

