"""测试Excel按行提取需求功能"""
import os
from requirement_manager import RequirementManager


def main():
    # 查找Excel文件
    input_dir = "input"
    excel_file = None

    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                excel_file = os.path.join(input_dir, filename)
                break

    if not excel_file:
        print("错误: 在input目录中未找到Excel文件")
        return

    print(f"找到Excel文件: {excel_file}\n")

    # 提取需求
    req_manager = RequirementManager()
    requirements = req_manager.extract_requirements_from_excel(excel_file)

    # 显示前5条需求作为示例
    print(f"\n提取到 {len(requirements)} 条需求")
    print("\n显示前5条需求作为示例：\n")

    for req in requirements[:5]:
        print("="*80)
        print(f"需求 #{req['id']}")
        print(f"来源: 工作表 [{req['sheet']}] 第 {req['row']} 行")
        print("="*80)
        print(req['content'])
        print()


if __name__ == "__main__":
    main()
