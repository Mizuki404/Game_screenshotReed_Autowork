import subprocess
import cv2
import numpy as np
import os
from pathlib import Path  # 添加Path库用于路径处理

class MumuScreenshot:
    def __init__(self, adb_path=None, default_instance=1):
        """
        初始化MuMu截图工具
        
        参数:
            adb_path: MuMu模拟器ADB路径
            default_instance: 默认模拟器实例编号(1表示第一个实例)
        """
        # 默认ADB路径(根据MuMu12实际安装位置调整)
        self.adb_path = str(Path(adb_path or r"D:\Program Files\Netease\MuMu Player 12\shell\adb.exe"))  # 确保路径为字符串
        self.default_instance = default_instance
        
        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(f"未找到ADB工具，请检查路径: {self.adb_path}")

    def capture(self, instance_num=None, save_path=None):
        """
        截取MuMu模拟器屏幕
        
        参数:
            instance_num: 模拟器实例编号
            save_path: 可选，保存截图的路径
            
        返回:
            OpenCV格式的图像(numpy数组)
        """
        port = 7554 + (instance_num or self.default_instance)
        
        try:
            # 连接到模拟器
            subprocess.run(
                f'"{self.adb_path}" connect 127.0.0.1:{port}',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 获取截图数据
            result = subprocess.run(
                f'"{self.adb_path}" -s 127.0.0.1:{port} exec-out screencap -p',
                shell=True,
                capture_output=True,
                check=True
            )
            
            # 转换为OpenCV格式
            img_array = np.frombuffer(result.stdout, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("截图数据解析失败")
                
            # 可选保存 - 修复的部分
            if save_path:
                # 确保路径是字符串
                save_path = str(Path(save_path))  # 转换为字符串
                # 确保目录存在
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                # 保存图像
                if not cv2.imwrite(save_path, img):
                    raise RuntimeError(f"无法保存图像到: {save_path}")
            
            return img
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('gbk', errors='ignore') or e.stdout.decode('gbk', errors='ignore')
            raise RuntimeError(f"ADB命令执行失败: {error_msg}") from e
        except Exception as e:
            raise RuntimeError(f"截图过程中发生错误: {str(e)}") from e

# 提供默认实例方便快速使用
default_screenshot = MumuScreenshot()