---
name: data-visualization
description: Python(matplotlib, seaborn, plotly)으로 효과적인 데이터 시각화 생성. 차트 작성, 데이터셋에 적합한 차트 유형 선택, 출판 품질의 그래프 제작, 접근성 및 색상 이론 등 디자인 원칙 적용 시 사용합니다.
---

# 데이터 시각화 스킬

효과적인 데이터 시각화를 위한 차트 선택 가이드, Python 시각화 코드 패턴, 디자인 원칙, 접근성 고려사항을 제공합니다.

## 차트 선택 가이드

### 데이터 관계에 따른 선택

| 표현하려는 것 | 최적 차트 | 대안 |
|------------|---------|------|
| **시간에 따른 추세** | 꺾은선 차트 | 영역 차트 (누적 또는 구성 표현 시) |
| **범주 간 비교** | 수직 막대 차트 | 수평 막대 (범주가 많을 때), 롤리팝 차트 |
| **순위** | 수평 막대 차트 | 점 플롯, 기울기 차트 (두 기간 비교 시) |
| **전체 대비 부분 구성** | 누적 막대 차트 | 트리맵 (계층 구조), 와플 차트 |
| **시간에 따른 구성 변화** | 누적 영역 차트 | 100% 누적 막대 (비율 집중 시) |
| **분포** | 히스토그램 | 박스 플롯 (그룹 비교), 바이올린 플롯, 스트립 플롯 |
| **상관관계 (2변수)** | 산점도 | 버블 차트 (크기로 3번째 변수 추가) |
| **상관관계 (다변수)** | 히트맵 (상관 행렬) | 페어 플롯 |
| **지리적 패턴** | 코로플레스 지도 | 버블 지도, 헥스 지도 |
| **흐름/프로세스** | 생키 다이어그램 | 퍼널 차트 (순차적 단계) |
| **관계 네트워크** | 네트워크 그래프 | 코드 다이어그램 |
| **목표 대비 성과** | 불릿 차트 | 게이지 (단일 KPI만) |
| **여러 KPI 동시 표시** | 스몰 멀티플 | 개별 차트 대시보드 |

### 특정 차트를 사용하지 말아야 할 때

- **파이 차트**: 범주가 6개 미만이고 정확한 비율보다 대략적인 비교가 중요할 때만 사용. 사람은 각도 비교에 서툼. 대신 막대 차트 사용.
- **3D 차트**: 절대 사용 금지. 인식을 왜곡하고 정보를 추가하지 않음.
- **이중 축 차트**: 신중하게 사용. 상관관계를 암시하여 오해를 줄 수 있음. 사용 시 두 축 모두 명확히 레이블.
- **누적 막대 (범주 많을 때)**: 중간 세그먼트 비교 어려움. 스몰 멀티플 또는 그룹 막대 사용.
- **도넛 차트**: 파이 차트보다 약간 낫지만 동일한 근본적 문제. 단일 KPI 표시에만 사용.

## Python 시각화 코드 패턴

### 설정 및 스타일

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

# 전문적인 스타일 설정
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 150,
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
})

# 색맹 친화적 팔레트
PALETTE_CATEGORICAL = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860']
PALETTE_SEQUENTIAL = 'YlOrRd'
PALETTE_DIVERGING = 'RdBu_r'
```

### 꺾은선 차트 (시계열)

```python
fig, ax = plt.subplots(figsize=(10, 6))

for label, group in df.groupby('category'):
    ax.plot(group['date'], group['value'], label=label, linewidth=2)

ax.set_title('범주별 지표 추세', fontweight='bold')
ax.set_xlabel('날짜')
ax.set_ylabel('값')
ax.legend(loc='upper left', frameon=True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# x축 날짜 형식 지정
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig('trend_chart.png', dpi=150, bbox_inches='tight')
```

### 막대 차트 (비교)

```python
fig, ax = plt.subplots(figsize=(10, 6))

# 읽기 쉽게 값 기준 정렬
df_sorted = df.sort_values('metric', ascending=True)

bars = ax.barh(df_sorted['category'], df_sorted['metric'], color=PALETTE_CATEGORICAL[0])

# 값 레이블 추가
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{width:,.0f}', ha='left', va='center', fontsize=10)

ax.set_title('범주별 지표 (순위)', fontweight='bold')
ax.set_xlabel('지표 값')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('bar_chart.png', dpi=150, bbox_inches='tight')
```

### 히스토그램 (분포)

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['value'], bins=30, color=PALETTE_CATEGORICAL[0], edgecolor='white', alpha=0.8)

# 평균 및 중앙값 선 추가
mean_val = df['value'].mean()
median_val = df['value'].median()
ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'평균: {mean_val:,.1f}')
ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'중앙값: {median_val:,.1f}')

ax.set_title('값 분포', fontweight='bold')
ax.set_xlabel('값')
ax.set_ylabel('빈도')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('histogram.png', dpi=150, bbox_inches='tight')
```

### 히트맵

```python
fig, ax = plt.subplots(figsize=(10, 8))

# 히트맵 형식으로 데이터 피벗
pivot = df.pivot_table(index='row_dim', columns='col_dim', values='metric', aggfunc='sum')

sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd',
            linewidths=0.5, ax=ax, cbar_kws={'label': '지표 값'})

ax.set_title('행/열 차원별 지표', fontweight='bold')
ax.set_xlabel('열 차원')
ax.set_ylabel('행 차원')

plt.tight_layout()
plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
```

### 스몰 멀티플 (Small Multiples)

```python
categories = df['category'].unique()
n_cats = len(categories)
n_cols = min(3, n_cats)
n_rows = (n_cats + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows), sharex=True, sharey=True)
axes = axes.flatten() if n_cats > 1 else [axes]

for i, cat in enumerate(categories):
    ax = axes[i]
    subset = df[df['category'] == cat]
    ax.plot(subset['date'], subset['value'], color=PALETTE_CATEGORICAL[i % len(PALETTE_CATEGORICAL)])
    ax.set_title(cat, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# 빈 서브플롯 숨기기
for j in range(i+1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle('범주별 추세', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('small_multiples.png', dpi=150, bbox_inches='tight')
```

### 숫자 형식 헬퍼

```python
def format_number(val, format_type='number'):
    """차트 레이블용 숫자 형식 지정."""
    if format_type == 'currency':
        if abs(val) >= 1e9:
            return f'${val/1e9:.1f}B'
        elif abs(val) >= 1e6:
            return f'${val/1e6:.1f}M'
        elif abs(val) >= 1e3:
            return f'${val/1e3:.1f}K'
        else:
            return f'${val:,.0f}'
    elif format_type == 'percent':
        return f'{val:.1f}%'
    elif format_type == 'number':
        if abs(val) >= 1e9:
            return f'{val/1e9:.1f}B'
        elif abs(val) >= 1e6:
            return f'{val/1e6:.1f}M'
        elif abs(val) >= 1e3:
            return f'{val/1e3:.1f}K'
        else:
            return f'{val:,.0f}'
    return str(val)

# 축 포매터와 함께 사용
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format_number(x, 'currency')))
```

### Plotly 인터랙티브 차트

```python
import plotly.express as px
import plotly.graph_objects as go

# 간단한 인터랙티브 꺾은선 차트
fig = px.line(df, x='date', y='value', color='category',
              title='인터랙티브 지표 추세',
              labels={'value': '지표 값', 'date': '날짜'})
fig.update_layout(hovermode='x unified')
fig.write_html('interactive_chart.html')
fig.show()

# 호버 데이터 포함 인터랙티브 산점도
fig = px.scatter(df, x='metric_a', y='metric_b', color='category',
                 size='size_metric', hover_data=['name', 'detail_field'],
                 title='상관관계 분석')
fig.show()
```

## 디자인 원칙

### 색상

- **색상을 목적 있게 사용**: 색상은 데이터를 인코딩해야지 장식이 되어선 안 됨
- **핵심 스토리 강조**: 핵심 인사이트에 강한 액센트 색상 사용; 나머지는 회색 처리
- **순차적 데이터**: 순서 있는 값에는 단일 색조 그라디언트(밝음→어두움) 사용
- **발산형 데이터**: 의미 있는 중심점이 있는 데이터에는 중립 중간점을 가진 이중 색조 그라디언트 사용
- **범주형 데이터**: 뚜렷한 색조 사용, 혼란스러워지기 전 최대 6~8개
- **적/녹 단독 사용 금지**: 남성의 8%가 적녹 색맹. 주요 쌍으로 파랑/주황 사용

### 타이포그래피

- **제목은 인사이트 표현**: "매출 전년 대비 23% 성장"이 "월별 매출"보다 좋음
- **부제목은 컨텍스트 추가**: 날짜 범위, 적용된 필터, 데이터 소스
- **축 레이블은 읽기 쉽게**: 가능하면 90도 회전 금지. 대신 축약하거나 줄바꿈
- **데이터 레이블은 정밀도 추가**: 모든 막대가 아닌 핵심 포인트에만 사용
- **주석으로 강조**: 텍스트 주석으로 특정 포인트 호출

### 레이아웃

- **차트 잡음 줄이기**: 정보를 담지 않는 격자선, 테두리, 배경 제거
- **의미 있게 정렬**: 자연스러운 순서(월, 단계)가 없으면 알파벳이 아닌 값 기준으로 범주 정렬
- **적절한 종횡비**: 시계열은 세로보다 가로가 길게 (3:1 ~ 2:1); 비교는 더 정사각형에 가깝게
- **여백은 좋은 것**: 차트를 빽빽하게 채우지 말 것. 각 시각화에 충분한 공간 제공

### 정확성

- **막대 차트는 항상 0에서 시작**: 예외 없음. 95에서 100까지 막대는 5% 차이를 과장함
- **꺾은선 차트는 0이 아닌 기준선 가능**: 변동 범위가 의미 있을 때
- **패널 간 일관된 스케일**: 여러 차트를 비교할 때 동일한 축 범위 사용
- **불확실성 표시**: 데이터가 불확실할 때 오차 막대, 신뢰 구간 또는 범위 표시
- **축에 레이블 필수**: 독자가 숫자의 의미를 추측하게 만들지 말 것

## 접근성 고려사항

### 색맹

- 데이터 계열을 구분하기 위해 색상에만 의존하지 말 것
- 패턴 채우기, 다른 선 스타일(실선, 파선, 점선), 또는 직접 레이블 추가
- 색맹 시뮬레이터로 테스트 (예: Coblis, Sim Daltonism)
- 색맹 친화적 팔레트 사용: `sns.color_palette("colorblind")`

### 스크린 리더

- 차트의 핵심 발견을 설명하는 대체 텍스트(alt text) 포함
- 시각화와 함께 데이터 표 대안 제공
- 의미 있는 제목과 레이블 사용

### 일반 접근성

- 데이터 요소와 배경 간 충분한 대비
- 레이블 최소 10pt, 제목 최소 12pt 텍스트 크기
- 공간적 위치만으로 정보 전달 금지 (레이블 추가)
- 인쇄 고려: 흑백으로도 차트가 동작하는가?

### 접근성 체크리스트

시각화 공유 전:
- [ ] 색상 없이도 차트 동작 (패턴, 레이블, 또는 선 스타일로 계열 구분)
- [ ] 표준 확대 수준에서 텍스트 읽기 가능
- [ ] 제목이 데이터가 아닌 인사이트를 설명
- [ ] 축에 단위 포함한 레이블 있음
- [ ] 범례가 명확하고 데이터를 가리지 않는 위치에 있음
- [ ] 데이터 소스와 날짜 범위 명시
