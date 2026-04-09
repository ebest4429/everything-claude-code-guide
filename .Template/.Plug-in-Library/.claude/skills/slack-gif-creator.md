---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

Slack에 최적화된 애니메이션 GIF를 제작하기 위한 유틸리티 및 지식을 제공하는 툴킷입니다.

## Slack 요구사항

**크기:**
- 이모지 GIF: 128x128 (권장)
- 메시지 GIF: 480x480

**파라미터:**
- FPS: 10~30 (낮을수록 파일 크기 감소)
- 색상 수: 48~128 (적을수록 파일 크기 감소)
- 재생 시간: 이모지 GIF는 3초 이내 권장

## 기본 워크플로우

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 빌더 생성
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 프레임 생성
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # PIL 기본 도형으로 애니메이션 그리기
    # (원, 다각형, 선 등)

    builder.add_frame(frame)

# 3. 최적화 저장
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 그래픽 그리기

### 사용자 업로드 이미지 활용
사용자가 이미지를 업로드한 경우, 다음 중 어떤 용도인지 판단합니다:
- **직접 사용** (예: "이걸 애니메이션으로 만들어", "프레임으로 쪼개줘")
- **참고용** (예: "이런 스타일로 만들어줘")

PIL로 이미지 불러오기:
```python
from PIL import Image

uploaded = Image.open('file.png')
# 직접 사용하거나, 색상/스타일 참고용으로만 사용
```

### 처음부터 그리기
PIL ImageDraw 기본 도형으로 그래픽을 직접 생성합니다:

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# 원/타원
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 별, 삼각형, 임의 다각형
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 선
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 사각형
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**사용 금지:** 이모지 폰트(플랫폼 간 호환성 불안정), 이 스킬에 미리 패키징된 그래픽 가정.

### 그래픽 품질 높이기

그래픽은 단순한 수준이 아니라 세련되고 창의적으로 보여야 합니다:

**선 굵기를 늘리세요** — 외곽선과 선은 항상 `width=2` 이상으로 설정. 얇은 선(width=1)은 거칠고 조악해 보입니다.

**시각적 깊이 추가:**
- 배경에 그라데이션 사용 (`create_gradient_background`)
- 여러 도형을 겹쳐 복잡성 표현 (예: 큰 별 안에 작은 별)

**도형을 더 흥미롭게:**
- 단순한 원 대신 하이라이트, 링, 패턴을 추가
- 별에 글로우 효과 추가 (반투명한 더 큰 버전을 뒤에 배치)
- 여러 도형 조합 (별 + 스파클, 원 + 링)

**색상에 신경 쓰기:**
- 선명하고 보색 관계의 색상 사용
- 대비 추가 (밝은 도형에 어두운 외곽선, 어두운 도형에 밝은 외곽선)
- 전체 구성 고려

**복잡한 도형** (하트, 눈꽃송이 등):
- 다각형과 타원의 조합 사용
- 대칭을 위해 좌표를 신중하게 계산
- 디테일 추가 (하트에 하이라이트 곡선, 눈꽃에 세밀한 가지)

창의적이고 세밀하게 작업하세요! 좋은 Slack GIF는 임시 그래픽이 아닌 완성도 높은 결과물이어야 합니다.

## 사용 가능한 유틸리티

### GIFBuilder (`core.gif_builder`)
프레임을 조합하고 Slack에 최적화합니다:
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # PIL Image 추가
builder.add_frames(frames)  # 프레임 리스트 추가
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### Validators (`core.validators`)
GIF가 Slack 요구사항을 충족하는지 확인합니다:
```python
from core.validators import validate_gif, is_slack_ready

# 상세 검증
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# 빠른 확인
if is_slack_ready('my.gif'):
    print("준비 완료!")
```

### 이징 함수 (`core.easing`)
선형 움직임 대신 부드러운 동작을 구현합니다:
```python
from core.easing import interpolate

# 진행률 0.0 ~ 1.0
t = i / (num_frames - 1)

# 이징 적용
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# 사용 가능: linear, ease_in, ease_out, ease_in_out,
#           bounce_out, elastic_out, back_out
```

### 프레임 헬퍼 (`core.frame_composer`)
자주 사용하는 기능을 편리하게 제공합니다:
```python
from core.frame_composer import (
    create_blank_frame,         # 단색 배경
    create_gradient_background,  # 세로 그라데이션
    draw_circle,                # 원 그리기 헬퍼
    draw_text,                  # 간단한 텍스트 렌더링
    draw_star                   # 5각 별 그리기
)
```

## 애니메이션 개념

### 흔들기/진동
위치를 진동시켜 오프셋을 만듭니다:
- `math.sin()` 또는 `math.cos()`를 프레임 인덱스와 함께 사용
- 자연스러운 느낌을 위해 작은 랜덤 변화 추가
- x 및/또는 y 위치에 적용

### 맥동/심장박동
오브젝트 크기를 리드미컬하게 변화시킵니다:
- 부드러운 맥동을 위해 `math.sin(t * frequency * 2 * math.pi)` 사용
- 심장박동: 두 번의 빠른 맥동 후 일시 정지 (사인파 조정)
- 기본 크기의 0.8~1.2 사이로 스케일 조정

### 바운스
오브젝트가 떨어졌다가 튕깁니다:
- 착지 시 `interpolate()`에 `easing='bounce_out'` 사용
- 떨어질 때 `easing='ease_in'` 사용 (가속)
- 매 프레임마다 y 속도를 증가시켜 중력 구현

### 회전/스핀
오브젝트를 중심점 기준으로 회전시킵니다:
- PIL: `image.rotate(angle, resample=Image.BICUBIC)`
- 흔들림 효과: 선형 대신 사인파를 각도에 사용

### 페이드 인/아웃
서서히 나타나거나 사라집니다:
- RGBA 이미지 생성 후 알파 채널 조정
- 또는 `Image.blend(image1, image2, alpha)` 사용
- 페이드 인: 알파 0→1
- 페이드 아웃: 알파 1→0

### 슬라이드
화면 밖에서 지정 위치로 이동합니다:
- 시작 위치: 프레임 경계 밖
- 종료 위치: 목표 위치
- 부드러운 정지를 위해 `interpolate()`에 `easing='ease_out'` 사용
- 오버슈트 효과: `easing='back_out'` 사용

### 줌
줌 효과를 위해 스케일 및 위치를 조정합니다:
- 줌 인: 0.1 → 2.0으로 스케일, 중앙 크롭
- 줌 아웃: 2.0 → 1.0으로 스케일
- 극적인 효과를 위해 모션 블러 추가 가능 (PIL 필터)

### 폭발/파티클 버스트
파티클이 사방으로 퍼져나가는 효과:
- 랜덤 각도와 속도로 파티클 생성
- 각 파티클 업데이트: `x += vx`, `y += vy`
- 중력 추가: `vy += gravity_constant`
- 시간이 지남에 따라 파티클 페이드 아웃 (알파 감소)

## 최적화 전략

파일 크기를 줄여달라는 요청을 받은 경우에만 다음 방법 중 일부를 적용합니다:

1. **프레임 수 줄이기** — FPS 낮추기 (20 대신 10) 또는 재생 시간 단축
2. **색상 수 줄이기** — `num_colors=48` (128 대신)
3. **크기 줄이기** — 480x480 대신 128x128
4. **중복 제거** — `save()`에서 `remove_duplicates=True`
5. **이모지 모드** — `optimize_for_emoji=True`로 자동 최적화

```python
# 이모지용 최대 최적화
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 철학

이 스킬이 제공하는 것:
- **지식**: Slack 요구사항 및 애니메이션 개념
- **유틸리티**: GIFBuilder, 검증기, 이징 함수
- **유연성**: PIL 기본 도형을 활용한 애니메이션 로직 구현

제공하지 않는 것:
- 고정된 애니메이션 템플릿이나 미리 만들어진 함수
- 이모지 폰트 렌더링 (플랫폼 간 호환성 불안정)
- 스킬에 내장된 미리 패키징된 그래픽 라이브러리

**사용자 업로드 이미지 관련**: 이 스킬에는 미리 만들어진 그래픽이 없지만, 사용자가 이미지를 업로드하면 PIL로 불러와 작업할 수 있습니다 — 직접 사용할지, 참고용으로만 활용할지는 요청 내용을 보고 판단합니다.

창의적으로 접근하세요! 개념을 조합하고 (바운스 + 회전, 맥동 + 슬라이드 등) PIL의 모든 기능을 활용하세요.

## 의존성

```bash
pip install pillow imageio numpy
```
