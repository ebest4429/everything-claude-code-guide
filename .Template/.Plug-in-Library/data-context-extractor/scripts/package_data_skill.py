#!/usr/bin/env python3
"""
[package_data_skill.py]
====================
[역할] 생성된 데이터 분석 스킬 폴더를 배포 가능한 .skill 파일(zip 형식)로 패키징합니다.

[주요 기능]
  - 스킬 폴더 구조 유효성 검사 (SKILL.md, 프론트매터, 플레이스홀더 확인)
  - 유효한 스킬 폴더를 .zip 파일로 패키징
  - 숨김 파일 및 불필요한 파일 자동 제외

[사용법]
  python package_data_skill.py <스킬폴더경로> [출력디렉토리]
  예: python package_data_skill.py /home/claude/acme-data-analyst
  예: python package_data_skill.py /home/claude/acme-data-analyst /tmp/outputs

[주요 함수]
  - validate_skill(): 스킬 구조 유효성 검사
  - package_skill()  : 스킬 폴더를 .zip으로 패키징
  - main()           : 커맨드라인 진입점
"""

import sys
import zipfile
from pathlib import Path


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """스킬 구조 기본 유효성 검사."""

    # SKILL.md 존재 확인
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md가 없습니다"

    # SKILL.md 프론트매터 확인
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "SKILL.md에 YAML 프론트매터가 없습니다"

    # 필수 프론트매터 필드 확인
    if "name:" not in content[:500]:
        return False, "SKILL.md 프론트매터에 'name' 필드가 없습니다"
    if "description:" not in content[:1000]:
        return False, "SKILL.md 프론트매터에 'description' 필드가 없습니다"

    # 채워지지 않은 플레이스홀더 텍스트 확인
    if "[PLACEHOLDER]" in content or "[COMPANY]" in content:
        return False, "SKILL.md에 채워지지 않은 플레이스홀더 텍스트가 있습니다"

    return True, "유효성 검사 통과"


def package_skill(skill_path: str, output_dir: str = None) -> Path | None:
    """
    스킬 폴더를 .skill 파일로 패키징합니다.

    Args:
        skill_path: 스킬 폴더 경로
        output_dir: 선택적 출력 디렉토리

    Returns:
        생성된 .skill 파일의 경로, 오류 시 None
    """
    skill_path = Path(skill_path).resolve()

    # 폴더 존재 확인
    if not skill_path.exists():
        print(f"오류: 스킬 폴더를 찾을 수 없습니다: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"오류: 경로가 디렉토리가 아닙니다: {skill_path}")
        return None

    # 유효성 검사 실행
    print("스킬 유효성 검사 중...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"유효성 검사 실패: {message}")
        return None
    print(f"{message}\n")

    # 출력 위치 결정
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
    else:
        output_path = Path.cwd()

    output_path.mkdir(parents=True, exist_ok=True)
    skill_filename = output_path / f"{skill_name}.zip"

    # zip 파일 생성
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # 숨김 파일 및 불필요한 파일 건너뜀
                    if any(part.startswith('.') for part in file_path.parts):
                        continue
                    if file_path.name in ['__pycache__', '.DS_Store', 'Thumbs.db']:
                        continue

                    # zip 내 상대 경로 계산
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  추가됨: {arcname}")

        print(f"\n스킬 패키징 완료: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"zip 파일 생성 오류: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"스킬 패키징 중: {skill_path}")
    if output_dir:
        print(f"   출력 디렉토리: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
