import random
import time
import re

from src.tasks.GameScript import GameScript
from src.tasks.MyBaseTask import MyBaseTask


def join_game(self):
    """进入游戏"""
    for i in range(3):
        choose_mode = self.find_one("choose_mode")
        if choose_mode:
            print("选择玩法...")
            self.click_box(choose_mode)
            print("进入选择页面")

            print("选择塔防模式...")
            if not self.wait_click_feature('tafang', raise_if_not_found=False, time_out=5,
                                           click_after_delay=0.5):
                print("选择塔防模式失败")
                continue
            print("选择塔防模式成功")

            print("点击开始游戏...")
            if not self.wait_click_feature('begin_game', raise_if_not_found=False, time_out=5,
                                           click_after_delay=0.5):
                print("开始游戏失败")
                continue

            # ========== 新增：检测单人挑战确认框 ==========
            print("检测是否弹出单人挑战确认框...")
            if self.wait_ocr(match=re.compile(r'是否确认开启单人挑战.*'),
                             raise_if_not_found=False,
                             settle_time=0.2,
                             time_out=2.5):
                print("✅ 检测到单人挑战确认框")
                if self.wait_click_ocr(match='确认开启',
                                       raise_if_not_found=False,
                                       settle_time=0.3,
                                       time_out=2):
                    print("✅ 已点击确认开启")
                else:
                    print("⚠️  未找到确认开启按钮")
            else:
                print("未检测到单人挑战确认框，继续...")

            # ==========================================

            print("等待跳过动画...")
            if not self.wait_ocr(match=re.compile(r'长按跳过.*'), box="top_right",
                                 raise_if_not_found=False, settle_time=0.2, time_out=6):
                print("未检测到跳过提示")
            self.send_key(key=" ", down_time=3, after_sleep=0.5)
            print("跳过动画完成")

            print("等待进入塔防...")
            if not self.wait_ocr(match=re.compile(r'水晶耐久.*'), box="top",
                                 raise_if_not_found=False, settle_time=0.2, time_out=20):
                print("⚠️  未捕捉关键字 水晶耐久")
            self.sleep(0.5)
            print("✅ 进入塔防成功")
            return True
        else:
            print("未找到选择玩法按钮，尝试返回主菜单")
            self.send_key(key="esc", down_time=0.5, after_sleep=1)

    print("❌ 进入游戏失败")
    return False


class SpaceStationTask(MyBaseTask, GameScript):
    """
    逆战未来 - 空间站塔防任务

    任务流程：
    1. 执行初始移动路径（左3秒→下5秒→右2.5秒→下6秒→左8秒→下8秒→右4秒→前10秒）
    2. 循环战斗直到游戏结束
    """

    def run(self):
        """主任务入口"""
        start_time = time.time()

        print("=" * 50)
        print("开始执行空间站塔防任务")
        print("=" * 50)

        while True:
            self.send_key('g')
            self.sleep(3)

        # self.find_feature("grid",box=self.box_of_screen(0.2, 0.17, 0.7, 0.9),)
        #
        # try:
        #     # 等待游戏加载
        #     print("等待游戏加载...")
        #     if not join_game(self):
        #         print("未能开始游戏")
        #         return
        #     print("开始选择陷阱...")
        #     self.sleep(0.5)
        #     self.right_click()
        #     self.choose_trap_by_image()
        #     print("陷阱选择完成")
        #
        #     # 执行初始移动路径
        #     self.execute_initial_path()
        #     # 设置陷阱
        #     self.set_trap()
        #     #
        #     # # 步骤2：循环执行战斗
        #     # self.execute_battle_loop()
        #
        #     # 任务完成
        #     elapsed = time.time() - start_time
        #     print("=" * 50)
        #     print(f"任务完成！总用时: {elapsed:.0f}秒")
        #     print("=" * 50)
        #
        #
        #
        # except Exception as e:
        #     print(f"任务执行失败: {e}")
        #     import traceback
        #     traceback.print_exc()
        #     self.cleanup()
        #     raise

    def set_trap(self):
        print("开始设置陷阱...")
        self.send_key(key="o", down_time=0.5, after_sleep=0.5)
        self.send_key(key="left", down_time=0.5, after_sleep=0.5)
        # self.scroll_relative(0.5, 0.5, 5)
        for i in range(5):
            self.scroll_relative(0.5, 0.5, -100)

    def execute_initial_path(self):
        """执行初始移动路径"""
        print("\n【阶段1】开始执行初始移动路径")
        print("-" * 50)

        # 1. 往左移动 3 秒
        self.move_direction('left', 3)

        # 2. 往下移动 5 秒
        self.move_direction('backward', 5)

        # 3. 往右移动 2.5 秒
        self.move_direction('right', 2.5)

        # 4. 往下移动 6 秒
        self.move_direction('backward', 6)

        # 5. 往左移动 8 秒
        self.move_direction('left', 6.5)

        # 6. 往下移动 8 秒
        self.move_direction('backward', 7.5)

        # 7. 往右移动 4 秒
        self.move_direction('right', 4.3)

        # 8. 往前移动 10 秒
        self.move_direction('forward', 10)

        print("-" * 50)
        print("【阶段1】初始移动路径完成\n")

    def execute_battle_loop(self):
        """循环执行战斗逻辑直到游戏结束"""
        print("【阶段2】开始循环战斗")
        print("-" * 50)

        loop_count = 0
        max_loops = 100
        check_interval = 2.0
        game_ended = False

        while not game_ended and loop_count < max_loops:
            loop_count += 1
            print(f"\n--- 第 {loop_count} 轮战斗 ---")

            # 执行一轮战斗
            self.execute_one_battle_round()

            # 检查游戏是否结束
            if self.check_game_end():
                print("✓ 检测到游戏结束！")
                game_ended = True
                break

            # 等待间隔
            self.sleep(check_interval)

        if loop_count >= max_loops:
            print(f"\n⚠ 达到最大循环次数 {max_loops}，任务结束")

    def execute_one_battle_round(self):
        """执行一轮战斗"""
        # 1. 持续射击 3 秒
        self.continuous_shoot(3)

        # 2. 调整位置
        self.adjust_position()

    def move_direction(self, direction, duration):
        """
        向指定方向移动

        Args:
            direction: 方向 'left', 'right', 'forward', 'backward'
            duration: 持续时间（秒）
        """
        key_map = {
            'left': ('a', '左'),
            'right': ('d', '右'),
            'forward': ('w', '前'),
            'backward': ('s', '下')
        }

        if direction not in key_map:
            print(f"❌ 错误：无效的方向 {direction}")
            return

        key, name = key_map[direction]
        print(f"  → 往{name}移动 {duration:.1f} 秒")

        try:
            self.do_send_key_down(key)
            self.sleep(duration)
            self.do_send_key_up(key)
        except Exception as e:
            print(f"❌ 移动失败: {e}")
            self.do_send_key_up(key)
            raise

    def continuous_shoot(self, duration):
        """
        持续射击

        Args:
            duration: 射击持续时间（秒）
        """
        print(f"  🔫 持续射击 {duration} 秒")

        try:
            self.do_mouse_down('left')
            self.sleep(duration)
            self.do_mouse_up('left')
        except Exception as e:
            print(f"❌ 射击失败: {e}")
            self.do_mouse_up('left')
            raise

    def adjust_position(self):
        """微调位置"""
        directions = ['left', 'right', 'forward', 'backward']
        direction = random.choice(directions)
        duration = random.uniform(0.5, 1.5)

        name_map = {
            'left': '左',
            'right': '右',
            'forward': '前',
            'backward': '后'
        }

        print(f"  📍 调整位置: 往{name_map[direction]} {duration:.1f}秒")
        self.move_direction(direction, duration)

    def check_game_end(self):
        """
        检查游戏是否结束
        通过识别游戏结束图标

        Returns:
            bool: 游戏是否结束
        """
        try:
            result = self.find_one('game_end', threshold=0.8)
            if result:
                print("  ✓ 识别到游戏结束图标")
                return True
            return False
        except Exception as e:
            return False

    def cleanup(self):
        """清理资源，释放所有按键"""
        print("\n清理资源...")

        keys = ['w', 'a', 's', 'd', 'shift', 'e', 'q', 'r']
        for key in keys:
            try:
                self.do_send_key_up(key)
            except:
                pass

        try:
            self.do_mouse_up('left')
            self.do_mouse_up('right')
        except:
            pass

    def place_trap(self, x: int, y: int, trap_name: str):
        """
        放置单个陷阱（双击放置）

        Args:
            x: 点击的 x 坐标
            y: 点击的 y 坐标
            trap_name: 陷阱名称（如 'trap1', 'trap2', 'trap3', 'trap4'）
        """
        # 陷阱名称到按键的映射（按选入顺序：4, 5, 6, 7）
        trap_key_map = {
            'trap1': '4',
            'trap2': '5',
            'trap3': '6',
            'trap4': '7'
        }

        # 获取陷阱对应的按键
        key = trap_key_map.get(trap_name)
        if not key:
            print(f"⚠️  未知的陷阱名称: {trap_name}")
            return

        print(f"放置陷阱 {trap_name}（按键 {key}）到坐标 ({x}, {y})")

        # 1. 按 O 键打开地图
        print("打开地图...")
        self.send_key(key='o', down_time=0.1, after_sleep=1)

        # 2. 拖动地图到左下角（设置较大的移动距离）
        print("拖动地图到左下角...")
        # 从屏幕中心开始拖动到左下角，移动距离设置为 2000 像素
        screen_center_x = self.width // 2
        screen_center_y = self.height // 2
        for i in range(4):
            self.mouse_down(960, 540)
            self.move(1800, 1000)
            self.mouse_up()

        self.sleep(0.3)

        # 3. 键入数字，选择陷阱
        self.send_key(key=key, down_time=0.1, after_sleep=0.2)

        self.sleep(1)
        # 2. 双击指定坐标放置陷阱
        self.move(x, y)
        self.sleep(5)
        self.send_key('left')
        self.sleep(5)  # 两次点击间隔 0.3 秒（可调整为 0.2-0.5 之间）
        self.send_key('left')
        self.sleep(0.2)

        # 5. 再次键入数字，取消选择
        self.send_key(key=key, down_time=0.1, after_sleep=0.2)

        # 6. 按 O 键关闭地图
        print("关闭地图...")
        self.send_key(key='o', down_time=0.1, after_sleep=0.3)

        print(f"✅ 陷阱 {trap_name} 放置完成")


