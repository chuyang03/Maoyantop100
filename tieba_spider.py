import requests
from requests.exceptions import RequestException


def get_one_page(url):
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
        return None


def main():
    url = 'https://tieba.baidu.com/p/3598419649#!/l/p1'
    html = get_one_page(url)
    print(html)


if __name__ == '__main__':
    main()
