from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
CORS(app)  # 允许跨域请求
# 上传文件保存的目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print('111')
@app.route('/data', methods=['POST'])
def handle_data():
    try:
        # if 'files' in request.files:
            # 获取上传的文件数据
        print('loading')
        file = request.files['files']
        # 处理文件数据，例如保存到本地或者进行其他操作
        # 这里直接打印文件名和文件内容
        print(file.filename)
        # 保存文件到指定路径
        filename=file.filename
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})
        # else:
        #     return '未找到上传的文件', 400
    except Exception as e:
        print('处理请求时发生异常：', e)
        return jsonify({'error': '处理请求时发生异常'}),600

if __name__ == '__main__':
    app.run(debug=True, port=8081)