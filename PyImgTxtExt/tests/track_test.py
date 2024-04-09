import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class OpenCVTrackbarWidget(QWidget):
    def __init__(self, parent=None):
        super(OpenCVTrackbarWidget, self).__init__(parent)

        # OpenCV initialization
        self.image = np.zeros((400, 400, 3), np.uint8)
        cv2.namedWindow("OpenCV Trackbar")
        cv2.createTrackbar("Value", "OpenCV Trackbar", 0, 255, self.on_trackbar_change)

        # PyQt5 initialization
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Timer for updating the OpenCV image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(30)

    def on_trackbar_change(self, value):
        pass  # You can add logic here to handle trackbar changes

    def update_image(self):
        # Update OpenCV image
        self.image[:] = [cv2.getTrackbarPos("Value", "OpenCV Trackbar")] * 3

        # Convert OpenCV image to QImage
        q_img = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)

        # Display the QImage
        self.label.setPixmap(QPixmap.fromImage(q_img))


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    opencv_widget = OpenCVTrackbarWidget()
    layout.addWidget(opencv_widget)
    window.setLayout(layout)
    window.setWindowTitle("OpenCV Trackbar in PyQt5")
    window.show()
    app.exec_()
