"""
[pack.py]
====================
[역할] 디렉토리를 DOCX, PPTX, XLSX 파일로 재압축합니다.

[주요 기능]
  - 자동 수리 기능이 포함된 XML 스키마 검증
  - XML 포맷 압축 (불필요한 공백 제거)
  - Office 파일 생성

[사용법]
  python pack.py <입력_디렉토리> <출력_파일> [--original <원본파일>] [--validate true|false]

[예시]
  python pack.py unpacked/ output.docx --original input.docx
  python pack.py unpacked/ output.pptx --validate false

[주요 함수]
  - pack()             : 메인 패킹 함수
  - _run_validation()  : 검증 및 자동 수리 실행
  - _condense_xml()    : XML 파일 압축 (공백 제거)
"""

import argparse
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path

import defusedxml.minidom

from validators import DOCXSchemaValidator, PPTXSchemaValidator, RedliningValidator

def pack(
    input_directory: str,
    output_file: str,
    original_file: str | None = None,
    validate: bool = True,
    infer_author_func=None,
) -> tuple[None, str]:
    input_dir = Path(input_directory)
    output_path = Path(output_file)
    suffix = output_path.suffix.lower()

    if not input_dir.is_dir():
        return None, f"오류: {input_dir} 는 디렉토리가 아닙니다"

    if suffix not in {".docx", ".pptx", ".xlsx"}:
        return None, f"오류: {output_file} 는 .docx, .pptx, .xlsx 파일이어야 합니다"

    if validate and original_file:
        original_path = Path(original_file)
        if original_path.exists():
            success, output = _run_validation(
                input_dir, original_path, suffix, infer_author_func
            )
            if output:
                print(output)
            if not success:
                return None, f"오류: {input_dir} 검증 실패"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_content_dir = Path(temp_dir) / "content"
        shutil.copytree(input_dir, temp_content_dir)

        for pattern in ["*.xml", "*.rels"]:
            for xml_file in temp_content_dir.rglob(pattern):
                _condense_xml(xml_file)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in temp_content_dir.rglob("*"):
                if f.is_file():
                    zf.write(f, f.relative_to(temp_content_dir))

    return None, f"{input_dir} 를 {output_file} 로 패킹 완료"


def _run_validation(
    unpacked_dir: Path,
    original_file: Path,
    suffix: str,
    infer_author_func=None,
) -> tuple[bool, str | None]:
    output_lines = []
    validators = []

    if suffix == ".docx":
        author = "Claude"
        if infer_author_func:
            try:
                author = infer_author_func(unpacked_dir, original_file)
            except ValueError as e:
                print(f"경고: {e} 기본 작성자 'Claude' 사용.", file=sys.stderr)

        validators = [
            DOCXSchemaValidator(unpacked_dir, original_file),
            RedliningValidator(unpacked_dir, original_file, author=author),
        ]
    elif suffix == ".pptx":
        validators = [PPTXSchemaValidator(unpacked_dir, original_file)]

    if not validators:
        return True, None

    total_repairs = sum(v.repair() for v in validators)
    if total_repairs:
        output_lines.append(f"자동 수리 완료: {total_repairs}개 문제")

    success = all(v.validate() for v in validators)

    if success:
        output_lines.append("모든 검증 통과!")

    return success, "\n".join(output_lines) if output_lines else None


def _condense_xml(xml_file: Path) -> None:
    try:
        with open(xml_file, encoding="utf-8") as f:
            dom = defusedxml.minidom.parse(f)

        for element in dom.getElementsByTagName("*"):
            if element.tagName.endswith(":t"):
                continue

            for child in list(element.childNodes):
                if (
                    child.nodeType == child.TEXT_NODE
                    and child.nodeValue
                    and child.nodeValue.strip() == ""
                ) or child.nodeType == child.COMMENT_NODE:
                    element.removeChild(child)

        xml_file.write_bytes(dom.toxml(encoding="UTF-8"))
    except Exception as e:
        print(f"오류: {xml_file.name} 파싱 실패: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="디렉토리를 DOCX, PPTX, XLSX 파일로 패킹합니다"
    )
    parser.add_argument("input_directory", help="압축 해제된 Office 문서 디렉토리")
    parser.add_argument("output_file", help="출력 Office 파일 (.docx/.pptx/.xlsx)")
    parser.add_argument(
        "--original",
        help="검증 비교용 원본 파일",
    )
    parser.add_argument(
        "--validate",
        type=lambda x: x.lower() == "true",
        default=True,
        metavar="true|false",
        help="자동 수리와 함께 검증 실행 (기본값: true)",
    )
    args = parser.parse_args()

    _, message = pack(
        args.input_directory,
        args.output_file,
        original_file=args.original,
        validate=args.validate,
    )
    print(message)

    if "오류" in message:
        sys.exit(1)
