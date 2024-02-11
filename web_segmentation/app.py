from flask import Flask, request, jsonify, render_template
import re
import os

from models import modeling

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


# 업로드된 이미지를 저장할 디렉토리
UPLOAD_FOLDER = './static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 파일 업로드 허용 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 파일 확장자 검사 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_images():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')

    file_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            file_paths.append(file_path)

    modeling(get_file_index(file.filename))
    return jsonify({'uploaded_files': file_paths}), 200


def get_file_index(filename):
    match = re.search(r'\d+', filename)
    if match:
        extracted_number = int(match.group())
        return extracted_number
    else:
        print("No number found in the filename")


@app.route('/image-delete', methods=['DELETE'])
def delete_files():
    folder_path = './static/uploads'  # 삭제할 폴더 경로로 변경해주세요

    try:
        # 폴더 내의 모든 파일 목록 가져오기
        file_list = os.listdir(folder_path)

        # 폴더 내의 모든 파일 삭제
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)

        return 'All files in the folder have been deleted successfully.'
    except Exception as e:
        return f'Error occurred while deleting files: {e}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
