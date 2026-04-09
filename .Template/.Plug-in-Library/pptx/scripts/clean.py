"""
[clean.py]
====================
[역할] 압축 해제된 PPTX 디렉토리에서 참조되지 않는 파일을 제거합니다.

[주요 기능]
  - sldIdLst에 없는 고아 슬라이드 및 관계 파일 제거
  - [trash] 디렉토리 제거
  - 삭제된 리소스의 고아 .rels 파일 제거
  - 참조되지 않는 미디어, 임베딩, 차트, 다이어그램, 드로잉, 잉크 파일 제거
  - 참조되지 않는 테마 파일 제거
  - 참조되지 않는 노트 슬라이드 제거
  - 삭제된 파일의 Content-Type 오버라이드 제거

[사용법]
  python clean.py <압축해제_디렉토리>

[예시]
  python clean.py unpacked/

[주요 함수]
  - clean_unused_files()      : 전체 정리 실행 (메인 진입점)
  - remove_orphaned_slides()  : 고아 슬라이드 제거
  - remove_orphaned_files()   : 참조되지 않는 리소스 제거
"""

import sys
from pathlib import Path

import defusedxml.minidom


import re


def get_slides_in_sldidlst(unpacked_dir: Path) -> set[str]:
    pres_path = unpacked_dir / "ppt" / "presentation.xml"
    pres_rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"

    if not pres_path.exists() or not pres_rels_path.exists():
        return set()

    rels_dom = defusedxml.minidom.parse(str(pres_rels_path))
    rid_to_slide = {}
    for rel in rels_dom.getElementsByTagName("Relationship"):
        rid = rel.getAttribute("Id")
        target = rel.getAttribute("Target")
        rel_type = rel.getAttribute("Type")
        if "slide" in rel_type and target.startswith("slides/"):
            rid_to_slide[rid] = target.replace("slides/", "")

    pres_content = pres_path.read_text(encoding="utf-8")
    referenced_rids = set(re.findall(r'<p:sldId[^>]*r:id="([^"]+)"', pres_content))

    return {rid_to_slide[rid] for rid in referenced_rids if rid in rid_to_slide}


def remove_orphaned_slides(unpacked_dir: Path) -> list[str]:
    slides_dir = unpacked_dir / "ppt" / "slides"
    slides_rels_dir = slides_dir / "_rels"
    pres_rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"

    if not slides_dir.exists():
        return []

    referenced_slides = get_slides_in_sldidlst(unpacked_dir)
    removed = []

    for slide_file in slides_dir.glob("slide*.xml"):
        if slide_file.name not in referenced_slides:
            rel_path = slide_file.relative_to(unpacked_dir)
            slide_file.unlink()
            removed.append(str(rel_path))

            rels_file = slides_rels_dir / f"{slide_file.name}.rels"
            if rels_file.exists():
                rels_file.unlink()
                removed.append(str(rels_file.relative_to(unpacked_dir)))

    if removed and pres_rels_path.exists():
        rels_dom = defusedxml.minidom.parse(str(pres_rels_path))
        changed = False

        for rel in list(rels_dom.getElementsByTagName("Relationship")):
            target = rel.getAttribute("Target")
            if target.startswith("slides/"):
                slide_name = target.replace("slides/", "")
                if slide_name not in referenced_slides:
                    if rel.parentNode:
                        rel.parentNode.removeChild(rel)
                        changed = True

        if changed:
            with open(pres_rels_path, "wb") as f:
                f.write(rels_dom.toxml(encoding="utf-8"))

    return removed


def remove_trash_directory(unpacked_dir: Path) -> list[str]:
    trash_dir = unpacked_dir / "[trash]"
    removed = []

    if trash_dir.exists() and trash_dir.is_dir():
        for file_path in trash_dir.iterdir():
            if file_path.is_file():
                rel_path = file_path.relative_to(unpacked_dir)
                removed.append(str(rel_path))
                file_path.unlink()
        trash_dir.rmdir()

    return removed


def get_slide_referenced_files(unpacked_dir: Path) -> set:
    referenced = set()
    slides_rels_dir = unpacked_dir / "ppt" / "slides" / "_rels"

    if not slides_rels_dir.exists():
        return referenced

    for rels_file in slides_rels_dir.glob("*.rels"):
        dom = defusedxml.minidom.parse(str(rels_file))
        for rel in dom.getElementsByTagName("Relationship"):
            target = rel.getAttribute("Target")
            if not target:
                continue
            target_path = (rels_file.parent.parent / target).resolve()
            try:
                referenced.add(target_path.relative_to(unpacked_dir.resolve()))
            except ValueError:
                pass

    return referenced


def remove_orphaned_rels_files(unpacked_dir: Path) -> list[str]:
    resource_dirs = ["charts", "diagrams", "drawings"]
    removed = []
    slide_referenced = get_slide_referenced_files(unpacked_dir)

    for dir_name in resource_dirs:
        rels_dir = unpacked_dir / "ppt" / dir_name / "_rels"
        if not rels_dir.exists():
            continue

        for rels_file in rels_dir.glob("*.rels"):
            resource_file = rels_dir.parent / rels_file.name.replace(".rels", "")
            try:
                resource_rel_path = resource_file.resolve().relative_to(unpacked_dir.resolve())
            except ValueError:
                continue

            if not resource_file.exists() or resource_rel_path not in slide_referenced:
                rels_file.unlink()
                rel_path = rels_file.relative_to(unpacked_dir)
                removed.append(str(rel_path))

    return removed


def get_referenced_files(unpacked_dir: Path) -> set:
    referenced = set()

    for rels_file in unpacked_dir.rglob("*.rels"):
        dom = defusedxml.minidom.parse(str(rels_file))
        for rel in dom.getElementsByTagName("Relationship"):
            target = rel.getAttribute("Target")
            if not target:
                continue
            target_path = (rels_file.parent.parent / target).resolve()
            try:
                referenced.add(target_path.relative_to(unpacked_dir.resolve()))
            except ValueError:
                pass

    return referenced


def remove_orphaned_files(unpacked_dir: Path, referenced: set) -> list[str]:
    resource_dirs = ["media", "embeddings", "charts", "diagrams", "tags", "drawings", "ink"]
    removed = []

    for dir_name in resource_dirs:
        dir_path = unpacked_dir / "ppt" / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.glob("*"):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))

    theme_dir = unpacked_dir / "ppt" / "theme"
    if theme_dir.exists():
        for file_path in theme_dir.glob("theme*.xml"):
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))
                theme_rels = theme_dir / "_rels" / f"{file_path.name}.rels"
                if theme_rels.exists():
                    theme_rels.unlink()
                    removed.append(str(theme_rels.relative_to(unpacked_dir)))

    notes_dir = unpacked_dir / "ppt" / "notesSlides"
    if notes_dir.exists():
        for file_path in notes_dir.glob("*.xml"):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(unpacked_dir)
            if rel_path not in referenced:
                file_path.unlink()
                removed.append(str(rel_path))

        notes_rels_dir = notes_dir / "_rels"
        if notes_rels_dir.exists():
            for file_path in notes_rels_dir.glob("*.rels"):
                notes_file = notes_dir / file_path.name.replace(".rels", "")
                if not notes_file.exists():
                    file_path.unlink()
                    removed.append(str(file_path.relative_to(unpacked_dir)))

    return removed


def update_content_types(unpacked_dir: Path, removed_files: list[str]) -> None:
    ct_path = unpacked_dir / "[Content_Types].xml"
    if not ct_path.exists():
        return

    dom = defusedxml.minidom.parse(str(ct_path))
    changed = False

    for override in list(dom.getElementsByTagName("Override")):
        part_name = override.getAttribute("PartName").lstrip("/")
        if part_name in removed_files:
            if override.parentNode:
                override.parentNode.removeChild(override)
                changed = True

    if changed:
        with open(ct_path, "wb") as f:
            f.write(dom.toxml(encoding="utf-8"))


def clean_unused_files(unpacked_dir: Path) -> list[str]:
    all_removed = []

    slides_removed = remove_orphaned_slides(unpacked_dir)
    all_removed.extend(slides_removed)

    trash_removed = remove_trash_directory(unpacked_dir)
    all_removed.extend(trash_removed)

    while True:
        removed_rels = remove_orphaned_rels_files(unpacked_dir)
        referenced = get_referenced_files(unpacked_dir)
        removed_files = remove_orphaned_files(unpacked_dir, referenced)

        total_removed = removed_rels + removed_files
        if not total_removed:
            break

        all_removed.extend(total_removed)

    if all_removed:
        update_content_types(unpacked_dir, all_removed)

    return all_removed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python clean.py <압축해제_디렉토리>", file=sys.stderr)
        print("예시: python clean.py unpacked/", file=sys.stderr)
        sys.exit(1)

    unpacked_dir = Path(sys.argv[1])

    if not unpacked_dir.exists():
        print(f"오류: {unpacked_dir} 를 찾을 수 없습니다", file=sys.stderr)
        sys.exit(1)

    removed = clean_unused_files(unpacked_dir)

    if removed:
        print(f"참조되지 않는 파일 {len(removed)}개 제거:")
        for f in removed:
            print(f"  {f}")
    else:
        print("참조되지 않는 파일 없음")
