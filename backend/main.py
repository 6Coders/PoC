import os
import time
from chatsql import ChatSQL
from flask import Flask, jsonify
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
CORS(app, resources={'/*': {'origins': '*'}})

current_file = None
chatSql = None

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
        loaded = False #non ancora possibile applicare la logica di caricamento 
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
    global current_file
    global chatSql

    try:
        current_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(current_file):
        
            if (chatSql is not None):
                del chatSql
            
            chatSql = ChatSQL(current_file)
                    
            return jsonify({'message': f'File {filename} found', 'found': True, 'filename': filename})
        else:
            return jsonify({'message': f'File {filename} does not exist', 'found': False})
    except Exception as e:
        return jsonify({'message': str(e), 'found': False})

@app.route('/getloadedfile', methods=['GET'])
def getloadedfile():
    try:
        return jsonify({'filepath': current_file}, success=True)
    except Exception as e:
        return jsonify({'message': str(e), 'found': False})


if __name__ == '__main__':
    app.run()