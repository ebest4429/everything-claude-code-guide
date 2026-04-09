---
name: docx
description: "사용자가 Word 문서(.docx 파일)를 생성, 읽기, 편집 또는 조작하려 할 때 이 스킬을 사용합니다. 트리거 조건: '워드 문서', 'word doc', '.docx' 언급 또는 목차, 제목, 페이지 번호, 레터헤드 등 서식이 있는 전문 문서 제작 요청. 또한 .docx 파일에서 콘텐츠를 추출하거나 재구성할 때, 문서에 이미지를 삽입하거나 교체할 때, Word 파일에서 찾기·바꾸기 수행 시, 변경 내용 추적 또는 주석 작업 시, 콘텐츠를 세련된 Word 문서로 변환할 때 사용합니다. 사용자가 '보고서', '메모', '편지', '템플릿' 또는 유사한 결과물을 Word 또는 .docx 파일로 요청하는 경우에도 이 스킬을 사용합니다. PDF, 스프레드시트, Google Docs, 문서 생성과 관련 없는 일반 코딩 작업에는 사용하지 마세요."
license: 독점 소유. 전체 약관은 LICENSE.txt 참조
---

# DOCX 생성, 편집 및 분석

## 개요

.docx 파일은 XML 파일을 포함하는 ZIP 아카이브입니다.

## 빠른 참조

| 작업 | 접근 방법 |
|------|----------|
| 콘텐츠 읽기/분석 | `pandoc` 또는 원시 XML용 언팩 |
| 새 문서 생성 | `docx-js` 사용 — 아래 새 문서 생성 참조 |
| 기존 문서 편집 | 언팩 → XML 편집 → 리팩 — 아래 기존 문서 편집 참조 |

### .doc를 .docx로 변환

편집 전 레거시 `.doc` 파일을 먼저 변환해야 합니다:

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 콘텐츠 읽기

```bash
# 변경 내용 추적이 포함된 텍스트 추출
pandoc --track-changes=all document.docx -o output.md

# 원시 XML 접근
python scripts/office/unpack.py document.docx unpacked/
```

### 이미지로 변환

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 변경 내용 추적 승인

모든 변경 내용 추적을 승인한 깨끗한 문서 생성 (LibreOffice 필요):

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 새 문서 생성

JavaScript로 .docx 파일 생성 후 검증. 설치: `npm install -g docx`

### 설정
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 콘텐츠 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 검증
파일 생성 후 반드시 검증합니다. 검증 실패 시 언팩하고 XML을 수정한 후 리팩합니다.
```bash
python scripts/office/validate.py doc.docx
```

### 페이지 크기

```javascript
// 중요: docx-js 기본값은 A4이며 US Letter가 아님
// 일관된 결과를 위해 항상 페이지 크기를 명시적으로 설정할 것
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5인치 (DXA 단위)
        height: 15840   // 11인치 (DXA 단위)
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1인치 여백
    }
  },
  children: [/* 콘텐츠 */]
}]
```

**일반 페이지 크기 (DXA 단위, 1440 DXA = 1인치):**

| 용지 | 너비 | 높이 | 콘텐츠 너비 (1인치 여백) |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (기본) | 11,906 | 16,838 | 9,026 |

**가로 방향:** docx-js는 내부적으로 너비/높이를 교환하므로, 세로 방향 치수를 전달하고 교환은 자동 처리:
```javascript
size: {
  width: 12240,   // 짧은 변을 너비로 전달
  height: 15840,  // 긴 변을 높이로 전달
  orientation: PageOrientation.LANDSCAPE  // docx-js가 XML에서 교환 처리
},
// 콘텐츠 너비 = 15840 - 왼쪽 여백 - 오른쪽 여백 (긴 변 기준)
```

### 스타일 (내장 제목 재정의)

기본 폰트로 Arial 사용 (범용 지원). 가독성을 위해 제목은 검정색 유지.

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 기본 12pt
    paragraphStyles: [
      // 중요: 내장 스타일 재정의를 위해 정확한 ID 사용
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // TOC에 outlineLevel 필수
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### 목록 (유니코드 글머리 기호 절대 사용 금지)

```javascript
// ❌ 잘못된 방법 - 글머리 기호 문자 직접 삽입 금지
new Paragraph({ children: [new TextRun("• Item")] })  // 잘못됨
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // 잘못됨

// ✅ 올바른 방법 - LevelFormat.BULLET과 numbering config 사용
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ 각 reference는 독립적인 번호 매기기를 생성
// 같은 reference = 연속 (1,2,3 이후 4,5,6)
// 다른 reference = 재시작 (1,2,3 이후 다시 1,2,3)
```

### 표

**중요: 표에는 이중 너비 설정 필요** — 표의 `columnWidths`와 각 셀의 `width` 모두 설정. 두 가지 모두 없으면 일부 플랫폼에서 표가 올바르게 렌더링되지 않습니다.

```javascript
// 중요: 일관된 렌더링을 위해 항상 표 너비 설정
// 중요: 검정 배경 방지를 위해 ShadingType.CLEAR 사용 (SOLID 아님)
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 항상 DXA 사용 (퍼센트는 Google Docs에서 깨짐)
  columnWidths: [4680, 4680], // 표 너비의 합계와 일치해야 함 (DXA: 1440 = 1인치)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 각 셀에도 설정
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // SOLID 아닌 CLEAR
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 셀 패딩 (내부, 너비에 추가되지 않음)
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

**표 너비 계산:**

항상 `WidthType.DXA` 사용 — `WidthType.PERCENTAGE`는 Google Docs에서 깨집니다.

```javascript
// 표 너비 = columnWidths 합계 = 콘텐츠 너비
// 1인치 여백의 US Letter: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 표 너비의 합계와 일치해야 함
```

**너비 규칙:**
- **항상 `WidthType.DXA` 사용** — `WidthType.PERCENTAGE` 절대 사용 금지 (Google Docs 비호환)
- 표 너비는 `columnWidths` 합계와 같아야 함
- 셀 `width`는 해당 `columnWidth`와 일치해야 함
- 셀 `margins`는 내부 패딩 — 셀 너비에 추가되지 않고 콘텐츠 영역을 줄임
- 전체 너비 표: 콘텐츠 너비 사용 (페이지 너비 - 왼쪽 여백 - 오른쪽 여백)

### 이미지

```javascript
// 중요: type 매개변수 필수
new Paragraph({
  children: [new ImageRun({
    type: "png", // 필수: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // 세 가지 모두 필수
  })]
})
```

### 페이지 나누기

```javascript
// 중요: PageBreak는 반드시 Paragraph 안에 있어야 함
new Paragraph({ children: [new PageBreak()] })

// 또는 pageBreakBefore 사용
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### 하이퍼링크

```javascript
// 외부 링크
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// 내부 링크 (북마크 + 참조)
// 1. 목적지에 북마크 생성
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
// 2. 링크 연결
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter 1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### 각주

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### 탭 정지

```javascript
// 같은 줄에서 텍스트를 오른쪽 정렬 (예: 제목 반대편 날짜)
new Paragraph({
  children: [
    new TextRun("Company Name"),
    new TextRun("\tJanuary 2025"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// 점 리더 (예: 목차 스타일)
new Paragraph({
  children: [
    new TextRun("Introduction"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 다단 레이아웃

```javascript
// 동일 너비 단
sections: [{
  properties: {
    column: {
      count: 2,          // 단 수
      space: 720,        // 단 간격 DXA (720 = 0.5인치)
      equalWidth: true,
      separate: true,    // 단 사이에 세로선
    },
  },
  children: [/* 콘텐츠가 단에 자연스럽게 흐름 */]
}]

// 사용자 지정 너비 단 (equalWidth는 반드시 false)
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* 콘텐츠 */]
}]
```

`type: SectionType.NEXT_COLUMN`을 사용하는 새 섹션으로 단 나누기를 강제합니다.

### 목차

```javascript
// 중요: 제목은 반드시 HeadingLevel만 사용 — 사용자 지정 스타일 사용 금지
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### 머리글/바닥글

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1인치
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* 콘텐츠 */]
}]
```

### docx-js 핵심 규칙

- **페이지 크기 명시적 설정** — docx-js 기본값은 A4; 미국 문서에는 US Letter (12240 x 15840 DXA) 사용
- **가로 방향: 세로 방향 치수 전달** — docx-js는 너비/높이를 내부적으로 교환; 짧은 변을 `width`, 긴 변을 `height`로 전달하고 `orientation: PageOrientation.LANDSCAPE` 설정
- **`\n` 절대 사용 금지** — 별도의 Paragraph 요소 사용
- **유니코드 글머리 기호 절대 사용 금지** — numbering config와 `LevelFormat.BULLET` 사용
- **PageBreak는 반드시 Paragraph 안에** — 독립형은 잘못된 XML 생성
- **ImageRun에 `type` 필수** — 항상 png/jpg/etc 지정
- **항상 DXA로 표 `width` 설정** — `WidthType.PERCENTAGE` 절대 사용 금지 (Google Docs에서 깨짐)
- **표에는 이중 너비 필요** — `columnWidths` 배열과 셀 `width` 모두 설정, 두 값 일치해야 함
- **표 너비 = columnWidths 합계** — DXA에서 정확히 합산되는지 확인
- **항상 셀 여백 추가** — 읽기 쉬운 패딩을 위해 `margins: { top: 80, bottom: 80, left: 120, right: 120 }` 사용
- **`ShadingType.CLEAR` 사용** — 표 음영에 SOLID 절대 사용 금지
- **표를 구분선/규칙으로 절대 사용 금지** — 셀에는 최소 높이가 있어 빈 상자로 렌더링됨 (머리글/바닥글 포함); 대신 Paragraph에서 `border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }` 사용. 2단 바닥글에는 표 대신 탭 정지 사용 (탭 정지 섹션 참조)
- **TOC는 HeadingLevel만 필요** — 제목 단락에 사용자 지정 스타일 없음
- **내장 스타일 재정의** — 정확한 ID 사용: "Heading1", "Heading2" 등
- **`outlineLevel` 포함** — TOC에 필수 (H1은 0, H2는 1 등)

---

## 기존 문서 편집

**3단계를 반드시 순서대로 따르세요.**

### 1단계: 언팩
```bash
python scripts/office/unpack.py document.docx unpacked/
```
ZIP을 추출하고, XML을 보기 좋게 출력하고, 인접한 런을 병합하고, 스마트 따옴표를 XML 엔티티(`&#x201C;` 등)로 변환하여 편집 후에도 살아남도록 합니다. 런 병합을 건너뛰려면 `--merge-runs false` 사용.

### 2단계: XML 편집

`unpacked/word/`의 파일을 편집합니다. XML 패턴은 아래 XML 참조를 참고하세요.

변경 내용 추적 및 주석의 **작성자로 "Claude" 사용**. 단, 사용자가 다른 이름을 명시적으로 요청하는 경우 제외.

**문자열 교체에는 Edit 도구를 직접 사용. Python 스크립트 작성 금지.** 스크립트는 불필요한 복잡성을 초래합니다. Edit 도구는 교체되는 내용을 정확히 보여줍니다.

**중요: 새 콘텐츠에는 스마트 따옴표 사용.** 아포스트로피나 따옴표가 있는 텍스트 추가 시 XML 엔티티를 사용하여 스마트 따옴표 생성:
```xml
<!-- 전문적인 타이포그래피를 위해 이 엔티티 사용 -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
| 엔티티 | 문자 |
|--------|-----------|
| `&#x2018;` | ' (왼쪽 단일 따옴표) |
| `&#x2019;` | ' (오른쪽 단일 따옴표 / 아포스트로피) |
| `&#x201C;` | " (왼쪽 이중 따옴표) |
| `&#x201D;` | " (오른쪽 이중 따옴표) |

**주석 추가:** 여러 XML 파일에서 상용구를 처리하려면 `comment.py` 사용 (텍스트는 미리 이스케이프된 XML이어야 함):
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # 주석 0에 대한 답글
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # 사용자 지정 작성자 이름
```
그런 다음 document.xml에 마커 추가 (XML 참조의 주석 섹션 참조).

### 3단계: 팩
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
자동 수정으로 검증하고, XML을 압축하고, DOCX를 생성합니다. 검증을 건너뛰려면 `--validate false` 사용.

**자동 수정이 처리하는 항목:**
- 0x7FFFFFFF 이상의 `durableId` (유효한 ID 재생성)
- 공백이 있는 `<w:t>`의 누락된 `xml:space="preserve"`

**자동 수정이 처리하지 못하는 항목:**
- 잘못된 형식의 XML, 잘못된 요소 중첩, 누락된 관계, 스키마 위반

### 일반적인 함정

- **전체 `<w:r>` 요소 교체**: 변경 내용 추적 추가 시 전체 `<w:r>...</w:r>` 블록을 형제 요소로서 `<w:del>...<w:ins>...`로 교체. 런 안에 변경 내용 추적 태그 삽입 금지.
- **`<w:rPr>` 서식 보존**: 원본 런의 `<w:rPr>` 블록을 변경 내용 추적 런에 복사하여 굵게, 폰트 크기 등을 유지.

---

## XML 참조

### 스키마 준수

- **`<w:pPr>`의 요소 순서**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` 마지막
- **공백**: 선행/후행 공백이 있는 `<w:t>`에 `xml:space="preserve"` 추가
- **RSID**: 8자리 16진수여야 함 (예: `00AB1234`)

### 변경 내용 추적

**삽입:**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**삭제:**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**`<w:del>` 안에서**: `<w:t>` 대신 `<w:delText>` 사용, `<w:instrText>` 대신 `<w:delInstrText>` 사용.

**최소 편집** — 변경되는 내용만 표시:
```xml
<!-- "30 days"를 "60 days"로 변경 -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

**전체 단락/목록 항목 삭제** — 단락에서 모든 콘텐츠를 제거할 때, 다음 단락과 병합되도록 단락 마크도 삭제로 표시. `<w:pPr><w:rPr>` 안에 `<w:del/>` 추가:
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- 목록 번호 매기기 (있는 경우) -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```
`<w:pPr><w:rPr>`에 `<w:del/>`이 없으면 변경 내용 승인 시 빈 단락/목록 항목이 남습니다.

**다른 작성자의 삽입 거부** — 삽입 안에 삭제 중첩:
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

**다른 작성자의 삭제 복원** — 삽입을 뒤에 추가 (그들의 삭제는 수정하지 않음):
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

### 주석

`comment.py` 실행 후 (2단계 참조), document.xml에 마커 추가. 답글의 경우 `--parent` 플래그를 사용하고 마커를 부모 마커 안에 중첩합니다.

**중요: `<w:commentRangeStart>`와 `<w:commentRangeEnd>`는 `<w:r>`의 형제 요소이며, 절대로 `<w:r>` 안에 있으면 안 됩니다.**

```xml
<!-- 주석 마커는 w:p의 직접 자식, w:r 안에 절대 넣지 않음 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted</w:delText></w:r>
</w:del>
<w:r><w:t> more text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- 주석 0과 그 안에 중첩된 답글 1 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>text</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 이미지

1. `word/media/`에 이미지 파일 추가
2. `word/_rels/document.xml.rels`에 관계 추가:
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3. `[Content_Types].xml`에 콘텐츠 유형 추가:
```xml
<Default Extension="png" ContentType="image/png"/>
```
4. document.xml에서 참조:
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMU 단위: 914400 = 1인치 -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## 의존성

- **pandoc**: 텍스트 추출
- **docx**: `npm install -g docx` (새 문서 생성)
- **LibreOffice**: PDF 변환 (`scripts/office/soffice.py`를 통해 샌드박스 환경에서 자동 구성)
- **Poppler**: 이미지용 `pdftoppm`
