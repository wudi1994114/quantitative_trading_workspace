import os
import sys
# 将项目根目录添加到 sys.path 中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from handledata.realtime_callback import RealtimeCallback
from scraping.dynamic_network_cache import WebScraper, URL
from scraping.stock_code import StockCode
from client.canvas.mpl_canvas import * 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.callback_handler = RealtimeCallback(self.plot_widget)

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Control Center')

        self.plot_widget = RealtimePricePlotWidget()
        self.setCentralWidget(self.plot_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    stock = StockCode.sh_603259
    scraper = WebScraper(URL.EAST_MONEY, main_window.callback_handler, area=stock.area, code=stock.code)
    scraper.open_page_and_wait('//div')
    sys.exit(app.exec_())