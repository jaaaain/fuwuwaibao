from flask import Flask, request, jsonify,render_template, send_file
from flask_cors import CORS
from os.path import basename
from werkzeug.utils import secure_filename
import os
import joblib
import pandas as pd
import numpy as np
import chardet
import base64

class my_model:
    def __init__(self, cat=None, xgb=None, lgb=None, RFC=None):
        self.cat = cat
        self.xgb = xgb
        self.lgb = lgb
        self.RFC = RFC
    def predict(self, test_x, threshold=0.95):
        test_output_df = pd.DataFrame(columns=['lgb', 'xgb', 'cat'], index=range(test_x.shape[0]))
        test_output_df = test_output_df.fillna(0)
        for i in range(10):
            test_output_df['cat'] += self.cat[i].predict_proba(test_x)[:, 1] / 10
            test_output_df['xgb'] += self.xgb[i].predict_proba(test_x)[:, 1] / 10
            test_output_df['lgb'] += self.lgb[i].predict_proba(test_x)[:, 1] / 10
        pred = self.RFC.predict_proba(test_output_df)[:, 1]
        final_pred = np.array([1 if x >= threshold else 0 for x in pred])
        return final_pred

    @classmethod
    def load(cls, path):
        return joblib.load(path)#特殊的模型处理
model = joblib.load("model/my_model.dat")
app = Flask(__name__)
CORS(app)  # 允许跨域请求
# 上传文件保存的目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# 全局变量保存文件地址
file_path = None
@app.route('/data', methods=['POST'])
def get_data():
    try:
        # if 'files' in request.files:
            # 获取上传的文件数据
        print('loading')
        file = request.files['files']
        # 处理文件数据，例如保存到本地或者进行其他操作

        return handle_data(file)
    except Exception as e:
        print('处理请求时发生异常：', e)
        return jsonify({'error': '处理请求时发生异常'}),400
def handle_data(file):
    try:
        print('handling')
        filename = file.filename
        global file_path  # 使用全局变量保存文件地址
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # 使用 chardet 检测文件编码
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        # 输出检测结果
        print(result['encoding'])
        # 使用检测结果的编码方式读取文件
        df = pd.read_csv(file_path, encoding=result['encoding'])
        #特征处理
        df['月就诊天数_SUM'] = df['月就诊天数_AVG'] * df['就诊的月数']
        df['max占最大月的百分比'] = df['月统筹金额_MAX'] /df['统筹支付金额_SUM']
        df = df.fillna(0)
        # 提取特征列
        X = df[['月统筹金额_MAX','月就诊天数_SUM','月就诊次数_MAX','统筹支付金额_SUM','本次审批金额_SUM','max占最大月的百分比']]

        # 进行预测
        predictions = model.predict(X)

        # 将预测结果添加到文件中
        df['res'] = predictions

        # 保存带有预测结果的文件
        df.to_csv(file_path, index=False)

        return jsonify({'message': 'File uploaded successfully'})
        # else:
        #     return '未找到上传的文件', 400
    except Exception as e:
        print('处理请求时发生异常：', e)
        return jsonify({'error': '处理请求时发生异常'}),600
@app.route('/predict_view', methods=['POST'])
def Predict_view():
    try:
        global file_path  # 使用全局变量获取文件地址
        if file_path is None:
            return jsonify({'error': '文件地址为空，请先上传文件'}), 400
        # 使用 chardet 检测文件编码
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        # 输出检测结果
        print(result['encoding'])
        # 使用检测结果的编码方式读取文件
        feature_columns = ['个人编码','res']
        df = pd.read_csv(file_path, encoding=result['encoding'], usecols=feature_columns)
        # 读取上传的文件内容并转换为模型输入格式（假设为CSV文件）
        # 获取前八行数据并返回
        first_eight_rows = df.head(8).to_dict(orient='records')
        return jsonify({'first_eight_rows': first_eight_rows})
    except Exception as e:
        print('处理获取前八行数据请求时发生异常：', e)
        return jsonify({'error': '处理获取前八行数据请求时发生异常'}), 500

# 路由处理文件下载请求
@app.route('/download-file', methods=['GET'])
def download_file():
    global file_path  # 声明file_path为全局变量
    file_name = basename(file_path)  # 提取文件名
    try:
        if file_path is not None and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_content = base64.b64encode(f.read()).decode('utf-8')
            return jsonify({'file_name': file_name, 'file_content': file_content})
        else:
            return jsonify({'error': '文件不存在或未设置文件路径'}), 404
    except Exception as e:
        print('处理下载请求时发生异常：', e)
        return jsonify({'error': '处理下载请求时发生异常'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)