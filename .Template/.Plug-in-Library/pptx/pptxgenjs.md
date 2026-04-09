# PptxGenJS 튜토리얼

## 설정 및 기본 구조

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // 또는 'LAYOUT_16x10', 'LAYOUT_4x3', 'LAYOUT_WIDE'
pres.author = 'Your Name';
pres.title = 'Presentation Title';

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

pres.writeFile({ fileName: "Presentation.pptx" });
```

## 레이아웃 크기

슬라이드 크기 (좌표 단위: 인치):
- `LAYOUT_16x9`: 10" × 5.625" (기본값)
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"
- `LAYOUT_WIDE`: 13.3" × 7.5"

---

## 텍스트 & 서식

```javascript
// 기본 텍스트
slide.addText("Simple Text", {
  x: 1, y: 1, w: 8, h: 2, fontSize: 24, fontFace: "Arial",
  color: "363636", bold: true, align: "center", valign: "middle"
});

// 자간 (letterSpacing은 무시되므로 charSpacing 사용)
slide.addText("SPACED TEXT", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });

// 리치 텍스트 배열
slide.addText([
  { text: "굵게 ", options: { bold: true } },
  { text: "이탤릭 ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// 여러 줄 텍스트 (breakLine: true 필요)
slide.addText([
  { text: "1번째 줄", options: { breakLine: true } },
  { text: "2번째 줄", options: { breakLine: true } },
  { text: "3번째 줄" }  // 마지막 항목은 breakLine 불필요
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// 텍스트 박스 여백 (내부 패딩)
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  margin: 0  // 도형이나 아이콘과 텍스트를 정확히 정렬할 때 0 사용
});
```

**팁:** 텍스트 박스에는 기본 내부 여백이 있습니다. 도형, 선, 아이콘과 같은 x 위치에 정확히 정렬해야 할 때 `margin: 0`을 설정하세요.

---

## 목록 & 불릿

```javascript
// ✅ 올바른 예: 여러 불릿
slide.addText([
  { text: "첫 번째 항목", options: { bullet: true, breakLine: true } },
  { text: "두 번째 항목", options: { bullet: true, breakLine: true } },
  { text: "세 번째 항목", options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// ❌ 잘못된 예: 유니코드 불릿 절대 사용 금지
slide.addText("• 첫 번째 항목", { ... });  // 이중 불릿 생성

// 하위 항목 및 번호 목록
{ text: "하위 항목", options: { bullet: true, indentLevel: 1 } }
{ text: "첫 번째", options: { bullet: { type: "number" }, breakLine: true } }
```

---

## 도형

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" }, line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0, line: { color: "FF0000", width: 3, dashType: "dash" }
});

// 투명도 적용
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});

// 둥근 사각형 (rectRadius는 ROUNDED_RECTANGLE에서만 동작, RECTANGLE에서는 안 됨)
// ⚠️ 직사각형 강조 오버레이와 함께 사용 금지 — 둥근 모서리를 덮지 못합니다. RECTANGLE을 사용하세요.
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" }, rectRadius: 0.1
});

// 그림자 적용
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
});
```

그림자 옵션:

| 속성 | 타입 | 범위 | 비고 |
|----------|------|-------|-------|
| `type` | 문자열 | `"outer"`, `"inner"` | |
| `color` | 문자열 | 6자리 hex (예: `"000000"`) | `#` 접두사 금지, 8자리 hex 금지 — 흔한 함정 참조 |
| `blur` | 숫자 | 0-100 pt | |
| `offset` | 숫자 | 0-200 pt | **반드시 0 이상** — 음수 값은 파일을 손상시킵니다 |
| `angle` | 숫자 | 0-359도 | 그림자가 떨어지는 방향 (135 = 오른쪽 아래, 270 = 위쪽) |
| `opacity` | 숫자 | 0.0-1.0 | 투명도에 이것을 사용하고, 색상 문자열에 인코딩하면 안 됩니다 |

그림자를 위쪽으로 드리우려면 (예: 푸터 바), 양수 offset과 `angle: 270`을 사용하세요 — 음수 offset을 사용하면 안 됩니다.

**참고**: 그라디언트 채우기는 네이티브로 지원되지 않습니다. 그라디언트 이미지를 배경으로 사용하세요.

---

## 이미지

### 이미지 소스

```javascript
// 파일 경로
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// base64 (빠름, 파일 I/O 없음)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });
```

### 이미지 옵션

```javascript
slide.addImage({
  path: "image.png",
  x: 1, y: 1, w: 5, h: 3,
  rotate: 45,              // 0-359도
  rounding: true,          // 원형 크롭
  transparency: 50,        // 0-100
  flipH: true,             // 수평 반전
  flipV: false,            // 수직 반전
  altText: "설명",          // 접근성
  hyperlink: { url: "https://example.com" }
});
```

### 이미지 크기 모드

```javascript
// Contain — 비율 유지하며 내부에 맞춤
{ sizing: { type: 'contain', w: 4, h: 3 } }

// Cover — 비율 유지하며 영역 채움 (잘릴 수 있음)
{ sizing: { type: 'cover', w: 4, h: 3 } }

// Crop — 특정 부분 잘라내기
{ sizing: { type: 'crop', x: 0.5, y: 0.5, w: 2, h: 2 } }
```

### 크기 계산 (비율 유지)

```javascript
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;

slide.addImage({ path: "image.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight });
```

### 지원 형식

- **표준**: PNG, JPG, GIF (애니메이션 GIF는 Microsoft 365에서 동작)
- **SVG**: 최신 PowerPoint/Microsoft 365에서 동작

---

## 아이콘

react-icons로 SVG 아이콘을 생성한 다음 범용 호환성을 위해 PNG로 래스터화하세요.

### 설정

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle, FaChartLine } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

### 슬라이드에 아이콘 추가

```javascript
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);

slide.addImage({
  data: iconData,
  x: 1, y: 1, w: 0.5, h: 0.5  // 크기 단위: 인치
});
```

**참고**: 선명한 아이콘을 위해 256 이상의 크기를 사용하세요. size 파라미터는 래스터화 해상도를 제어하며, 슬라이드의 표시 크기(`w`와 `h`, 단위 인치)와는 별개입니다.

### 아이콘 라이브러리

설치: `npm install -g react-icons react react-dom sharp`

react-icons의 인기 아이콘 세트:
- `react-icons/fa` — Font Awesome
- `react-icons/md` — Material Design
- `react-icons/hi` — Heroicons
- `react-icons/bi` — Bootstrap Icons

---

## 슬라이드 배경

```javascript
// 단색
slide.background = { color: "F1F1F1" };

// 투명도가 있는 색상
slide.background = { color: "FF3399", transparency: 50 };

// URL 이미지
slide.background = { path: "https://example.com/bg.jpg" };

// base64 이미지
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## 표

```javascript
slide.addTable([
  ["헤더 1", "헤더 2"],
  ["셀 1", "셀 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// 셀 병합이 있는 고급 표
let tableData = [
  [{ text: "헤더", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "셀"],
  [{ text: "병합", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

---

## 차트

```javascript
// 막대 차트
slide.addChart(pres.charts.BAR, [{
  name: "매출", labels: ["1분기", "2분기", "3분기", "4분기"], values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col',
  showTitle: true, title: '분기별 매출'
});

// 선형 차트
slide.addChart(pres.charts.LINE, [{
  name: "기온", labels: ["1월", "2월", "3월"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// 파이 차트
slide.addChart(pres.charts.PIE, [{
  name: "점유율", labels: ["A", "B", "기타"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });
```

### 더 나은 차트 만들기

기본 차트는 구식으로 보입니다. 다음 옵션을 적용하여 현대적이고 깔끔한 외관을 만드세요:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // 커스텀 색상 (프레젠테이션 팔레트와 맞춤)
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // 깔끔한 배경
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // 부드러운 축 레이블
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // 미묘한 격자선 (값 축만)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // 막대 위 데이터 레이블
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // 단일 시리즈에는 범례 숨김
  showLegend: false,
});
```

**주요 스타일 옵션:**
- `chartColors: [...]` — 시리즈/세그먼트의 hex 색상
- `chartArea: { fill, border, roundedCorners }` — 차트 배경
- `catGridLine/valGridLine: { color, style, size }` — 격자선 (`style: "none"`으로 숨기기)
- `lineSmooth: true` — 곡선 (선형 차트)
- `legendPos: "r"` — 범례 위치: "b", "t", "l", "r", "tr"

---

## 슬라이드 마스터

```javascript
pres.defineSlideMaster({
  title: 'TITLE_SLIDE', background: { color: '283A5E' },
  objects: [{
    placeholder: { options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });
```

---

## 흔한 함정

⚠️ 다음 문제들은 파일 손상, 시각적 버그, 잘못된 출력을 유발합니다. 반드시 피하세요.

1. **hex 색상에 "#" 절대 사용 금지** — 파일 손상 유발
   ```javascript
   color: "FF0000"      // ✅ 올바른 예
   color: "#FF0000"     // ❌ 잘못된 예
   ```

2. **hex 색상 문자열에 투명도 인코딩 절대 금지** — 8자리 색상 (예: `"00000020"`)은 파일을 손상시킵니다. 대신 `opacity` 속성을 사용하세요.
   ```javascript
   shadow: { type: "outer", blur: 6, offset: 2, color: "00000020" }          // ❌ 파일 손상
   shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.12 }  // ✅ 올바른 예
   ```

3. **`bullet: true` 사용** — "•" 같은 유니코드 기호 절대 사용 금지 (이중 불릿 생성)

4. **배열 항목 또는 텍스트 런 사이에 `breakLine: true` 사용**

5. **불릿과 함께 `lineSpacing` 사용 금지** — 과도한 간격 유발; 대신 `paraSpaceAfter` 사용

6. **각 프레젠테이션에 새 인스턴스 사용** — `pptxgen()` 객체 재사용 금지

7. **옵션 객체를 여러 호출에 재사용 절대 금지** — PptxGenJS는 객체를 직접 수정합니다 (예: shadow 값을 EMU로 변환). 하나의 객체를 여러 호출에 공유하면 두 번째 도형이 손상됩니다.
   ```javascript
   const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });  // ❌ 두 번째 호출은 이미 변환된 값을 받음
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });

   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });  // ✅ 매번 새 객체
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   ```

8. **`ROUNDED_RECTANGLE`과 강조 테두리 함께 사용 금지** — 직사각형 오버레이 바가 둥근 모서리를 덮지 못합니다. 대신 `RECTANGLE` 사용.
   ```javascript
   // ❌ 잘못된 예: 강조 바가 둥근 모서리를 덮지 못함
   slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });

   // ✅ 올바른 예: 깔끔한 정렬을 위해 RECTANGLE 사용
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });
   ```

---

## 빠른 참조

- **도형**: RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE
- **차트**: BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR
- **레이아웃**: LAYOUT_16x9 (10"×5.625"), LAYOUT_16x10, LAYOUT_4x3, LAYOUT_WIDE
- **정렬**: "left", "center", "right"
- **차트 데이터 레이블**: "outEnd", "inEnd", "center"
