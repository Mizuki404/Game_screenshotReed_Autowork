import subprocess
import cv2
import numpy as np
import os

def adb_screenshot(instance_num=1, save_path=None):
    """使用MuMu自带的ADB进行截图"""
    # MuMu12 ADB路径（根据实际安装位置修改）
    MUMU_ADB_PATH = r"D:\Program Files\Netease\MuMu Player 12\shell\adb.exe"
    
    if not os.path.exists(MUMU_ADB_PATH):
        raise FileNotFoundError(f"未找到MuMu ADB工具，请检查路径: {MUMU_ADB_PATH}")
    
    port = 7554 + instance_num  # 计算多开端口
    
    try:
        # 连接到模拟器
        subprocess.run(f'"{MUMU_ADB_PATH}" connect 127.0.0.1:{port}', shell=True)
        
        # 直接获取截图数据到内存
        result = subprocess.run(
            f'"{MUMU_ADB_PATH}" -s 127.0.0.1:{port} exec-out screencap -p',
            shell=True,
            capture_output=True,
            check=True
        )
        
        # 转换为OpenCV格式
        img_array = np.frombuffer(result.stdout, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("截图数据解析失败，可能ADB连接异常")
            
        # 可选：保存到文件
        if save_path:
            cv2.imwrite(save_path, img)
            
        return img
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ADB命令执行失败: {e.stderr.decode('gbk')}") from e

# 使用示例
try:
    # 获取截图
    screenshot = adb_screenshot(instance_num=1, save_path="mumu_screen.png")
    
    # 显示截图
    cv2.imshow('MuMu12 Screenshot', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
except Exception as e:
    print(f"发生错误: {str(e)}")


# 2. 加载按钮模板图片（提前截取好的小按钮图片）
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建模板文件的绝对路径
template_path = os.path.join(script_dir, 'button_template.png')
template = cv2.imread(template_path, cv2.IMREAD_COLOR)
if template is None:
    raise Exception("无法加载按钮模板图片")

# 3. 获取当前屏幕截图

# 4. 使用模板匹配
result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 5. 设置匹配阈值（0.8表示80%相似度）
threshold = 0.8
if max_val >= threshold:
    # 获取按钮位置和尺寸
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # 在屏幕上绘制矩形标记按钮
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
    
    # 计算按钮中心坐标
    button_center = (top_left[0] + w//2, top_left[1] + h//2)
    print(f"按钮中心坐标: {button_center}")
    
    # 显示结果
    cv2.imshow('Detected Button', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("未找到匹配的按钮")