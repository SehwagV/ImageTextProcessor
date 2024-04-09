import sys
from PyQt5.QtWidgets import QApplication

from window import ScreenSelectorWindow

app_styles = """
QFrame {
    background-color: #3f3f3f;
}

QPushButton {
    border-radius: 5px;
    background-color: rgb(60, 90, 255);
    padding: 10px;
    color: white;
    font-weight: bold;
    font-family: Arial;
    font-size: 12px;
}

QPushButton::hover {
    background-color: rgb(60, 20, 255);
}

QLabel {
    color: white;
    font-weight: bold;
    font-family: Arial;
    font-size: 17px;
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(app_styles)
    main_window = ScreenSelectorWindow()
    main_window.sketch_snip_layout()
    main_window.sketch_ocr_layout()
    main_window.show()
    app.exit(app.exec_())
