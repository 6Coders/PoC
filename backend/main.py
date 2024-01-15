import os
import time
import chatsql 
from flask_cors import CORS
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'sql', 'json'}

# instantiate the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
@app.route('/upload', methods=['POST'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if 'file' not in request.files:
        return 'No file part in the request'
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return 'File successfully uploaded'

@app.route('/files', methods=['GET'])
def get_files():
    files_dir = app.config['UPLOAD_FOLDER']
    files = []
    for filename in os.listdir(files_dir):
        path = os.path.join(files_dir, filename)
        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        date = time.ctime(mtime)
        name, extension = os.path.splitext(filename)
        loaded = chatsql.verify_file_name(filename)
        print(loaded)
        files.append({
            'name': name,
            'extension': extension,
            'date': date,
            'size': size,
            'loaded': loaded
        })
    return jsonify(files)

@app.route('/file/<filename>', methods=['GET'])
def get_file_info(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            chatsql.set_file_path(file_path)
            chatsql.Init()
            return jsonify({'message': f'File {filename} found', 'found': True, 'filename': filename})
        else:
            return jsonify({'message': f'File {filename} does not exist', 'found': False})
    except Exception as e:
        return jsonify({'message': str(e), 'found': False})

@app.route('/getfileloaded', methods=['GET'])
def get_file_loaded():
    try:
        print(chatsql.get_file_name())
        return jsonify({'loaded': chatsql.get_file_name()})
    except Exception as e:
        return jsonify({'message': str(e)})
    
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'File successfully deleted'})
        else:
            return jsonify({'message': 'File does not exist'})
    except Exception as e:
        return jsonify({'message': str(e)})


if __name__ == '__main__':
    app.run()
