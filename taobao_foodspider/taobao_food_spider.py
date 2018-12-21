from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def search():
    try:
        browser.get('https://www.taobao.com')
        # 输入搜索的内容
        input = wait.until(
            #  "#q"  是淘宝搜索框的css选择器
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        # 根据搜索框内的内容进行搜索
        submit = wait.until(
            #  "#J_TSearchForm > div.search-button > button"  是淘宝首页搜索按钮的css选择器
            EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button"))
        )

        input.send_keys('美食')
        # 点击搜索
        submit.click()

        total = wait.until(
            #  "#J_TSearchForm > div.search-button > button"  是淘宝首页搜索按钮的css选择器
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        return total.text
    except TimeoutException:
        return search()

def main():
    total = search()
    print(total)

if __name__ == '__main__':
    main()
