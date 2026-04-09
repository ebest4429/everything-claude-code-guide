#!/usr/bin/env python3
"""
[validators.py]
====================
[역할] GIF가 Slack 요구사항을 충족하는지 검증하는 유틸리티

[주요 기능]
  - 이모지/메시지 GIF 크기 및 해상도 검증
  - 파일 크기, 프레임 수, FPS, 재생 시간 정보 조회
  - 빠른 Slack 호환성 확인 (is_slack_ready)

[사용법]
  from core.validators import validate_gif, is_slack_ready

  # 상세 검증
  passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

  # 빠른 확인
  if is_slack_ready('my.gif'):
      print("준비 완료!")

[주요 함수]
  - validate_gif()    : GIF 상세 검증 (결과 딕셔너리 반환)
  - is_slack_ready()  : Slack 업로드 가능 여부 빠른 확인
"""

from pathlib import Path


def validate_gif(
    gif_path: str | Path, is_emoji: bool = True, verbose: bool = True
) -> tuple[bool, dict]:
    """
    GIF가 Slack 요구사항(해상도, 크기, 프레임 수)을 충족하는지 검증합니다.

    Args:
        gif_path: GIF 파일 경로
        is_emoji: True이면 이모지 GIF (128x128 권장), False이면 메시지 GIF
        verbose: True이면 검증 결과 출력

    Returns:
        (통과 여부: bool, 상세 결과: dict) 튜플
    """
    from PIL import Image

    gif_path = Path(gif_path)

    if not gif_path.exists():
        return False, {"error": f"파일을 찾을 수 없습니다: {gif_path}"}

    # 파일 크기 조회
    size_bytes = gif_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    # 해상도 및 프레임 정보 조회
    try:
        with Image.open(gif_path) as img:
            width, height = img.size

            # 프레임 수 계산
            frame_count = 0
            try:
                while True:
                    img.seek(frame_count)
                    frame_count += 1
            except EOFError:
                pass

            # 재생 시간 계산
            try:
                duration_ms = img.info.get("duration", 100)
                total_duration = (duration_ms * frame_count) / 1000
                fps = frame_count / total_duration if total_duration > 0 else 0
            except:
                total_duration = None
                fps = None

    except Exception as e:
        return False, {"error": f"GIF 읽기 실패: {e}"}

    # 해상도 검증
    if is_emoji:
        optimal = width == height == 128
        acceptable = width == height and 64 <= width <= 128
        dim_pass = acceptable
    else:
        aspect_ratio = (
            max(width, height) / min(width, height)
            if min(width, height) > 0
            else float("inf")
        )
        dim_pass = aspect_ratio <= 2.0 and 320 <= min(width, height) <= 640

    results = {
        "file": str(gif_path),
        "passes": dim_pass,
        "width": width,
        "height": height,
        "size_kb": size_kb,
        "size_mb": size_mb,
        "frame_count": frame_count,
        "duration_seconds": total_duration,
        "fps": fps,
        "is_emoji": is_emoji,
        "optimal": optimal if is_emoji else None,
    }

    # verbose 모드 출력
    if verbose:
        print(f"\n{gif_path.name} 검증 중:")
        print(
            f"  해상도: {width}x{height}"
            + (
                f" ({'최적' if optimal else '허용 범위'})"
                if is_emoji and acceptable
                else ""
            )
        )
        print(
            f"  크기: {size_kb:.1f} KB"
            + (f" ({size_mb:.2f} MB)" if size_mb >= 1.0 else "")
        )
        print(
            f"  프레임: {frame_count}개"
            + (f" @ {fps:.1f} fps ({total_duration:.1f}초)" if fps else "")
        )

        if not dim_pass:
            print(
                f"  참고: {'이모지는 128x128이어야 합니다' if is_emoji else 'Slack에 적합하지 않은 해상도입니다'}"
            )

        if size_mb > 5.0:
            print(f"  참고: 파일 크기가 큽니다 — 프레임 수 또는 색상 수 감소를 고려하세요")

    return dim_pass, results


def is_slack_ready(
    gif_path: str | Path, is_emoji: bool = True, verbose: bool = True
) -> bool:
    """
    GIF가 Slack에 업로드 가능한지 빠르게 확인합니다.

    Args:
        gif_path: GIF 파일 경로
        is_emoji: True이면 이모지 GIF, False이면 메시지 GIF
        verbose: True이면 결과 출력

    Returns:
        해상도가 허용 범위이면 True
    """
    passes, _ = validate_gif(gif_path, is_emoji, verbose)
    return passes
