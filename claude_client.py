"""Claude API客户端模块"""
import os
from anthropic import Anthropic


class ClaudeClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("MY_CLAUDE_AUTH_TOKEN") or os.getenv("ANTHROPIC_AUTH_TOKEN") or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.getenv("MY_CLAUDE_BASE_URL") or os.getenv("ANTHROPIC_BASE_URL")

        if not self.api_key:
            raise ValueError("需要提供MY_CLAUDE_AUTH_TOKEN或ANTHROPIC_AUTH_TOKEN")

        if self.base_url:
            self.client = Anthropic(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = Anthropic(api_key=self.api_key)

    def generate_content(self, prompt: str, model: str = "claude-sonnet-4-6") -> str:
        print(f"[API] 正在调用Claude API...")
        print(f"[API] 模型: {model}")
        print(f"[API] Base URL: {self.base_url or '官方API'}")
        print(f"[API] API Key前缀: {self.api_key[:20]}..." if self.api_key else "[API] 无API Key")
        print(f"[API] 请求发送中，等待响应...")

        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            print(f"[API] 响应接收完成")
            print(f"[API] 响应长度: {len(message.content[0].text)} 字符")
            return message.content[0].text
        except Exception as e:
            print(f"[API] 错误: {type(e).__name__}")
            print(f"[API] 错误信息: {str(e)}")
            raise
