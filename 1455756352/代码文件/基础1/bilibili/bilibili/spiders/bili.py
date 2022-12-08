import scrapy
import re
import time
from urllib.parse import urlencode
from bilibili.items import BilibiliItem, AssessItem

class BiliSpider(scrapy.Spider):
    name = 'bili'
    BV = 'BV1o84y1C7c5'
    aid = ''
    url1 = ''
    # allowed_domains = ['www.bilibili.com']
    start_urls = ['https://www.bilibili.com/video/'+BV+'/?spm_id_from=333.999.0.0&vd_source=10e062689830f4f8064af3674e7fbc63']

    # 时间戳转化
    def time_change(self,ctime):
        ctime = time.localtime(ctime)
        return time.strftime("%Y-%m-%d %H:%M:%S", ctime)

    # 评论数据提取
    def sub_assess(self, assess_detail):
        member = assess_detail['member']['uname']
        content = assess_detail['content']['message']
        content = re.sub('[\n\t]', '', content)
        _time = self.time_change(assess_detail['ctime'])
        like = assess_detail['like']
        assess_dir = {
            'name': member,
            'content': content,
            'assess_time': _time,
            'like': like
        }
        return assess_dir

    # 子评论处理
    def parse_sub_assess(self, response):
        assess = response.json()
        assess = assess['data']
        replies_list = assess['replies']
        if replies_list == None:
            return
        for reply in replies_list:
            item = AssessItem(self.sub_assess(reply))
            item['sub'] = True
            yield item

    def parse_assess_first(self, response):
        assess = response.json()
        assess = assess['data']
        item = response.meta['item']
        assess_num = assess['cursor']['all_count']
        item['QWE_as']['评论（A）'] = assess_num
        yield item
        # 提取置顶评论
        top = assess['top_replies'][0]
        item = AssessItem(self.sub_assess(top))
        item['sub'] = False
        yield item
        root = top['rpid']
        sub_assess_num = top['count']
        if sub_assess_num == 0:
            return
        for i in range(1, (sub_assess_num + 9) // 10 + 1):
            params = {
                'csrf': '2d86dcb1d9f38f5cc5396f655eea972e',
                'oid': self.aid,
                'pn': i,
                'ps': 10,
                'root': root,
                'type': 1
            }
            url = 'https://api.bilibili.com/x/v2/reply/reply?' + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_sub_assess)

    def parse_assess(self, response):
        assess = response.json()
        assess = assess['data']
        if assess['replies'] == []:
            return
        next_num = assess['cursor']['next']
        yield scrapy.Request(self.url1 + str(next_num), callback=self.parse_assess)
        replies_list = assess['replies']
        for k in range(len(replies_list)):
            reply = replies_list[k]
            item = AssessItem(self.sub_assess(reply))
            item['sub'] = False
            yield item
            # 子评论爬取
            root = reply['rpid']
            sub_assess_num = reply['count']
            if sub_assess_num == 0:
                continue
            for i in range(1,(sub_assess_num+9)//10 + 1):
                params = {
                    'csrf': '2d86dcb1d9f38f5cc5396f655eea972e',
                    'oid': self.aid,
                    'pn': i,
                    'ps': 10,
                    'root': root,
                    'type': 1
                }
                url = 'https://api.bilibili.com/x/v2/reply/reply?' + urlencode(params)
                yield scrapy.Request(url, callback=self.parse_sub_assess)


    def parse(self, response):
        # 点赞，投币，收藏
        QWE_dir = {}
        QWE_list = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span')
        for i in range(len(QWE_list)-1):
            QWE = QWE_list[i]
            QWE_name = QWE.xpath('./@title').extract_first()
            QWE_num = QWE.xpath('./span/text()').extract_first()
            QWE_dir[QWE_name] = eval(QWE_num)
        item = BilibiliItem()
        item['QWE_as'] = QWE_dir
        # 用bv号提取av号
        ex = '"aid":(\d*),"bvid":"'+self.BV+'"'
        self.aid = re.findall(ex, response.text)[0]
        next_num = 0
        params = {
            'csrf': '2d86dcb1d9f38f5cc5396f655eea972e',
            'mode': 3,
            'oid': self.aid,
            'plat': 1,
            'seek_rpid': '',
            'type': 1
        }
        # 第一次提取评论总数和置顶评论
        url = 'https://api.bilibili.com/x/v2/reply/main?'
        url = url + urlencode(params) + '&next='
        self.url1 = url
        yield scrapy.Request(url+str(next_num), callback=self.parse_assess_first, meta={'item': item})
        yield scrapy.Request(url+str(next_num+1), callback=self.parse_assess)