"""MiniMax API客户端模块"""
import os
import time
from openai import OpenAI


class MinimaxClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")

        if not self.api_key:
            raise ValueError("需要提供OPENAI_API_KEY环境变量")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate_content(self, prompt: str, model: str = "MiniMax-M2.7", max_retries: int = 3) -> str:
        print(f"[API] 正在调用MiniMax API...")
        print(f"[API] 模型: {model}")
        print(f"[API] Base URL: {self.base_url or '默认URL'}")
        print(f"[API] API Key前缀: {self.api_key[:20]}..." if self.api_key else "[API] 无API Key")
        print(f"[API] Prompt长度: {len(prompt)} 字符")

        for attempt in range(max_retries):
            try:
                print(f"[API] 第 {attempt + 1}/{max_retries} 次尝试，请求发送中...")
                print(f"[API] 正在等待服务器响应，这可能需要30-60秒...")

                # 记录开始时间
                import time
                start_time = time.time()

                # 创建一个线程来显示进度
                import threading
                stop_progress = threading.Event()

                def show_progress():
                    dots = 0
                    while not stop_progress.is_set():
                        dots = (dots + 1) % 4
                        elapsed = int(time.time() - start_time)
                        print(f"\r[API] 等待中{'.' * dots}{' ' * (3 - dots)} (已等待 {elapsed} 秒)", end='', flush=True)
                        time.sleep(1)

                progress_thread = threading.Thread(target=show_progress)
                progress_thread.daemon = True
                progress_thread.start()

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的测试用例生成助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    extra_body={"reasoning_split": True}
                )

                # 停止进度显示
                stop_progress.set()
                progress_thread.join(timeout=1)
                elapsed_time = int(time.time() - start_time)
                print(f"\r[API] 响应接收完成 (耗时 {elapsed_time} 秒)                    ")

                # 检查是否有思考过程
                if hasattr(response.choices[0].message, 'reasoning_details') and response.choices[0].message.reasoning_details:
                    thinking = response.choices[0].message.reasoning_details[0]['text']
                    print(f"[API] 思考过程长度: {len(thinking)} 字符")

                content = response.choices[0].message.content
                print(f"[API] 响应长度: {len(content)} 字符")
                return content

            except Exception as e:
                # 停止进度显示
                stop_progress.set()
                progress_thread.join(timeout=1)

                error_name = type(e).__name__
                error_msg = str(e)
                print(f"\r[API] 错误: {error_name}                    ")
                print(f"[API] 错误信息: {error_msg}")

                # 如果是529错误（服务器过载）且还有重试次数，则等待后重试
                if "529" in error_msg or "overloaded" in error_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5  # 5秒、10秒、15秒
                        print(f"[API] 服务器负载过高，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                        continue

                # 其他错误或最后一次重试失败，直接抛出
                raise
