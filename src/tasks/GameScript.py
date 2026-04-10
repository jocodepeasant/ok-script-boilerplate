from src.tasks.TrapSelector import TrapSelector


class GameScript(TrapSelector):
    def run(self):
        """主运行函数"""
        self.log("游戏脚本启动...")

        # 配置要放入陷阱栏的陷阱（从左到右）
        self.TRAP_IMAGE_MAP = {
            '自修复磁暴塔': 'trap_auto_repair_tower',
            '防空导弹': 'trap_anti_air_missile',
            '破坏者': 'trap_destroyer',
            # 可以继续添加更多陷阱
            # '陷阱名称': '对应的图片特征名称',
        }

        # 执行陷阱选择，放入陷阱栏
        self.choose_trap()

        self.log("游戏脚本执行完成")
