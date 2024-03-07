from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def handle_data():
    try:
        # if 'files' in request.files:
            # 获取上传的文件数据
        file = request.files['files']
        # 处理文件数据，例如保存到本地或者进行其他操作
        # 这里直接打印文件名和文件内容
        print(file.filename)
        return '文件上传成功', 200
        # else:
        #     return '未找到上传的文件', 400
    except Exception as e:
        print('处理请求时发生异常：', e)
        return jsonify({'error': '处理请求时发生异常'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=80)