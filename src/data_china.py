#coding: utf8
'''
Created on 2020年2月4日
'''
import sys
from jieba.analyse import textrank
sys.path.append('..')

from src.libs.database import Database
from src.data.region import src_province
from src.libs.utils import date_less
from src.rumor.run import is_rumor
'''
    地图数据统一格式：
    [code, value, name, ...]
'''
def get_data_latest(level = 1, code=86):
    db = Database()
    whr = "" if level == 1 else " and region_parent={}".format(code)
    sql = '''select a.region_code, region_name, numb_confirmed, numb_suspected, numb_die, numb_ok, 
            a.data_date from patients a 
        join (SELECT region_code, max(data_date) as tm FROM patients 
            where region_level={}'''.format(level) + whr + ''' 
            group by region_code) b 
            on a.region_code=b.region_code and a.data_date=b.tm'''
    lines = []
    for (code, name, confirmed, suspected, die, ok, tm) in db.select(sql):
        lines.append([code, confirmed, name, suspected, die, ok, str(tm)])
        
    return lines

'''
    获取汇总数据：
    最新汇总结果及相对昨日新增的数据
'''
def get_data_summary(level=1, code=86):
    dts = get_time_data(level, code)
    tms = sorted(list(dts.keys()),reverse = True)
    ''' confirmed, suspected, die, ok '''
    sums = [[0, 0, 0, 0], [0, 0, 0, 0]]
    idxs = [1, 3, 4, 5]
    lines = [dts[tms[0]], dts[tms[0 if len(tms) == 1 else 1]] ]
    update_time = None
    for i in range(2):
        for line in lines[i]:
            if i == 0 and line[-1]:
                if not update_time or date_less(update_time, line[-1]): update_time = line[-1] 
            for j in range(4): sums[i][j] += line[idxs[j]]
    for i in range(4): 
        sums[1][i] = sums[0][i] - sums[1][i]
    
    return {"updateTime": update_time, "summary": sums}

def get_news_data(province=None, keyword=None, date=None, page=None, num=None):
    db = Database()

    sql = "select * from news"
    has_where = False

    if province:
        if province == '北京':
            sql += " where summary not like '%北京时间%' and summary like '%北京%'"
        else:
            sql += " where summary like '%{}%'".format(province)
        has_where = True

    if keyword:
        if has_where:
            sql += " and summary like '%{}%'".format(keyword)
        else:
            sql += " where summary like '%{}%'".format(keyword)
            has_where = True

    if date:
        if has_where:
            sql += " and DATE_FORMAT(pubDate, '%Y%m%d') between '{}' and '20210101' order by pubDate asc ".format(date)
        else:
            sql += " where DATE_FORMAT(pubDate, '%Y%m%d') between '{}' and '20210101' order by pubDate asc ".format(date)
            has_where = True
    else:
        sql += " order by pubDate desc"

    news = db.selectDict(sql)

    if page and num and int(page) > 0 and int(num) > 0:
        page = int(page)
        num = int(num)
        return news[(page-1)*num:page*num], len(news)
    else:
        return news[0:10], len(news)

def get_news_data_example():
    db = Database()
    sql = "select * from news limit 0, 20"
    news = db.selectDict(sql)
    return news

def get_rumor_data(keyword=None, type=None, page=None, num=None):
    db = Database()
    sql = "select * from rumor"
    has_where = False

    if keyword:
        if keyword == '北京':
            sql += " where mainSummary not like '%北京时间%' and (mainSummary like '%北京%' or title like '%北京%' or body like '%北京%')"
            has_where = True
        else:
            sql += " where (mainSummary like '%{}%' or title like '%{}%' or body like '%{}%')".format(keyword, keyword, keyword)
            has_where = True

    if type and 0 <= int(type) <= 2:
        if has_where:
            sql += " and rumorType={}".format(type)
        else:
            sql += " where rumorType={}".format(type)
            has_where = True

    rumor = db.selectDict(sql)

    if page and num and int(page) > 0 and int(num) > 0:
        page = int(page)
        num = int(num)
        return rumor[(page - 1) * num:page * num], len(rumor)
    else:
        return rumor[0:10], len(rumor)


def get_topic(date):
    sql = ''
    if date:
        sql = "select date, topic, new, dead from topic where DATE_FORMAT(date, '%Y%m%d') ='{}'".format(date)
    else:
        sql = "select date, topic, new, dead from topic order by date desc"
    db = Database()
    data = db.select(sql)
    return data


def get_rumor_data_example():
    db = Database()
    sql = "select * from rumor limit 0, 20"
    rumor = db.selectDict(sql)
    return rumor


def test_rumor(sentence):
    if not sentence:
        return None
    result = {}
    result['isRumor'] = is_rumor(sentence)
    result['related'] = []
    for keyword, weight in textrank(sentence, topK=3, withWeight=True):
        for line in get_rumor_data(keyword, page=1, num=2)[0]:
            result['related'].append(line)
    return result


'''
Return: {
    '2020-02-09': [code, value, name, ...]
}
注：各地区每天可能有多次数据记录，也可能没有记录
    原思路：查每天各地区的最新数据作为该地区的当天数据
    瑕疵：可能某天某地并没有数据
  TODO:    若当日无数据，应取昨日数据(暂使用代码方式解决)
'''
def get_time_data(level=1, code=86):
    db = Database()
    whr = "" if level == 1 else " and region_parent={}".format(code)
    sql = '''select a.region_code, region_name, numb_confirmed, numb_suspected, numb_die, numb_ok, 
            a.data_date, DATE(tm) from patients a 
        join (SELECT region_code, max(data_date) as tm FROM patients 
            where region_level={}'''.format(level) + whr + ''' 
            group by region_code, DATE(data_date)) b 
            on a.region_code=b.region_code and a.data_date=b.tm order by data_date'''
    dts, latest, yesterday, _yesterday = {}, {}, None, None
    regions = get_regions(code, db)
    
    '''数据检查与填充'''
    def data_fill(date_):
        for p in regions:
            if p['code'] in dts[date_]: continue
            dts[date_][p['code']] = latest.get(p['code'], [p['code'], 0, p['name'], 0, 0, 0, 0, date_])
    for (code, name, confirmed, suspected, die, ok, tm, date_) in db.select(sql):
        date_ = str(date_)
        if date_ not in dts: 
            dts[date_] = {}
            '''昨日数据检查填补，以下四行 '''
            if yesterday: data_fill(yesterday)
            _yesterday = yesterday
            yesterday = date_
        '''新增计算 '''
        '''TODO: 地域判别，code可能不是直属地区'''
        add_c = confirmed - dts[_yesterday][code][1] if _yesterday and code > 0 else confirmed
        '''各地区缓存一份最新数据，用于数据填补''' 
        latest[code] = [code, confirmed, name, suspected, die, ok, add_c, str(tm)] 
        
        dts[date_][code] = latest[code]
    if yesterday: data_fill(yesterday)
 
    return dict((k, list(dts[k].values())) for k in dts)

'''获取下级行政区域列表'''
def get_regions(code=86, db=None):
    if code==86: return src_province
    if not db: db = Database()
    sql = "select code, name from region where parent=%s"
    return [{'name': name, 'code': code} for (code, name) in db.select(sql, (code, ))] 
    
    
    
if __name__ == '__main__':
#     for item in get_data_latest():
#         print(item)
#     for item in get_data_latest(2, "500000"):
#         print(item)
#     print(get_time_data(2, 410000))
    get_data_summary(2, 410000)
#     for item in get_time_data():
#         print(item)
#     for item in get_time_data(2, "500000"):
#         print(item)
    
        
    