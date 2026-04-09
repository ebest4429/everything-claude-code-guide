"""
[simplify_redlines.py]
====================
[역할] 인접한 w:ins 또는 w:del 요소를 병합하여 변경 내용 추적을 단순화합니다.

[주요 기능]
  - 동일 작성자의 인접 <w:ins> 요소를 단일 요소로 병합
  - 동일 작성자의 인접 <w:del> 요소를 단일 요소로 병합
  - 변경 내용 추적 래퍼 수를 줄여 heavily-redlined 문서 작업을 편리하게 함

[병합 규칙]
  - w:ins와 w:ins, w:del과 w:del만 병합 (동일 요소 타입)
  - 동일 작성자인 경우에만 병합 (타임스탬프 차이 무시)
  - 진정으로 인접한 경우에만 병합 (사이에 공백만 있는 경우)

[주요 함수]
  - simplify_redlines(): 메인 진입점 — DOCX에서 변경 내용 추적 단순화
  - infer_author()     : 수정된 문서에서 새 변경 작성자 추론
"""

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import defusedxml.minidom

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def simplify_redlines(input_dir: str) -> tuple[int, str]:
    doc_xml = Path(input_dir) / "word" / "document.xml"

    if not doc_xml.exists():
        return 0, f"오류: {doc_xml} 파일을 찾을 수 없습니다"

    try:
        dom = defusedxml.minidom.parseString(doc_xml.read_text(encoding="utf-8"))
        root = dom.documentElement

        merge_count = 0

        containers = _find_elements(root, "p") + _find_elements(root, "tc")

        for container in containers:
            merge_count += _merge_tracked_changes_in(container, "ins")
            merge_count += _merge_tracked_changes_in(container, "del")

        doc_xml.write_bytes(dom.toxml(encoding="UTF-8"))
        return merge_count, f"변경 내용 추적 {merge_count}건 단순화 완료"

    except Exception as e:
        return 0, f"오류: {e}"


def _merge_tracked_changes_in(container, tag: str) -> int:
    merge_count = 0

    tracked = [
        child
        for child in container.childNodes
        if child.nodeType == child.ELEMENT_NODE and _is_element(child, tag)
    ]

    if len(tracked) < 2:
        return 0

    i = 0
    while i < len(tracked) - 1:
        curr = tracked[i]
        next_elem = tracked[i + 1]

        if _can_merge_tracked(curr, next_elem):
            _merge_tracked_content(curr, next_elem)
            container.removeChild(next_elem)
            tracked.pop(i + 1)
            merge_count += 1
        else:
            i += 1

    return merge_count


def _is_element(node, tag: str) -> bool:
    name = node.localName or node.tagName
    return name == tag or name.endswith(f":{tag}")


def _get_author(elem) -> str:
    author = elem.getAttribute("w:author")
    if not author:
        for attr in elem.attributes.values():
            if attr.localName == "author" or attr.name.endswith(":author"):
                return attr.value
    return author


def _can_merge_tracked(elem1, elem2) -> bool:
    if _get_author(elem1) != _get_author(elem2):
        return False

    node = elem1.nextSibling
    while node and node != elem2:
        if node.nodeType == node.ELEMENT_NODE:
            return False
        if node.nodeType == node.TEXT_NODE and node.data.strip():
            return False
        node = node.nextSibling

    return True


def _merge_tracked_content(target, source):
    while source.firstChild:
        child = source.firstChild
        source.removeChild(child)
        target.appendChild(child)


def _find_elements(root, tag: str) -> list:
    results = []

    def traverse(node):
        if node.nodeType == node.ELEMENT_NODE:
            name = node.localName or node.tagName
            if name == tag or name.endswith(f":{tag}"):
                results.append(node)
            for child in node.childNodes:
                traverse(child)

    traverse(root)
    return results


def get_tracked_change_authors(doc_xml_path: Path) -> dict[str, int]:
    if not doc_xml_path.exists():
        return {}

    try:
        tree = ET.parse(doc_xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return {}

    namespaces = {"w": WORD_NS}
    author_attr = f"{{{WORD_NS}}}author"

    authors: dict[str, int] = {}
    for tag in ["ins", "del"]:
        for elem in root.findall(f".//w:{tag}", namespaces):
            author = elem.get(author_attr)
            if author:
                authors[author] = authors.get(author, 0) + 1

    return authors


def _get_authors_from_docx(docx_path: Path) -> dict[str, int]:
    try:
        with zipfile.ZipFile(docx_path, "r") as zf:
            if "word/document.xml" not in zf.namelist():
                return {}
            with zf.open("word/document.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()

                namespaces = {"w": WORD_NS}
                author_attr = f"{{{WORD_NS}}}author"

                authors: dict[str, int] = {}
                for tag in ["ins", "del"]:
                    for elem in root.findall(f".//w:{tag}", namespaces):
                        author = elem.get(author_attr)
                        if author:
                            authors[author] = authors.get(author, 0) + 1
                return authors
    except (zipfile.BadZipFile, ET.ParseError):
        return {}


def infer_author(modified_dir: Path, original_docx: Path, default: str = "Claude") -> str:
    modified_xml = modified_dir / "word" / "document.xml"
    modified_authors = get_tracked_change_authors(modified_xml)

    if not modified_authors:
        return default

    original_authors = _get_authors_from_docx(original_docx)

    new_changes: dict[str, int] = {}
    for author, count in modified_authors.items():
        original_count = original_authors.get(author, 0)
        diff = count - original_count
        if diff > 0:
            new_changes[author] = diff

    if not new_changes:
        return default

    if len(new_changes) == 1:
        return next(iter(new_changes))

    raise ValueError(
        f"여러 작성자가 새 변경 사항을 추가했습니다: {new_changes}. "
        "검사할 작성자를 추론할 수 없습니다."
    )
