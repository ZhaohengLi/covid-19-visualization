#coding: utf8

import sys
sys.path.append('..')

import os
import src.libs.platform_version
import json
from flask import Flask, request, Response, current_app, g, render_template, redirect, make_response
from flask_cors import CORS
from src.config import Config as C
# from src.common.key import KEY
from src.libs.log import L
from src.common.response import NormalResponseJson, NormalResponse, ErrorResponse, ErrorResponseJson, ErrorResponseData

import src.data_china as DC
import src.data_pos as DP
import json

app = Flask(__name__, static_url_path='')
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'AreUOK'
app.config['TOKEN_EXPIRATION'] = 86400
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/static/upload/"
FILE_PATH = os.path.dirname(__file__) + "/"

count_file = "./logs/count.txt"
rumor_user_file = "./logs/rumor_user.json"

def read_count():
    with open(count_file, 'r') as file:
        return int(file.read().strip())


def add_count():
    old = read_count()
    with open(count_file, 'w') as file:
        file.write(str(old+1))


@app.route('/getCount')
def get_count():
    data = dict()
    data['count'] = read_count()
    return str(data)


@app.route('/')
def index():
    add_count()
    return "Welcome..."


@app.route('/test')
def test(r):
    R = request.form if request.method=='POST' else request.args
    status = R.get('status', '')
    if status=='': return ErrorResponseJson("请求的参数有误！")
    return NormalResponseJson(request, {'status': status}) 

@app.route('/getDataSummary')
def get_data_summary():
    add_count()
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '86')
    if code == 'china' or code == '': code = '86'
    
    data = DC.get_data_summary(level, code)
    return NormalResponseJson(request, data)

@app.route('/getDataDetails')
def get_data_details():
    add_count()
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '')
    
    data = DC.get_data_latest(level, code)
    return NormalResponseJson(request, data)

@app.route('/getTimeData')
def get_time_data():
    add_count()
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '86')
    if code == 'china' or code == '': code = '86'
    
    data = DC.get_time_data(level, int(code))
    return NormalResponseJson(request, data)

@app.route('/getNewsData')
def get_news_data():
    add_count()
    R = request.args
    province = R.get('province', None)
    keyword = R.get('keyword', None)
    date = R.get('pubDate', None)
    page = R.get('page', None)
    num = R.get('num', None)
    data, length = DC.get_news_data(province, keyword, date, page, num)
    return NormalResponseJson(request, data, length)

@app.route('/getRumorData')
def get_rumor_data():
    add_count()
    R = request.args
    keyword = R.get('keyword', None)
    type = R.get('rumorType', None)
    page = R.get('page', None)
    num = R.get('num', None)
    data, length = DC.get_rumor_data(keyword, type, page, num)
    return NormalResponseJson(request, data, length)

@app.route('/testRumor')
def test_rumor_data():
    add_count()
    R = request.args
    sentence = R.get('sentence', None)
    if not sentence:
        return ErrorResponseJson("参数不正确")
    data = DC.test_rumor(sentence)

    rumor_user_list = read_rumor_user()
    had = False
    for i in rumor_user_list:
        if sentence == i["info"]:
            had = True
            break
    if not had:
        item = dict()
        item["id"] = len(rumor_user_list)
        item["info"] = sentence
        item["url"] = ""
        rumor_user_list.append(item)
        write_rumor_user(rumor_user_list)

    return NormalResponseJson(request, data)


@app.route('/getTopic')
def get_topic():
    add_count()
    R = request.args
    date = R.get('date', None)
    data = DC.get_topic(date)
    return NormalResponseJson(request, data, len(data))


# @app.route('/testNewsData')
# def test_news_data():
#     pass
#     data = DC.get_news_data_example()
#     return NormalResponseJson(request, data)
#
# @app.route('/testRumorData')
# def test_rumor_data():
#     data = DC.get_rumor_data_example()
#     return NormalResponseJson(request, data)

@app.route('/getInfoUser', methods=['POST', 'GET'])
def get_rumor_user():
    add_count()
    if request.method == 'POST':
        R = request.form
        id = R.get("id", None)
        url = R.get("url", None)
        if id and url:
            rumor_user_list = read_rumor_user()
            if int(id) < len(rumor_user_list):
                rumor_user_list[int(id)]["url"] = url
                write_rumor_user(rumor_user_list)
                return NormalResponseJson(request, rumor_user_list[int(id)])
        else:
            return ErrorResponseJson()

    if request.method == "GET":
        rumor_user_list = read_rumor_user()
        return NormalResponseJson(request, rumor_user_list)


def read_rumor_user():
    with open(rumor_user_file, 'r') as file:
        rumor_user_list = json.load(file)
        return rumor_user_list


def write_rumor_user(rumor_user_list):
    with open(rumor_user_file, 'w') as file:
        json.dump(rumor_user_list, file)


@app.route('/getDataPos')
def get_data_pos():
    add_count()
    R = request.form if request.method=='POST' else request.args
    code = R.get('code', '420000')
    
    data = DP.get_region_data(int(code))
    return NormalResponseJson(request, data)


@app.route('/getMap')
def get_map():
    R = request.form if request.method=='POST' else request.args
    name = R.get('id', '')
    path = FILE_PATH + "/data/geojson/{}.json".format(name)
    if not os.path.exists(path):
        return ErrorResponseJson("地图文件不存在")
    
    with open(path, encoding='utf8') as fp:
        data = ''.join(fp.readlines())
        return NormalResponseJson(request, data)

    
    
if __name__ == '__main__':
    L.info("Server Start...")
    app.run(host="0.0.0.0",port=C.web.PORT, debug=True)

