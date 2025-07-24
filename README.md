# 尝试写一个基于OpenCV的mumu模拟器游戏截图识别程序

该项目旨在创建一个图形用户界面应用程序，利用OpenCV库从MuMu模拟器中截取屏幕并识别特定图标。以下是项目的结构和功能概述：

## 项目结构

```
Game_screenshotReed_Autowork
├── core
│   ├── __init__.py          # 导出核心功能类
│   ├── mumu_screenshot.py    # 处理MuMu模拟器截图的类
│   ├── show_detector.py      # 显示带矩形框的图像的类
│   └── start_icon_detector.py # 识别图标的类
├── gui
│   ├── __init__.py          # 初始化GUI模块
│   └── main_window.py       # 定义主窗口的类
├── templates
│   └── button_template.png   # 用于图标识别的模板图像
├── test                     # 存储测试图像或文件
├── main.py                  # 应用程序的入口点
└── README.md                # 项目的文档
```

## 功能概述

1. **截图功能**: 使用`MumuScreenshot`类从MuMu模拟器中截取屏幕。
2. **图标识别**: 使用`IconDetector`类在截图中查找特定图标。
3. **图像显示**: 使用`Showdetector`类显示带有识别结果的图像，并保存标记后的图像。
4. **图形用户界面**: 通过`gui/main_window.py`实现用户友好的界面，方便用户操作和查看结果。

## 使用说明

1. 确保已安装MuMu模拟器并正确配置ADB路径。
2. 将模板图像放置在`templates`目录下。
3. 运行`main.py`以启动应用程序。
4. 按照界面提示进行操作，查看识别结果。

## 依赖项

- Python 3.x
- OpenCV
- NumPy

请根据需要安装相关依赖项。
