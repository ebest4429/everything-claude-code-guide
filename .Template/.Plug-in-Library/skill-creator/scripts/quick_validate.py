#!/usr/bin/env python3
"""
스킬 빠른 유효성 검사 스크립트 - 최소 버전
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """스킬의 기본 유효성을 검사합니다."""
    skill_path = Path(skill_path)

    # SKILL.md 존재 확인
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md를 찾을 수 없습니다"

    # 프런트매터 읽기 및 유효성 검사
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "YAML 프런트매터를 찾을 수 없습니다"

    # 프런트매터 추출
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "유효하지 않은 프런트매터 형식"

    frontmatter_text = match.group(1)

    # YAML 프런트매터 파싱
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "프런트매터는 YAML 딕셔너리여야 합니다"
    except yaml.YAMLError as e:
        return False, f"프런트매터의 YAML이 유효하지 않습니다: {e}"

    # 허용된 속성 정의
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # 예상치 못한 속성 확인 (metadata 아래 중첩 키 제외)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.md 프런트매터에 예상치 못한 키: {', '.join(sorted(unexpected_keys))}. "
            f"허용된 속성: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 필수 필드 확인
    if 'name' not in frontmatter:
        return False, "프런트매터에 'name'이 없습니다"
    if 'description' not in frontmatter:
        return False, "프런트매터에 'description'이 없습니다"

    # 이름 유효성 검사
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"이름은 문자열이어야 합니다. {type(name).__name__} 받음"
    name = name.strip()
    if name:
        # 이름 규칙 확인 (케밥 케이스: 소문자, 하이픈만)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"이름 '{name}'은 케밥 케이스여야 합니다 (소문자, 숫자, 하이픈만)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"이름 '{name}'은 하이픈으로 시작/끝나거나 연속 하이픈을 포함할 수 없습니다"
        # 이름 길이 확인 (최대 64자)
        if len(name) > 64:
            return False, f"이름이 너무 깁니다 ({len(name)}자). 최대 64자"

    # 설명 추출 및 유효성 검사
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"설명은 문자열이어야 합니다. {type(description).__name__} 받음"
    description = description.strip()
    if description:
        # 꺾쇠괄호 확인
        if '<' in description or '>' in description:
            return False, "설명에 꺾쇠괄호 (< 또는 >)를 포함할 수 없습니다"
        # 설명 길이 확인 (최대 1024자)
        if len(description) > 1024:
            return False, f"설명이 너무 깁니다 ({len(description)}자). 최대 1024자"

    # 호환성 필드 유효성 검사 (선택 사항)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"호환성은 문자열이어야 합니다. {type(compatibility).__name__} 받음"
        if len(compatibility) > 500:
            return False, f"호환성이 너무 깁니다 ({len(compatibility)}자). 최대 500자"

    return True, "스킬이 유효합니다!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python quick_validate.py <스킬디렉토리>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
