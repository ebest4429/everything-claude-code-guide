"""
[fill_fillable_fields.py]
====================
[역할] 작성 가능한 PDF 양식 필드에 값을 채워넣습니다

[주요 기능]
  - field_values.json의 필드 ID 및 페이지 번호 유효성 검사
  - 체크박스, 라디오 그룹, 선택 필드 값 유효성 검사
  - 유효성 검사 통과 후 PDF 필드에 값 적용하여 저장

[사용법]
  python fill_fillable_fields.py [input pdf] [field_values.json] [output pdf]
  예: python fill_fillable_fields.py form.pdf field_values.json filled_form.pdf

[주요 클래스/함수]
  - fill_pdf_fields()                  : PDF 필드에 값을 채우는 메인 함수
  - validation_error_for_field_value() : 필드 값 유효성 검사
  - monkeypatch_pydpf_method()         : pypdf 내부 메서드 패치
"""
import json
import sys

from pypdf import PdfReader, PdfWriter

from extract_form_field_info import get_field_info




def fill_pdf_fields(input_pdf_path: str, fields_json_path: str, output_pdf_path: str):
    with open(fields_json_path) as f:
        fields = json.load(f)
    fields_by_page = {}
    for field in fields:
        if "value" in field:
            field_id = field["field_id"]
            page = field["page"]
            if page not in fields_by_page:
                fields_by_page[page] = {}
            fields_by_page[page][field_id] = field["value"]

    reader = PdfReader(input_pdf_path)

    has_error = False
    field_info = get_field_info(reader)
    fields_by_ids = {f["field_id"]: f for f in field_info}
    for field in fields:
        existing_field = fields_by_ids.get(field["field_id"])
        if not existing_field:
            has_error = True
            print(f"오류: `{field['field_id']}`은(는) 유효하지 않은 필드 ID입니다")
        elif field["page"] != existing_field["page"]:
            has_error = True
            print(f"오류: `{field['field_id']}`의 페이지 번호가 올바르지 않습니다 (입력값: {field['page']}, 실제: {existing_field['page']})")
        else:
            if "value" in field:
                err = validation_error_for_field_value(existing_field, field["value"])
                if err:
                    print(err)
                    has_error = True
    if has_error:
        sys.exit(1)

    writer = PdfWriter(clone_from=reader)
    for page, field_values in fields_by_page.items():
        writer.update_page_form_field_values(writer.pages[page - 1], field_values, auto_regenerate=False)

    writer.set_need_appearances_writer(True)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)


def validation_error_for_field_value(field_info, field_value):
    field_type = field_info["type"]
    field_id = field_info["field_id"]
    if field_type == "checkbox":
        checked_val = field_info["checked_value"]
        unchecked_val = field_info["unchecked_value"]
        if field_value != checked_val and field_value != unchecked_val:
            return f'오류: 체크박스 필드 "{field_id}"에 유효하지 않은 값 "{field_value}"입니다. 선택 값은 "{checked_val}", 해제 값은 "{unchecked_val}"입니다'
    elif field_type == "radio_group":
        option_values = [opt["value"] for opt in field_info["radio_options"]]
        if field_value not in option_values:
            return f'오류: 라디오 그룹 필드 "{field_id}"에 유효하지 않은 값 "{field_value}"입니다. 유효한 값: {option_values}'
    elif field_type == "choice":
        choice_values = [opt["value"] for opt in field_info["choice_options"]]
        if field_value not in choice_values:
            return f'오류: 선택 필드 "{field_id}"에 유효하지 않은 값 "{field_value}"입니다. 유효한 값: {choice_values}'
    return None


def monkeypatch_pydpf_method():
    from pypdf.generic import DictionaryObject
    from pypdf.constants import FieldDictionaryAttributes

    original_get_inherited = DictionaryObject.get_inherited

    def patched_get_inherited(self, key: str, default = None):
        result = original_get_inherited(self, key, default)
        if key == FieldDictionaryAttributes.Opt:
            if isinstance(result, list) and all(isinstance(v, list) and len(v) == 2 for v in result):
                result = [r[0] for r in result]
        return result

    DictionaryObject.get_inherited = patched_get_inherited


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("사용법: fill_fillable_fields.py [input pdf] [field_values.json] [output pdf]")
        sys.exit(1)
    monkeypatch_pydpf_method()
    input_pdf = sys.argv[1]
    fields_json = sys.argv[2]
    output_pdf = sys.argv[3]
    fill_pdf_fields(input_pdf, fields_json, output_pdf)
