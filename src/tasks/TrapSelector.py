import time


class TrapSelector:
    """陷阱选择器 Mixin 类（不继承 MyBaseTask）"""

    # 陷阱名称到图片文件的映射字典
    TRAP_IMAGE_MAP = {
        '自修复磁暴塔': 'trap_auto_repair_tower',
        '防空导弹': 'trap_anti_air_missile',
        '破坏者': 'trap_destroyer',
        # 可以继续添加更多陷阱
        # '陷阱名称': '对应的图片特征名称',
    }

    def choose_trap(self):
        """
        选择陷阱放入陷阱栏的主函数
        - 按N键打开陷阱选择界面
        - 根据配置从左往右依次单击陷阱，将其放入陷阱栏
        - 前一个未成功选中则不执行下一个
        - 全部选择完成后按ESC退出
        """
        # 获取陷阱栏配置
        trap_loadout = getattr(self, 'trap_loadout', ['自修复磁暴塔', '防空导弹', '破坏者'])

        print("========== 开始选择陷阱放入陷阱栏 ==========")

        # 1. 按N键打开陷阱选择界面
        if not self.open_trap_menu():
            print("❌ 打开陷阱菜单失败")
            return False

        # 2. 按顺序选择陷阱放入陷阱栏
        for index, trap_name in enumerate(trap_loadout):
            print(f"正在选择第 {index + 1}/{len(trap_loadout)} 个陷阱: [{trap_name}]")

            # 单击陷阱，将其放入陷阱栏
            success = self.select_trap_to_loadout(trap_name, index + 1)

            if not success:
                print(f"❌ [{trap_name}] 选择失败，停止后续操作")
                break

            print(f"✅ [{trap_name}] 已放入陷阱栏位置 {index + 1}")

        # 3. 按ESC退出陷阱选择界面
        self.close_trap_menu()

        print("========== 陷阱栏配置完成 ==========")
        return True

    def open_trap_menu(self):
        """按N键打开陷阱选择菜单"""
        print("按下 N 键打开陷阱选择菜单...")

        # 使用 send_key 方法按N键
        self.send_key('n')
        time.sleep(0.5)

        print("✅ 陷阱选择菜单已打开")
        return True

    def select_trap_to_loadout(self, trap_name, position):
        """
        识别陷阱文本并点击，将其放入陷阱栏

        Args:
            trap_name: 陷阱名称（'自修复磁暴塔'/'防空导弹'/'破坏者'）
            position: 陷阱栏位置（1, 2, 3...）

        Returns:
            bool: 是否成功选中
        """
        print(f"  查找并点击陷阱: [{trap_name}]")

        try:
            # 使用 wait_click_ocr 方法识别文本并点击
            result = self.wait_click_ocr(
                match=trap_name,
                raise_if_not_found=True,
                settle_time=1,
                recheck_time=1
            )

            if result:
                print(f"  ✅ [{trap_name}] 已成功点击并放入陷阱栏")
                return True
            else:
                print(f"  ❌ 未找到陷阱: {trap_name}")
                return False

        except Exception as e:
            print(f"  ❌ 点击陷阱失败: {trap_name}, 错误: {str(e)}")
            return False

    def close_trap_menu(self):
        """按ESC键关闭陷阱选择菜单"""
        print("按下 ESC 键关闭陷阱选择菜单...")

        # 使用 send_key 方法按ESC键
        self.send_key('esc')
        time.sleep(0.5)

        print("✅ 陷阱选择菜单已关闭")

    # ==================== 新增：基于图片识别的方法 ====================

    def choose_trap_by_image(self):
        """
        使用图片识别方式选择陷阱放入陷阱栏
        - 按N键打开陷阱选择界面
        - 根据配置使用图片特征识别陷阱并点击
        - 前一个未成功选中则不执行下一个
        - 全部选择完成后按ESC退出
        """
        # 获取陷阱栏配置
        trap_loadout = getattr(self, 'trap_loadout', ['自修复磁暴塔', '防空导弹', '破坏者'])

        print("========== 开始选择陷阱放入陷阱栏（图片识别模式） ==========")

        # 1. 按N键打开陷阱选择界面
        if not self.open_trap_menu():
            print("❌ 打开陷阱菜单失败")
            return False

        # 2. 按顺序选择陷阱放入陷阱栏
        for index, trap_name in enumerate(trap_loadout):
            print(f"正在选择第 {index + 1}/{len(trap_loadout)} 个陷阱: [{trap_name}]")

            # 使用图片识别方式单击陷阱
            success = self.select_trap_by_image(trap_name, index + 1)

            if not success:
                print(f"❌ [{trap_name}] 选择失败，停止后续操作")
                break

            print(f"✅ [{trap_name}] 已放入陷阱栏位置 {index + 1}")
            time.sleep(0.3)  # 短暂延迟等待UI响应

        # 3. 按ESC退出陷阱选择界面
        self.close_trap_menu()

        print("========== 陷阱栏配置完成（图片识别模式） ==========")
        return True

    def select_trap_by_image(self, trap_name, position):
        """
        使用图片特征识别陷阱并点击，将其放入陷阱栏

        Args:
            trap_name: 陷阱名称（'自修复磁暴塔'/'防空导弹'/'破坏者'）
            position: 陷阱栏位置（1, 2, 3...）

        Returns:
            bool: 是否成功选中
        """
        # 获取对应的图片特征名称
        feature_name = self.TRAP_IMAGE_MAP.get(trap_name)

        if not feature_name:
            print(f"  ⚠️  未配置图片特征映射: {trap_name}")
            return False

        print(f"  使用图片特征查找陷阱: [{trap_name}] -> {feature_name}")

        try:
            # 检查特征是否存在
            if not self.feature_exists(feature_name):
                print(f"  ❌ 图片特征不存在: {feature_name}")
                return False

            # 使用 wait_click_feature 方法识别图片并点击，wait_click_feature 无法选中，故加了后面的逻辑
            result = self.wait_click_feature(
                feature_name,
                box=self.box_of_screen(0.2, 0.17, 0.7, 0.9),
                time_out=5,
                raise_if_not_found=False,
                click_after_delay=0
            )

            self.do_mouse_down('left')
            self.move_direction('left', 1)
            self.do_mouse_up('left')

            if result:
                print(f"  ✅ [{trap_name}] 已成功通过图片识别点击")
                return True
            else:
                print(f"  ❌ 未找到陷阱图片: {trap_name} ({feature_name})")
                return False

        except Exception as e:
            print(f"  ❌ 图片识别点击失败: {trap_name}, 错误: {str(e)}")
            return False

    def choose_trap_hybrid(self):
        """
        混合模式：优先使用OCR，失败时自动切换到图片识别
        - 按N键打开陷阱选择界面
        - 先尝试OCR识别，失败则使用图片识别
        - 前一个未成功选中则不执行下一个
        - 全部选择完成后按ESC退出
        """
        # 获取陷阱栏配置
        trap_loadout = getattr(self, 'trap_loadout', ['自修复磁暴塔', '防空导弹', '破坏者'])

        print("========== 开始选择陷阱放入陷阱栏（混合识别模式） ==========")

        # 1. 按N键打开陷阱选择界面
        if not self.open_trap_menu():
            print("❌ 打开陷阱菜单失败")
            return False

        # 2. 按顺序选择陷阱放入陷阱栏
        for index, trap_name in enumerate(trap_loadout):
            print(f"正在选择第 {index + 1}/{len(trap_loadout)} 个陷阱: [{trap_name}]")

            # 混合识别方式：OCR优先，图片备用
            success = self.select_trap_hybrid_mode(trap_name, index + 1)

            if not success:
                print(f"❌ [{trap_name}] 选择失败（OCR和图片识别均失败），停止后续操作")
                break

            print(f"✅ [{trap_name}] 已放入陷阱栏位置 {index + 1}")
            time.sleep(0.3)

        # 3. 按ESC退出陷阱选择界面
        self.close_trap_menu()

        print("========== 陷阱栏配置完成（混合识别模式） ==========")
        return True

    def select_trap_hybrid_mode(self, trap_name, position):
        """
        混合识别模式：先OCR后图片

        Args:
            trap_name: 陷阱名称
            position: 陷阱栏位置

        Returns:
            bool: 是否成功选中
        """
        print(f"  [混合模式] 查找陷阱: [{trap_name}]")

        # 第一步：尝试OCR识别
        print(f"    → 尝试 OCR 文本识别...")
        try:
            result = self.wait_click_ocr(
                match=trap_name,
                time_out=3,  # 较短的超时时间
                raise_if_not_found=False,
                settle_time=0.5,
                recheck_time=0
            )

            if result:
                print(f"    ✅ [OCR] 成功识别并点击")
                return True
            else:
                print(f"    ⚠️  [OCR] 未识别到文本，切换到图片识别...")

        except Exception as e:
            print(f"    ⚠️  [OCR] 识别异常: {str(e)}，切换到图片识别...")

        # 第二步：OCR失败，尝试图片识别
        feature_name = self.TRAP_IMAGE_MAP.get(trap_name)

        if not feature_name:
            print(f"    ❌ 未配置图片特征映射: {trap_name}")
            return False

        print(f"    → 尝试图片特征识别: {feature_name}")

        try:
            if not self.feature_exists(feature_name):
                print(f"    ❌ 图片特征不存在: {feature_name}")
                return False

            result = self.wait_click_feature(
                feature=feature_name,
                time_out=5,
                raise_if_not_found=False,
                threshold=0.8,
                settle_time=1
            )

            if result:
                print(f"    ✅ [图片] 成功识别并点击")
                return True
            else:
                print(f"    ❌ [图片] 未识别到特征")
                return False

        except Exception as e:
            print(f"    ❌ [图片] 识别异常: {str(e)}")
            return False

    def find_trap_by_image(self, trap_name, box=None, threshold=0.8):
        """
        仅查找陷阱图片位置，不点击

        Args:
            trap_name: 陷阱名称
            box: 搜索区域（可选）
            threshold: 匹配阈值

        Returns:
            Box对象或None
        """
        feature_name = self.TRAP_IMAGE_MAP.get(trap_name)

        if not feature_name:
            print(f"未配置图片特征映射: {trap_name}")
            return None

        if not self.feature_exists(feature_name):
            print(f"图片特征不存在: {feature_name}")
            return None

        try:
            # 使用 find_one 查找单个特征
            result = self.find_one(
                feature_name=feature_name,
                threshold=threshold,
                box=box
            )
            return result

        except Exception as e:
            print(f"查找陷阱图片失败: {trap_name}, 错误: {str(e)}")
            return None

    def click_trap_by_image(self, trap_name, box=None, threshold=0.8, relative_x=0.5, relative_y=0.5):
        """
        查找并点击陷阱图片

        Args:
            trap_name: 陷阱名称
            box: 搜索区域（可选）
            threshold: 匹配阈值
            relative_x: 点击位置x（相对于找到的box）
            relative_y: 点击位置y（相对于找到的box）

        Returns:
            bool: 是否成功
        """
        trap_box = self.find_trap_by_image(trap_name, box, threshold)

        if trap_box:
            # 使用 click_box 点击找到的位置
            self.click_box(trap_box, relative_x, relative_y)
            print(f"✅ 已点击陷阱: {trap_name}")
            return True
        else:
            print(f"❌ 未找到陷阱: {trap_name}")
            return False

    def add_trap_image_mapping(self, trap_name, feature_name):
        """
        动态添加陷阱名称到图片特征的映射

        Args:
            trap_name: 陷阱名称
            feature_name: 对应的图片特征名称
        """
        self.TRAP_IMAGE_MAP[trap_name] = feature_name
        print(f"✅ 已添加陷阱映射: {trap_name} -> {feature_name}")

    def remove_trap_image_mapping(self, trap_name):
        """
        移除陷阱映射

        Args:
            trap_name: 陷阱名称
        """
        if trap_name in self.TRAP_IMAGE_MAP:
            del self.TRAP_IMAGE_MAP[trap_name]
            print(f"✅ 已移除陷阱映射: {trap_name}")
        else:
            print(f"⚠️  陷阱映射不存在: {trap_name}")

    def get_trap_image_mapping(self):
        """获取当前的陷阱图片映射字典"""
        return self.TRAP_IMAGE_MAP.copy()

    def list_trap_mappings(self):
        """打印所有陷阱映射"""
        print("\n========== 当前陷阱图片映射 ==========")
        if not self.TRAP_IMAGE_MAP:
            print("  (空)")
        else:
            for trap_name, feature_name in self.TRAP_IMAGE_MAP.items():
                exists = "✅" if self.feature_exists(feature_name) else "❌"
                print(f"  {exists} {trap_name} -> {feature_name}")
        print("=" * 40 + "\n")
