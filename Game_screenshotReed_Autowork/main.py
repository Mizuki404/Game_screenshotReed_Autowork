import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from core import MumuScreenshot, IconDetector, Showdetector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏截图识别程序")
        self.setGeometry(100, 100, 600, 400)

        self.screenshot_tool = MumuScreenshot()
        template_path = os.path.join(os.path.dirname(__file__), "templates", "button_template.png")
        self.detector = IconDetector(template_path)
        self.display = Showdetector(output_dir="test")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("点击按钮进行截图和识别", self)
        layout.addWidget(self.label)

        self.capture_button = QPushButton("截取屏幕并识别图标", self)
        self.capture_button.clicked.connect(self.capture_and_detect)
        layout.addWidget(self.capture_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def capture_and_detect(self):
        try:
            self.label.setText("正在截取模拟器屏幕...")
            screenshot = self.screenshot_tool.capture()

            self.label.setText("正在识别按钮...")
            (x, y), confidence = self.detector.find_icon(screenshot)

            if x is not None:
                self.label.setText(f"找到按钮: 中心坐标({x}, {y}), 置信度: {confidence:.2f}")
                h, w = self.detector.template.shape[:2]
                top_left = (x - w // 2, y - h // 2)
                bottom_right = (x + w // 2, y + h // 2)
                self.display.show_image_with_rectangle(screenshot, top_left, bottom_right)
            else:
                self.label.setText(f"未找到按钮 (最高置信度: {confidence:.2f})")
        except Exception as e:
            self.label.setText(f"程序出错: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()