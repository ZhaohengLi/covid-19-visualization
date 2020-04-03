#coding: utf8
'''
Created on 2020年1月30日
'''

import sys
sys.path.append('..')
sys.path.append('../..')
import json
import time
import traceback
from src.libs.log import L
from urllib import parse
from src.common.tools import request_url
from src.libs.utils import TS2S, date_less
from src.libs.database import Database
from src.data.region_recognition import REGIONS, check_city
from src.data.region import src_province as SP


def test_get_data():
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
    rst = request_url(url)
    rst = json.loads(rst, encoding = "utf8")
    with open("data-all.json", "w", encoding="utf8") as fp:
        json.dump(rst["results"], fp, ensure_ascii = False)


        
def translate(items, p, lines):    
    keys = {'confirmedCount': 'numb_confirmed', 'suspectedCount': 'numb_suspected', 
        'curedCount': 'numb_ok', 'deadCount': 'numb_die', 'comment': 'comment'}
    
    for item in items:
        line = dict((keys[k], item[k]) for k in item if k in keys)
        line['data_date'] = TS2S(item['updateTime'] / 1000.0)
        line['region_code'], line['region_name'] = p['code'], p['name']
        line['sum_type'], line['region_level'], line['region_parent'] = 1, 1, 86
        lines.append(line)
        
        if item.get('cities', None):
            for ct in item['cities']:
                cline = dict((keys[k], ct.get(k, "")) for k in ct if k in keys)
                cline['sum_type'], cline['region_level'] = 1, 2
                cline['region_name'], cline['region_parent'] = ct['cityName'], p['code']
                cline['data_date'] = line['data_date']
                cline['region_code'] = ct.get('locationId', 0)
                '''行政编码和级别判断'''
                if cline['region_code'] not in  REGIONS[p['code']]['children']:
                    cline['region_code'] = check_city(ct['cityName'], p['code'])
                    if not cline['region_code']: cline['region_level'] = 3

                lines.append(cline)
        '''End If'''
    '''End For'''
    
'''为市级区域增加清洗后的行政区域代码'''    
def add_city_code():
    db = Database()
    sql = "select id, region_name, region_parent FROM patients WHERE region_level=2 and region_code=0"
    comands = []
    for (id_, name, parent) in db.select(sql):
        code = check_city(name, parent)
        if not code: 
            print(parent, name, code)
            continue
        sql = "update patients set region_code=%s where id=%s"
        comands.append([sql, (code, id_)])
    db.Transaction(comands)

'''
各地区数据最新时间
前提：历史数据是准确的，不会在后期有改动
'''
def getLatest(db=None):
    if not db: db = Database()
    dt = {}
    sql = '''select region_code, region_name, region_parent, max(data_date) from patients \
        group by region_code, region_name, region_parent'''
    for (code, name, parent, tm) in db.select(sql):
        dt['_'.join([str(code), name, str(parent)])] = tm
        
    return dt    

def request_data(url, name):
    err_count = 0
    while True:
        try:
            rst = request_url(url)
            rst = json.loads(rst, encoding = "utf8")
            return rst
        except Exception as e:
            err_count += 1
            L.info("Error request found when {}, the {} times".format(name, err_count))
            L.info("Due to {}".format(str(e)))
            if err_count > 10: return None
            time.sleep(3)
    return None

'''
    各省核心数据请求，含港澳台地区
        逻辑前提：中国数据等于各省数据之和
'''    
def request_data_province():
    names = {'香港特别行政区': '香港', '澳门特别行政区': '澳门', '台湾省': '台湾'}
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province="
    db = Database()
    history = getLatest(db)
    idx = 0
    for p in SP:
        idx += 1
        # if idx <= 23: continue
        purl = url + parse.quote(names.get(p['name'], p['name']))
        rst = request_data(purl, p['name'])
        if not rst: continue
        data, lines = rst['results'], []
        translate(data, p, lines)
        L.info("Get data collects count:" + str(len(data)))
        
        comands = []
        for line in lines:
            '''排除已有历史数据''' 
            key = '_'.join([str(line['region_code']), line['region_name'], str(line['region_parent'])])
            if key in history and not date_less(history[key], line['data_date']): continue 
            
            ks = line.keys()
            sql = "insert into patients (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
            params = [line[k] for k in ks]
            comands.append([sql, params])
        L.info("New data lines count:" + str(len(comands)))
        if len(comands) > 0: db.Transaction(comands)
        L.info("{}\t {}  finished!".format(idx, p['name']))
        time.sleep(3)


def request_data_time_series():
    needed = {}
    for p in SP:
        if p['name'] == '香港特别行政区':
            needed['香港'] = p
        if p['name'] == '澳门特别行政区':
            needed['澳门'] = p
        if p['name'] == '台湾省':
            needed['台湾'] = p
        needed[p['name']] = p
    
    # url = "https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/json/DXYArea-TimeSeries.json"
    # data = request_data(url, "")
    # if not data:
    #     L.info('Get data from github fialed.')
    #     return

    with open('./json/data_time_series.json', 'r') as file:
        data = json.load(file)

    db = Database()
    history = getLatest(db)
    lines = []
    for province in data:
        if province["provinceName"] in needed:
            p = needed[province["provinceName"]]
            translate([province], p, lines)

    comands = []
    for line in lines:
        '''排除已有历史数据''' 
        key = '_'.join([str(line['region_code']), line['region_name'], str(line['region_parent'])])
        if key in history and not date_less(history[key], line['data_date']):
            continue
        ks = line.keys()
        sql = "insert into patients (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
        params = [line[k] for k in ks]
        comands.append([sql, params])

    L.info("New data lines count:" + str(len(comands)))
    if len(comands) > 0:
        db.Transaction(comands)


def request_news_time_series():
    with open('./json/news_time_series.json', 'r') as file:
        data = json.load(file)

    db = Database()
    update_num = 0
    for line in data:
        key = ['id', 'provinceId', 'title', 'summary', 'infoSource', 'sourceUrl', 'pubDate', 'province']
        data = db.select("select * from news where id={}".format(line['id']))
        if not data:
            update_num += 1
            sql = "insert into news (" + ','.join(key) + ") values (" + ', '.join(['%s' for k in key]) + ")"
            line['pubDate'] = TS2S(line['pubDate'] / 1000.0)
            if line['provinceId'] == "":
                line['provinceId'] = None
            line['summary'] = line['summary'][0:4096]
            if 'province' not in line:
                 line['province'] = None
            params = [line[k] for k in key]
            db.execute(sql, params)
    L.info('Update {} news data.'.format(update_num))

def request_rumor_time_series():
    with open('./json/rumor_time_series.json', 'r') as file:
        data = json.load(file)

    db = Database()
    update_num = 0
    for line in data:
        key = ['id', 'title', 'mainSummary', 'body', 'sourceUrl', 'rumorType', 'crawlTime']
        data = db.select("select * from rumor where id={}".format(line['id']))
        if not data:
            update_num += 1
            sql = "insert into rumor (" + ','.join(key) + ") values (" + ', '.join(['%s' for k in key]) + ")"
            line['crawlTime'] = TS2S(line['crawlTime'] / 1000.0)
            line['mainSummary'] = line['mainSummary'][0:1024]
            line['body'] = line['body'][0:1024]
            params = [line[k] for k in key]
            db.execute(sql, params)
    L.info('Update {} news data.'.format(update_num))



'''暂未使用（本项目当前只关心国内）'''
def request_data_overall():
    url = "https://lab.isaaclin.cn/nCoV/api/overall?latest=0"
    rst = request_data(url, "全国")
    if not rst: return 
    data, lines = rst['results'], []

def request_rumor_data():
    L.info("Collecting rumor data.")
    for i in range(0, 3):
        request_rumor_type_data(i)

def request_rumor_type_data(rumor_type = 0):
    error_times = 0
    db = Database()
    i = 0
    while i < 5:
        i += 1
        L.info("Preparing for type {} page {}".format(str(rumor_type), str(i)))

        time.sleep(3)
        rst = request_data("https://lab.isaaclin.cn/nCoV/api/rumors?num=50&rumorType={}&page={}".format(str(rumor_type), str(i)), str(i))

        if rst['success'] == False:
            if error_times == 10 : break
            error_times += 1
            L.info("This is the {} times fail at getting page {}, will try it again.".format(str(error_times),str(i)))
            i -= 1
            continue
        else:
            error_times = 0

        if not rst['results']:
            L.info("Collecting type {} rumor data finished.".format(rumor_type))
            break

        comands = []
        for line in rst['results']:
            ks = line.keys()
            params = line['title']
            sql = "select * from rumor where title ='{}'".format(params)
            data = db.select(sql)

            if not data:
                sql = "insert into rumor (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
                params = [line[k] for k in ks]
                comands.append([sql, params])
        try:
            db.Transaction(comands)
            L.info("Writing database for {} rumor.".format(str(len(comands))))
        except Exception as e:
            if error_times == 10 : break
            error_times += 1
            L.info("This is the {} times fail at wirting database due to {}, will try this page again.".format(str(error_times), str(e)))
            i -= 1
            continue

    if error_times == 10:
        L.info("Collecting rumor data finished with error.")
    else:
        L.info("Collecting rumor data finished.")


def request_news_data():
    L.info("Collecting news data.")
    error_times = 0
    db = Database()
    url = "https://lab.isaaclin.cn/nCoV/api/news?num=50&page="
    i = 0
    while i < 100:
        i += 1
        L.info("Preparing for page {}".format(str(i)))

        time.sleep(3)
        rst = request_data(url+str(i), str(i))

        if rst['success'] == False:
            if error_times == 10 : break
            error_times += 1
            L.info("This is the {} times fail at getting page {}, will try it again.".format(str(error_times),str(i)))
            i -= 1
            continue
        else:
            error_times = 0

        if not rst['results']:
            L.info("Collecting news data finished.")
            break

        comands = []
        for line in rst['results']:
            ks = line.keys()
            params = line['title']
            sql = "select * from news where title ='{}'".format(params)
            data = db.select(sql)
            if not data:
                sql = "insert into news (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
                params = [line[k] for k in ks]
                comands.append([sql, params])
        try:
            db.Transaction(comands)
            L.info("Writing database for {} news.".format(str(len(comands))))
        except Exception as e:
            if error_times == 10 : break
            error_times += 1
            L.info("This is the {} times fail at wirting database due to {}, will try this page again.".format(str(error_times), str(e)))
            i -= 1
            continue

    if error_times == 10:
        L.info("Collecting news data finished with error.")
    else:
        L.info("Collecting news data finished.")
    
if __name__ == '__main__':
    pass
    # request_data_time_series()
    request_news_time_series()
    # request_rumor_time_series()
    # request_rumor_data()
    # request_news_data()
    # test_get_data()
    # request_data_province()
    # request_data_overall()
    # add_city_code()
