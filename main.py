import cv2
import os
from pathlib import Path
from core import MumuScreenshot, IconDetector, Showdetector



def main():
    try:
        # 初始化项目路径
        project_dir = Path(__file__).parent
        template_path = project_dir / "templates" / "button_template.png"
        
        # 1. 初始化工具
        screenshot_tool = MumuScreenshot()
        detector = IconDetector(str(template_path))  # 转为字符串
        display = Showdetector(output_dir="test")  # 设置输出目录
        
        # 2. 截取屏幕
        print("正在截取模拟器屏幕...")
        screenshot = screenshot_tool.capture()
        
        # 3. 识别图标
        print("正在识别按钮...")
        (x, y), confidence = detector.find_icon(screenshot)
        
        if x is not None:
            print(f"找到按钮: 中心坐标({x}, {y}), 置信度: {confidence:.2f}")
            
            # 获取按钮区域坐标
            h, w = detector.template.shape[:2]
            top_left = (x - w//2, y - h//2)
            bottom_right = (x + w//2, y + h//2)
            
            # 显并保存带绿框的图片
            display.show_image_with_rectangle(screenshot, top_left, bottom_right)
            
            # 这里可以添加点击操作或其他逻辑
        else:
            print(f"未找到按钮 (最高置信度: {confidence:.2f})")
            
    except Exception as e:
        print(f"程序出错: {str(e)}")

if __name__ == "__main__":
    main()