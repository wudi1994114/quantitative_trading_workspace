import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
"""
    用来展示实时价格的折线图
"""
class RealtimePriceCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        super().__init__(fig)

class RealtimePricePlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = RealtimePriceCanvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, df):
        self.canvas.ax.clear()
        self.canvas.ax.plot(pd.to_datetime(df['DateTime']), df['Close'])
        self.canvas.ax.set_xlabel('DateTime')
        self.canvas.ax.set_ylabel('Close')
        self.canvas.ax.set_title('Close Prices Over Time')
        self.canvas.draw()