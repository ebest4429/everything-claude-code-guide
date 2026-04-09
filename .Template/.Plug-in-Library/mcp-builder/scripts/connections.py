"""
MCP 서버 연결 관리 모듈 (connections.py)
=========================================

[역할]
evaluation.py에서 내부적으로 사용하는 MCP 서버 연결 클래스 모음입니다.
직접 실행하는 파일이 아닙니다.

[지원 연결 방식]
  stdio  - 로컬 서버 (subprocess로 직접 실행)
  sse    - 원격 서버 (Server-Sent Events, 레거시)
  http   - 원격 서버 (Streamable HTTP, 권장)

[사용 예시 - 코드에서 import하여 사용]
  from connections import create_connection

  # 로컬 Python 서버 연결
  conn = create_connection("stdio", command="python", args=["my_server.py"])

  # 원격 HTTP 서버 연결
  conn = create_connection("http", url="https://example.com/mcp",
                           headers={"Authorization": "Bearer TOKEN"})

  # async with로 연결 후 도구 사용
  async with conn:
      tools  = await conn.list_tools()                            # 도구 목록 조회
      result = await conn.call_tool("tool_name", {"param": "v"}) # 도구 호출
"""

from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client


class MCPConnection(ABC):
    """MCP 서버 연결을 위한 기반(추상) 클래스."""

    def __init__(self):
        self.session = None
        self._stack = None

    @abstractmethod
    def _create_context(self):
        """연결 유형에 맞는 컨텍스트를 생성합니다."""

    async def __aenter__(self):
        """MCP 서버 연결을 초기화합니다."""
        self._stack = AsyncExitStack()
        await self._stack.__aenter__()

        try:
            ctx = self._create_context()
            result = await self._stack.enter_async_context(ctx)

            if len(result) == 2:
                read, write = result
            elif len(result) == 3:
                read, write, _ = result
            else:
                raise ValueError(f"Unexpected context result: {result}")

            session_ctx = ClientSession(read, write)
            self.session = await self._stack.enter_async_context(session_ctx)
            await self.session.initialize()
            return self
        except BaseException:
            await self._stack.__aexit__(None, None, None)
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """MCP 서버 연결 리소스를 정리합니다."""
        if self._stack:
            await self._stack.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None
        self._stack = None

    async def list_tools(self) -> list[dict[str, Any]]:
        """MCP 서버에서 사용 가능한 도구 목록을 가져옵니다."""
        response = await self.session.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """MCP 서버의 지정된 도구를 주어진 인수로 호출합니다."""
        result = await self.session.call_tool(tool_name, arguments=arguments)
        return result.content


class MCPConnectionStdio(MCPConnection):
    """표준 입출력(stdio)을 사용하는 MCP 연결 — 로컬 서버 전용."""

    def __init__(self, command: str, args: list[str] = None, env: dict[str, str] = None):
        super().__init__()
        self.command = command
        self.args = args or []
        self.env = env

    def _create_context(self):
        return stdio_client(
            StdioServerParameters(command=self.command, args=self.args, env=self.env)
        )


class MCPConnectionSSE(MCPConnection):
    """Server-Sent Events(SSE)를 사용하는 MCP 연결 — 원격 서버 (레거시)."""

    def __init__(self, url: str, headers: dict[str, str] = None):
        super().__init__()
        self.url = url
        self.headers = headers or {}

    def _create_context(self):
        return sse_client(url=self.url, headers=self.headers)


class MCPConnectionHTTP(MCPConnection):
    """Streamable HTTP를 사용하는 MCP 연결 — 원격 서버 권장 방식."""

    def __init__(self, url: str, headers: dict[str, str] = None):
        super().__init__()
        self.url = url
        self.headers = headers or {}

    def _create_context(self):
        return streamablehttp_client(url=self.url, headers=self.headers)


def create_connection(
    transport: str,
    command: str = None,
    args: list[str] = None,
    env: dict[str, str] = None,
    url: str = None,
    headers: dict[str, str] = None,
) -> MCPConnection:
    """연결 유형에 맞는 MCPConnection 인스턴스를 생성하는 팩토리 함수.

    Args:
        transport: 연결 방식 — "stdio", "sse", "http" 중 하나
        command:   실행할 명령어 (stdio 전용, 예: "python", "node")
        args:      명령어 인수 목록 (stdio 전용, 예: ["my_server.py"])
        env:       환경 변수 딕셔너리 (stdio 전용, 예: {"API_KEY": "abc"})
        url:       서버 URL (sse/http 전용, 예: "https://example.com/mcp")
        headers:   HTTP 헤더 딕셔너리 (sse/http 전용)

    Returns:
        MCPConnection 하위 인스턴스
          - stdio → MCPConnectionStdio
          - sse   → MCPConnectionSSE
          - http  → MCPConnectionHTTP

    Raises:
        ValueError: 필수 인수 누락 또는 지원하지 않는 transport 유형
    """
    transport = transport.lower()

    if transport == "stdio":
        if not command:
            raise ValueError("stdio 전송 방식에는 command 인수가 필요합니다")
        return MCPConnectionStdio(command=command, args=args, env=env)

    elif transport == "sse":
        if not url:
            raise ValueError("sse 전송 방식에는 url 인수가 필요합니다")
        return MCPConnectionSSE(url=url, headers=headers)

    elif transport in ["http", "streamable_http", "streamable-http"]:
        if not url:
            raise ValueError("http 전송 방식에는 url 인수가 필요합니다")
        return MCPConnectionHTTP(url=url, headers=headers)

    else:
        raise ValueError(f"지원하지 않는 전송 방식: {transport}. 'stdio', 'sse', 'http' 중 하나를 사용하세요")
