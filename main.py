"""主程序入口"""
import json
import sys
import io
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
from minimax_client import MinimaxClient
from test_case_generator import TestCaseGenerator
from file_reader import FileReader
from excel_writer import ExcelWriter
from requirement_manager import RequirementManager


def main():
    # 修复Windows控制台中文显示
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='测试用例生成工具')
    parser.add_argument(
        '--mode',
        choices=['greed', 'rationality'],
        default='greed',
        help='运行模式: greed=直接生成, rationality=交互式确认需求'
    )
    args = parser.parse_args()

    print(f"[主程序] 运行模式: {args.mode}")
    print()

    load_dotenv()

    # 读取input目录中的文件
    input_dir = "input"
    print(f"[主程序] 开始读取 {input_dir} 目录中的文件...")

    file_content = ""

    # 遍历input目录
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)

            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                print(f"[主程序] 读取Excel文件: {filename}")
                content = FileReader.read_excel(file_path)
                file_content += f"\n\n=== Excel文件: {filename} ===\n{content}"

            elif filename.endswith('.docx') or filename.endswith('.doc'):
                print(f"[主程序] 读取Word文件: {filename}")
                content = FileReader.read_word(file_path)
                file_content += f"\n\n=== Word文件: {filename} ===\n{content}"
    else:
        print(f"[主程序] 警告: {input_dir} 目录不存在")
        return

    if not file_content.strip():
        print("[主程序] 错误: 没有读取到任何文件内容")
        return

    print(f"[主程序] 文件读取完成，总长度: {len(file_content)} 字符")

    # 根据模式选择不同的处理流程
    if args.mode == 'greed':
        run_greed_mode(file_content)
    elif args.mode == 'rationality':
        run_rationality_mode(file_content)


def run_greed_mode(file_content: str):
    """贪婪模式：直接生成测试用例"""
    print("\n[主程序] === 贪婪模式 ===")
    print("[主程序] 将直接使用所有文档内容生成测试用例\n")

    # 打印提取的文档内容
    print("\n" + "="*80)
    print("[主程序] 提取的文档内容:")
    print("="*80)
    print(file_content)
    print("="*80 + "\n")

    # 初始化客户端和生成器
    client = MinimaxClient()
    generator = TestCaseGenerator(client)

    print("\n[主程序] 正在生成测试用例...")
    test_cases = generator.generate_test_cases_from_files(file_content)

    save_test_cases(test_cases)


def run_rationality_mode(file_content: str):
    """理性模式：交互式确认需求后生成测试用例"""
    print("\n[主程序] === 理性模式 ===")
    print("[主程序] 将从Excel文件按行提取需求，逐条显示并由您确认后生成测试用例\n")

    # 查找Excel文件
    input_dir = "input"
    excel_file = None

    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                excel_file = os.path.join(input_dir, filename)
                break

    if not excel_file:
        print("[主程序] 错误: 在input目录中未找到Excel文件")
        print("[主程序] 理性模式需要Excel文件来按行提取需求")
        return

    # 从Excel按行提取需求
    req_manager = RequirementManager()
    requirements = req_manager.extract_requirements_from_excel(excel_file)

    if not requirements:
        print("[主程序] 错误: 未能从Excel文件提取到任何需求")
        return

    # 交互式确认需求
    confirmed_requirements = req_manager.confirm_requirements_interactive()

    if not confirmed_requirements:
        print("[主程序] 没有确认任何需求，退出")
        return

    # 保存确认的需求
    req_manager.save_requirements(confirmed_requirements, "confirmed_requirements.json")

    # 合并确认的需求内容
    merged_content = "\n\n".join([req['content'] for req in confirmed_requirements])

    print(f"\n[主程序] 使用 {len(confirmed_requirements)} 条确认的需求生成测试用例...")

    # 初始化客户端和生成器
    client = MinimaxClient()
    generator = TestCaseGenerator(client)

    test_cases = generator.generate_test_cases_from_files(merged_content)

    save_test_cases(test_cases)


def save_test_cases(test_cases: list):
    """保存测试用例到JSON和Excel"""
    print("\n生成的测试用例：")
    print(json.dumps(test_cases, ensure_ascii=False, indent=2))

    # 保存JSON格式
    json_output = "test_cases_output.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=2)
    print(f"\n[主程序] JSON格式已保存到 {json_output}")

    # 保存Excel格式
    print("\n[主程序] 开始生成Excel文件...")
    template_path = "outputformat/MxSim.Mechanical-通用-GUI-V3.0.0测试用例.xlsx"
    excel_writer = ExcelWriter(template_path=template_path if os.path.exists(template_path) else None)

    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_output = f"test_cases_output_{timestamp}.xlsx"

    # 写入Excel
    excel_writer.write_test_cases(
        test_cases=test_cases,
        output_path=excel_output,
        product_name="MxSim.Mechanical",
        requirement="基于文档自动生成的测试用例",
        creator="AI助手",
        developer=""
    )

    print(f"\n[主程序] Excel格式已保存到 {excel_output}")
    print(f"[主程序] 完成！共生成 {len(test_cases)} 个测试用例")


if __name__ == "__main__":
    main()
