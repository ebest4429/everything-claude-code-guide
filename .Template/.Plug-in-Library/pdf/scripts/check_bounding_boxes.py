"""
[check_bounding_boxes.py]
====================
[역할] fields.json의 경계 상자 유효성을 검사합니다

[주요 기능]
  - 레이블/입력 경계 상자 간 교차 여부 확인
  - 입력 상자가 지정된 폰트 크기에 비해 너무 작은지 확인
  - 오류 발생 시 상세한 위치 정보 출력

[사용법]
  python check_bounding_boxes.py [fields.json]
  예: python check_bounding_boxes.py fields.json

[주요 클래스/함수]
  - RectAndField       : 경계 상자와 필드 정보를 담는 데이터 클래스
  - get_bounding_box_messages(): 유효성 검사 메시지 목록 반환
"""
from dataclasses import dataclass
import json
import sys




@dataclass
class RectAndField:
    rect: list[float]
    rect_type: str
    field: dict


def get_bounding_box_messages(fields_json_stream) -> list[str]:
    messages = []
    fields = json.load(fields_json_stream)
    messages.append(f"{len(fields['form_fields'])}개 필드를 읽었습니다")

    def rects_intersect(r1, r2):
        disjoint_horizontal = r1[0] >= r2[2] or r1[2] <= r2[0]
        disjoint_vertical = r1[1] >= r2[3] or r1[3] <= r2[1]
        return not (disjoint_horizontal or disjoint_vertical)

    rects_and_fields = []
    for f in fields["form_fields"]:
        rects_and_fields.append(RectAndField(f["label_bounding_box"], "label", f))
        rects_and_fields.append(RectAndField(f["entry_bounding_box"], "entry", f))

    has_error = False
    for i, ri in enumerate(rects_and_fields):
        for j in range(i + 1, len(rects_and_fields)):
            rj = rects_and_fields[j]
            if ri.field["page_number"] == rj.field["page_number"] and rects_intersect(ri.rect, rj.rect):
                has_error = True
                if ri.field is rj.field:
                    messages.append(f"실패: `{ri.field['description']}`의 레이블과 입력 경계 상자가 교차합니다 ({ri.rect}, {rj.rect})")
                else:
                    messages.append(f"실패: `{ri.field['description']}`의 {ri.rect_type} 경계 상자 ({ri.rect})와 `{rj.field['description']}`의 {rj.rect_type} 경계 상자 ({rj.rect})가 교차합니다")
                if len(messages) >= 20:
                    messages.append("추가 검사를 중단합니다. 경계 상자를 수정하고 다시 시도하세요")
                    return messages
        if ri.rect_type == "entry":
            if "entry_text" in ri.field:
                font_size = ri.field["entry_text"].get("font_size", 14)
                entry_height = ri.rect[3] - ri.rect[1]
                if entry_height < font_size:
                    has_error = True
                    messages.append(f"실패: `{ri.field['description']}`의 입력 경계 상자 높이({entry_height})가 텍스트 내용(폰트 크기: {font_size})에 비해 너무 낮습니다. 상자 높이를 늘리거나 폰트 크기를 줄이세요.")
                    if len(messages) >= 20:
                        messages.append("추가 검사를 중단합니다. 경계 상자를 수정하고 다시 시도하세요")
                        return messages

    if not has_error:
        messages.append("성공: 모든 경계 상자가 유효합니다")
    return messages

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: check_bounding_boxes.py [fields.json]")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        messages = get_bounding_box_messages(f)
    for msg in messages:
        print(msg)
