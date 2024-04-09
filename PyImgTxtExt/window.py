from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFileDialog
)

from img_cvprocessor import CVProcessor, get_resize_trackbar, get_thresh_trackbar, get_thresh_inv_trackbar, \
    get_blur_trackbar, get_canny_trackbar, get_erode_dilate_trackbar, get_contours_trackbar
from img_snipper import ImgSnipper


def convert_cv_to_qt_img(cv_img=None):
    size = len(cv_img.shape)
    if size == 2:
        height, width = cv_img.shape
    else:
        height, width, channel = cv_img.shape
    bytes_per_line = 3 * width
    if size == 2:
        qt_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    else:
        qt_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
    qt_pixmap = QPixmap.fromImage(qt_img)
    return qt_pixmap


class ScreenSelectorWindow(QMainWindow):

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("Text Extraction - Python OCR")
        desktop_widget = QApplication.desktop()
        m_width = desktop_widget.width() / 4
        m_height = desktop_widget.height() / 4
        # m_width = 400
        # m_height = 500
        self.setMinimumSize(int(m_width), int(m_height))
        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QVBoxLayout(frame)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(5, 30, 5, 30)
        self.main_layout.setSpacing(10)
        self.capture_layout = QVBoxLayout()
        self.capture_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.capture_layout.setContentsMargins(5, 15, 5, 15)
        self.upload_layout = QVBoxLayout()
        self.upload_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_layout.setContentsMargins(5, 15, 5, 15)
        self.process_layout = QGridLayout()
        self.process_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.process_layout.setContentsMargins(5, 15, 5, 15)
        self.main_layout.addLayout(self.capture_layout, stretch=1)
        self.main_layout.addLayout(self.upload_layout, stretch=1)
        self.main_layout.addLayout(self.process_layout, stretch=1)
        self.setCentralWidget(frame)
        self.image_map = None
        self.capture_caption = None
        self.capture_label = None
        self.capture_btn = None
        self.save_btn = None
        self.capturer = None
        self.upload_caption = None
        self.upload_label = None
        self.upload_btn = None
        self.upload_file = None
        self.process_btn = None
        self.cv_processor = None
        self.btn_layout1 = None
        self.btn_layout2 = None
        self.btn_layout3 = None
        self.process_caption = None
        self.process_label = None
        self.img_resize = None
        self.img_gray = None
        self.img_thresh = None
        self.img_thresh_inv = None
        self.img_blur = None
        self.img_canny = None
        self.img_erode = None
        self.img_dilate = None
        self.draw_contours = None
        self.recognize_text = None
        self.img_restore = None

    def resize_and_move_enter(self, resize=1):
        desktop_widget = QApplication.desktop()
        m_width = desktop_widget.width() / resize
        m_height = desktop_widget.height() / resize
        self.resize(int(m_width), int(m_height))
        frame_geometry = self.frameGeometry()
        available_geometry = desktop_widget.availableGeometry().center()
        frame_geometry.moveCenter(available_geometry)
        self.move(frame_geometry.topLeft())

    def sketch_snip_layout(self):
        self.capture_caption = QLabel()
        self.capture_caption.setText("Capture Image")
        self.capture_label = QLabel()
        self.capture_btn = QPushButton("Capture")
        self.capture_btn.clicked.connect(self.capture)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)
        self.save_btn.setVisible(False)
        self.capture_layout.addWidget(self.capture_caption)
        self.capture_layout.addWidget(self.capture_label)
        self.capture_layout.addWidget(self.capture_btn)
        self.capture_layout.addWidget(self.save_btn)

    def show_snip_layout(self):
        if self.capture_caption.isHidden():
            self.capture_caption.show()
        if self.capture_label.isHidden():
            self.capture_label.show()
        if self.capture_btn.isHidden():
            self.capture_btn.show()
        if self.save_btn.isHidden():
            self.save_btn.show()

    def hide_snip_layout(self):
        if not self.capture_caption.isHidden():
            self.capture_caption.hide()
        if not self.capture_label.isHidden():
            self.capture_label.hide()
        if not self.capture_btn.isHidden():
            self.capture_btn.hide()
        if not self.save_btn.isHidden():
            self.save_btn.hide()

    def capture(self):
        self.show_snip_layout()
        self.capturer = ImgSnipper(self)
        self.capturer.show()
        self.save_btn.setVisible(True)
        self.resize_and_move_enter(resize=2)
        self.hide_ocr_layout()

    def save(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *jpeg *.bmp)")
        if file_name:
            self.capturer.img_map.save(file_name)

    def sketch_ocr_layout(self):
        self.upload_caption = QLabel()
        self.upload_caption.setText("Upload Image")
        self.upload_label = QLabel()
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload)
        self.process_btn = QPushButton("Process Image")
        self.process_btn.clicked.connect(self.process_img)
        self.process_btn.setVisible(False)
        self.upload_layout.addWidget(self.upload_caption)
        self.upload_layout.addWidget(self.upload_label)
        self.upload_layout.addWidget(self.upload_btn)
        self.upload_layout.addWidget(self.process_btn)

    def show_ocr_layout(self):
        if self.upload_caption.isHidden():
            self.upload_caption.show()
        if self.upload_label.isHidden():
            self.upload_label.show()
        if self.upload_btn.isHidden():
            self.upload_btn.show()
        if self.process_btn.isHidden():
            self.process_btn.show()

    def hide_ocr_layout(self):
        if not self.upload_caption.isHidden():
            self.upload_caption.hide()
        if not self.upload_label.isHidden():
            self.upload_label.hide()
        if not self.upload_btn.isHidden():
            self.upload_btn.hide()
        if not self.process_btn.isHidden():
            self.process_btn.hide()

    def upload(self):
        self.show_ocr_layout()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.upload_file = file_name
            img_map = QPixmap(file_name)
            self.image_map = img_map.copy()
            self.upload_label.setPixmap(img_map)
            self.process_btn.setVisible(True)
        self.resize_and_move_enter(resize=2)
        self.hide_snip_layout()

    def process_img(self):
        self.hide_snip_layout()
        self.hide_ocr_layout()
        self.main_layout.removeItem(self.capture_layout)
        self.main_layout.removeItem(self.upload_layout)
        self.sketch_grid_layout()

    def sketch_grid_layout(self):
        self.process_caption = QLabel()
        self.process_caption.setText("Image Processing - Computer Vision")
        self.process_label = QLabel()
        if self.image_map:
            self.process_label.setPixmap(self.image_map)
            self.cv_processor = CVProcessor(img=self.upload_file)
            self.img_resize = QPushButton("Resize")
            self.img_resize.clicked.connect(self.resize_img)
            self.img_gray = QPushButton("Gray")
            self.img_gray.clicked.connect(self.gray_img)
            self.img_thresh = QPushButton("Thresh")
            self.img_thresh.clicked.connect(self.thresh_img)
            self.img_thresh_inv = QPushButton("Thresh Inv")
            self.img_thresh_inv.clicked.connect(self.thresh_inv_img)
            self.img_blur = QPushButton("Blur")
            self.img_blur.clicked.connect(self.blur_img)
            self.img_canny = QPushButton("Canny")
            self.img_canny.clicked.connect(self.canny_img)
            self.img_erode = QPushButton("Erode")
            self.img_erode.clicked.connect(self.erode_img)
            self.img_dilate = QPushButton("Dilate")
            self.img_dilate.clicked.connect(self.dilate_img)
            self.draw_contours = QPushButton("Draw Contours")
            self.draw_contours.clicked.connect(self.contours_img)
            self.recognize_text = QPushButton("Recognize Text")
            self.img_restore = QPushButton("Restore Image")
            self.img_restore.clicked.connect(self.restore_img)
            self.btn_layout1 = QHBoxLayout()
            self.btn_layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.btn_layout1.setContentsMargins(5, 15, 5, 15)
            self.btn_layout2 = QHBoxLayout()
            self.btn_layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.btn_layout2.setContentsMargins(5, 15, 5, 15)
            self.btn_layout3 = QHBoxLayout()
            self.btn_layout3.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.btn_layout3.setContentsMargins(5, 15, 5, 15)
            self.btn_layout1.addWidget(self.img_resize)
            self.btn_layout1.addWidget(self.img_gray)
            self.btn_layout1.addWidget(self.img_thresh)
            self.btn_layout1.addWidget(self.img_thresh_inv)
            self.btn_layout2.addWidget(self.img_blur)
            self.btn_layout2.addWidget(self.img_canny)
            self.btn_layout2.addWidget(self.img_erode)
            self.btn_layout2.addWidget(self.img_dilate)
            self.btn_layout3.addWidget(self.draw_contours)
            self.btn_layout3.addWidget(self.recognize_text)
            self.btn_layout3.addWidget(self.img_restore)
            self.process_layout.addWidget(self.process_caption, 0, 0)
            self.process_layout.addWidget(self.process_label, 1, 0)
            self.process_layout.addLayout(self.btn_layout1, 2, 0)
            self.process_layout.addLayout(self.btn_layout2, 3, 0)
            self.process_layout.addLayout(self.btn_layout3, 4, 0)

    def resize_img(self):
        value = get_resize_trackbar()
        if not value == 0:
            value /= 10
        else:
            value = 0.1
        resize_img = self.cv_processor.resize_image(x_scale=value, y_scale=value)
        if resize_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=resize_img)
            self.process_label.setPixmap(qt_pixmap)

    def gray_img(self):
        gray_img = self.cv_processor.gray_image()
        if gray_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=gray_img)
            self.process_label.setPixmap(qt_pixmap)

    def thresh_img(self):
        value = get_thresh_trackbar()
        thresh_img = self.cv_processor.thresh_image(thresh_val=value)
        if thresh_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=thresh_img)
            self.process_label.setPixmap(qt_pixmap)

    def thresh_inv_img(self):
        value = get_thresh_inv_trackbar()
        thresh_inv_img = self.cv_processor.thresh_inv_image(thresh_val=value)
        if thresh_inv_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=thresh_inv_img)
            self.process_label.setPixmap(qt_pixmap)

    def blur_img(self):
        value = get_blur_trackbar()
        if value % 2 == 0:
            value -= 1
        blur_img = self.cv_processor.blur_image(blur_val=value)
        if blur_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=blur_img)
            self.process_label.setPixmap(qt_pixmap)

    def canny_img(self):
        value = get_canny_trackbar()
        canny_img = self.cv_processor.canny_image(lower_thresh=value / 3, upper_thresh=value)
        if canny_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=canny_img)
            self.process_label.setPixmap(qt_pixmap)

    def erode_img(self):
        kernel_val, iterations_val = get_erode_dilate_trackbar()
        erode_img = self.cv_processor.erode_image(kernel_val=kernel_val, iteration_val=iterations_val)
        if erode_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=erode_img)
            self.process_label.setPixmap(qt_pixmap)

    def dilate_img(self):
        kernel_val, iterations_val = get_erode_dilate_trackbar()
        dilate_img = self.cv_processor.dilate_image(kernel_val=kernel_val, iteration_val=iterations_val)
        if dilate_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=dilate_img)
            self.process_label.setPixmap(qt_pixmap)

    def contours_img(self):
        size_val, color_val, thickness_val = get_contours_trackbar()
        contours_img = self.cv_processor.draw_contours(area_size=size_val, rectangle_color=color_val,
                                                       thickness=thickness_val)
        if contours_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=contours_img)
            self.process_label.setPixmap(qt_pixmap)

    def restore_img(self):
        restore_img = self.cv_processor.restore_original()
        if restore_img is not None:
            qt_pixmap = convert_cv_to_qt_img(cv_img=restore_img)
            self.process_label.setPixmap(qt_pixmap)
