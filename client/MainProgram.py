import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        data = np.random.random(100)
        self.ax.plot(data, 'r-')
        self.ax.set_title('Random Data')
        self.draw()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quantitative Analysis Tool')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        plot_canvas = PlotCanvas(self)
        layout.addWidget(plot_canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())