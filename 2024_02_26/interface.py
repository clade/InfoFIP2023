import time
from pyqtgraph.Qt import QtWidgets

class StopWatchWindows(QtWidgets.QWidget):
    def __init__(self, args):
        self.app = QtWidgets.QApplication([])
        QtWidgets.QWidget.__init__(self)
        self.main_layout = main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        
        self.label = QtWidgets.QLabel('Hello')


if __name__ == "__main__":
    main = StopWatchWindows([])
    main.show()
    exit(main.app.exec())

