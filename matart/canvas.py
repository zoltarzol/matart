# matart/canvas.py

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtGui     import QPalette
from PySide6.QtCore import Qt, QPointF

from .geometry import Shape

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shapes = []               # list of Shape instances
        self.offset = QPointF(0, 0)    # pan offset
        self.scale = 1.0               # zoom level
        self.current_shape = None      # e.g. "square", "circle"

        self._last_pan_pos = None      # track pan start point

        # Make the widget background white
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, Qt.white)
        self.setPalette(pal)

        self.setMouseTracking(True)
    
    def set_current_shape(self, name: str):
        self.current_shape = name

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # paint a white background just in case
        painter.fillRect(self.rect(), Qt.white)
        painter.translate(self.offset)
        painter.scale(self.scale, self.scale)

        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for shape in self.shapes:
            self._draw_shape(painter, shape)

    def _draw_shape(self, painter: QPainter, shape: Shape):
        p = shape.params
        x, y = p.get("x", 0), p.get("y", 0)
        size = p.get("size", 100)
        if shape.name == "square":
            painter.drawRect(x - size/2, y - size/2, size, size)
        elif shape.name == "circle":
            painter.drawEllipse(x - size/2, y - size/2, size, size)
        # TODO: add triangle, diamond, polygons

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_shape:
            # map from widget coords to scene coords
            pt = event.position()
            scene_x = (pt.x() - self.offset.x()) / self.scale
            scene_y = (pt.y() - self.offset.y()) / self.scale
            shape = Shape(
                name=self.current_shape,
                params={"x": scene_x, "y": scene_y, "size": 100}
            )
            self.shapes.append(shape)
            self.update()

    def wheelEvent(self, event):
        # zoom on scroll
        angle = event.angleDelta().y()
        factor = 1 + angle / 240.0
        self.scale *= factor
        self.update()

    def mouseMoveEvent(self, event):
        # pan on right-click drag
        if event.buttons() & Qt.RightButton:
            if self._last_pan_pos is None:
                # first move after pressing R-button
                self._last_pan_pos = event.position()
            else:
                delta = event.position() - self._last_pan_pos
                self.offset += delta
                self._last_pan_pos = event.position()
                self.update()

    def mouseReleaseEvent(self, event):
        # reset pan tracker
        if event.button() == Qt.RightButton:
            self._last_pan_pos = None