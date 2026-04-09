"""
[convert_pdf_to_images.py]
====================
[역할] PDF 파일을 페이지별 PNG 이미지로 변환합니다

[주요 기능]
  - PDF의 각 페이지를 개별 PNG 이미지로 저장
  - 최대 치수(max_dim)를 초과하는 이미지 자동 리사이즈
  - 200 DPI로 렌더링 후 지정 디렉토리에 저장

[사용법]
  python convert_pdf_to_images.py [input pdf] [output directory]
  예: python convert_pdf_to_images.py form.pdf images/

[주요 클래스/함수]
  - convert(): PDF를 이미지로 변환하는 메인 함수
"""
import os
import sys

from pdf2image import convert_from_path




def convert(pdf_path, output_dir, max_dim=1000):
    images = convert_from_path(pdf_path, dpi=200)

    for i, image in enumerate(images):
        width, height = image.size
        if width > max_dim or height > max_dim:
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height))

        image_path = os.path.join(output_dir, f"page_{i+1}.png")
        image.save(image_path)
        print(f"{i+1}페이지를 {image_path}로 저장했습니다 (크기: {image.size})")

    print(f"{len(images)}페이지를 PNG 이미지로 변환했습니다")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: convert_pdf_to_images.py [input pdf] [output directory]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert(pdf_path, output_directory)
