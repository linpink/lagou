import re
import time

import requests

from fake_useragent import UserAgent

ua = UserAgent()


class LaGouSpider:
    # 构造请求头
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.api_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
        self.headers = {
            'User-Agent': ua.random
        }

        self.api_headers = {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'User-Agent': ua.random

        }
        # self.sess = requests.session()
        # 获取cookie

    # 构造请求参数
    def get_params(self, first='false', kd='python', pn='1'):

        form_data = {
            'first': first,
            'pn': pn,
            'kd': kd
        }
        return form_data

    # 获取请求接口数据
    def get_api_data(self, form_data):
        time.sleep(5)
        sess = requests.session()
        sess.headers.update(self.api_headers)
        sess.get(url=self.url)
        response = sess.post(url=self.api_url, data=form_data)
        return response.json()

    # 解析数据
    def parse(self, form_data, position):
        response_json = self.get_api_data(form_data)
        parse_data_lis = response_json['content']['positionResult']['result']
        for data in parse_data_lis:
            lagou_data = []
            # 城市
            lagou_data.append(data['city'])
            # 公司名
            lagou_data.append(data['companyFullName'])
            # 公司规模
            lagou_data.append(data['companySize'])
            # 学历
            lagou_data.append(data['education'])
            # 职位
            lagou_data.append(data['positionName'])
            # 工作性质
            lagou_data.append(data['jobNature'])
            # 工资
            lagou_data.append(data['salary'])
            # 工作年限
            lagou_data.append(data['workYear'])
            print(lagou_data)
            lagou_data_str = "\t".join(lagou_data)
            lagou_data_str = str(lagou_data)
            # lagou_data_str_done =  re.sub("\[|\]|\'", "", lagou_data_str)
            # print(lagou_data_str_done)
            self.save_lagou_data(lagou_data_str, position)

    def write_head(self,position):
        with open(f'{position}拉钩.csv', mode='w', encoding='utf-8', newline='') as fp:
            fp.write("city\tcompanyFullName\tcompanySize\teducation\tpositionName\tjobNature\tsalary\tworkYear" + '\n')

    def save_lagou_data(self, lagou_data_str, position):
        with open(f'{position}拉钩.csv', mode='a', encoding='utf-8', newline='') as fp:
            fp.writelines(lagou_data_str + '\n')

    def main(self, page=5, kd='python'):
        for page in range(page):
            form_data = self.get_params(pn=str(page), kd=kd)
            position = form_data.get('kd')
            self.parse(form_data, position)
            print(f"------正在爬取{page}页的{position}职位的招聘信息----")


if __name__ == '__main__':
    spider = LaGouSpider()
    kd = input("你想爬的职位:")
    pn = int(input('爬的页数:'))
    spider.main(kd=kd, page=pn)
