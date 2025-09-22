import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import datetime # Import datetime for timestamp
import zipfile # Import zipfile for handling zip files
import shutil # Import shutil for removing directories

app = Flask(__name__)
UPLOAD_FOLDER = 'files/Temps'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("\n" + "-"*50) # Separator
    client_ip = request.remote_addr
    print(f"[{os.getpid()}] Received upload request from {client_ip}.") # Log request with client IP
    relative_path = request.form.get('relative_path', '') # Get relative_path
    print(f"[{os.getpid()}] Relative path: {relative_path}")

    if 'file' not in request.files:
        print(f"[{os.getpid()}] Error: No file part in the request.")
        print("-" * 50 + "\n") # Separator
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        print(f"[{os.getpid()}] Error: No selected file.")
        print("-" * 50 + "\n") # Separator
        return jsonify({'error': 'No selected file'}), 400
    if file:
        
        # Construct the full target directory
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], os.path.dirname(relative_path))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True) # Create directories if they don't exist

        original_filename = file.filename
        filename_without_ext, file_extension = os.path.splitext(original_filename)
        
        new_filename = original_filename
        filepath = os.path.join(target_dir, new_filename)

        # Handle duplicate filenames by appending a timestamp
        if os.path.exists(filepath):
            timestamp = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
            new_filename = f"{filename_without_ext}{timestamp}{file_extension}"
            filepath = os.path.join(target_dir, new_filename)
            print(f"[{os.getpid()}] Duplicate file detected. Renaming to: {new_filename}")

        print(f"[{os.getpid()}] Saving file: {new_filename} to {filepath}")
        file.save(filepath)

        # Check if the uploaded file is a client-zipped folder
        if new_filename.endswith('-clientzip.zip'):
            print(f"[{os.getpid()}] Detected client-zipped file: {new_filename}")
            unzip_path = target_dir
            
            try:
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)
                print(f"[{os.getpid()}] Successfully unzipped {new_filename} to {unzip_path}")
                os.remove(filepath) # Remove the zip file after extraction
                print(f"[{os.getpid()}] Removed temporary zip file: {filepath}")
                return jsonify({'message': f'[server respond..] {new_filename} unzipped successfully to {unzip_path}'}), 200
            except Exception as e:
                print(f"[{os.getpid()}] Error unzipping file {new_filename}: {e}")
                return jsonify({'error': f'Error unzipping file {new_filename}: {e}'}), 500
        else:
            print(f"[{os.getpid()}] Successfully saved file: {new_filename}.")
            print("-" * 50 + "\n") # Separator
            return jsonify({'message': f'[server respond..] {new_filename} uploaded successfully to {relative_path}'}), 200

if __name__ == '__main__':
    print(f"[{os.getpid()}] Server starting on http://{app.config['SERVER_NAME'] or '0.0.0.0'}:{5009}")
    print(f"[{os.getpid()}] Uploads will be saved to: {os.path.abspath(UPLOAD_FOLDER)}")
    print("-" * 50 + "\n") # Initial separator

    app.run(debug=True, host='0.0.0.0', port=5009)
