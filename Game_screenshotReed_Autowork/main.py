import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from core import MumuScreenshot, IconDetector, Showdetector, Tapscreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏截图识别程序")
        self.setGeometry(100, 100, 600, 400)

        self.screenshot_tool = MumuScreenshot()
        self.tapscreen_tool = Tapscreen()
        template_path = os.path.join(os.path.dirname(__file__), "templates", "button_template.png")
        self.detector = IconDetector(template_path)
        self.display = Showdetector(output_dir="test")

        self.last_detected_x = None
        self.last_detected_y = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("点击按钮进行截图和识别", self)


        self.capture_button = QPushButton("截取屏幕并识别图标", self)
        self.capture_button.clicked.connect(self.capture_and_detect)
        layout.addWidget(self.capture_button)

        layout.addWidget(self.label)
        self.capture_button = QPushButton("点击已经识别的图标", self)
        self.capture_button.clicked.connect(self.tap_screen)
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
                self.last_detected_x = x
                self.last_detected_y = y
                self.label.setText(f"找到按钮: 中心坐标({x}, {y}), 置信度: {confidence:.2f}\n正在点击按钮...")
                h, w = self.detector.template.shape[:2]
                top_left = (x - w // 2, y - h // 2)
                bottom_right = (x + w // 2, y + h // 2)
                self.display.show_image_with_rectangle(screenshot, top_left, bottom_right)
                # 自动点击识别到的坐标
              
            else:
                self.label.setText(f"未找到按钮 (最高置信度: {confidence:.2f})")
        except Exception as e:
            self.label.setText(f"程序出错: {str(e)}")
    
    def tap_screen(self):
            
            try:
                self.label.setText("正在点击...")
               
                self.tapscreen_tool.tap_screen(self.last_detected_x, self.last_detected_y)
                self.label.setText(f"已点击按钮: ({self.last_detected_x}, {self.last_detected_y})")
            except Exception as e:
                self.label.setText(f"点击失败: {str(e)}")
        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()