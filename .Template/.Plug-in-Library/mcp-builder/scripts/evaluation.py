"""
MCP 서버 평가 실행 스크립트 (evaluation.py)
============================================

[역할]
XML 평가 파일의 질문을 Claude가 MCP 서버 도구를 사용해 풀게 하고,
정답률·도구 호출 수·소요 시간을 포함한 보고서를 생성합니다.

[사전 준비]
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=your_api_key_here

[실행 명령]
  # 로컬 Python 서버 평가
  python evaluation.py -t stdio -c python -a my_server.py eval.xml

  # 로컬 Node 서버 평가
  python evaluation.py -t stdio -c node -a dist/index.js eval.xml

  # 원격 HTTP 서버 평가 (서버를 먼저 실행해야 함)
  python evaluation.py -t http -u https://example.com/mcp \\
      -H "Authorization: Bearer TOKEN" eval.xml

  # 결과를 파일로 저장
  python evaluation.py -t stdio -c python -a my_server.py -o report.md eval.xml

  # 환경 변수 전달
  python evaluation.py -t stdio -c python -a my_server.py \\
      -e API_KEY=abc123 -e DEBUG=true eval.xml

[주요 옵션]
  eval_file          평가 XML 파일 경로 (필수)
  -t, --transport    연결 방식: stdio / sse / http  (기본: stdio)
  -m, --model        사용할 Claude 모델            (기본: claude-3-7-sonnet-20250219)
  -c, --command      서버 실행 명령어              (stdio 전용)
  -a, --args         명령어 인수                   (stdio 전용)
  -e, --env          환경 변수 KEY=VALUE           (stdio 전용)
  -u, --url          서버 URL                      (sse/http 전용)
  -H, --header       HTTP 헤더 'Key: Value'        (sse/http 전용)
  -o, --output       보고서 저장 파일 경로          (없으면 stdout 출력)

[출력 보고서 항목]
  - 정확도 (정답 수 / 전체)
  - 평균 작업 시간 (초)
  - 평균·총 도구 호출 수
  - 질문별 상세: 예상 답변 / 실제 답변 / 정오 / 요약 / 도구 피드백
"""

import argparse
import asyncio
import json
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from connections import create_connection

# [LLM 지시문] Claude API에 직접 전달되는 system prompt — 영문 유지 필수
# 역할: 평가 질문을 풀 때 Claude가 따라야 할 응답 형식을 지정합니다.
#   <summary>  태그 : 도구 사용 순서·입출력·풀이 과정 요약
#   <feedback> 태그 : 도구 이름·설명·파라미터에 대한 개선 의견
#   <response> 태그 : 최종 답변 (evaluation.py의 extract_xml_content()가 이 태그를 파싱)
# ※ 태그명(summary / feedback / response)을 변경하면 파싱 로직이 깨집니다.
EVALUATION_PROMPT = """You are an AI assistant with access to tools.

When given a task, you MUST:
1. Use the available tools to complete the task
2. Provide summary of each step in your approach, wrapped in <summary> tags
3. Provide feedback on the tools provided, wrapped in <feedback> tags
4. Provide your final response, wrapped in <response> tags

Summary Requirements:
- In your <summary> tags, you must explain:
  - The steps you took to complete the task
  - Which tools you used, in what order, and why
  - The inputs you provided to each tool
  - The outputs you received from each tool
  - A summary for how you arrived at the response

Feedback Requirements:
- In your <feedback> tags, provide constructive feedback on the tools:
  - Comment on tool names: Are they clear and descriptive?
  - Comment on input parameters: Are they well-documented? Are required vs optional parameters clear?
  - Comment on descriptions: Do they accurately describe what the tool does?
  - Comment on any errors encountered during tool usage: Did the tool fail to execute? Did the tool return too many tokens?
  - Identify specific areas for improvement and explain WHY they would help
  - Be specific and actionable in your suggestions

Response Requirements:
- Your response should be concise and directly address what was asked
- Always wrap your final response in <response> tags
- If you cannot solve the task return <response>NOT_FOUND</response>
- For numeric responses, provide just the number
- For IDs, provide just the ID
- For names or text, provide the exact text requested
- Your response should go last"""

# -----------------------------------------------------------------------
# [EVALUATION_PROMPT 한글 번역 참조용 — 실제 실행에는 영문 원본이 사용됨]
#
# 당신은 도구를 사용할 수 있는 AI 어시스턴트입니다.
#
# 작업이 주어지면 반드시 다음을 수행해야 합니다:
# 1. 사용 가능한 도구를 사용하여 작업을 완료합니다.
# 2. 접근 방법의 각 단계 요약을 <summary> 태그로 감싸서 제공합니다.
# 3. 제공된 도구에 대한 피드백을 <feedback> 태그로 감싸서 제공합니다.
# 4. 최종 응답을 <response> 태그로 감싸서 제공합니다.
#
# <summary> 태그 작성 요구사항:
#   - 작업을 완료하기 위해 취한 단계
#   - 어떤 도구를 어떤 순서로 사용했는지, 그리고 그 이유
#   - 각 도구에 제공한 입력값
#   - 각 도구로부터 받은 출력값
#   - 최종 응답에 도달한 과정 요약
#
# <feedback> 태그 작성 요구사항:
#   - 도구 이름: 명확하고 설명적인가?
#   - 입력 파라미터: 잘 문서화되어 있는가? 필수/선택 파라미터가 명확한가?
#   - 설명: 도구가 하는 일을 정확히 설명하는가?
#   - 도구 사용 중 발생한 오류: 실행 실패 여부, 토큰 초과 여부 등
#   - 개선이 필요한 구체적인 영역과 그 이유 (구체적이고 실행 가능하게)
#
# <response> 태그 작성 요구사항:
#   - 응답은 간결하고 질문에 직접 답해야 합니다.
#   - 반드시 최종 응답을 <response> 태그로 감싸야 합니다.
#   - 작업을 풀 수 없으면 <response>NOT_FOUND</response>를 반환합니다.
#   - 숫자 응답은 숫자만 제공합니다.
#   - ID 응답은 ID만 제공합니다.
#   - 이름/텍스트는 요청된 정확한 텍스트를 제공합니다.
#   - 응답은 항상 마지막에 위치해야 합니다.
# -----------------------------------------------------------------------


def parse_evaluation_file(file_path: Path) -> list[dict[str, Any]]:
    """XML 평가 파일에서 qa_pair 요소를 파싱하여 질문-답변 목록을 반환합니다."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        evaluations = []

        for qa_pair in root.findall(".//qa_pair"):
            question_elem = qa_pair.find("question")
            answer_elem = qa_pair.find("answer")

            if question_elem is not None and answer_elem is not None:
                evaluations.append({
                    "question": (question_elem.text or "").strip(),
                    "answer": (answer_elem.text or "").strip(),
                })

        return evaluations
    except Exception as e:
        print(f"평가 파일 파싱 오류 {file_path}: {e}")
        return []


def extract_xml_content(text: str, tag: str) -> str | None:
    """XML 태그 사이의 내용을 추출합니다."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[-1].strip() if matches else None


async def agent_loop(
    client: Anthropic,
    model: str,
    question: str,
    tools: list[dict[str, Any]],
    connection: Any,
) -> tuple[str, dict[str, Any]]:
    """MCP 도구를 사용해 에이전트 루프를 실행하고 최종 응답과 도구 호출 통계를 반환합니다."""
    messages = [{"role": "user", "content": question}]

    response = await asyncio.to_thread(
        client.messages.create,
        model=model,
        max_tokens=4096,
        system=EVALUATION_PROMPT,
        messages=messages,
        tools=tools,
    )

    messages.append({"role": "assistant", "content": response.content})

    tool_metrics = {}

    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        tool_start_ts = time.time()
        try:
            tool_result = await connection.call_tool(tool_name, tool_input)
            tool_response = json.dumps(tool_result) if isinstance(tool_result, (dict, list)) else str(tool_result)
        except Exception as e:
            tool_response = f"Error executing tool {tool_name}: {str(e)}\n"
            tool_response += traceback.format_exc()
        tool_duration = time.time() - tool_start_ts

        if tool_name not in tool_metrics:
            tool_metrics[tool_name] = {"count": 0, "durations": []}
        tool_metrics[tool_name]["count"] += 1
        tool_metrics[tool_name]["durations"].append(tool_duration)

        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_response,
            }]
        })

        response = await asyncio.to_thread(
            client.messages.create,
            model=model,
            max_tokens=4096,
            system=EVALUATION_PROMPT,
            messages=messages,
            tools=tools,
        )
        messages.append({"role": "assistant", "content": response.content})

    response_text = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None,
    )
    return response_text, tool_metrics


async def evaluate_single_task(
    client: Anthropic,
    model: str,
    qa_pair: dict[str, Any],
    tools: list[dict[str, Any]],
    connection: Any,
    task_index: int,
) -> dict[str, Any]:
    """단일 QA 쌍을 평가하고 점수·시간·도구 호출 정보를 포함한 결과를 반환합니다."""
    start_time = time.time()

    print(f"작업 {task_index + 1}: 질문 실행 중 — {qa_pair['question']}")
    response, tool_metrics = await agent_loop(client, model, qa_pair["question"], tools, connection)

    response_value = extract_xml_content(response, "response")
    summary = extract_xml_content(response, "summary")
    feedback = extract_xml_content(response, "feedback")

    duration_seconds = time.time() - start_time

    return {
        "question": qa_pair["question"],
        "expected": qa_pair["answer"],
        "actual": response_value,
        "score": int(response_value == qa_pair["answer"]) if response_value else 0,
        "total_duration": duration_seconds,
        "tool_calls": tool_metrics,
        "num_tool_calls": sum(len(metrics["durations"]) for metrics in tool_metrics.values()),
        "summary": summary,
        "feedback": feedback,
    }


REPORT_HEADER = """
# 평가 보고서

## 요약

- **정확도**: {correct}/{total} ({accuracy:.1f}%)
- **평균 작업 시간**: {average_duration_s:.2f}초
- **작업당 평균 도구 호출 수**: {average_tool_calls:.2f}
- **총 도구 호출 수**: {total_tool_calls}

---
"""

TASK_TEMPLATE = """
### 작업 {task_num}

**질문**: {question}
**정답**: `{expected_answer}`
**실제 답변**: `{actual_answer}`
**정오**: {correct_indicator}
**소요 시간**: {total_duration:.2f}초
**도구 호출**: {tool_calls}

**접근 방법 요약**
{summary}

**도구 피드백**
{feedback}

---
"""


async def run_evaluation(
    eval_path: Path,
    connection: Any,
    model: str = "claude-3-7-sonnet-20250219",
) -> str:
    """MCP 서버 도구를 사용해 전체 평가를 실행하고 보고서 문자열을 반환합니다."""
    print("🚀 평가 시작")

    client = Anthropic()

    tools = await connection.list_tools()
    print(f"📋 MCP 서버에서 {len(tools)}개 도구 로드 완료")

    qa_pairs = parse_evaluation_file(eval_path)
    print(f"📋 평가 작업 {len(qa_pairs)}개 로드 완료")

    results = []
    for i, qa_pair in enumerate(qa_pairs):
        print(f"작업 처리 중 {i + 1}/{len(qa_pairs)}")
        result = await evaluate_single_task(client, model, qa_pair, tools, connection, i)
        results.append(result)

    correct = sum(r["score"] for r in results)
    accuracy = (correct / len(results)) * 100 if results else 0
    average_duration_s = sum(r["total_duration"] for r in results) / len(results) if results else 0
    average_tool_calls = sum(r["num_tool_calls"] for r in results) / len(results) if results else 0
    total_tool_calls = sum(r["num_tool_calls"] for r in results)

    report = REPORT_HEADER.format(
        correct=correct,
        total=len(results),
        accuracy=accuracy,
        average_duration_s=average_duration_s,
        average_tool_calls=average_tool_calls,
        total_tool_calls=total_tool_calls,
    )

    report += "".join([
        TASK_TEMPLATE.format(
            task_num=i + 1,
            question=qa_pair["question"],
            expected_answer=qa_pair["answer"],
            actual_answer=result["actual"] or "N/A",
            correct_indicator="✅" if result["score"] else "❌",
            total_duration=result["total_duration"],
            tool_calls=json.dumps(result["tool_calls"], indent=2),
            summary=result["summary"] or "N/A",
            feedback=result["feedback"] or "N/A",
        )
        for i, (qa_pair, result) in enumerate(zip(qa_pairs, results))
    ])

    return report


def parse_headers(header_list: list[str]) -> dict[str, str]:
    """'Key: Value' 형식의 헤더 문자열 목록을 딕셔너리로 변환합니다."""
    headers = {}
    if not header_list:
        return headers

    for header in header_list:
        if ":" in header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            print(f"경고: 잘못된 형식의 헤더를 무시합니다: {header}")
    return headers


def parse_env_vars(env_list: list[str]) -> dict[str, str]:
    """'KEY=VALUE' 형식의 환경 변수 문자열 목록을 딕셔너리로 변환합니다."""
    env = {}
    if not env_list:
        return env

    for env_var in env_list:
        if "=" in env_var:
            key, value = env_var.split("=", 1)
            env[key.strip()] = value.strip()
        else:
            print(f"경고: 잘못된 형식의 환경 변수를 무시합니다: {env_var}")
    return env


async def main():
    parser = argparse.ArgumentParser(
        description="테스트 질문으로 MCP 서버를 평가합니다",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 로컬 stdio MCP 서버 평가
  python evaluation.py -t stdio -c python -a my_server.py eval.xml

  # SSE MCP 서버 평가
  python evaluation.py -t sse -u https://example.com/mcp -H "Authorization: Bearer token" eval.xml

  # HTTP MCP 서버 평가 (모델 지정)
  python evaluation.py -t http -u https://example.com/mcp -m claude-3-5-sonnet-20241022 eval.xml
        """,
    )

    parser.add_argument("eval_file", type=Path, help="평가 XML 파일 경로")
    parser.add_argument("-t", "--transport", choices=["stdio", "sse", "http"], default="stdio", help="연결 방식 (기본: stdio)")
    parser.add_argument("-m", "--model", default="claude-3-7-sonnet-20250219", help="사용할 Claude 모델 (기본: claude-3-7-sonnet-20250219)")

    stdio_group = parser.add_argument_group("stdio 옵션")
    stdio_group.add_argument("-c", "--command", help="MCP 서버 실행 명령어 (stdio 전용)")
    stdio_group.add_argument("-a", "--args", nargs="+", help="명령어 인수 (stdio 전용)")
    stdio_group.add_argument("-e", "--env", nargs="+", help="환경 변수 KEY=VALUE 형식 (stdio 전용)")

    remote_group = parser.add_argument_group("sse/http 옵션")
    remote_group.add_argument("-u", "--url", help="MCP 서버 URL (sse/http 전용)")
    remote_group.add_argument("-H", "--header", nargs="+", dest="headers", help="HTTP 헤더 'Key: Value' 형식 (sse/http 전용)")

    parser.add_argument("-o", "--output", type=Path, help="보고서 저장 파일 경로 (없으면 stdout 출력)")

    args = parser.parse_args()

    if not args.eval_file.exists():
        print(f"오류: 평가 파일을 찾을 수 없습니다: {args.eval_file}")
        sys.exit(1)

    headers = parse_headers(args.headers) if args.headers else None
    env_vars = parse_env_vars(args.env) if args.env else None

    try:
        connection = create_connection(
            transport=args.transport,
            command=args.command,
            args=args.args,
            env=env_vars,
            url=args.url,
            headers=headers,
        )
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)

    print(f"🔗 {args.transport} 방식으로 MCP 서버에 연결 중...")

    async with connection:
        print("✅ 연결 성공")
        report = await run_evaluation(args.eval_file, connection, args.model)

        if args.output:
            args.output.write_text(report)
            print(f"\n✅ 보고서가 저장되었습니다: {args.output}")
        else:
            print("\n" + report)


if __name__ == "__main__":
    asyncio.run(main())
