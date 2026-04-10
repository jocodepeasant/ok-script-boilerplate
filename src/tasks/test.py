import cv2
import numpy as np


def get_blue_points(image_path, tolerance=30):
    """
    获取图像中所有蓝色点的位置坐标

    参数:
        image_path: 图像文件路径
        tolerance: 颜色容差值，用于定义"蓝色"的范围

    返回:
        blue_points: 蓝色点的坐标列表 [(x1, y1), (x2, y2), ...]
    """
    # 读取图像
    img = cv2.imread(image_path)

    # 转换为 HSV 色彩空间（更容易检测颜色）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 定义蓝色的 HSV 范围
    # 蓝色的 H 值大约在 100-130 之间
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # 创建蓝色掩码
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 获取所有蓝色像素的坐标
    blue_points = np.column_stack(np.where(mask > 0))

    # 转换为 (x, y) 格式（OpenCV 中是 (row, col)，需要转换为 (x, y)）
    blue_points = [(point[1], point[0]) for point in blue_points]

    return blue_points


# 使用示例
if __name__ == "__main__":
    # 替换为你的图像路径
    image_path = "E:\\projects\\ok-script-boilerplate\\assets\\4.png"

    # 获取蓝色点坐标
    points = get_blue_points(image_path)

    print(f"找到 {len(points)} 个蓝色点")
    print("前10个坐标：")
    for i, (x, y) in enumerate(points[:10]):
        print(f"点 {i + 1}: ({x}, {y})")
