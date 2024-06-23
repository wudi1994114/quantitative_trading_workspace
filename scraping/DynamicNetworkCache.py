from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5.QtWidgets import QApplication

from enum import Enum
import sys
import os
# 获取项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)

from handledata.east_stream_check import StreamListener as listener
from handledata.RealtimeCallback import RealtimeCallback as callback
import time


class URL(Enum):
    EAST_MONEY = "http://quote.eastmoney.com/{area}{code}.html"

    def generate_url(self, **kwargs):
        return self.value.format(**kwargs)

class WebScraper:
    def __init__(self, target_url_enum, **url_params):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 开启无头模式
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.target_url = target_url_enum.generate_url(**url_params)
        self.target_url_part = 'push2.eastmoney.com/api/qt/stock/trends2/sse'
        self.driver.request_interceptor = self.request_interceptor
        self.listener = listener(callback())

    def request_interceptor(self, request):
        try:
            if self.target_url_part in request.url:
                print(f"拦截到的URL: {request.url}")
                self.listener.add_url(request.url)
        except Exception as e:
            print(f"Error intercepting request: {e}")    

    def open_page_and_wait(self, xpath, wait_time=20):
        try:
            self.driver.get(self.target_url)
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        finally:
            self.driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scraper = WebScraper(URL.EAST_MONEY, area='sh', code='603259')
    scraper.open_page_and_wait('//div')
    while True:
        time.sleep(10)
        print('still alive...')
