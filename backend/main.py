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
CORS(app, resources={r'/*': {'origins': '*'}})

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
        loaded = path == current_file
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

@app.route('/getfileloaded', methods=['GET'])
def get_file_loaded():
    try:
        loaded_file_name = os.path.basename(chatSql.get_path())
        print(loaded_file_name)
        return jsonify({'loaded': loaded_file_name})
    except Exception as e:
        return jsonify({'message': str(e)})
        
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            os.remove(file_path)
            return jsonify({'message': 'File Deleted'})
        except OSError as er:
            err_message = "Error: "+er.filename+" - "+er.strerror
            return jsonify({'message': err_message})
    except Exception as e:
        return jsonify({'message': str(e)})


if __name__ == '__main__':
    app.run()
