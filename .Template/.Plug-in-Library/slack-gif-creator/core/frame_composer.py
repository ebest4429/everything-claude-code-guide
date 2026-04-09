#!/usr/bin/env python3
"""
[frame_composer.py]
====================
[역할] 애니메이션 프레임에 시각적 요소를 합성하는 유틸리티

[주요 기능]
  - 단색/그라데이션 배경 프레임 생성
  - 원, 텍스트, 별 등 기본 도형 그리기
  - PIL ImageDraw 래퍼 함수 제공

[사용법]
  from core.frame_composer import create_blank_frame, draw_circle, draw_star
  frame = create_blank_frame(128, 128, color=(240, 248, 255))
  draw_circle(frame, center=(64, 64), radius=30, fill_color=(255, 0, 0))

[주요 함수]
  - create_blank_frame()         : 단색 배경 프레임 생성
  - create_gradient_background() : 세로 그라데이션 배경 생성
  - draw_circle()                : 원 그리기
  - draw_text()                  : 텍스트 그리기
  - draw_star()                  : 5각 별 그리기
"""

from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_blank_frame(
    width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    단색 배경의 빈 프레임을 생성합니다.

    Args:
        width: 프레임 너비
        height: 프레임 높이
        color: RGB 색상 튜플 (기본값: 흰색)

    Returns:
        PIL Image
    """
    return Image.new("RGB", (width, height), color)


def draw_circle(
    frame: Image.Image,
    center: tuple[int, int],
    radius: int,
    fill_color: Optional[tuple[int, int, int]] = None,
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    프레임에 원을 그립니다.

    Args:
        frame: 그릴 대상 PIL Image
        center: (x, y) 중심 좌표
        radius: 원의 반지름
        fill_color: RGB 채우기 색상 (None이면 채우기 없음)
        outline_color: RGB 외곽선 색상 (None이면 외곽선 없음)
        outline_width: 외곽선 두께 (픽셀)

    Returns:
        수정된 프레임
    """
    draw = ImageDraw.Draw(frame)
    x, y = center
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_text(
    frame: Image.Image,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = (0, 0, 0),
    centered: bool = False,
) -> Image.Image:
    """
    프레임에 텍스트를 그립니다.

    Args:
        frame: 그릴 대상 PIL Image
        text: 그릴 텍스트
        position: (x, y) 위치 (centered=False이면 좌상단 기준)
        color: RGB 텍스트 색상
        centered: True이면 position을 중심으로 텍스트를 가운데 정렬

    Returns:
        수정된 프레임
    """
    draw = ImageDraw.Draw(frame)

    # Pillow 기본 폰트 사용.
    # 이모지용 폰트를 변경해야 할 경우 여기에 추가 로직 작성.
    font = ImageFont.load_default()

    if centered:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        position = (x, y)

    draw.text(position, text, fill=color, font=font)
    return frame


def create_gradient_background(
    width: int,
    height: int,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """
    세로 방향 그라데이션 배경을 생성합니다.

    Args:
        width: 프레임 너비
        height: 프레임 높이
        top_color: 상단 RGB 색상
        bottom_color: 하단 RGB 색상

    Returns:
        그라데이션이 적용된 PIL Image
    """
    frame = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(frame)

    # 각 행의 색상 변화량 계산
    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color

    for y in range(height):
        # 색상 보간
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)

        # 가로 선 그리기
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return frame


def draw_star(
    frame: Image.Image,
    center: tuple[int, int],
    size: int,
    fill_color: tuple[int, int, int],
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    5각 별을 그립니다.

    Args:
        frame: 그릴 대상 PIL Image
        center: (x, y) 중심 좌표
        size: 별의 크기 (외부 반지름)
        fill_color: RGB 채우기 색상
        outline_color: RGB 외곽선 색상 (None이면 외곽선 없음)
        outline_width: 외곽선 두께

    Returns:
        수정된 프레임
    """
    import math

    draw = ImageDraw.Draw(frame)
    x, y = center

    # 별의 꼭짓점 계산
    points = []
    for i in range(10):
        angle = (i * 36 - 90) * math.pi / 180  # 꼭짓점당 36도, 맨 위에서 시작
        radius = size if i % 2 == 0 else size * 0.4  # 외부/내부 반지름 교대
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))

    # 별 그리기
    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)

    return frame
