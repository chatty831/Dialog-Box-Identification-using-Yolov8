from flask import Flask, request, jsonify, render_template
import os
from ultralytics import YOLO
from generate import *

app = Flask(__name__)

original_image_path = None
changed_image_path = None
model = None
original_image = None

model_names = {
    'Bounding Box v1' : 'segmented_dialog_box.pt',
    'Bounding Box v2' : 'manhwa_best.pt'
    }


UPLOAD_FOLDER = '/static/uploads/'
TRANSFORM_FOLDER = '/static/transforms/'
ALLOWED_EXTENSIONS = set([
    'bmp',
    'dng',
    'jpeg',
    'jpg', 
    'png', 
    'tif',   
    'tiff',  
    'webp',  
    'pfm',
])

# Create the 'uploads' folder if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

app.config['ROOT_FOLDER'] = os.path.dirname(os.path.abspath(__file__))
app.config['MODEL_FOLDER'] = '/models/'
app.config['UPLOAD_FOLDER'] = os.path.normpath((os.path.dirname(os.path.abspath(__file__))+UPLOAD_FOLDER))
app.config['TRANSFORM_FOLDER'] = os.path.normpath((os.path.dirname(os.path.abspath(__file__))+TRANSFORM_FOLDER))

os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
os.makedirs(app.config['TRANSFORM_FOLDER'],exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

def clean_directory(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path,file)
        os.remove(file_path)
        print('Removed: ', file_path)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/send_model', methods=['POST'])
def model_init():
    global model
    data= request.get_json()
    model_name = data.get('stringData')
    model_name = model_names[model_name]
    model = YOLO(os.path.normpath(app.config['ROOT_FOLDER'] + app.config['MODEL_FOLDER'] + model_name))
    return jsonify({'message': 'Option received successfully'})
    
    
@app.route('/upload', methods=['POST'])
def upload():

    clean_directory(app.config['UPLOAD_FOLDER'])
    clean_directory(app.config['TRANSFORM_FOLDER'])
    
    global original_image
    # Get the file from the request
    original_image = request.files['image']

    # If a file is present
    if original_image and allowed_file(original_image.filename):
        file_path = app.config['UPLOAD_FOLDER'] +'\\' +  original_image.filename
        original_image.save(file_path)
        
        global original_image_path 
        original_image_path = file_path
        return render_template('index.html', original_image='uploads/' + original_image.filename)
    
    return render_template('index.html')

@app.route('/generate')
def get_result():
    global original_image_path, model
    changed_image_path = generate(original_image_path,model)
    print('before change', changed_image_path)
    
    return jsonify({'result': 'Image generated successfully', 'changed_image': changed_image_path})
    
    
# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
