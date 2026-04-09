"""
[extract_form_structure.py]
====================
[역할] 작성 불가능한 PDF에서 양식 구조를 추출합니다

[주요 기능]
  - 텍스트 레이블과 정확한 좌표 추출
  - 수평선(행 경계) 감지
  - 체크박스(작은 사각형) 위치 추출
  - 행 경계 계산 및 JSON 저장

[사용법]
  python extract_form_structure.py <input.pdf> <output.json>
  예: python extract_form_structure.py form.pdf form_structure.json

[주요 클래스/함수]
  - extract_form_structure(): PDF에서 양식 구조 추출
  - main()                  : 인수 파싱 및 실행 진입점
"""

import json
import sys
import pdfplumber


def extract_form_structure(pdf_path):
    structure = {
        "pages": [],
        "labels": [],
        "lines": [],
        "checkboxes": [],
        "row_boundaries": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            structure["pages"].append({
                "page_number": page_num,
                "width": float(page.width),
                "height": float(page.height)
            })

            words = page.extract_words()
            for word in words:
                structure["labels"].append({
                    "page": page_num,
                    "text": word["text"],
                    "x0": round(float(word["x0"]), 1),
                    "top": round(float(word["top"]), 1),
                    "x1": round(float(word["x1"]), 1),
                    "bottom": round(float(word["bottom"]), 1)
                })

            for line in page.lines:
                if abs(float(line["x1"]) - float(line["x0"])) > page.width * 0.5:
                    structure["lines"].append({
                        "page": page_num,
                        "y": round(float(line["top"]), 1),
                        "x0": round(float(line["x0"]), 1),
                        "x1": round(float(line["x1"]), 1)
                    })

            for rect in page.rects:
                width = float(rect["x1"]) - float(rect["x0"])
                height = float(rect["bottom"]) - float(rect["top"])
                if 5 <= width <= 15 and 5 <= height <= 15 and abs(width - height) < 2:
                    structure["checkboxes"].append({
                        "page": page_num,
                        "x0": round(float(rect["x0"]), 1),
                        "top": round(float(rect["top"]), 1),
                        "x1": round(float(rect["x1"]), 1),
                        "bottom": round(float(rect["bottom"]), 1),
                        "center_x": round((float(rect["x0"]) + float(rect["x1"])) / 2, 1),
                        "center_y": round((float(rect["top"]) + float(rect["bottom"])) / 2, 1)
                    })

    lines_by_page = {}
    for line in structure["lines"]:
        page = line["page"]
        if page not in lines_by_page:
            lines_by_page[page] = []
        lines_by_page[page].append(line["y"])

    for page, y_coords in lines_by_page.items():
        y_coords = sorted(set(y_coords))
        for i in range(len(y_coords) - 1):
            structure["row_boundaries"].append({
                "page": page,
                "row_top": y_coords[i],
                "row_bottom": y_coords[i + 1],
                "row_height": round(y_coords[i + 1] - y_coords[i], 1)
            })

    return structure


def main():
    if len(sys.argv) != 3:
        print("사용법: extract_form_structure.py <input.pdf> <output.json>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"{pdf_path}에서 구조를 추출하는 중...")
    structure = extract_form_structure(pdf_path)

    with open(output_path, "w") as f:
        json.dump(structure, f, indent=2)

    print(f"발견된 항목:")
    print(f"  - 페이지: {len(structure['pages'])}개")
    print(f"  - 텍스트 레이블: {len(structure['labels'])}개")
    print(f"  - 수평선: {len(structure['lines'])}개")
    print(f"  - 체크박스: {len(structure['checkboxes'])}개")
    print(f"  - 행 경계: {len(structure['row_boundaries'])}개")
    print(f"{output_path}에 저장되었습니다")


if __name__ == "__main__":
    main()
