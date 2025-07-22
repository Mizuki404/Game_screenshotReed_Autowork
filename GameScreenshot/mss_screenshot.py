# 导入截屏模块
import mss

# 实例化 mss对象，并重命名为sct，固定写法
with mss.mss() as sct:
    # shot方法用于截屏，output参数指定输出文件名
     sct.shot(output='screenshot.png')