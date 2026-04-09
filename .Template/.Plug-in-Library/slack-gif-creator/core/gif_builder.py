#!/usr/bin/env python3
"""
[gif_builder.py]
====================
[역할] 프레임을 조합하여 Slack에 최적화된 GIF를 생성하는 핵심 모듈

[주요 기능]
  - PIL Image 또는 numpy 배열로 프레임 추가
  - 색상 팔레트 최적화 (전역/프레임별)
  - 중복 프레임 제거
  - 이모지 모드 자동 최적화 (128x128, 색상 감소)
  - GIF 파일 저장 및 파일 정보 반환

[사용법]
  from core.gif_builder import GIFBuilder
  builder = GIFBuilder(width=128, height=128, fps=10)
  builder.add_frame(frame)
  builder.save('output.gif', num_colors=48, optimize_for_emoji=True)

[주요 클래스/함수]
  - GIFBuilder      : GIF 생성 빌더 클래스
  - add_frame()     : 단일 프레임 추가
  - add_frames()    : 프레임 리스트 추가
  - optimize_colors(): 색상 팔레트 최적화
  - deduplicate_frames(): 중복 프레임 제거
  - save()          : GIF 파일 저장
  - clear()         : 프레임 목록 초기화
"""

from pathlib import Path
from typing import Optional

import imageio.v3 as imageio
import numpy as np
from PIL import Image


class GIFBuilder:
    """프레임으로 최적화된 GIF를 생성하는 빌더."""

    def __init__(self, width: int = 480, height: int = 480, fps: int = 15):
        """
        GIF 빌더를 초기화합니다.

        Args:
            width: 프레임 너비 (픽셀)
            height: 프레임 높이 (픽셀)
            fps: 초당 프레임 수
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.frames: list[np.ndarray] = []

    def add_frame(self, frame: np.ndarray | Image.Image):
        """
        GIF에 프레임을 추가합니다.

        Args:
            frame: numpy 배열 또는 PIL Image 형태의 프레임 (RGB로 변환됨)
        """
        if isinstance(frame, Image.Image):
            frame = np.array(frame.convert("RGB"))

        # 프레임 크기가 맞지 않으면 리사이즈
        if frame.shape[:2] != (self.height, self.width):
            pil_frame = Image.fromarray(frame)
            pil_frame = pil_frame.resize(
                (self.width, self.height), Image.Resampling.LANCZOS
            )
            frame = np.array(pil_frame)

        self.frames.append(frame)

    def add_frames(self, frames: list[np.ndarray | Image.Image]):
        """여러 프레임을 한 번에 추가합니다."""
        for frame in frames:
            self.add_frame(frame)

    def optimize_colors(
        self, num_colors: int = 128, use_global_palette: bool = True
    ) -> list[np.ndarray]:
        """
        양자화(quantization)를 사용하여 모든 프레임의 색상을 줄입니다.

        Args:
            num_colors: 목표 색상 수 (8~256)
            use_global_palette: True이면 모든 프레임에 단일 팔레트 사용 (압축률 향상)

        Returns:
            색상이 최적화된 프레임 목록
        """
        optimized = []

        if use_global_palette and len(self.frames) > 1:
            # 모든 프레임에서 전역 팔레트 생성
            # 샘플 프레임으로 팔레트 구성
            sample_size = min(5, len(self.frames))
            sample_indices = [
                int(i * len(self.frames) / sample_size) for i in range(sample_size)
            ]
            sample_frames = [self.frames[i] for i in sample_indices]

            # 샘플 프레임을 단일 이미지로 합쳐 팔레트 생성
            # 각 프레임을 펼쳐 전체 픽셀 스택 생성
            all_pixels = np.vstack(
                [f.reshape(-1, 3) for f in sample_frames]
            )  # (전체_픽셀, 3)

            # 픽셀 데이터로 적절한 크기의 RGB 이미지 생성
            # 전체 픽셀로 대략 정사각형 이미지 구성
            total_pixels = len(all_pixels)
            width = min(512, int(np.sqrt(total_pixels)))  # 최대 512의 적절한 너비
            height = (total_pixels + width - 1) // width  # 올림 나눗셈

            # 사각형을 채우기 위해 필요시 패딩
            pixels_needed = width * height
            if pixels_needed > total_pixels:
                padding = np.zeros((pixels_needed - total_pixels, 3), dtype=np.uint8)
                all_pixels = np.vstack([all_pixels, padding])

            # 올바른 RGB 이미지 형식으로 변환 (H, W, 3)
            img_array = (
                all_pixels[:pixels_needed].reshape(height, width, 3).astype(np.uint8)
            )
            combined_img = Image.fromarray(img_array, mode="RGB")

            # 전역 팔레트 생성
            global_palette = combined_img.quantize(colors=num_colors, method=2)

            # 모든 프레임에 전역 팔레트 적용
            for frame in self.frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(palette=global_palette, dither=1)
                optimized.append(np.array(quantized.convert("RGB")))
        else:
            # 프레임별 양자화 사용
            for frame in self.frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(colors=num_colors, method=2, dither=1)
                optimized.append(np.array(quantized.convert("RGB")))

        return optimized

    def deduplicate_frames(self, threshold: float = 0.9995) -> int:
        """
        연속된 중복 또는 거의 동일한 프레임을 제거합니다.

        Args:
            threshold: 유사도 임계값 (0.0~1.0). 높을수록 엄격 (0.9995 = 거의 동일).
                      미세한 애니메이션 보존: 0.9995+, 적극적 제거: 0.98

        Returns:
            제거된 프레임 수
        """
        if len(self.frames) < 2:
            return 0

        deduplicated = [self.frames[0]]
        removed_count = 0

        for i in range(1, len(self.frames)):
            # 이전 프레임과 비교
            prev_frame = np.array(deduplicated[-1], dtype=np.float32)
            curr_frame = np.array(self.frames[i], dtype=np.float32)

            # 유사도 계산 (정규화)
            diff = np.abs(prev_frame - curr_frame)
            similarity = 1.0 - (np.mean(diff) / 255.0)

            # 충분히 다른 프레임만 유지
            # 높은 임계값(0.9995+)은 거의 동일한 프레임만 제거
            if similarity < threshold:
                deduplicated.append(self.frames[i])
            else:
                removed_count += 1

        self.frames = deduplicated
        return removed_count

    def save(
        self,
        output_path: str | Path,
        num_colors: int = 128,
        optimize_for_emoji: bool = False,
        remove_duplicates: bool = False,
    ) -> dict:
        """
        프레임을 Slack에 최적화된 GIF로 저장합니다.

        Args:
            output_path: GIF 저장 경로
            num_colors: 사용할 색상 수 (적을수록 파일 크기 감소)
            optimize_for_emoji: True이면 이모지 크기로 최적화 (128x128, 색상 감소)
            remove_duplicates: True이면 연속된 중복 프레임 제거 (선택적)

        Returns:
            파일 정보 딕셔너리 (path, size, dimensions, frame_count)
        """
        if not self.frames:
            raise ValueError("저장할 프레임이 없습니다. add_frame()으로 프레임을 추가하세요.")

        output_path = Path(output_path)

        # 중복 프레임 제거로 파일 크기 감소
        if remove_duplicates:
            removed = self.deduplicate_frames(threshold=0.9995)
            if removed > 0:
                print(
                    f"  거의 동일한 프레임 {removed}개 제거 (미세한 애니메이션 보존)"
                )

        # 이모지 최적화 처리
        if optimize_for_emoji:
            if self.width > 128 or self.height > 128:
                print(
                    f"  이모지용으로 {self.width}x{self.height} → 128x128 리사이즈"
                )
                self.width = 128
                self.height = 128
                # 모든 프레임 리사이즈
                resized_frames = []
                for frame in self.frames:
                    pil_frame = Image.fromarray(frame)
                    pil_frame = pil_frame.resize((128, 128), Image.Resampling.LANCZOS)
                    resized_frames.append(np.array(pil_frame))
                self.frames = resized_frames
            num_colors = min(num_colors, 48)  # 이모지용 색상 수 강제 제한

            # 이모지용 적극적 FPS 감소
            if len(self.frames) > 12:
                print(
                    f"  이모지 크기를 위해 프레임 수 {len(self.frames)}개 → 약 12개로 감소"
                )
                # 12프레임에 가깝게 n번째 프레임만 유지
                keep_every = max(1, len(self.frames) // 12)
                self.frames = [
                    self.frames[i] for i in range(0, len(self.frames), keep_every)
                ]

        # 전역 팔레트로 색상 최적화
        optimized_frames = self.optimize_colors(num_colors, use_global_palette=True)

        # 프레임 지속 시간 계산 (밀리초)
        frame_duration = 1000 / self.fps

        # GIF 저장
        imageio.imwrite(
            output_path,
            optimized_frames,
            duration=frame_duration,
            loop=0,  # 무한 반복
        )

        # 파일 정보 조회
        file_size_kb = output_path.stat().st_size / 1024
        file_size_mb = file_size_kb / 1024

        info = {
            "path": str(output_path),
            "size_kb": file_size_kb,
            "size_mb": file_size_mb,
            "dimensions": f"{self.width}x{self.height}",
            "frame_count": len(optimized_frames),
            "fps": self.fps,
            "duration_seconds": len(optimized_frames) / self.fps,
            "colors": num_colors,
        }

        # 결과 출력
        print(f"\n✓ GIF 생성 완료!")
        print(f"  경로: {output_path}")
        print(f"  크기: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
        print(f"  해상도: {self.width}x{self.height}")
        print(f"  프레임: {len(optimized_frames)}개 @ {self.fps} fps")
        print(f"  재생 시간: {info['duration_seconds']:.1f}초")
        print(f"  색상 수: {num_colors}")

        # 크기 관련 안내
        if optimize_for_emoji:
            print(f"  이모지 최적화 적용 (128x128, 색상 감소)")
        if file_size_mb > 1.0:
            print(f"\n  참고: 파일 크기가 큽니다 ({file_size_kb:.1f} KB)")
            print("  프레임 수 감소, 해상도 축소, 또는 색상 수 감소를 고려하세요")

        return info

    def clear(self):
        """모든 프레임을 초기화합니다 (여러 GIF 생성 시 유용)."""
        self.frames = []
