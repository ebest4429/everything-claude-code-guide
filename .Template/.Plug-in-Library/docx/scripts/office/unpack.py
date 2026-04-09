"""
[unpack.py]
====================
[역할] Office 파일(DOCX, PPTX, XLSX)을 편집 가능한 형태로 압축 해제합니다.

[주요 기능]
  - ZIP 아카이브 추출 및 XML 파일 들여쓰기 포맷 변환
  - 동일 서식의 인접 run 병합 (DOCX 전용, 선택사항)
  - 동일 작성자의 인접 변경 내용 추적 단순화 (DOCX 전용, 선택사항)

[사용법]
  python unpack.py <office_파일> <출력_디렉토리> [옵션]
  예: python unpack.py document.docx unpacked/
  예: python unpack.py presentation.pptx unpacked/
  예: python unpack.py document.docx unpacked/ --merge-runs false

[주요 함수]
  - unpack()             : Office 파일 압축 해제
  - _pretty_print_xml() : XML 들여쓰기 포맷 변환
  - _escape_smart_quotes(): 스마트 따옴표 이스케이프 처리
"""

import argparse
import sys
import zipfile
from pathlib import Path

import defusedxml.minidom

from helpers.merge_runs import merge_runs as do_merge_runs
from helpers.simplify_redlines import simplify_redlines as do_simplify_redlines

SMART_QUOTE_REPLACEMENTS = {
    "\u201c": "&#x201C;",  
    "\u201d": "&#x201D;",  
    "\u2018": "&#x2018;",  
    "\u2019": "&#x2019;",  
}


def unpack(
    input_file: str,
    output_directory: str,
    merge_runs: bool = True,
    simplify_redlines: bool = True,
) -> tuple[None, str]:
    input_path = Path(input_file)
    output_path = Path(output_directory)
    suffix = input_path.suffix.lower()

    if not input_path.exists():
        return None, f"오류: {input_file} 파일이 존재하지 않습니다"

    if suffix not in {".docx", ".pptx", ".xlsx"}:
        return None, f"오류: {input_file} 은 .docx, .pptx, .xlsx 파일이어야 합니다"

    try:
        output_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(input_path, "r") as zf:
            zf.extractall(output_path)

        xml_files = list(output_path.rglob("*.xml")) + list(output_path.rglob("*.rels"))
        for xml_file in xml_files:
            _pretty_print_xml(xml_file)

        message = f"{input_file} 압축 해제 완료 (XML {len(xml_files)}개)"

        if suffix == ".docx":
            if simplify_redlines:
                simplify_count, _ = do_simplify_redlines(str(output_path))
                message += f", 변경 내용 추적 {simplify_count}건 단순화"

            if merge_runs:
                merge_count, _ = do_merge_runs(str(output_path))
                message += f", run {merge_count}개 병합"

        for xml_file in xml_files:
            _escape_smart_quotes(xml_file)

        return None, message

    except zipfile.BadZipFile:
        return None, f"오류: {input_file} 은 유효한 Office 파일이 아닙니다"
    except Exception as e:
        return None, f"압축 해제 오류: {e}"


def _pretty_print_xml(xml_file: Path) -> None:
    try:
        content = xml_file.read_text(encoding="utf-8")
        dom = defusedxml.minidom.parseString(content)
        xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="utf-8"))
    except Exception:
        pass  


def _escape_smart_quotes(xml_file: Path) -> None:
    try:
        content = xml_file.read_text(encoding="utf-8")
        for char, entity in SMART_QUOTE_REPLACEMENTS.items():
            content = content.replace(char, entity)
        xml_file.write_text(content, encoding="utf-8")
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Office 파일(DOCX, PPTX, XLSX)을 편집용으로 압축 해제합니다"
    )
    parser.add_argument("input_file", help="압축 해제할 Office 파일")
    parser.add_argument("output_directory", help="출력 디렉토리")
    parser.add_argument(
        "--merge-runs",
        type=lambda x: x.lower() == "true",
        default=True,
        metavar="true|false",
        help="동일 서식의 인접 run 병합 (DOCX 전용, 기본값: true)",
    )
    parser.add_argument(
        "--simplify-redlines",
        type=lambda x: x.lower() == "true",
        default=True,
        metavar="true|false",
        help="동일 작성자의 인접 변경 내용 추적 병합 (DOCX 전용, 기본값: true)",
    )
    args = parser.parse_args()

    _, message = unpack(
        args.input_file,
        args.output_directory,
        merge_runs=args.merge_runs,
        simplify_redlines=args.simplify_redlines,
    )
    print(message)

    if "Error" in message:
        sys.exit(1)
