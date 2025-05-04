# matart/app.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QSplitter
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from .canvas import CanvasWidget

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

        # Single CanvasWidget instance
        canvas = CanvasWidget()

        # Shape-selection actions
        for name in ("square", "triangle", "circle", "diamond", "polygon"):
            action = QAction(name.capitalize(), self)
            action.setCheckable(True)
            # When clicked, set the current shape on the canvas
            action.triggered.connect(lambda checked, s=name: canvas.set_current_shape(s))
            toolbar.addAction(action)

        # 3) Central splitter: canvas | params
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(canvas)

        params = QWidget()
        params.setMinimumWidth(250)
        splitter.addWidget(params)

        self.setCentralWidget(splitter)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
