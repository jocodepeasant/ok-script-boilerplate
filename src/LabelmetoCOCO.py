import os
import json
import numpy as np
from PIL import Image
from pathlib import Path
from datetime import datetime


class LabelmetoCOCO:
    """Labelme 批量转换为 COCO 格式"""

    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.category_dict = {}
        self.category_id = 1
        self.annotation_id = 1
        self.image_id = 1

    def add_category(self, label):
        """添加类别"""
        if label not in self.category_dict:
            self.category_dict[label] = self.category_id
            self.categories.append({
                "id": self.category_id,
                "name": label,
                "supercategory": label
            })
            self.category_id += 1
        return self.category_dict[label]

    def process_single_json(self, json_path, image_dir):
        """处理单个 JSON 文件"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 获取图像文件名
            image_name = data.get('imagePath', os.path.basename(json_path).replace('.json', '.jpg'))
            image_name = os.path.basename(image_name)

            # 尝试找到图像文件
            image_path = None
            for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
                test_path = os.path.join(image_dir, os.path.splitext(image_name)[0] + ext)
                if os.path.exists(test_path):
                    image_path = test_path
                    image_name = os.path.basename(test_path)
                    break

            # 获取图像尺寸
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                width, height = img.size
            else:
                width = data.get('imageWidth', 640)
                height = data.get('imageHeight', 480)
                print(f"⚠️  图像文件未找到，使用默认尺寸: {image_name} ({width}x{height})")

            # 添加图像信息
            image_info = {
                "id": self.image_id,
                "file_name": image_name,
                "width": width,
                "height": height,
                "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.images.append(image_info)

            # 处理每个标注
            shapes_count = 0
            for shape in data.get('shapes', []):
                label = shape['label']
                points = shape['points']
                shape_type = shape.get('shape_type', 'polygon')

                # 添加类别
                category_id = self.add_category(label)

                # 处理不同类型的标注
                if shape_type == 'rectangle':
                    x1, y1 = points[0]
                    x2, y2 = points[1]
                    x_min, x_max = min(x1, x2), max(x1, x2)
                    y_min, y_max = min(y1, y2), max(y1, y2)

                    bbox = [x_min, y_min, x_max - x_min, y_max - y_min]
                    segmentation = [[x_min, y_min, x_max, y_min, x_max, y_max, x_min, y_max]]

                elif shape_type == 'polygon':
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    x_min, x_max = min(x_coords), max(x_coords)
                    y_min, y_max = min(y_coords), max(y_coords)

                    bbox = [x_min, y_min, x_max - x_min, y_max - y_min]
                    segmentation = [np.array(points).flatten().tolist()]

                elif shape_type == 'circle':
                    center = points[0]
                    edge = points[1]
                    radius = np.sqrt((edge[0] - center[0]) ** 2 + (edge[1] - center[1]) ** 2)

                    # 生成圆形的多边形近似
                    circle_points = []
                    for i in range(32):
                        angle = 2 * np.pi * i / 32
                        x = center[0] + radius * np.cos(angle)
                        y = center[1] + radius * np.sin(angle)
                        circle_points.extend([x, y])

                    x_min = center[0] - radius
                    y_min = center[1] - radius
                    bbox = [x_min, y_min, radius * 2, radius * 2]
                    segmentation = [circle_points]

                else:
                    print(f"⚠️  不支持的标注类型: {shape_type}")
                    continue

                # 计算面积
                area = bbox[2] * bbox[3]

                # 添加标注
                annotation = {
                    "id": self.annotation_id,
                    "image_id": self.image_id,
                    "category_id": category_id,
                    "bbox": bbox,
                    "area": float(area),
                    "segmentation": segmentation,
                    "iscrowd": 0
                }
                self.annotations.append(annotation)
                self.annotation_id += 1
                shapes_count += 1

            self.image_id += 1
            return True, shapes_count

        except Exception as e:
            print(f"❌ 处理失败 {json_path}: {e}")
            return False, 0

    def convert(self, labelme_dir, output_json, image_dir=None):
        """批量转换"""
        if image_dir is None:
            image_dir = labelme_dir

        # 查找所有 JSON 文件
        json_files = [f for f in list(Path(labelme_dir).glob('*.json')) if f.name not in output_json]

        if not json_files:
            print(f"❌ 未找到 JSON 文件: {labelme_dir}")
            return False

        print(f"{'=' * 70}")
        print(f"🎯 Labelme 批量转换为 COCO 格式")
        print(f"{'=' * 70}")
        print(f"📁 输入目录: {labelme_dir}")
        print(f"🖼️  图像目录: {image_dir}")
        print(f"📄 找到 {len(json_files)} 个 JSON 文件")
        print(f"{'=' * 70}\n")
        print("🔄 开始转换...\n")

        success_count = 0

        for idx, json_file in enumerate(json_files, 1):
            success, shapes_count = self.process_single_json(str(json_file), image_dir)
            if success:
                success_count += 1
                print(f"✅ [{idx:3d}/{len(json_files)}] {json_file.name:40s} - {shapes_count} 个标注")
            else:
                print(f"❌ [{idx:3d}/{len(json_files)}] {json_file.name:40s} - 失败")

        # 生成 COCO 格式
        coco_output = {
            "info": {
                "description": "COCO Dataset converted from Labelme",
                "version": "1.0",
                "year": datetime.now().year,
                "contributor": "Auto Generated",
                "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "licenses": [{
                "id": 1,
                "name": "Unknown",
                "url": ""
            }],
            "images": self.images,
            "annotations": self.annotations,
            "categories": self.categories
        }

        # 保存
        output_path = Path(output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(coco_output, f, indent=2, ensure_ascii=False)

        # 打印统计信息
        print(f"\n{'=' * 70}")
        print(f"✅ 转换完成！")
        print(f"{'=' * 70}")
        print(f"📊 统计信息：")
        print(f"   ├─ 成功处理: {success_count}/{len(json_files)} 个文件")
        print(f"   ├─ 图像数量: {len(self.images)}")
        print(f"   ├─ 标注数量: {len(self.annotations)}")
        print(f"   ├─ 类别数量: {len(self.categories)}")
        print(f"   └─ 平均标注: {len(self.annotations) / len(self.images):.2f} 个/图")
        print(f"\n📋 类别列表：")
        for cat in self.categories:
            cat_count = sum(1 for ann in self.annotations if ann['category_id'] == cat['id'])
            print(f"   ├─ {cat['name']:20s}: {cat_count:4d} 个标注")
        print(f"\n💾 输出文件: {output_json}")
        print(f"   └─ 文件大小: {os.path.getsize(output_json) / 1024:.2f} KB")
        print(f"{'=' * 70}")

        return True


# 主程序
if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description='将多个 Labelme JSON 文件转换为单个 COCO JSON 文件')
    # parser.add_argument('assets/labelme/result', help='Labelme JSON 文件所在目录')
    # parser.add_argument('assets', help='输出的 COCO JSON 文件路径')
    # parser.add_argument('assets/labelme', default=None, help='图像文件所在目录（默认与 JSON 同目录）')
    #
    # args = parser.parse_args()

    # 执行转换
    converter = LabelmetoCOCO()
    # 执行转换
    converter.convert(
        labelme_dir='../assets',  # Labelme JSON 文件目录
        output_json='../assets/result.json',  # 输出的 COCO 文件
        image_dir='../assets'  # 图像文件目录（可选）
    )
