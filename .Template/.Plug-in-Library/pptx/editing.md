# 프레젠테이션 편집

## 템플릿 기반 워크플로우

기존 프레젠테이션을 템플릿으로 사용할 때:

1. **기존 슬라이드 분석**:
   ```bash
   python scripts/thumbnail.py template.pptx
   python -m markitdown template.pptx
   ```
   `thumbnails.jpg`에서 레이아웃을 확인하고, markitdown 출력으로 플레이스홀더 텍스트를 확인하세요.

2. **슬라이드 매핑 계획**: 각 콘텐츠 섹션에 맞는 템플릿 슬라이드를 선택하세요.

   ⚠️ **다양한 레이아웃을 사용하세요** — 단조로운 프레젠테이션은 흔한 실패 사례입니다. 단순 제목+불릿 슬라이드를 기본값으로 사용하지 마세요. 다음을 적극 활용하세요:
   - 다단 레이아웃 (2단, 3단)
   - 이미지 + 텍스트 조합
   - 전체 블리드 이미지 + 텍스트 오버레이
   - 인용 또는 콜아웃 슬라이드
   - 섹션 구분자
   - 통계/숫자 콜아웃
   - 아이콘 그리드 또는 아이콘 + 텍스트 행

   **피해야 할 것:** 모든 슬라이드에 같은 텍스트 중심 레이아웃 반복 사용.

   콘텐츠 유형에 맞는 레이아웃 스타일을 매칭하세요 (예: 핵심 포인트 → 불릿 슬라이드, 팀 정보 → 다단, 추천사 → 인용 슬라이드).

3. **압축 해제**: `python scripts/office/unpack.py template.pptx unpacked/`

4. **프레젠테이션 구성** (서브에이전트 없이 직접 처리):
   - 불필요한 슬라이드 삭제 (`<p:sldIdLst>`에서 제거)
   - 재사용할 슬라이드 복제 (`add_slide.py`)
   - `<p:sldIdLst>`에서 슬라이드 순서 변경
   - **5단계 진행 전에 모든 구조 변경 완료**

5. **내용 편집**: 각 `slide{N}.xml`에서 텍스트를 업데이트하세요.
   **가능하면 서브에이전트 사용** — 슬라이드는 별도 XML 파일이므로 서브에이전트가 병렬로 편집할 수 있습니다.

6. **정리**: `python scripts/clean.py unpacked/`

7. **재압축**: `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

---

## 스크립트

| 스크립트 | 역할 |
|--------|---------|
| `unpack.py` | PPTX 압축 해제 및 XML 포맷팅 |
| `add_slide.py` | 슬라이드 복제 또는 레이아웃으로 생성 |
| `clean.py` | 고아 파일 제거 |
| `pack.py` | 검증과 함께 재압축 |
| `thumbnail.py` | 슬라이드 시각적 그리드 생성 |

### unpack.py

```bash
python scripts/office/unpack.py input.pptx unpacked/
```

PPTX를 추출하고 XML을 예쁘게 포맷팅하며 스마트 따옴표를 이스케이프 처리합니다.

### add_slide.py

```bash
python scripts/add_slide.py unpacked/ slide2.xml      # 슬라이드 복제
python scripts/add_slide.py unpacked/ slideLayout2.xml # 레이아웃으로 생성
```

`<p:sldIdLst>`의 원하는 위치에 추가할 `<p:sldId>`를 출력합니다.

### clean.py

```bash
python scripts/clean.py unpacked/
```

`<p:sldIdLst>`에 없는 슬라이드, 참조되지 않는 미디어, 고아 rels 파일을 제거합니다.

### pack.py

```bash
python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

검증, 수리, XML 압축, 스마트 따옴표 재인코딩을 수행합니다.

### thumbnail.py

```bash
python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]
```

슬라이드 파일명(예: slide1.xml)을 레이블로 사용하여 `thumbnails.jpg`를 생성합니다. 기본 3열, 그리드당 최대 12개.

**템플릿 분석 전용** (레이아웃 선택용). 시각적 QA에는 `soffice` + `pdftoppm`으로 고해상도 개별 슬라이드 이미지를 생성하세요 — SKILL.md 참조.

---

## 슬라이드 작업

슬라이드 순서는 `ppt/presentation.xml` → `<p:sldIdLst>`에 있습니다.

**순서 변경**: `<p:sldId>` 요소의 순서를 변경하세요.

**삭제**: `<p:sldId>`를 제거한 후 `clean.py`를 실행하세요.

**추가**: `add_slide.py`를 사용하세요. 슬라이드 파일을 수동으로 복사하지 마세요 — 스크립트가 노트 참조, Content_Types.xml, 관계 ID를 처리합니다. 수동 복사 시 이 항목들이 누락됩니다.

---

## 내용 편집

**서브에이전트:** 가능하면 여기서 사용하세요 (4단계 완료 후). 각 슬라이드는 별도 XML 파일이므로 서브에이전트가 병렬로 편집할 수 있습니다. 서브에이전트 프롬프트에 다음을 포함하세요:
- 편집할 슬라이드 파일 경로
- **"모든 변경에 Edit 도구 사용"**
- 아래의 서식 규칙과 흔한 함정

각 슬라이드에 대해:
1. 슬라이드 XML 읽기
2. 모든 플레이스홀더 내용 식별 — 텍스트, 이미지, 차트, 아이콘, 캡션
3. 각 플레이스홀더를 최종 내용으로 교체

**sed나 Python 스크립트 대신 Edit 도구를 사용하세요.** Edit 도구는 무엇을 어디서 교체할지 구체적으로 지정하도록 강제하여 더 높은 신뢰성을 제공합니다.

### 서식 규칙

- **모든 헤더, 소제목, 인라인 레이블을 굵게**: `<a:rPr>`에 `b="1"` 사용. 다음 항목 포함:
  - 슬라이드 제목
  - 슬라이드 내 섹션 헤더
  - 줄 시작 부분의 인라인 레이블 (예: "상태:", "설명:")
- **유니코드 불릿(•) 절대 사용 금지**: `<a:buChar>` 또는 `<a:buAutoNum>`으로 올바른 목록 서식 사용
- **불릿 일관성**: 레이아웃에서 상속되도록 하세요. `<a:buChar>` 또는 `<a:buNone>`만 지정하세요.

---

## 흔한 함정

### 템플릿 적용

소스 콘텐츠가 템플릿보다 항목 수가 적을 때:
- **여분의 요소를 완전히 제거하세요** (이미지, 도형, 텍스트 박스) — 텍스트만 지우면 안 됩니다
- 텍스트 내용을 지운 후 고아 시각 요소가 있는지 확인하세요
- 시각적 QA를 실행하여 항목 수 불일치를 잡아내세요

텍스트를 길이가 다른 내용으로 교체할 때:
- **짧은 교체**: 보통 안전합니다
- **긴 교체**: 오버플로우 또는 예상치 못한 줄 바꿈이 생길 수 있습니다
- 텍스트 변경 후 시각적 QA로 테스트하세요
- 템플릿 디자인 제약에 맞게 내용을 줄이거나 분리하는 것을 고려하세요

**템플릿 슬롯 ≠ 소스 항목**: 템플릿에 팀원 4명이 있는데 소스에 사용자 3명이 있다면, 4번째 팀원의 전체 그룹(이미지 + 텍스트 박스)을 삭제하고 텍스트만 지우면 안 됩니다.

### 다중 항목 콘텐츠

소스에 여러 항목(번호 목록, 여러 섹션)이 있으면 각각 별도의 `<a:p>` 요소로 만드세요 — **하나의 문자열로 이어 붙이면 안 됩니다**.

**❌ 잘못된 예** — 모든 항목이 하나의 단락에:
```xml
<a:p>
  <a:r><a:rPr .../><a:t>1단계: 첫 번째 작업. 2단계: 두 번째 작업.</a:t></a:r>
</a:p>
```

**✅ 올바른 예** — 굵은 헤더가 있는 별도 단락:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>1단계</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>첫 번째 작업.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>2단계</a:t></a:r>
</a:p>
<!-- 패턴 계속 -->
```

줄 간격을 유지하려면 원본 단락의 `<a:pPr>`을 복사하세요. 헤더에는 `b="1"` 사용.

### 스마트 따옴표

unpack/pack에서 자동으로 처리됩니다. 하지만 Edit 도구는 스마트 따옴표를 ASCII로 변환합니다.

**새 텍스트에 따옴표를 추가할 때는 XML 엔티티를 사용하세요:**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

| 문자 | 이름 | 유니코드 | XML 엔티티 |
|-----------|------|---------|------------|
| `"` | 왼쪽 이중 따옴표 | U+201C | `&#x201C;` |
| `"` | 오른쪽 이중 따옴표 | U+201D | `&#x201D;` |
| `'` | 왼쪽 단일 따옴표 | U+2018 | `&#x2018;` |
| `'` | 오른쪽 단일 따옴표 | U+2019 | `&#x2019;` |

### 기타

- **공백**: 앞뒤 공백이 있는 `<a:t>`에는 `xml:space="preserve"` 사용
- **XML 파싱**: 네임스페이스를 손상시키는 `xml.etree.ElementTree` 대신 `defusedxml.minidom` 사용
