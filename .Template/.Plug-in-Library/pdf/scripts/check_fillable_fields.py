"""
[check_fillable_fields.py]
====================
[역할] PDF에 작성 가능한 양식 필드가 있는지 확인합니다

[주요 기능]
  - pypdf를 사용하여 PDF의 양식 필드 존재 여부 감지
  - 결과에 따라 다음 단계 안내 메시지 출력

[사용법]
  python check_fillable_fields.py <file.pdf>
  예: python check_fillable_fields.py form.pdf
"""
import sys
from pypdf import PdfReader




reader = PdfReader(sys.argv[1])
if (reader.get_fields()):
    print("이 PDF에는 작성 가능한 양식 필드가 있습니다")
else:
    print("이 PDF에는 작성 가능한 양식 필드가 없습니다. 데이터를 입력할 위치를 시각적으로 파악해야 합니다")
