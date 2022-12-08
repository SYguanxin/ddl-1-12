import requests
import re
import pymysql
import json
from lxml import html
etree=html.etree
parser = etree.HTMLParser(encoding='utf-8')
if __name__ == '__main__':

    def dayinmonth(month):
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 28

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='csm.zhinai.123',
                         database='fzu')
    cursor = db.cursor()
    cursor.execute('drop table if exists baidu')
    sql = """create table baidu(
             year char(10),
             type char(50),
             title char(50),
             descs TEXT)"""

    cursor.execute(sql)

    headers = {
        'cookie':'BAIDUID=C337DB3BC80E02C90BFDA9B50D322C59:FG=1; BIDUPSID=C337DB3BC80E02C90BFDA9B50D322C59; PSTM=1656482507; BDUSS=kJiTWE1Tm9VaXpJMVZ5Y0xyflowaktJR1kydlpBWFB3THp0OHpOOWo1Y2ZaaHRqRVFBQUFBJCQAAAAAAAAAAAEAAAAskS1zYnVfeGlhbzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB~Z82If2fNiW; BDUSS_BFESS=kJiTWE1Tm9VaXpJMVZ5Y0xyflowaktJR1kydlpBWFB3THp0OHpOOWo1Y2ZaaHRqRVFBQUFBJCQAAAAAAAAAAAEAAAAskS1zYnVfeGlhbzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB~Z82If2fNiW; FPTOKEN=30$UizlWf6VzHP/sO/FQYPfzoa7Il8PkI2yHz7UEz8rz0iYBZm4ZfS8oN3vOncft/FxGLRKIY0rFJke2aZ0g7lgD1sJn1HECpQKWlEQStrAkIMs3GxO9rzzG4IZg9p9+gXsWFgEs/+/JbRUSFvgkkYPNPLiMzdVs3IOJn3dzymnuxSFmxXbfxyxdSewKEaIaM9/mJXg6kRyTUFRnjZx/cdXU5HAW03nniwMM3jHUlj2QqOc8bOqW5VNVpFN1HRp86/NY4wTeAgd+Wo4q0XOwyrJDSn9SSx0CyYwUodXw+ToFDBgK6CIqgjeKuJbNm3zQADuBzHg/tbelW3ICn5Uz2z+Jo+aJ/NzSVEkrp+4I9LVr1BNm0WEhm9PBv1truGN6/Pi|ueTzLEoVSQdCfnN/Vaas1kW8Cyvmup/F1l0aFUuTEh8=|10|e883585b60fc26d3d4fcaeba9141e7dd; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1666535351,1666797843,1667364817,1667787946; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; ZFY=:BRcJmNsoB2rNEIVn8lwy861zoPmV36tBbBsFZXDZiD0:C; BAIDUID_BFESS=C337DB3BC80E02C90BFDA9B50D322C59:FG=1; __bid_n=18438d5f7fe9c295a04207; baikeVisitId=39231ec1-e92a-4e5e-a506-b14c0f5006f7; ab_sr=1.0.1_OWVjZjRlYTJhNzYzMWI5NDE0NzhhYzEyYTk0ODg2ODBmODYzNmQ4NmZlNTg1MWMxOGU0ZmI5ZmUyMmVmNmQ3NzRmNjAyNmFiMTg5ZjRjNzk2MDBjYTdhOTdjMzVjZTFiMTkwMGNkMzYxY2NlYWRmMWRkNzI0NmMzMDE5MTk4YzNkZWU5ODk4M2Q0MDc3ODUzYWZmOTQ4ZjEyMTI5ZmUzYWY1YTk0YjUxOTkzY2YzM2FjZTcwOWMyMjdjYzc5MjQz',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }


    val = []
    for month in range(1, 13):  # 月份
        url = 'https://baike.baidu.com/cms/home/eventsOnHistory/' + str(month).zfill(2) + '.json'
        rps = requests.get(url=url,headers=headers)
        rps.encoding = 'utf-8'
        rps = rps.text
        rps = json.loads(rps)
        rps = rps[str(month).zfill(2)]
        for day in range(1,dayinmonth(month)+1):
            for j in range(len(rps[str(month).zfill(2) + str(day).zfill(2)])):  # 第month月第day天的第j个事件
                event_j = rps[str(month).zfill(2) + str(day).zfill(2)][j]
                event = {}
                tree = etree.HTML(event_j['title'], parser=parser)
                title = ''
                for k in tree.xpath('//text()'):
                    title += k
                if event_j['desc'] != '':
                    tree = etree.HTML(event_j['desc'], parser=parser)
                    desc = ''
                    for k in tree.xpath('//text()'):
                        desc += k
                event['year'] = re.sub('[\n \t\[\]\(\)]', '', event_j['year']+'/'+str(month)+'/'+str(day))
                event['title'] = re.sub('[\n \t\[\]\(\)]', '', title)  # 删除无用符号
                event['type'] = re.sub('[\n \t\[\]\(\)]', '', event_j['type'])
                event['desc'] = re.sub('[\n \t\[\]\(\)]', '', desc)
                print(event)
                val += [(event['year'], event['title'], event['type'], event['desc'])]

    sql = """insert into baidu(year, type, title, descs)
             values(%s,  %s,  %s,  %s)"""

    cursor.executemany(sql, val)
    db.commit()

    db.close()