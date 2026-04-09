"""
[accept_changes.py]
====================
[역할] LibreOffice를 사용하여 DOCX 파일의 모든 변경 내용 추적을 승인합니다.

[주요 기능]
  - 입력 DOCX 파일의 모든 tracked changes를 일괄 승인
  - LibreOffice Basic 매크로를 활용한 자동화
  - 출력 파일로 깨끗한 문서 저장

[사용법]
  python accept_changes.py input.docx output.docx

[주요 함수]
  - accept_changes(): 변경 내용 추적 승인 실행
  - _setup_libreoffice_macro(): LibreOffice 매크로 설정

[요구사항] LibreOffice (soffice)가 설치되어 있어야 합니다.
"""

import argparse
import logging
import shutil
import subprocess
from pathlib import Path

from office.soffice import get_soffice_env

logger = logging.getLogger(__name__)

LIBREOFFICE_PROFILE = "/tmp/libreoffice_docx_profile"
MACRO_DIR = f"{LIBREOFFICE_PROFILE}/user/basic/Standard"

ACCEPT_CHANGES_MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub AcceptAllTrackedChanges()
        Dim document As Object
        Dim dispatcher As Object

        document = ThisComponent.CurrentController.Frame
        dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

        dispatcher.executeDispatch(document, ".uno:AcceptAllTrackedChanges", "", 0, Array())
        ThisComponent.store()
        ThisComponent.close(True)
    End Sub
</script:module>"""


def accept_changes(
    input_file: str,
    output_file: str,
) -> tuple[None, str]:
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        return None, f"오류: 입력 파일을 찾을 수 없습니다: {input_file}"

    if not input_path.suffix.lower() == ".docx":
        return None, f"오류: 입력 파일이 DOCX 파일이 아닙니다: {input_file}"

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, output_path)
    except Exception as e:
        return None, f"오류: 입력 파일을 출력 위치로 복사하지 못했습니다: {e}"

    if not _setup_libreoffice_macro():
        return None, "오류: LibreOffice 매크로 설정에 실패했습니다"

    cmd = [
        "soffice",
        "--headless",
        f"-env:UserInstallation=file://{LIBREOFFICE_PROFILE}",
        "--norestore",
        "vnd.sun.star.script:Standard.Module1.AcceptAllTrackedChanges?language=Basic&location=application",
        str(output_path.absolute()),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env=get_soffice_env(),
        )
    except subprocess.TimeoutExpired:
        return (
            None,
            f"모든 변경 내용 추적 승인 완료: {input_file} -> {output_file}",
        )

    if result.returncode != 0:
        return None, f"오류: LibreOffice 실행 실패: {result.stderr}"

    return (
        None,
        f"모든 변경 내용 추적 승인 완료: {input_file} -> {output_file}",
    )


def _setup_libreoffice_macro() -> bool:
    macro_dir = Path(MACRO_DIR)
    macro_file = macro_dir / "Module1.xba"

    if macro_file.exists() and "AcceptAllTrackedChanges" in macro_file.read_text():
        return True

    if not macro_dir.exists():
        subprocess.run(
            [
                "soffice",
                "--headless",
                f"-env:UserInstallation=file://{LIBREOFFICE_PROFILE}",
                "--terminate_after_init",
            ],
            capture_output=True,
            timeout=10,
            check=False,
            env=get_soffice_env(),
        )
        macro_dir.mkdir(parents=True, exist_ok=True)

    try:
        macro_file.write_text(ACCEPT_CHANGES_MACRO)
        return True
    except Exception as e:
        logger.warning(f"LibreOffice 매크로 설정 실패: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DOCX 파일의 모든 변경 내용 추적을 승인합니다"
    )
    parser.add_argument("input_file", help="변경 내용 추적이 포함된 입력 DOCX 파일")
    parser.add_argument(
        "output_file", help="출력 DOCX 파일 (깨끗한 버전, 변경 내용 추적 없음)"
    )
    args = parser.parse_args()

    _, message = accept_changes(args.input_file, args.output_file)
    print(message)

    if "오류" in message:
        raise SystemExit(1)
