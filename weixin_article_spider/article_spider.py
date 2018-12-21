from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUID=F6177C7B3220910A000000058E4D679; SUV=1491392122762346; ABTEST=1|1491392129|v1; SNUID=0DED8681FBFEB69230E6BF3DFB2F8D6B; ld=OZllllllll2Yi2balllllV06C77lllllWTZgdkllll9lllllxv7ll5@@@@@@@@@@; LSTMV=189%2C31; LCLKINT=1805; weixinIndexVisited=1; SUIR=0DED8681FBFEB69230E6BF3DFB2F8D6B; JSESSIONID=aaa-BcHIDk9xYdr4odFSv; PHPSESSID=afohijek3ju93ab6l0eqeph902; sct=21; IPLOC=CN; ppinf=5|1491580643|1492790243|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQjQlOTQlRTUlQkElODYlRTYlODklOER8Y3J0OjEwOjE0OTE1ODA2NDN8cmVmbmljazoyNzolRTUlQjQlOTQlRTUlQkElODYlRTYlODklOER8dXNlcmlkOjQ0Om85dDJsdUJfZWVYOGRqSjRKN0xhNlBta0RJODRAd2VpeGluLnNvaHUuY29tfA; pprdig=j7ojfJRegMrYrl96LmzUhNq-RujAWyuXT_H3xZba8nNtaj7NKA5d0ORq-yoqedkBg4USxLzmbUMnIVsCUjFciRnHDPJ6TyNrurEdWT_LvHsQIKkygfLJH-U2MJvhwtHuW09enCEzcDAA_GdjwX6_-_fqTJuv9w9Gsw4rF9xfGf4; sgid=; ppmdig=1491580643000000d6ae8b0ebe76bbd1844c993d1ff47cea',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

keyword = '风景'

def get_html(url):
    try:

        response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')

    except ConnectionError as e:
        return get_html(url)

def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print(html)

if __name__ == '__main__':
    main()