"""
[fill_pdf_form_with_annotations.py]
====================
[역할] 작성 불가능한 PDF 양식에 텍스트 주석으로 값을 채워넣습니다

[주요 기능]
  - 이미지 좌표 또는 PDF 좌표 자동 감지 및 변환
  - FreeText 주석으로 지정 위치에 텍스트 삽입
  - 폰트명, 폰트 크기, 폰트 색상 설정 지원

[사용법]
  python fill_pdf_form_with_annotations.py [input pdf] [fields.json] [output pdf]
  예: python fill_pdf_form_with_annotations.py form.pdf fields.json filled_form.pdf

[주요 클래스/함수]
  - transform_from_image_coords(): 이미지 좌표를 PDF 좌표로 변환
  - transform_from_pdf_coords()  : PDF 좌표를 pypdf 내부 좌표로 변환
  - fill_pdf_form()              : 양식에 텍스트 주석을 추가하는 메인 함수
"""
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText




def transform_from_image_coords(bbox, image_width, image_height, pdf_width, pdf_height):
    x_scale = pdf_width / image_width
    y_scale = pdf_height / image_height

    left = bbox[0] * x_scale
    right = bbox[2] * x_scale

    top = pdf_height - (bbox[1] * y_scale)
    bottom = pdf_height - (bbox[3] * y_scale)

    return left, bottom, right, top


def transform_from_pdf_coords(bbox, pdf_height):
    left = bbox[0]
    right = bbox[2]

    pypdf_top = pdf_height - bbox[1]
    pypdf_bottom = pdf_height - bbox[3]

    return left, pypdf_bottom, right, pypdf_top


def fill_pdf_form(input_pdf_path, fields_json_path, output_pdf_path):

    with open(fields_json_path, "r") as f:
        fields_data = json.load(f)

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    writer.append(reader)

    pdf_dimensions = {}
    for i, page in enumerate(reader.pages):
        mediabox = page.mediabox
        pdf_dimensions[i + 1] = [mediabox.width, mediabox.height]

    annotations = []
    for field in fields_data["form_fields"]:
        page_num = field["page_number"]

        page_info = next(p for p in fields_data["pages"] if p["page_number"] == page_num)
        pdf_width, pdf_height = pdf_dimensions[page_num]

        if "pdf_width" in page_info:
            transformed_entry_box = transform_from_pdf_coords(
                field["entry_bounding_box"],
                float(pdf_height)
            )
        else:
            image_width = page_info["image_width"]
            image_height = page_info["image_height"]
            transformed_entry_box = transform_from_image_coords(
                field["entry_bounding_box"],
                image_width, image_height,
                float(pdf_width), float(pdf_height)
            )

        if "entry_text" not in field or "text" not in field["entry_text"]:
            continue
        entry_text = field["entry_text"]
        text = entry_text["text"]
        if not text:
            continue

        font_name = entry_text.get("font", "Arial")
        font_size = str(entry_text.get("font_size", 14)) + "pt"
        font_color = entry_text.get("font_color", "000000")

        annotation = FreeText(
            text=text,
            rect=transformed_entry_box,
            font=font_name,
            font_size=font_size,
            font_color=font_color,
            border_color=None,
            background_color=None,
        )
        annotations.append(annotation)
        writer.add_annotation(page_number=page_num - 1, annotation=annotation)

    with open(output_pdf_path, "wb") as output:
        writer.write(output)

    print(f"PDF 양식 작성 완료. {output_pdf_path}에 저장되었습니다")
    print(f"텍스트 주석 {len(annotations)}개를 추가했습니다")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("사용법: fill_pdf_form_with_annotations.py [input pdf] [fields.json] [output pdf]")
        sys.exit(1)
    input_pdf = sys.argv[1]
    fields_json = sys.argv[2]
    output_pdf = sys.argv[3]

    fill_pdf_form(input_pdf, fields_json, output_pdf)
