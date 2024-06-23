import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    def __init__(self, df, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.plot(df)

    def plot(self, df):
        df['DateTime'] = pd.to_datetime(df['DateTime'])  # Ensure DateTime is in datetime format
        self.axes.plot(df['DateTime'], df['Close'], marker='o', linestyle='-')
        self.axes.set_title('Close Price Over Time')
        self.axes.set_xlabel('DateTime')
        self.axes.set_ylabel('Close Price')
        self.axes.grid(True)

class MyWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle('Close Price Over Time')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.canvas = MyMplCanvas(df, self, width=8, height=6, dpi=100)
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)