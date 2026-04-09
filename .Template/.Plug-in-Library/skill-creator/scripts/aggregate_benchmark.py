#!/usr/bin/env python3
"""
개별 실행 결과를 벤치마크 요약 통계로 집계합니다.

grading.json 파일들을 실행 디렉토리에서 읽어 다음을 생성합니다:
- 각 지표에 대한 평균, 표준편차, 최소, 최대가 포함된 run_summary
- with_skill과 without_skill 구성 간의 delta

사용법:
    python aggregate_benchmark.py <benchmark_dir>

예시:
    python aggregate_benchmark.py benchmarks/2026-01-15T10-30-00/

스크립트는 두 가지 디렉토리 레이아웃을 지원합니다:

    워크스페이스 레이아웃 (skill-creator 반복에서):
    <benchmark_dir>/
    └── eval-N/
        ├── with_skill/
        │   ├── run-1/grading.json
        │   └── run-2/grading.json
        └── without_skill/
            ├── run-1/grading.json
            └── run-2/grading.json

    레거시 레이아웃 (runs/ 서브디렉토리 포함):
    <benchmark_dir>/
    └── runs/
        └── eval-N/
            ├── with_skill/
            │   └── run-1/grading.json
            └── without_skill/
                └── run-1/grading.json
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def calculate_stats(values: list[float]) -> dict:
    """값 목록에 대한 평균, 표준편차, 최소, 최대를 계산합니다."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4)
    }


def load_run_results(benchmark_dir: Path) -> dict:
    """
    벤치마크 디렉토리에서 모든 실행 결과를 로드합니다.

    구성 이름(예: "with_skill"/"without_skill")을 키로 하는 딕셔너리를 반환합니다.
    각 항목은 실행 결과 목록을 포함합니다.
    """
    # 두 가지 레이아웃 지원: benchmark_dir 바로 아래 eval 디렉토리 또는 runs/ 아래
    runs_dir = benchmark_dir / "runs"
    if runs_dir.exists():
        search_dir = runs_dir
    elif list(benchmark_dir.glob("eval-*")):
        search_dir = benchmark_dir
    else:
        print(f"{benchmark_dir} 또는 {benchmark_dir / 'runs'}에서 eval 디렉토리를 찾을 수 없습니다")
        return {}

    results: dict[str, list] = {}

    for eval_idx, eval_dir in enumerate(sorted(search_dir.glob("eval-*"))):
        metadata_path = eval_dir / "eval_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path) as mf:
                    eval_id = json.load(mf).get("eval_id", eval_idx)
            except (json.JSONDecodeError, OSError):
                eval_id = eval_idx
        else:
            try:
                eval_id = int(eval_dir.name.split("-")[1])
            except ValueError:
                eval_id = eval_idx

        # 이름을 하드코딩하지 않고 구성 디렉토리를 동적으로 검색
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            # 비구성 디렉토리(inputs, outputs 등) 건너뜀
            if not list(config_dir.glob("run-*")):
                continue
            config = config_dir.name
            if config not in results:
                results[config] = []

            for run_dir in sorted(config_dir.glob("run-*")):
                run_number = int(run_dir.name.split("-")[1])
                grading_file = run_dir / "grading.json"

                if not grading_file.exists():
                    print(f"경고: {run_dir}에서 grading.json을 찾을 수 없습니다")
                    continue

                try:
                    with open(grading_file) as f:
                        grading = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"경고: {grading_file}의 JSON이 유효하지 않습니다: {e}")
                    continue

                # 지표 추출
                result = {
                    "eval_id": eval_id,
                    "run_number": run_number,
                    "pass_rate": grading.get("summary", {}).get("pass_rate", 0.0),
                    "passed": grading.get("summary", {}).get("passed", 0),
                    "failed": grading.get("summary", {}).get("failed", 0),
                    "total": grading.get("summary", {}).get("total", 0),
                }

                # 타이밍 추출 — grading.json을 먼저 확인하고, 그다음 형제 timing.json 확인
                timing = grading.get("timing", {})
                result["time_seconds"] = timing.get("total_duration_seconds", 0.0)
                timing_file = run_dir / "timing.json"
                if result["time_seconds"] == 0.0 and timing_file.exists():
                    try:
                        with open(timing_file) as tf:
                            timing_data = json.load(tf)
                        result["time_seconds"] = timing_data.get("total_duration_seconds", 0.0)
                        result["tokens"] = timing_data.get("total_tokens", 0)
                    except json.JSONDecodeError:
                        pass

                # 가능한 경우 지표 추출
                metrics = grading.get("execution_metrics", {})
                result["tool_calls"] = metrics.get("total_tool_calls", 0)
                if not result.get("tokens"):
                    result["tokens"] = metrics.get("output_chars", 0)
                result["errors"] = metrics.get("errors_encountered", 0)

                # 어서션 추출 — 뷰어는 text, passed, evidence 필드를 필요로 함
                raw_expectations = grading.get("expectations", [])
                for exp in raw_expectations:
                    if "text" not in exp or "passed" not in exp:
                        print(f"경고: {grading_file}의 어서션에 필수 필드 누락 (text, passed, evidence): {exp}")
                result["expectations"] = raw_expectations

                # user_notes_summary에서 메모 추출
                notes_summary = grading.get("user_notes_summary", {})
                notes = []
                notes.extend(notes_summary.get("uncertainties", []))
                notes.extend(notes_summary.get("needs_review", []))
                notes.extend(notes_summary.get("workarounds", []))
                result["notes"] = notes

                results[config].append(result)

    return results


def aggregate_results(results: dict) -> dict:
    """
    실행 결과를 요약 통계로 집계합니다.

    각 구성과 delta에 대한 통계가 포함된 run_summary를 반환합니다.
    """
    run_summary = {}
    configs = list(results.keys())

    for config in configs:
        runs = results.get(config, [])

        if not runs:
            run_summary[config] = {
                "pass_rate": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "time_seconds": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0}
            }
            continue

        pass_rates = [r["pass_rate"] for r in runs]
        times = [r["time_seconds"] for r in runs]
        tokens = [r.get("tokens", 0) for r in runs]

        run_summary[config] = {
            "pass_rate": calculate_stats(pass_rates),
            "time_seconds": calculate_stats(times),
            "tokens": calculate_stats(tokens)
        }

    # 처음 두 구성 간의 delta 계산 (두 개가 있는 경우)
    if len(configs) >= 2:
        primary = run_summary.get(configs[0], {})
        baseline = run_summary.get(configs[1], {})
    else:
        primary = run_summary.get(configs[0], {}) if configs else {}
        baseline = {}

    delta_pass_rate = primary.get("pass_rate", {}).get("mean", 0) - baseline.get("pass_rate", {}).get("mean", 0)
    delta_time = primary.get("time_seconds", {}).get("mean", 0) - baseline.get("time_seconds", {}).get("mean", 0)
    delta_tokens = primary.get("tokens", {}).get("mean", 0) - baseline.get("tokens", {}).get("mean", 0)

    run_summary["delta"] = {
        "pass_rate": f"{delta_pass_rate:+.2f}",
        "time_seconds": f"{delta_time:+.1f}",
        "tokens": f"{delta_tokens:+.0f}"
    }

    return run_summary


def generate_benchmark(benchmark_dir: Path, skill_name: str = "", skill_path: str = "") -> dict:
    """
    실행 결과에서 완전한 benchmark.json을 생성합니다.
    """
    results = load_run_results(benchmark_dir)
    run_summary = aggregate_results(results)

    # benchmark.json을 위한 runs 배열 구성
    runs = []
    for config in results:
        for result in results[config]:
            runs.append({
                "eval_id": result["eval_id"],
                "configuration": config,
                "run_number": result["run_number"],
                "result": {
                    "pass_rate": result["pass_rate"],
                    "passed": result["passed"],
                    "failed": result["failed"],
                    "total": result["total"],
                    "time_seconds": result["time_seconds"],
                    "tokens": result.get("tokens", 0),
                    "tool_calls": result.get("tool_calls", 0),
                    "errors": result.get("errors", 0)
                },
                "expectations": result["expectations"],
                "notes": result["notes"]
            })

    # 결과에서 eval ID 결정
    eval_ids = sorted(set(
        r["eval_id"]
        for config in results.values()
        for r in config
    ))

    benchmark = {
        "metadata": {
            "skill_name": skill_name or "<스킬-이름>",
            "skill_path": skill_path or "<스킬/경로>",
            "executor_model": "<모델-이름>",
            "analyzer_model": "<모델-이름>",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": eval_ids,
            "runs_per_configuration": 3
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": []  # 분석가가 채울 예정
    }

    return benchmark


def generate_markdown(benchmark: dict) -> str:
    """벤치마크 데이터에서 사람이 읽을 수 있는 benchmark.md를 생성합니다."""
    metadata = benchmark["metadata"]
    run_summary = benchmark["run_summary"]

    # 구성 이름 결정 ("delta" 제외)
    configs = [k for k in run_summary if k != "delta"]
    config_a = configs[0] if len(configs) >= 1 else "config_a"
    config_b = configs[1] if len(configs) >= 2 else "config_b"
    label_a = config_a.replace("_", " ").title()
    label_b = config_b.replace("_", " ").title()

    lines = [
        f"# 스킬 벤치마크: {metadata['skill_name']}",
        "",
        f"**모델**: {metadata['executor_model']}",
        f"**날짜**: {metadata['timestamp']}",
        f"**Eval**: {', '.join(map(str, metadata['evals_run']))} (구성당 {metadata['runs_per_configuration']}회 실행)",
        "",
        "## 요약",
        "",
        f"| 지표 | {label_a} | {label_b} | Delta |",
        "|------|-----------|-----------|-------|",
    ]

    a_summary = run_summary.get(config_a, {})
    b_summary = run_summary.get(config_b, {})
    delta = run_summary.get("delta", {})

    # 통과율 형식화
    a_pr = a_summary.get("pass_rate", {})
    b_pr = b_summary.get("pass_rate", {})
    lines.append(f"| 통과율 | {a_pr.get('mean', 0)*100:.0f}% ± {a_pr.get('stddev', 0)*100:.0f}% | {b_pr.get('mean', 0)*100:.0f}% ± {b_pr.get('stddev', 0)*100:.0f}% | {delta.get('pass_rate', '—')} |")

    # 시간 형식화
    a_time = a_summary.get("time_seconds", {})
    b_time = b_summary.get("time_seconds", {})
    lines.append(f"| 시간 | {a_time.get('mean', 0):.1f}s ± {a_time.get('stddev', 0):.1f}s | {b_time.get('mean', 0):.1f}s ± {b_time.get('stddev', 0):.1f}s | {delta.get('time_seconds', '—')}s |")

    # 토큰 형식화
    a_tokens = a_summary.get("tokens", {})
    b_tokens = b_summary.get("tokens", {})
    lines.append(f"| 토큰 | {a_tokens.get('mean', 0):.0f} ± {a_tokens.get('stddev', 0):.0f} | {b_tokens.get('mean', 0):.0f} ± {b_tokens.get('stddev', 0):.0f} | {delta.get('tokens', '—')} |")

    # 메모 섹션
    if benchmark.get("notes"):
        lines.extend([
            "",
            "## 메모",
            ""
        ])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="벤치마크 실행 결과를 요약 통계로 집계합니다"
    )
    parser.add_argument(
        "benchmark_dir",
        type=Path,
        help="벤치마크 디렉토리 경로"
    )
    parser.add_argument(
        "--skill-name",
        default="",
        help="벤치마킹 중인 스킬 이름"
    )
    parser.add_argument(
        "--skill-path",
        default="",
        help="벤치마킹 중인 스킬 경로"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="benchmark.json 출력 경로 (기본값: <benchmark_dir>/benchmark.json)"
    )

    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"디렉토리를 찾을 수 없습니다: {args.benchmark_dir}")
        sys.exit(1)

    # 벤치마크 생성
    benchmark = generate_benchmark(args.benchmark_dir, args.skill_name, args.skill_path)

    # 출력 경로 결정
    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md = output_json.with_suffix(".md")

    # benchmark.json 저장
    with open(output_json, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"생성됨: {output_json}")

    # benchmark.md 저장
    markdown = generate_markdown(benchmark)
    with open(output_md, "w") as f:
        f.write(markdown)
    print(f"생성됨: {output_md}")

    # 요약 출력
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if k != "delta"]
    delta = run_summary.get("delta", {})

    print(f"\n요약:")
    for config in configs:
        pr = run_summary[config]["pass_rate"]["mean"]
        label = config.replace("_", " ").title()
        print(f"  {label}: {pr*100:.1f}% 통과율")
    print(f"  Delta:         {delta.get('pass_rate', '—')}")


if __name__ == "__main__":
    main()
