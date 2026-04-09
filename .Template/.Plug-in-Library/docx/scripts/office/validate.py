"""
[validate.py]
====================
[역할] Office 문서 XML 파일을 XSD 스키마 및 변경 내용 추적 기준으로 유효성 검사합니다.

[주요 기능]
  - XSD 스키마 기반 XML 유효성 검사
  - 변경 내용 추적(redlining) 유효성 검사
  - 자동 복구(auto-repair) 지원

[사용법]
  python validate.py <경로> [--original <원본_파일>] [--auto-repair] [--author 이름]
  첫 번째 인수는 다음 중 하나:
  - Office 문서 XML 파일이 담긴 압축 해제 디렉토리
  - 임시 디렉토리에 자동 압축 해제될 패킹된 Office 파일 (.docx/.pptx/.xlsx)

[자동 복구 항목]
  - OOXML 한도를 초과한 paraId/durableId 값
  - 공백이 있는 w:t 요소의 누락된 xml:space="preserve"

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
    parser = argparse.ArgumentParser(description="Office 문서 XML 파일 유효성 검사")
    parser.add_argument(
        "path",
        help="압축 해제된 디렉토리 또는 패킹된 Office 파일 경로 (.docx/.pptx/.xlsx)",
    )
    parser.add_argument(
        "--original",
        required=False,
        default=None,
        help="원본 파일 경로 (.docx/.pptx/.xlsx). 생략 시 모든 XSD 오류가 보고되고 redlining 검사는 건너뜁니다.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="상세 출력 활성화",
    )
    parser.add_argument(
        "--auto-repair",
        action="store_true",
        help="일반적인 문제 자동 복구 (hex ID, 공백 보존)",
    )
    parser.add_argument(
        "--author",
        default="Claude",
        help="redlining 검사에 사용할 작성자 이름 (기본값: Claude)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    assert path.exists(), f"오류: {path} 경로가 존재하지 않습니다"

    original_file = None
    if args.original:
        original_file = Path(args.original)
        assert original_file.is_file(), f"오류: {original_file} 은 파일이 아닙니다"
        assert original_file.suffix.lower() in [".docx", ".pptx", ".xlsx"], (
            f"오류: {original_file} 은 .docx, .pptx, .xlsx 파일이어야 합니다"
        )

    file_extension = (original_file or path).suffix.lower()
    assert file_extension in [".docx", ".pptx", ".xlsx"], (
        f"오류: {path} 에서 파일 형식을 확인할 수 없습니다. --original 옵션을 사용하거나 .docx/.pptx/.xlsx 파일을 지정하세요."
    )

    if path.is_file() and path.suffix.lower() in [".docx", ".pptx", ".xlsx"]:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(temp_dir)
        unpacked_dir = Path(temp_dir)
    else:
        assert path.is_dir(), f"오류: {path} 은 디렉토리 또는 Office 파일이 아닙니다"
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
            print(f"오류: {file_extension} 파일 형식은 유효성 검사를 지원하지 않습니다")
            sys.exit(1)

    if args.auto_repair:
        total_repairs = sum(v.repair() for v in validators)
        if total_repairs:
            print(f"자동 복구: {total_repairs}건 처리됨")

    success = all(v.validate() for v in validators)

    if success:
        print("모든 유효성 검사 통과!")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
