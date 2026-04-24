# ok-script 模板项目

## 项目简介

ok-script 是一个游戏自动化脚本开发框架，提供了一系列工具和模板，帮助开发者快速构建游戏自动化脚本。该框架支持Windows游戏和Android设备，提供了任务系统、OCR文字识别、模板匹配、GUI界面等功能，极大简化了游戏自动化脚本的开发流程。

## 主要特性

- **任务系统**：支持一次性任务（用户点击触发）和触发式任务（不断执行）
- **多平台支持**：支持Windows游戏和Android设备（通过ADB）
- **OCR文字识别**：内置ONNX OCR支持，可识别游戏中的文字
- **模板匹配**：支持基于COCO格式的模板匹配
- **GUI界面**：提供现代化的用户界面
- **国际化**：支持多语言
- **自动化测试**：内置测试框架

## 快速开始

### 环境要求

- Python 3.8+
- Windows 10+（对于Windows游戏）
- ADB（对于Android设备）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

### 开发流程

1. **fork 本仓库**：创建自己的项目副本
2. **修改配置**：编辑 `src/config.py` 文件，配置游戏信息和其他参数
3. **创建任务**：在 `src/tasks/` 目录下创建任务类
4. **运行项目**：执行 `python main.py` 启动应用

## 项目结构

```
├── src/
│   ├── tasks/         # 任务类
│   ├── ui/            # UI相关代码
│   ├── config.py      # 项目配置
│   └── globals.py     # 全局单例对象
├── tests/             # 自动化测试用例
├── assets/            # 模板匹配使用的资源
├── i18n/              # 国际化文件
├── icons/             # 图标文件
├── main.py            # 入口文件
├── main_debug.py      # 调试入口
├── requirements.txt   # 依赖文件
└── pyappify.yml       # 打包配置
```

## 核心模块

### 任务系统

ok-script 提供了两种类型的任务：

1. **一次性任务**：用户点击触发，执行一次后结束
2. **触发式任务**：不断执行，根据条件判断是否需要运行

任务类需要继承自 `BaseTask` 或 `TriggerTask`，并实现 `run` 方法。

### 配置系统

项目配置位于 `src/config.py` 文件中，包含以下主要配置项：

- **游戏配置**：游戏进程名称、窗口类等
- **OCR配置**：OCR库选择和参数
- **截图配置**：截图方法、处理函数等
- **GUI配置**：窗口大小、标题等
- **任务配置**：注册的任务列表

### 交互系统

提供了鼠标和键盘操作的接口，支持前台和后台操作：

- `click(x, y)`：点击屏幕坐标
- `send_key(key)`：发送键盘按键
- `mouse_down(key)`：按下鼠标按键
- `mouse_up(key)`：释放鼠标按键

### OCR系统

支持文字识别，可指定区域提高识别速度：

- `ocr(box, match)`：识别指定区域的文字
- `ocr(x1, y1, x2, y2, match)`：识别相对坐标区域的文字

### 模板匹配

支持基于COCO格式的模板匹配：

- `find_one(feature_name)`：查找单个特征
- `find_feature(feature_name)`：查找多个特征

## 开发指南

### 创建新任务

1. **创建任务类**：在 `src/tasks/` 目录下创建新的任务文件
2. **继承基类**：继承 `MyBaseTask` 或 `TriggerTask`
3. **实现方法**：实现 `run` 方法和其他必要的方法
4. **注册任务**：在 `config.py` 的 `onetime_tasks` 或 `trigger_tasks` 列表中注册任务

### 示例任务

```python
from src.tasks.MyBaseTask import MyBaseTask

class MyTask(MyBaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "我的任务"
        self.description = "这是一个示例任务"
    
    def run(self):
        self.log_info('任务开始运行!')
        # 执行任务逻辑
        self.click(0.5, 0.5)  # 点击屏幕中心
        self.sleep(1)  # 等待1秒
        self.log_info('任务运行完成!')
```

### 测试任务

在 `tests/` 目录下创建测试文件，使用 `TaskTestCase` 进行测试：

```python
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.MyTask import MyTask

class TestMyTask(TaskTestCase):
    task_class = MyTask
    
    def test_something(self):
        # 设置测试图片
        self.set_image('tests/images/test.png')
        # 执行测试
        result = self.task.some_method()
        # 断言结果
        self.assertEqual(result, expected_value)
```

## 国际化

项目支持国际化，国际化文件位于 `i18n/` 目录：

- `en_US/`：英语
- `zh_CN/`：中文

## 打包发布

使用 `pyappify.yml` 配置文件打包为可执行文件：

```bash
# 安装 pyappify
pip install pyappify

# 打包pyappify build
```

## 使用ok-script的项目

- 鸣潮 [https://github.com/ok-oldking/ok-wuthering-wave](https://github.com/ok-oldking/ok-wuthering-waves)
- 原神(不在维护, 但是后台过剧情可用) [https://github.com/ok-oldking/ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
- 少前2 [https://github.com/ok-oldking/ok-gf2](https://github.com/ok-oldking/ok-gf2)
- 星铁 [https://github.com/Shasnow/ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
- 星痕共鸣 [https://github.com/Sanheiii/ok-star-resonance](https://github.com/Sanheiii/ok-star-resonance)
- 二重螺旋 [https://github.com/BnanZ0/ok-duet-night-abyss](https://github.com/BnanZ0/ok-duet-night-abyss)
- 白荆回廊(停止更新) [https://github.com/ok-oldking/ok-baijing](https://github.com/ok-oldking/ok-baijing)

## 文档和资源

- [游戏自动化入门](https://github.com/ok-oldking/ok-script/blob/master/docs/intro_to_automation/README.md)
- [快速开始](https://github.com/ok-oldking/ok-script/blob/master/docs/quick_start/README.md)
- [进阶使用](https://github.com/ok-oldking/ok-script/blob/master/docs/after_quick_start/README.md)
- [API文档](https://github.com/ok-oldking/ok-script/blob/master/docs/api_doc/README.md)

## 开发者社区

- 开发者群: 938132715
- Discord: [https://discord.gg/vVyCatEBgA](https://discord.gg/vVyCatEBgA)

## 贡献

欢迎提交 issue 和 pull request！

## 许可证

本项目采用 MIT 许可证。