# matart/app.py

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QToolBar,
    QSplitter,
    QFormLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QScrollArea
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer

from .canvas import CanvasWidget
from .geometry import RULES, generate_sequence, Shape

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("matart – Generative Geometry")

        # Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        help_menu = menu.addMenu("Help")

        # Shape toolbar
        toolbar = QToolBar("Shape Tools")
        self.addToolBar(toolbar)
        self.canvas = CanvasWidget()
        for name in ("square", "triangle", "circle", "diamond", "polygon"):
            action = QAction(name.capitalize(), self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, s=name: self.canvas.set_current_shape(s))
            toolbar.addAction(action)

        # Parameter pane
        params_widget = QWidget()
        form = QFormLayout(params_widget)

        # Rule selector (includes primitives + presets)
        self.rule_combo = QComboBox()
        for key in RULES.keys():
            self.rule_combo.addItem(key)
        form.addRow(QLabel("Rule or Preset:"), self.rule_combo)

        # Initial size
        self.size_spin = QDoubleSpinBox()
        self.size_spin.setRange(1.0, 1000.0)
        self.size_spin.setValue(100.0)
        form.addRow(QLabel("Initial size:"), self.size_spin)

        # Iterations
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(1, 500)
        self.iter_spin.setValue(10)
        form.addRow(QLabel("Iterations:"), self.iter_spin)

        # Animation speed (ms per iteration)
        self.anim_spin = QSpinBox()
        self.anim_spin.setRange(0, 1000)
        self.anim_spin.setValue(0)
        form.addRow(QLabel("Animation speed (ms):"), self.anim_spin)

        # Run button
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_sequence)
        form.addRow(run_btn)

        # Scrollable area for parameters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(params_widget)

        # Layout: splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.canvas)
        splitter.addWidget(scroll)
        scroll.setMinimumWidth(250)

        self.setCentralWidget(splitter)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_step)
        self._pending_shapes = []

    def run_sequence(self):
        # Stop any existing animation
        if self.timer.isActive():
            self.timer.stop()
        # Build initial shape
        shape_name = self.canvas.current_shape or "square"
        start_shape = Shape(
            name=shape_name,
            params={
                "x": 0.0,
                "y": 0.0,
                "size": self.size_spin.value(),
                "angle": 0.0,
                "hue": 0.0
            }
        )
        # Generate full sequence
        rule_key = self.rule_combo.currentText()
        iterations = self.iter_spin.value()
        shapes = generate_sequence(start_shape, rule_key, iterations=iterations,
                                   scale_factor=1.1,
                                   rotation_increment=30,
                                   translate_dx=0,
                                   translate_dy=0,
                                   hue_shift=10)
        # Animate or draw all
        speed = self.anim_spin.value()
        if speed > 0:
            self.canvas.shapes = []
            self._pending_shapes = shapes.copy()
            self.timer.start(speed)
        else:
            self.canvas.shapes = shapes
            self.canvas.update()

    def _animate_step(self):
        if not self._pending_shapes:
            self.timer.stop()
            return
        # Append next shape
        self.canvas.shapes.append(self._pending_shapes.pop(0))
        self.canvas.update()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
