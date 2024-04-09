from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QRubberBand
from PyQt5.QtGui import QMouseEvent, QClipboard
from PyQt5.QtCore import Qt, QPoint, QRect
import time


class ImgSnipper(QWidget):

    def __init__(self, main_window: QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.main_window.hide()
        self.setMouseTracking(True)
        desktop_widget = QApplication.desktop()
        self.setGeometry(0, 0, desktop_widget.width(), desktop_widget.height())
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.15)
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()
        time.sleep(0.3)
        self.img_map = screen.grabWindow(QApplication.desktop().winId(), rect.x(), rect.y(), rect.width(),
                                         rect.height())

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            rect = self.rubber_band.geometry()
            QApplication.restoreOverrideCursor()
            self.img_map = self.img_map.copy(rect)
            clipboard_widget = QApplication.clipboard()
            clipboard_widget.setPixmap(self.img_map, mode=QClipboard.Mode.Clipboard)
            self.main_window.capture_label.setPixmap(self.img_map)
            self.main_window.show()
            self.close()
