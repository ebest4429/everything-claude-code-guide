"""
[create_validation_image.py]
====================
[역할] 경계 상자를 시각적으로 표시한 검증 이미지를 생성합니다

[주요 기능]
  - 입력 경계 상자를 빨간색 사각형으로 표시
  - 레이블 경계 상자를 파란색 사각형으로 표시
  - 특정 페이지의 모든 필드 경계 상자를 한 이미지에 표시

[사용법]
  python create_validation_image.py [page number] [fields.json file] [input image path] [output image path]
  예: python create_validation_image.py 1 fields.json page_1.png validation_page_1.png

[주요 클래스/함수]
  - create_validation_image(): 검증 이미지 생성 함수
"""
import json
import sys

from PIL import Image, ImageDraw




def create_validation_image(page_number, fields_json_path, input_path, output_path):
    with open(fields_json_path, 'r') as f:
        data = json.load(f)

        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        num_boxes = 0

        for field in data["form_fields"]:
            if field["page_number"] == page_number:
                entry_box = field['entry_bounding_box']
                label_box = field['label_bounding_box']
                draw.rectangle(entry_box, outline='red', width=2)
                draw.rectangle(label_box, outline='blue', width=2)
                num_boxes += 2

        img.save(output_path)
        print(f"{output_path}에 {num_boxes}개의 경계 상자가 포함된 검증 이미지를 생성했습니다")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("사용법: create_validation_image.py [page number] [fields.json file] [input image path] [output image path]")
        sys.exit(1)
    page_number = int(sys.argv[1])
    fields_json_path = sys.argv[2]
    input_image_path = sys.argv[3]
    output_image_path = sys.argv[4]
    create_validation_image(page_number, fields_json_path, input_image_path, output_image_path)
