from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import joblib
import pandas as pd
import numpy as np
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
        return joblib.load(path)
model = joblib.load("model/my_model.dat")
app = Flask(__name__)
CORS(app)  # 允许跨域请求
# 上传文件保存的目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/data', methods=['POST'])
def handle_data():#修改成三个数据
    try:
        # if 'files' in request.files:
            # 获取上传的文件数据
        print('loading')
        file = request.files['files']
        # 处理文件数据，例如保存到本地或者进行其他操作

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # 读取上传的文件内容并转换为模型输入格式（假设为CSV文件）
        df = pd.read_csv(file_path, encoding='gbk')
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

if __name__ == '__main__':
    app.run(debug=True, port=8081)