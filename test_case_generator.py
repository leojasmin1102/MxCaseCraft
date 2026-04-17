"""测试用例生成器模块"""
import json
from typing import List, Dict
from minimax_client import MinimaxClient


class TestCaseGenerator:
    def __init__(self, minimax_client: MinimaxClient):
        self.client = minimax_client

    def generate_test_cases_from_files(self, file_content: str) -> List[Dict]:
        """从文件内容生成测试用例"""
        print("[生成器] 开始构建提示词...")
        prompt = self._build_prompt_from_files(file_content)
        print(f"[生成器] 提示词长度: {len(prompt)} 字符")

        print("[生成器] 调用MiniMax API生成测试用例...")
        response = self.client.generate_content(prompt)

        print("[生成器] 开始解析响应...")
        result = self._parse_response(response)
        print(f"[生成器] 成功生成 {len(result)} 个测试用例")
        return result

    def generate_test_cases(
        self,
        requirement: str,
        test_plan: str,
        example_cases: List[Dict]
    ) -> List[Dict]:
        print("[生成器] 开始构建提示词...")
        prompt = self._build_prompt(requirement, test_plan, example_cases)
        print(f"[生成器] 提示词长度: {len(prompt)} 字符")

        print("[生成器] 调用MiniMax API生成测试用例...")
        response = self.client.generate_content(prompt)

        print("[生成器] 开始解析响应...")
        result = self._parse_response(response)
        print(f"[生成器] 成功生成 {len(result)} 个测试用例")
        return result

    def _build_prompt_from_files(self, file_content: str) -> str:
        """从文件内容构建提示词"""
        prompt = f"""请根据以下文档内容生成测试用例：

{file_content}

请仔细分析上述文档中的需求描述和测试方案，生成5-10个详细的测试用例。

要求：
1. 严格按照以下JSON格式输出（只输出JSON数组，不要其他内容）
2. 测试用例应该覆盖正常场景、异常场景和边界场景
3. 步骤要详细具体，预期结果要明确

输出格式：
[
  {{
    "title": "测试用例标题",
    "steps": ["步骤1", "步骤2", "步骤3"],
    "expected": "预期结果"
  }}
]"""
        return prompt

    def _build_prompt(
        self,
        requirement: str,
        test_plan: str,
        example_cases: List[Dict]
    ) -> str:
        examples_str = json.dumps(example_cases, ensure_ascii=False, indent=2)

        prompt = f"""请根据以下信息生成测试用例：

需求描述：
{requirement}

测试方案：
{test_plan}

示例测试用例：
{examples_str}

请生成3-5个测试用例，严格按照以下JSON格式输出（只输出JSON数组，不要其他内容）：
[
  {{
    "title": "测试用例标题",
    "steps": ["步骤1", "步骤2", "步骤3"],
    "expected": "预期结果"
  }}
]"""
        return prompt

    def _parse_response(self, response: str) -> List[Dict]:
        print("[解析器] 清理响应格式...")
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            print("[解析器] 解析JSON数据...")
            test_cases = json.loads(response)
            print("[解析器] JSON解析成功")
            return test_cases
        except json.JSONDecodeError as e:
            print(f"[解析器] 错误: JSON解析失败")
            raise ValueError(f"解析响应失败: {e}\n响应内容: {response}")
