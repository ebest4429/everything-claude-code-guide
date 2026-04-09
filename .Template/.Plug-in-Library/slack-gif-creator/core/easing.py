#!/usr/bin/env python3
"""
[easing.py]
====================
[역할] 부드러운 애니메이션을 위한 이징(easing) 타이밍 함수 모음

[주요 기능]
  - 선형, 이차, 삼차 이징 함수
  - 바운스, 탄성, 백(back) 이징 함수
  - 두 값 사이의 보간(interpolate) 유틸리티
  - 스쿼시/스트레치 스케일 계산
  - 포물선 호(arc) 궤적 계산

[사용법]
  from core.easing import interpolate
  y = interpolate(start=0, end=400, t=0.5, easing='ease_out')

[주요 함수]
  - interpolate()           : 두 값 사이를 이징 적용하여 보간
  - get_easing()            : 이름으로 이징 함수 조회
  - apply_squash_stretch()  : 스쿼시/스트레치 스케일 계산
  - calculate_arc_motion()  : 포물선 호 궤적 위치 계산
"""

import math


def linear(t: float) -> float:
    """선형 보간 (이징 없음)."""
    return t


def ease_in_quad(t: float) -> float:
    """이차 ease-in (천천히 시작, 가속)."""
    return t * t


def ease_out_quad(t: float) -> float:
    """이차 ease-out (빠르게 시작, 감속)."""
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    """이차 ease-in-out (천천히 시작, 천천히 끝)."""
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_in_cubic(t: float) -> float:
    """삼차 ease-in (천천히 시작)."""
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """삼차 ease-out (빠르게 시작)."""
    return (t - 1) * (t - 1) * (t - 1) + 1


def ease_in_out_cubic(t: float) -> float:
    """삼차 ease-in-out."""
    if t < 0.5:
        return 4 * t * t * t
    return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1


def ease_in_bounce(t: float) -> float:
    """바운스 ease-in (바운스 시작)."""
    return 1 - ease_out_bounce(1 - t)


def ease_out_bounce(t: float) -> float:
    """바운스 ease-out (바운스 끝)."""
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


def ease_in_out_bounce(t: float) -> float:
    """바운스 ease-in-out."""
    if t < 0.5:
        return ease_in_bounce(t * 2) * 0.5
    return ease_out_bounce(t * 2 - 1) * 0.5 + 0.5


def ease_in_elastic(t: float) -> float:
    """탄성 ease-in (스프링 효과)."""
    if t == 0 or t == 1:
        return t
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)


def ease_out_elastic(t: float) -> float:
    """탄성 ease-out (스프링 효과)."""
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1


def ease_in_out_elastic(t: float) -> float:
    """탄성 ease-in-out."""
    if t == 0 or t == 1:
        return t
    t = t * 2 - 1
    if t < 0:
        return -0.5 * math.pow(2, 10 * t) * math.sin((t - 0.1) * 5 * math.pi)
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) * 0.5 + 1


# 편의 매핑
EASING_FUNCTIONS = {
    "linear": linear,
    "ease_in": ease_in_quad,
    "ease_out": ease_out_quad,
    "ease_in_out": ease_in_out_quad,
    "bounce_in": ease_in_bounce,
    "bounce_out": ease_out_bounce,
    "bounce": ease_in_out_bounce,
    "elastic_in": ease_in_elastic,
    "elastic_out": ease_out_elastic,
    "elastic": ease_in_out_elastic,
}


def get_easing(name: str = "linear"):
    """이름으로 이징 함수를 반환합니다."""
    return EASING_FUNCTIONS.get(name, linear)


def interpolate(start: float, end: float, t: float, easing: str = "linear") -> float:
    """
    이징을 적용하여 두 값 사이를 보간합니다.

    Args:
        start: 시작 값
        end: 종료 값
        t: 진행률 (0.0 ~ 1.0)
        easing: 이징 함수 이름

    Returns:
        보간된 값
    """
    ease_func = get_easing(easing)
    eased_t = ease_func(t)
    return start + (end - start) * eased_t


def ease_back_in(t: float) -> float:
    """백 ease-in (앞으로 가기 전 살짝 뒤로 오버슈트)."""
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def ease_back_out(t: float) -> float:
    """백 ease-out (앞으로 오버슈트 후 제자리로)."""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


def ease_back_in_out(t: float) -> float:
    """백 ease-in-out (양 끝 모두 오버슈트)."""
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    return (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2


def apply_squash_stretch(
    base_scale: tuple[float, float], intensity: float, direction: str = "vertical"
) -> tuple[float, float]:
    """
    더 역동적인 애니메이션을 위한 스쿼시/스트레치 스케일을 계산합니다.

    Args:
        base_scale: (가로_스케일, 세로_스케일) 기본 스케일
        intensity: 스쿼시/스트레치 강도 (0.0~1.0)
        direction: 'vertical'(세로), 'horizontal'(가로), 'both'(양방향)

    Returns:
        스쿼시/스트레치가 적용된 (가로_스케일, 세로_스케일)
    """
    width_scale, height_scale = base_scale

    if direction == "vertical":
        # 세로 압축, 가로 확장 (부피 보존)
        height_scale *= 1 - intensity * 0.5
        width_scale *= 1 + intensity * 0.5
    elif direction == "horizontal":
        # 가로 압축, 세로 확장
        width_scale *= 1 - intensity * 0.5
        height_scale *= 1 + intensity * 0.5
    elif direction == "both":
        # 전체 스쿼시 (양 방향)
        width_scale *= 1 - intensity * 0.3
        height_scale *= 1 - intensity * 0.3

    return (width_scale, height_scale)


def calculate_arc_motion(
    start: tuple[float, float], end: tuple[float, float], height: float, t: float
) -> tuple[float, float]:
    """
    포물선 호(arc) 경로를 따라 위치를 계산합니다 (자연스러운 움직임).

    Args:
        start: (x, y) 시작 위치
        end: (x, y) 종료 위치
        height: 중간 지점의 호 높이 (양수 = 위쪽)
        t: 진행률 (0.0~1.0)

    Returns:
        호를 따른 (x, y) 위치
    """
    x1, y1 = start
    x2, y2 = end

    # x는 선형 보간
    x = x1 + (x2 - x1) * t

    # y는 포물선 보간
    # y = 시작 + 진행률 * (종료 - 시작) + 호 오프셋
    # 호 오프셋은 t=0.5에서 최대
    arc_offset = 4 * height * t * (1 - t)
    y = y1 + (y2 - y1) * t - arc_offset

    return (x, y)


# 새 이징 함수를 편의 매핑에 추가
EASING_FUNCTIONS.update(
    {
        "back_in": ease_back_in,
        "back_out": ease_back_out,
        "back_in_out": ease_back_in_out,
        "anticipate": ease_back_in,  # 별칭
        "overshoot": ease_back_out,  # 별칭
    }
)
