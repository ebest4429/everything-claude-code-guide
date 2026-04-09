"""
[validate.py]
====================
[역할] Office 문서 XML 파일을 XSD 스키마 및 추적 변경사항에 대해 검증하는 커맨드라인 도구입니다.

[주요 기능]
  - XSD 스키마 검증 (DOCX, PPTX)
  - 추적 변경사항(redlining) 검증
  - 자동 수복: OOXML 한도를 초과한 paraId/durableId 값 수정
  - 자동 수복: 공백이 있는 w:t 요소에 xml:space="preserve" 누락 추가

[사용법]
  python validate.py <path> [--original <original_file>] [--auto-repair] [--author NAME]
  예: python validate.py unpacked/ --original input.docx --auto-repair

[인수]
  path          : 언팩된 디렉터리 또는 패킹된 Office 파일(.docx/.pptx/.xlsx)
  --original    : 비교용 원본 파일 경로 (생략 시 모든 XSD 오류 보고, redline 검증 생략)
  --auto-repair : 일반적인 문제 자동 수복
  --author      : redline 검증용 작성자 이름 (기본값: Claude)

[주요 함수]
  - main(): 커맨드라인 진입점
"""

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

from validators import DOCXSchemaValidator, PPTXSchemaValidator, RedliningValidator


def main():
    parser = argparse.ArgumentParser(description="Validate Office document XML files")
    parser.add_argument(
        "path",
        help="Path to unpacked directory or packed Office file (.docx/.pptx/.xlsx)",
    )
    parser.add_argument(
        "--original",
        required=False,
        default=None,
        help="Path to original file (.docx/.pptx/.xlsx). If omitted, all XSD errors are reported and redlining validation is skipped.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--auto-repair",
        action="store_true",
        help="Automatically repair common issues (hex IDs, whitespace preservation)",
    )
    parser.add_argument(
        "--author",
        default="Claude",
        help="Author name for redlining validation (default: Claude)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    assert path.exists(), f"Error: {path} does not exist"

    original_file = None
    if args.original:
        original_file = Path(args.original)
        assert original_file.is_file(), f"Error: {original_file} is not a file"
        assert original_file.suffix.lower() in [".docx", ".pptx", ".xlsx"], (
            f"Error: {original_file} must be a .docx, .pptx, or .xlsx file"
        )

    file_extension = (original_file or path).suffix.lower()
    assert file_extension in [".docx", ".pptx", ".xlsx"], (
        f"Error: Cannot determine file type from {path}. Use --original or provide a .docx/.pptx/.xlsx file."
    )

    if path.is_file() and path.suffix.lower() in [".docx", ".pptx", ".xlsx"]:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(temp_dir)
        unpacked_dir = Path(temp_dir)
    else:
        assert path.is_dir(), f"Error: {path} is not a directory or Office file"
        unpacked_dir = path

    match file_extension:
        case ".docx":
            validators = [
                DOCXSchemaValidator(unpacked_dir, original_file, verbose=args.verbose),
            ]
            if original_file:
                validators.append(
                    RedliningValidator(unpacked_dir, original_file, verbose=args.verbose, author=args.author)  
                )
        case ".pptx":
            validators = [
                PPTXSchemaValidator(unpacked_dir, original_file, verbose=args.verbose),
            ]
        case _:
            print(f"Error: Validation not supported for file type {file_extension}")
            sys.exit(1)

    if args.auto_repair:
        total_repairs = sum(v.repair() for v in validators)
        if total_repairs:
            print(f"Auto-repaired {total_repairs} issue(s)")

    success = all(v.validate() for v in validators)

    if success:
        print("All validations PASSED!")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
