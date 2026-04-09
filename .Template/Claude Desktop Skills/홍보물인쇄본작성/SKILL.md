---
name: realestate-flyer
description: >
  매물정보.xlsx 파일의 매물정보 시트를 읽어 확인 체크박스가 체크되지 않은 매물에 대해
  hwpx 형식의 홍보 인쇄물을 매물별로 개별 생성합니다.
  사용자가 "매물 홍보물", "hwpx 생성", "매물 인쇄물", "부동산 전단지", "매물정보 파일로 문서 생성" 등을 언급하면
  반드시 이 스킬을 사용하세요. xlsx 매물 데이터에서 hwpx 파일 생성 작업 시 항상 이 스킬을 참조하세요.
---

# 부동산 매물 홍보 인쇄물 생성 스킬

## 개요

매물정보.xlsx의 **매물정보** 시트에서 **확인** 필드가 비어 있는(미확인) 매물을 추출하여,
샘플 hwpx 형식과 동일한 레이아웃으로 매물별 개별 hwpx 파일을 생성합니다.
생성 완료 후 **매물정보.xlsx의 확인 컬럼이 자동으로 '완료'로 업데이트**됩니다.

---

## 확인 컬럼 규칙

**확인** 컬럼은 처리 완료 여부를 나타내며, 실제 엑셀 파일에서는 **텍스트 값**으로 관리됩니다.

| 확인 컬럼 값 | 의미 | 처리 여부 |
|---|---|---|
| `'완료'` (텍스트) | 인쇄물 생성 완료 | ❌ 제외 (스킵) |
| 빈 셀 (`nan`) | 아직 미처리 | ✅ 포함 (생성 대상) |
| `False` / `0` / `''` | 미처리 (Boolean 방식) | ✅ 포함 (생성 대상) |

> **주의**: 엑셀에서 체크박스(Boolean True/False) 방식 대신 **'완료' 텍스트 입력 방식**을 사용합니다.
> 스크립트 필터는 `'완료'`가 아닌 모든 값(nan, false, 0, 빈문자열)을 미확인으로 처리합니다.

### 필터 로직

```python
# '완료' 텍스트가 없는 행 = 미확인 매물 (생성 대상)
미확인 = df[df['확인'].astype(str).str.lower().isin(['false', '0', 'nan', ''])]
# → '완료' 텍스트가 있는 행은 자동으로 제외됨
```

---

## 워크플로우

1. xlsx 파일 읽기 → 미확인 매물 필터링
2. 금액 포맷 변환 (rules 참조)
3. hwpx 템플릿 XML 기반으로 각 매물별 파일 생성
4. 파일 출력 → `/mnt/user-data/outputs/` 에 저장

---

## 실행 방법

```bash
python3 /path/to/skill/scripts/generate_flyers.py \
  --xlsx <매물정보.xlsx 경로> \
  --template <sample_apartment.hwpx 경로> \
  --outdir <출력 디렉토리>
```

또는 Python에서 직접 호출:
```python
# scripts/generate_flyers.py 실행
```

---

## 금액 표시 규칙

| 조건 | 표시 | 예시 |
|------|------|------|
| 10,000 이상 (억 단위) | N억 | 80,000 → 8억 |
| 10,000 이상 (억+천 단위) | N억 N천 | 15,000 → 1억5천 |
| 10,000 미만 (천 단위) | N천 | 5,000 → 5천 |
| 월세 | 보증금/월세 (원숫자) | 보증금 5,000 / 월세 100 → 5000/100 |

**주의**: 월세는 억/천 변환 없이 원래 숫자 그대로 표시 (예: `5000/100`)

### 금액 변환 함수 로직

```python
def format_price(value):
    """매매가/보증금/전세 금액 포맷"""
    if pd.isna(value):
        return ""
    v = int(value)
    eok = v // 10000
    cheon = (v % 10000) // 1000
    if eok > 0 and cheon > 0:
        return f"{eok}억{cheon}천"
    elif eok > 0:
        return f"{eok}억"
    elif cheon > 0:
        return f"{cheon}천"
    else:
        return str(v)

def format_price_display(row):
    """유형에 따른 가격 표시"""
    유형 = row['유형']
    if 유형 == '매매':
        return format_price(row['매매가격'])
    elif 유형 == '전세':
        return format_price(row['보증금'])
    elif 유형 == '월세':
        # 월세는 숫자 그대로 (변환 없음)
        보증금 = int(row['보증금']) if pd.notna(row['보증금']) else 0
        월세 = int(row['월세']) if pd.notna(row['월세']) else 0
        return f"{보증금}/{월세}"
    return ""
```

---

## hwpx 파일 구조

hwpx는 ZIP 파일이며 내부 구성:
```
파일.hwpx
├── mimetype
├── version.xml
├── settings.xml
├── Contents/
│   ├── header.xml   ← 폰트/스타일 정의 (템플릿에서 복사)
│   ├── section0.xml ← 실제 문서 내용 (6행 테이블)
│   └── content.hpf
├── Preview/
│   ├── PrvText.txt  ← 미리보기 텍스트
│   └── PrvImage.png ← 미리보기 이미지 (빈 PNG 사용)
└── META-INF/
    ├── container.xml
    ├── container.rdf
    └── manifest.xml
```

## 테이블 구조 (6행 × 1열)

| 행 | 내용 | 스타일 | borderFillIDRef |
|----|------|--------|-----------------|
| 0 | 단지명 | 대형 굵은 글씨 (charPrIDRef=12) | 5 (상하단 없음→위만) |
| 1 | 면적 | 중간 글씨 (charPrIDRef=8) | 6 (테두리 없음) |
| 2 | 유형 (매 매 / 전 세 / 월 세) | 중간 글씨 (charPrIDRef=11) | 6 |
| 3 | 가격 | 중간 글씨 (charPrIDRef=8) | 6 |
| 4 | 비고 | 작은 글씨 (charPrIDRef=9) | 3 (전체 테두리) |
| 5 | 공인중개사 정보 | 작은 글씨 (charPrIDRef=9) | 3 |

**유형 표시**: 글자 사이 공백 삽입 (매 매 / 전 세 / 월 세)

---

## 샘플 선택기

샘플 파일명으로 인쇄물 유형이 자동 결정됩니다.

파일명은 **한글(샘플_xxx)** 또는 **영문(sample_xxx)** 모두 지원됩니다.

| 샘플 파일명 (한글) | 샘플 파일명 (영문) | 인쇄물 유형 | 상태 |
|---|---|---|---|
| `샘플_아파트.hwpx` | `sample_apartment.hwpx` | 아파트 | ✅ 제공 |
| `샘플_건물.hwpx` | `sample_store.hwpx` | 상가/건물 | ✅ 제공 |
| `샘플_토지.hwpx` | `sample_land.hwpx` | 토지 | ✅ 제공 |
| `샘플_오피스텔.hwpx` | `sample_officetel.hwpx` | 오피스텔 | 추후 추가 |
| `샘플_빌라.hwpx` | `sample_villa.hwpx` | 빌라 | 추후 추가 |

새 샘플 추가 시 `scripts/generate_flyers.py` 상단의 `SAMPLE_REGISTRY` 딕셔너리에 파일명→유형명을 등록하면 됩니다 (한글/영문 각각).

사용 가능한 템플릿 목록 확인:
```bash
python3 scripts/generate_flyers.py --list-templates ./assets/
```

## 공인중개사 정보

샘플 파일 기준으로 고정 표시:
```
크로바공인중개사사무소
```

> 실제 운용 시 사용자가 원하는 사무소명으로 변경 가능.
> 스킬 실행 전 사용자에게 공인중개사 사무소명 확인 권장.

## 수정 이력

- **v1.3**: hwpx 생성 완료 후 매물정보.xlsx의 확인 컬럼을 '완료'로 자동 기입 기능 추가
- **v1.2**: 확인 컬럼 규칙 문서화 ('완료' 텍스트 방식 명시), 한글 샘플 파일명 지원 추가
- **v1.1**: 비고 텍스트 색상 검정(#000000) 처리, 비고 위쪽 라인 제거(borderFillIDRef=4), 샘플 선택기 구조 추가

---

## 스크립트 위치

- `scripts/generate_flyers.py` — 메인 생성 스크립트
- `assets/sample_apartment.hwpx` — 원본 템플릿 파일

## 참고

- 상세 XML 구조: `references/hwpx_structure.md`
- 스크립트 상세 로직: `scripts/generate_flyers.py` 내 주석 참조