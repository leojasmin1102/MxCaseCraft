"""测试rationality模式的演示脚本"""
import sys
import io

# 修复Windows控制台中文显示
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from requirement_manager import RequirementManager

# 模拟文档内容
test_content = """
=== 需求1 ===
当前版本不支持草图创建功能。需要开发草图基础图元：点、线段、多段线、圆心－半径画圆、椭圆弧、样条曲线等创建功能。

=== 需求2 ===
复杂工程模型的单部件四面体网格生成。软件支持对复杂工程模型的并行四面体网格生成，且剖分速度能达到Hypermesh的75%。

=== 需求3 ===
网格自定义剖分模块：支持拾取线、面、体创建包围盒进行自定义区域加密；支持创建包围盒、球、圆柱进行自定义区域加密。

=== 需求4 ===
网格质量检测模块：支持1D、2D、3D网格进行质量检测，检测完成后界面自动跳转至表格数据。
"""

print("="*80)
print("Rationality模式演示")
print("="*80)

# 创建需求管理器
req_manager = RequirementManager()

# 提取需求
requirements = req_manager.extract_requirements_from_content(test_content)

print(f"\n提取到 {len(requirements)} 条需求")
print("\n需求列表：")
for req in requirements:
    print(f"\n需求 #{req['id']}:")
    print(f"  内容: {req['content'][:100]}...")

print("\n" + "="*80)
print("在实际运行中，程序会逐条显示需求并等待您的确认")
print("您可以选择：")
print("  - 确认需求 (y)")
print("  - 编辑需求 (e)")
print("  - 跳过需求 (s)")
print("  - 退出 (q)")
print("="*80)
