from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import pymongo

from taobao_foodspider.config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def search():
    try:
        browser.get('https://www.jd.com')
        # 输入搜索的内容
        input = wait.until(
            #  "#q"  是京东搜索框的css选择器
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        # 根据搜索框内的内容进行搜索
        submit = wait.until(
            #  "#J_TSearchForm > div.search-button > button"  是京东首页搜索按钮的css选择器
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#search > div > div.form > button > i"))
        )

        input.send_keys(KEYWORD)
        # 点击搜索
        submit.click()

        total = wait.until(
            # 美食搜索页面的总页数
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b"))
        )
        # 美食搜索页面加载出来第一页后，获取该页的商品
        get_products()
        return total.text

    except TimeoutException:
        return search()

def next_page(page_number):

    try:
        input = wait.until(
            # 跳转页面的输入框
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input"))
        )

        submit = wait.until(
            #  跳转页面的确定按钮
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a"))
        )
        # 清空跳转页面输入框的内容
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#J_bottomPage > span.p-num > a.curr"),str(page_number))
        )

        # 获取每页的商品
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    # 浏览器等待，直到函数里面的内容执行正确
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"#J_goodsList .gl-warp .gl-item"))
    )
    # 获取浏览器当前内容的源代码
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-warp .gl-item').items()
    for item in items:
        # 输出一个字典形式
        #print(item)
        product = {
            # 图片地址在别的地方都能测试出来，不知道在这个程序中搜索不出来？问题没有解决
            'image':item.find('.p-img a img').attr('src'),
            'price':item.find('.p-price').text().replace('\n',''),
            'title':item.find('.p-name p-name-type-2').text(),
            'shop':item.find('.J_im_icon').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功！',result)
    except Exception:
        print('存储到MONGODB失败！',result)

def main():
    try:
        total = search()
        for i in range(2,int(total)+1):
            next_page(i)

    except Exception:
        print('出错了！！！')
    # finally 块保证最后浏览器关闭
    finally:
        browser.close()

if __name__ == '__main__':
    main()
