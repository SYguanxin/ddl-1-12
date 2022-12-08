import requests
import re
import os
import pymysql
from lxml import html
from bs4 import BeautifulSoup
etree = html.etree
parser = etree.HTMLParser(encoding='utf-8')
if __name__ == "__main__":
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='csm.zhinai.123',
                         database='fzu')
    cursor = db.cursor()
    cursor.execute('drop table if exists _fzu')
    sql = """create table _fzu(
             name char(10) NOT NULL,
             TITLE char(100),
             DAY char(10),
             URL char(100),
             html LONGTEXT,
             fj_names TEXT,
             fj_times char(20),
             fj_htmls TEXT)"""
    cursor.execute(sql)


    if not os.path.exists('./fjlib'):
        os.mkdir('./fjlib')


    #提取首页及剩下4页的信息，详细页url
    url = 'https://jwch.fzu.edu.cn/jxtz.htm'
    response = requests.get(url=url)
    response.encoding = response.apparent_encoding
    response = response.text
    soup = BeautifulSoup(response,'lxml')
    htm_list = re.findall("info/\d*/\d*.htm",response)
    time_list = re.findall(">.*?(\d{4}-\d{2}-\d{2}).*?</span>",response,re.S)
    name_list = re.findall("【(.*?)】",response,re.S)
    title_list = []
    soup_list = soup.select('body > .page .list-gl > li > a')
    for i in soup_list:
        title_list.append(i['title'])
    # 提取总页数
    tree = etree.HTML(response, parser=parser)
    page_NUM = \
    tree.xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/span[1]/span[9]/a/text()')[0]

    url2 = 'https://jwch.fzu.edu.cn/'
    url_list=[]
    for i in range(174,170,-1):
        url = "https://jwch.fzu.edu.cn/jxtz/"+str(i)+".htm"
        response = requests.get(url=url)
        response.encoding = response.apparent_encoding
        response = response.text
        soup = BeautifulSoup(response, 'lxml')

        time_list = time_list + re.findall('>.*?(\d{4}-\d{2}-\d{2}).*?</span>', response,re.S)
        htm_list = htm_list + re.findall("info/\d*/\d*.htm", response,re.S)
        name_list = name_list + re.findall("【(.*?)】", response, re.S)
        soup_list = soup.select('body > .page .list-gl > li > a')
        for i in soup_list:
            title_list.append(i['title'])

    # 提取详情页url
    for htm in htm_list:
        url_list.append(f"{url2}{htm}")

    notice_list = []
    for i in range(100):
        notice = {
            'name':name_list[i],
            'title':title_list[i],
            'time':time_list[i],
            'html':url_list[i],
        }
        notice_list.append(notice)



    #提取详情页及附件
    fj_list = []
    htm_list = []
    for i in range(len(url_list)):
        url = url_list[i]
        response = requests.get(url=url)
        response.encoding=response.apparent_encoding
        htm_list.append(response.text)
        tree = etree.HTML(response.text,parser=parser)
        li_list = tree.xpath('//ul[@style="list-style-type:none;"]/li')
        _fj = []
        if li_list != []:
            for li in li_list:
                fj = {
                    'name':li.xpath('./a/text()')[0],
                    'time':'',
                    'html':'https://jwch.fzu.edu.cn' + li.xpath('./a/@href')[0],
                }
                fj_url = 'https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp'
                params = {
                    'wbnewsid': re.findall("wbfileid=(\d*)",str(fj['html']),re.S)[0],
                    'owner': re.findall("owner=(\d*)",str(fj['html']),re.S)[0],
                    'type': 'wbnewsfile',
                    'randomid': 'nattach'
                }
                fj_rps = requests.get(url=fj_url,params=params).text
                fj['time'] = re.findall('\"wbshowtimes\":(\d*)',fj_rps,re.S)[0]
                _fj.append(fj)
                fj_rps = requests.get(url=fj['html']).content
                with open('./fjlib/' + fj['name'], 'wb') as fp:
                    fp.write(fj_rps)
            fj_list = fj_list + _fj
            notice_list[i]['fj'] = _fj


    #最后存入数据库
    val = []
    for i in range(100):
        name = notice_list[i]['name']
        title = notice_list[i]['title']
        time = notice_list[i]['time']
        url = notice_list[i]['html']
        htm = htm_list[i]
        fj = ''
        fj_names = ''
        fj_times = ''
        fj_htmls = ''
        if 'fj' in notice_list[i].keys():
            fj = notice_list[i]['fj']
            fj_names = fj[0]['name']
            fj_times = fj[0]['time']
            fj_htmls = fj[0]['html']
            for i in range(1,len(fj)):
                fj_names = fj_names + ';' + fj[i]['name']
                fj_times = fj_times + ';' + fj[i]['time']
                fj_htmls = fj_htmls + ';' + fj[i]['html']
        val = val + [(name, title, time, url, htm, fj_names, fj_times, fj_htmls)]
    sql = """insert into _fzu(name,TITLE,DAY,URL,html,fj_names,fj_times,fj_htmls)\
             VALUES (%s, %s,  %s,  %s,  %s,  %s,  %s,  %s)"""
    try:
        cursor.executemany(sql,val)
        db.commit()
    except:
        db.rollback()


    print('总页数为:', page_NUM)

    # 本地导出为excel(需要自己加列名)
    sql = 'select name,TITLE,DAY,URL,fj_names,fj_times,fj_htmls from _fzu into outfile "C://python/fzu.csv"'
    cursor.execute(sql)
    db.close()