from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtCore import Qt, QPoint, QRect

class CropRubberBand(QRubberBand):
    def __init__(self, parent=None):
        super().__init__(QRubberBand.Shape.Rectangle, parent)
        self.start_position = QPoint()
        self.is_dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if the click is within the rubber band
            if self.geometry().contains(event.pos()):
                self.is_dragging = True
                self.start_position = event.pos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            # Calculate the new position of the rubber band
            new_pos = event.pos() - self.start_position
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False