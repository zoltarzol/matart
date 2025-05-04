import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QToolBar,
    QMenuBar, QSplitter
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("matart – Generative Geometry")

        # 1) Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        help_menu = menu.addMenu("Help")

        # 2) Toolbar for shapes
        toolbar = QToolBar("Shape Tools")
        self.addToolBar(toolbar)
        for shape in ("Square", "Triangle", "Circle", "Diamond", "Polygon"):
            act = QAction(shape, self)
            toolbar.addAction(act)

        # 3) Central splitter: canvas | params
        splitter = QSplitter(Qt.Horizontal)
        # Left: canvas placeholder
        canvas = QWidget()
        canvas.setStyleSheet("background-color: white;")
        splitter.addWidget(canvas)
        # Right: params placeholder
        params = QWidget()
        params.setMinimumWidth(250)
        splitter.addWidget(params)

        self.setCentralWidget(splitter)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1024, 768)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
