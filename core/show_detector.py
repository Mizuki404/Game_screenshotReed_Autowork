import cv2
import os
from pathlib import Path

class Showdetector:
    def __init__(self, output_dir="test"):
        self.output_dir = output_dir

    def show_image_with_rectangle(self, image, top_left, bottom_right, window_name='Result', save_image=True):
        """显示带矩形框的图片"""
        marked_image = image.copy()  # 复制图像
        cv2.rectangle(marked_image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.imshow(window_name, marked_image)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        if save_image:
            self.save_marked_image(marked_image)

    def save_marked_image(self, image, filename_prefix="marked"):
        """
        保存标记后的图像到test文件夹
        
        参数:
            image: 要保存的图像
            filename_prefix: 文件名前缀
        """
        # 生成唯一文件名
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.png"
        save_path = Path(self.output_dir) / filename
        
        # 保存图像
        success = cv2.imwrite(str(save_path), image)
        if success:
            print(f"已保存标记图像到: {save_path}")
        else:
            print(f"无法保存图像到: {save_path}")