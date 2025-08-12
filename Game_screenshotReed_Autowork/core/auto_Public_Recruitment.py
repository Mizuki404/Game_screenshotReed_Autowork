import subprocess
import cv2
import numpy as np
import os
from pathlib import Path
from core import MumuScreenshot, IconDetector, Tapscreen


class Autorecruitment:
    #自动公招
    def __init__(self):
        self.screenshot_tool = MumuScreenshot()
        self.tapscreen_tool = Tapscreen()

    def run(self):
        
        from core import MumuScreenshot, IconDetector, Tapscreen
        import os

        screenshot_tool = MumuScreenshot()
        tapscreen_tool = Tapscreen()
        # 在首页找到“公开招募”按钮并点击
        template1 = os.path.join(os.path.dirname(__file__), "../templates/PublicRecruitment/gongkaizhaomu.png")
        detector1 = IconDetector(template1)

        screenshot1 = screenshot_tool.capture()
        (x1, y1), conf1 = detector1.find_icon(screenshot1)
        if x1 is not None:
            tapscreen_tool.tap_screen(x1, y1)
        else:
            print("未找到第一个按钮")
            return

        # 在“公开招募”页面找到“开始招募”按钮并点击
        template2 = os.path.join(os.path.dirname(__file__), "../templates/PublicRecruitment/kaishizhaomu.png")
        detector2 = IconDetector(template2)
        screenshot2 = screenshot_tool.capture()
        (x2, y2), conf2 = detector2.find_icon(screenshot2)
        if x2 is not None:
            tapscreen_tool.tap_screen(x2, y2)
        else:
            print("未找到第二个按钮")


default_PublicRecruitment = Autorecruitment()


