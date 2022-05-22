import flask
from flask import Flask, render_template, Blueprint
import cv2
from anonymize_face import anonymize_face_pixelate
from anonymize_face import anonymize_face_simple
from find_face import find_face

app = Flask(__name__)
mod = Blueprint('', __name__)


@app.route('/', methods=['GET'])
def new_checkout():
    return render_template('index.html')


@app.route('/image-upload/', methods=['GET', 'POST'])
def upload():
    imagefile = flask.request.files.get('imagefile', '')
    imagefile = cv2.imread('human.jpg')
    image = find_face(imagefile)
    return flask.send_file(image, as_attachment=True, mimetype='image/jpg', download_name='aaa')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
