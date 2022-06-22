import os
import cv2
import io
from base64 import encodebytes
from PIL import Image
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_swagger_ui import get_swaggerui_blueprint
from find_face import find_face

app = Flask(__name__)

SWAGGER_URL = '/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/openapi.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Programming project"
    },
)

app.register_blueprint(swaggerui_blueprint)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        directory = 'static/uploads/' + filename
        img = cv2.imread(directory)
        img = find_face(img)
        cv2.imwrite(directory, img)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>', methods=['GET'])
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/download/<filename>', methods=['GET'])
def download_image(filename):
    if filename == '':
        flash('No image selected for uploading')
        return 404

    image_path = 'static/uploads/' + filename
    pil_img = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    my_message = 'here is my message'
    message = {'Status': 'Success', 'message': my_message, 'ImageBytes': encoded_img}
    return jsonify(message), 200


port = int(os.environ.get("PORT", 8000))
app.run(host='0.0.0.0', port=port)
