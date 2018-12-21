import json
import os
import re
from _md5 import md5
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests import RequestException
import pymongo
from config import *

#创建mongodb客户端
from jiepai.config import MONGO_URL, MONGO_DB

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,

    }

    #urlencode(data)能把字典等数据转换成 URL query string（url请求参数）
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错',url)
        return None

def parse_page_detail(detail_html,url):
    soup = BeautifulSoup(detail_html,'lxml')
    #打印街拍美女详情页的标题
    title = soup.select('title')[0].get_text()
    print(title)

    images_pattern = re.compile('gallery: JSON\.parse\("(.*?)"\),',re.S)
    gallery = re.search(images_pattern,detail_html)

    if gallery:
        gallery = gallery.group(1)
        result = re.sub(r'\\', '', gallery)
        #print(result)
        data = json.loads(result)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            #sub_images 是一个列表，列表里面嵌套了字典，item表示一个一个的字典，
            # 最终结果表示获取到一个一个的图片url，images表示图片url列表
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            #返回一个字典
            '''return {
                'title': title,
                'url': url,
                'images': images
            }'''

def download_image(url):
    print('正在下载',url)
    try:
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            #response.content返回二进制内容
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片页出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('保存到mongodb成功！',result)
        return True
    return False

def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        print(url)

        detail_html = get_page_detail(url)
        #print(detail_html)

        if detail_html:
            result = parse_page_detail(detail_html,url)
            save_to_mongo(result)


if __name__ == '__main__':
    main()