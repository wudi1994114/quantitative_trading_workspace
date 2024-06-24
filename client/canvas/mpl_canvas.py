import traceback
import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator, FuncFormatter
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import font_manager

"""
    用来展示实时价格的折线图
"""
class RealtimePriceCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        # 设置全局字体为苹方字体
        font_path = 'config/PingFang.ttc'

        # 添加字体路径
        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)

        plt.rcParams['font.family'] = prop.get_name()

class RealtimePricePlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = RealtimePriceCanvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, df, stock):
        try:
            self.canvas.ax.clear()
            
            # 确保 DateTime 是日期时间格式
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            
            # 绘制折线图
            self.canvas.ax.plot(df['DateTime'], df['Close'], label='price-rmb')
            self.canvas.ax.set_xlabel('DateTime')
            self.canvas.ax.set_ylabel('Close Price')
            self.canvas.ax.set_title(f'{stock.stock_name}')
            
            # 计算y轴的最小值和最大值
            ymin, ymax = float(df['Close'].min()), float(df['Close'].max())
            
            # 设置y轴的范围并添加一些余量以便更好地可视化
            self.canvas.ax.set_ylim(ymin * 0.9, ymax * 1.1)
            
            print(f"Y轴范围: {ymin}, {ymax}")

            # 使用MaxNLocator设置y轴的刻度
            self.canvas.ax.yaxis.set_major_locator(MaxNLocator(nbins=10))

            # 格式化y轴标签
            self.canvas.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))

            # 设置x轴范围以显示所有数据点
            self.canvas.ax.set_xlim([df['DateTime'].min(), df['DateTime'].max()])

            # 格式化x轴以仅显示小时和分钟
            self.canvas.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.canvas.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            # 旋转x轴标签以便更好地阅读
            self.canvas.ax.tick_params(axis='x', rotation=45)

            self.canvas.ax.legend()
            self.canvas.draw()
        except Exception as e:
            traceback.print_exc()

 