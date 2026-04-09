#!/usr/bin/env python3
"""
스킬 패키저 - 스킬 폴더를 배포 가능한 .skill 파일로 만듭니다.

사용법:
    python utils/package_skill.py <스킬폴더경로> [출력디렉토리]

예시:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import fnmatch
import sys
import zipfile
from pathlib import Path
from scripts.quick_validate import validate_skill

# 스킬 패키징 시 제외할 패턴
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
# 스킬 루트에서만 제외되는 디렉토리 (더 깊은 중첩에는 적용되지 않음)
ROOT_EXCLUDE_DIRS = {"evals"}


def should_exclude(rel_path: Path) -> bool:
    """경로를 패키징에서 제외해야 하는지 확인합니다."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    # rel_path는 skill_path.parent에 상대적이므로 parts[0]은 스킬 폴더 이름,
    # parts[1](있는 경우)은 첫 번째 서브디렉토리입니다.
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_skill(skill_path, output_dir=None):
    """
    스킬 폴더를 .skill 파일로 패키징합니다.

    Args:
        skill_path: 스킬 폴더 경로
        output_dir: .skill 파일의 선택적 출력 디렉토리 (기본값: 현재 디렉토리)

    Returns:
        생성된 .skill 파일 경로, 오류 시 None
    """
    skill_path = Path(skill_path).resolve()

    # 스킬 폴더 존재 확인
    if not skill_path.exists():
        print(f"❌ 오류: 스킬 폴더를 찾을 수 없습니다: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ 오류: 경로가 디렉토리가 아닙니다: {skill_path}")
        return None

    # SKILL.md 존재 확인
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ 오류: {skill_path}에서 SKILL.md를 찾을 수 없습니다")
        return None

    # 패키징 전 유효성 검사 실행
    print("🔍 스킬 유효성 검사 중...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ 유효성 검사 실패: {message}")
        print("   패키징 전에 유효성 검사 오류를 수정하세요.")
        return None
    print(f"✅ {message}\n")

    # 출력 위치 결정
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # .skill 파일 생성 (zip 형식)
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 스킬 디렉토리를 순회하며 빌드 아티팩트 제외
            for file_path in skill_path.rglob('*'):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname):
                    print(f"  건너뜀: {arcname}")
                    continue
                zipf.write(file_path, arcname)
                print(f"  추가됨: {arcname}")

        print(f"\n✅ 스킬을 성공적으로 패키징했습니다: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ .skill 파일 생성 오류: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("사용법: python utils/package_skill.py <스킬폴더경로> [출력디렉토리]")
        print("\n예시:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 스킬 패키징 중: {skill_path}")
    if output_dir:
        print(f"   출력 디렉토리: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
