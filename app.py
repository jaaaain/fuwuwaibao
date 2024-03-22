from flask import Flask, request, jsonify,render_template, send_file
from flask_cors import CORS
from os.path import basename
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import os
import torch
import joblib
import pandas as pd
import numpy as np
import chardet
import base64
import torch.nn.functional as F
#模型函数定义
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
        return joblib.load(path)#特殊的模型处理#

class BPNetModel(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(BPNetModel, self).__init__()
        self.hidden_1 = torch.nn.Linear(n_feature, n_hidden[0])  # 定义隐层网络
        self.hidden_2 = torch.nn.Linear(n_hidden[0], n_hidden[1])
        self.out = torch.nn.Linear(n_hidden[1], n_output)  # 定义输出层网络

    def forward(self, x):
        relu_1 = torch.nn.ReLU()
        x = relu_1(self.hidden_1(x))  # 隐层激活函数采用ReLu函数
        relu_2 = torch.nn.ReLU()
        x = relu_2(self.hidden_2(x))
        out = self.out(x)
        return out

def risk(net_model,X):
    sclaer = MinMaxScaler()
    X = torch.FloatTensor(sclaer.fit_transform(X))
    tmp = F.softmax(net_model(X),dim=1)
    return sclaer.fit_transform(tmp[:,1].detach().numpy().reshape(-1,1))
#读取模型
model = joblib.load("model/my_model.dat")
net_model=torch.load("model/my_net.pth")
app = Flask(__name__)

CORS(app)  # 允许跨域请求
# 上传文件保存的目录
UPLOAD_FOLDER = 'uploads'
SUM_FOLDER='sum'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(SUM_FOLDER):
    os.makedirs(SUM_FOLDER)#创建放置总体文件的
# 全局变量保存文件地址
file_path = None
# 定义CSV文件名和路径
sum_filename = 'sum.csv'
sum_path = os.path.join(SUM_FOLDER, sum_filename)
#e 定义模版文件名和路径
exa_filename = 'example.csv'
exa_path=os.path.join(SUM_FOLDER, exa_filename)
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
        # 备份原始数据集
        df_temper = df.copy()

        #特征处理
        df_temper['月就诊天数_SUM'] = df_temper['月就诊天数_AVG'] * df_temper['就诊的月数']
        #df_temper['max占最大月的百分比'] = df_temper['月统筹金额_MAX'] /df_temper['统筹支付金额_SUM']
        df_temper = df_temper.fillna(0)

        # 提取特征列
        X = df_temper[['月统筹金额_MAX','本次审批金额_SUM','ALL_SUM','月就诊次数_MAX','月就诊天数_SUM']]
        # 进行预测
        predictions = model.predict(X)
        # 将预测结果添加到原始文件中
        df['RES'] = predictions
        # 二次读取
        df = pd.read_csv(file_path, encoding=result['encoding'])
        #风险预测
        X = df_temper[['月统筹金额_MAX', '本次审批金额_SUM', 'ALL_SUM', '月就诊次数_MAX', '月就诊天数_SUM','RES']]
        new_X = X[X['RES'] == 0].drop(['RES'], axis=1)
        predictions_risk=risk(net_model,new_X)
        # 使用 numpy.round() 对概率值进行四舍五入到四位小数
        predictions_risk= np.round(predictions_risk, decimals=4)
        # 使用条件索引将预测结果赋值给 'risk' 列
        df.loc[df['RES'] == 0, 'risk'] = predictions_risk
        # 对 'RES' 列值为 1 的行，在 'RISK' 列中填充 1
        df.loc[df['RES'] == 1, 'risk'] = 1
        # 保存带有预测结果的文件
        df.to_csv(file_path, index=False)
        # 将新数据追加到现有CSV文件中，从空行开始存入数据
        with open(sum_path, 'a', newline='') as f:
            df.to_csv(f, index=False, header=False)
        return jsonify({'message': 'File uploaded successfully'})
        # else:
        #     return '未找到上传的文件', 400
    except Exception as e:
        print('处理请求时发生异常：', e)
        return jsonify({'error': '处理请求时发生异常'}),600
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
        return jsonify({'error': '处理下载请求时发生异常'}), 504
@app.route('/download', methods=['GET'])
def download_example():
    file_path = exa_path
    file_name = basename(file_path)  # 提取文件名
    try:
        if file_path is not None and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_content = base64.b64encode(f.read()).decode('utf-8')
            return jsonify({'file_name': file_name, 'file_content': file_content})
        else:
            return jsonify({'error': '文件不存在或未设置文件路径'}), 405
    except Exception as e:
        print('处理下载请求时发生异常：', e)
        return jsonify({'error': '处理下载请求时发生异常'}), 505
@app.route('/result', methods=['get'])
def get_result():
    try:
        global file_path  # 使用全局变量获取文件地址
        if file_path is None:
            return jsonify({'error': '文件地址为空，请先上传文件'}), 401
        # 使用检测结果的编码方式读取文件
        feature_columns = ['个人编码','RES','本次审批金额_SUM','risk']
        df = pd.read_csv(file_path, encoding='utf-8',usecols=feature_columns)
        sum_result = df.to_dict(orient='records')
        # 读取上传的文件内容并转换为模型输入格式（假设为CSV文件）
        return jsonify({'sum_result': sum_result})
    except Exception as e:
        print('处理获取详细数据请求时发生异常：', e)
        return jsonify({'error': '处理获取详细数据请求时发生异常'}), 501

if __name__ == '__main__':
    app.run(debug=True, port=5000)