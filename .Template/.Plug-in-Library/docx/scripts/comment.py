"""
[comment.py]
====================
[역할] DOCX 문서에 주석을 추가합니다.

[주요 기능]
  - Word 문서 XML에 주석 및 답글 추가
  - 주석 관련 XML 파일(comments, commentsExtended 등) 자동 관리
  - 스마트 따옴표 엔티티 인코딩 처리

[사용법]
  python comment.py unpacked/ 0 "주석 텍스트"
  python comment.py unpacked/ 1 "답글 텍스트" --parent 0

  텍스트는 미리 이스케이프된 XML이어야 합니다 (예: &amp; → &, &#x2019; → 스마트 따옴표).

  실행 후 document.xml에 마커를 추가하세요:
    <w:commentRangeStart w:id="0"/>
    ... 주석이 달린 내용 ...
    <w:commentRangeEnd w:id="0"/>
    <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

[주요 함수]
  - add_comment(): 주석 추가 실행
"""

import argparse
import random
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import defusedxml.minidom

TEMPLATE_DIR = Path(__file__).parent / "templates"
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
}

COMMENT_XML = """\
<w:comment w:id="{id}" w:author="{author}" w:date="{date}" w:initials="{initials}">
  <w:p w14:paraId="{para_id}" w14:textId="77777777">
    <w:r>
      <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
      <w:annotationRef/>
    </w:r>
    <w:r>
      <w:rPr>
        <w:color w:val="000000"/>
        <w:sz w:val="20"/>
        <w:szCs w:val="20"/>
      </w:rPr>
      <w:t>{text}</w:t>
    </w:r>
  </w:p>
</w:comment>"""

COMMENT_MARKER_TEMPLATE = """
document.xml에 추가 (마커는 w:p의 직접 자식이어야 하며, w:r 안에 넣으면 안 됩니다):
  <w:commentRangeStart w:id="{cid}"/>
  <w:r>...</w:r>
  <w:commentRangeEnd w:id="{cid}"/>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>"""

REPLY_MARKER_TEMPLATE = """
부모 {pid}의 마커 안에 중첩 (마커는 w:p의 직접 자식이어야 하며, w:r 안에 넣으면 안 됩니다):
  <w:commentRangeStart w:id="{pid}"/><w:commentRangeStart w:id="{cid}"/>
  <w:r>...</w:r>
  <w:commentRangeEnd w:id="{cid}"/><w:commentRangeEnd w:id="{pid}"/>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{pid}"/></w:r>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>"""


def _generate_hex_id() -> str:
    return f"{random.randint(0, 0x7FFFFFFE):08X}"


SMART_QUOTE_ENTITIES = {
    "\u201c": "&#x201C;",
    "\u201d": "&#x201D;",
    "\u2018": "&#x2018;",
    "\u2019": "&#x2019;",
}


def _encode_smart_quotes(text: str) -> str:
    for char, entity in SMART_QUOTE_ENTITIES.items():
        text = text.replace(char, entity)
    return text


def _append_xml(xml_path: Path, root_tag: str, content: str) -> None:
    dom = defusedxml.minidom.parseString(xml_path.read_text(encoding="utf-8"))
    root = dom.getElementsByTagName(root_tag)[0]
    ns_attrs = " ".join(f'xmlns:{k}="{v}"' for k, v in NS.items())
    wrapper_dom = defusedxml.minidom.parseString(f"<root {ns_attrs}>{content}</root>")
    for child in wrapper_dom.documentElement.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            root.appendChild(dom.importNode(child, True))
    output = _encode_smart_quotes(dom.toxml(encoding="UTF-8").decode("utf-8"))
    xml_path.write_text(output, encoding="utf-8")


def _find_para_id(comments_path: Path, comment_id: int) -> str | None:
    dom = defusedxml.minidom.parseString(comments_path.read_text(encoding="utf-8"))
    for c in dom.getElementsByTagName("w:comment"):
        if c.getAttribute("w:id") == str(comment_id):
            for p in c.getElementsByTagName("w:p"):
                if pid := p.getAttribute("w14:paraId"):
                    return pid
    return None


def _get_next_rid(rels_path: Path) -> int:
    dom = defusedxml.minidom.parseString(rels_path.read_text(encoding="utf-8"))
    max_rid = 0
    for rel in dom.getElementsByTagName("Relationship"):
        rid = rel.getAttribute("Id")
        if rid and rid.startswith("rId"):
            try:
                max_rid = max(max_rid, int(rid[3:]))
            except ValueError:
                pass
    return max_rid + 1


def _has_relationship(rels_path: Path, target: str) -> bool:
    dom = defusedxml.minidom.parseString(rels_path.read_text(encoding="utf-8"))
    for rel in dom.getElementsByTagName("Relationship"):
        if rel.getAttribute("Target") == target:
            return True
    return False


def _has_content_type(ct_path: Path, part_name: str) -> bool:
    dom = defusedxml.minidom.parseString(ct_path.read_text(encoding="utf-8"))
    for override in dom.getElementsByTagName("Override"):
        if override.getAttribute("PartName") == part_name:
            return True
    return False


def _ensure_comment_relationships(unpacked_dir: Path) -> None:
    rels_path = unpacked_dir / "word" / "_rels" / "document.xml.rels"
    if not rels_path.exists():
        return

    if _has_relationship(rels_path, "comments.xml"):
        return

    dom = defusedxml.minidom.parseString(rels_path.read_text(encoding="utf-8"))
    root = dom.documentElement
    next_rid = _get_next_rid(rels_path)

    rels = [
        (
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments",
            "comments.xml",
        ),
        (
            "http://schemas.microsoft.com/office/2011/relationships/commentsExtended",
            "commentsExtended.xml",
        ),
        (
            "http://schemas.microsoft.com/office/2016/09/relationships/commentsIds",
            "commentsIds.xml",
        ),
        (
            "http://schemas.microsoft.com/office/2018/08/relationships/commentsExtensible",
            "commentsExtensible.xml",
        ),
    ]

    for rel_type, target in rels:
        rel = dom.createElement("Relationship")
        rel.setAttribute("Id", f"rId{next_rid}")
        rel.setAttribute("Type", rel_type)
        rel.setAttribute("Target", target)
        root.appendChild(rel)
        next_rid += 1

    rels_path.write_bytes(dom.toxml(encoding="UTF-8"))


def _ensure_comment_content_types(unpacked_dir: Path) -> None:
    ct_path = unpacked_dir / "[Content_Types].xml"
    if not ct_path.exists():
        return

    if _has_content_type(ct_path, "/word/comments.xml"):
        return

    dom = defusedxml.minidom.parseString(ct_path.read_text(encoding="utf-8"))
    root = dom.documentElement

    overrides = [
        (
            "/word/comments.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml",
        ),
        (
            "/word/commentsExtended.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml",
        ),
        (
            "/word/commentsIds.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml",
        ),
        (
            "/word/commentsExtensible.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtensible+xml",
        ),
    ]

    for part_name, content_type in overrides:
        override = dom.createElement("Override")
        override.setAttribute("PartName", part_name)
        override.setAttribute("ContentType", content_type)
        root.appendChild(override)

    ct_path.write_bytes(dom.toxml(encoding="UTF-8"))


def add_comment(
    unpacked_dir: str,
    comment_id: int,
    text: str,
    author: str = "Claude",
    initials: str = "C",
    parent_id: int | None = None,
) -> tuple[str, str]:
    word = Path(unpacked_dir) / "word"
    if not word.exists():
        return "", f"오류: {word} 를 찾을 수 없습니다"

    para_id, durable_id = _generate_hex_id(), _generate_hex_id()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    comments = word / "comments.xml"
    first_comment = not comments.exists()
    if first_comment:
        shutil.copy(TEMPLATE_DIR / "comments.xml", comments)
        _ensure_comment_relationships(Path(unpacked_dir))
        _ensure_comment_content_types(Path(unpacked_dir))
    _append_xml(
        comments,
        "w:comments",
        COMMENT_XML.format(
            id=comment_id,
            author=author,
            date=ts,
            initials=initials,
            para_id=para_id,
            text=text,
        ),
    )

    ext = word / "commentsExtended.xml"
    if not ext.exists():
        shutil.copy(TEMPLATE_DIR / "commentsExtended.xml", ext)
    if parent_id is not None:
        parent_para = _find_para_id(comments, parent_id)
        if not parent_para:
            return "", f"오류: 부모 주석 {parent_id} 를 찾을 수 없습니다"
        _append_xml(
            ext,
            "w15:commentsEx",
            f'<w15:commentEx w15:paraId="{para_id}" w15:paraIdParent="{parent_para}" w15:done="0"/>',
        )
    else:
        _append_xml(
            ext,
            "w15:commentsEx",
            f'<w15:commentEx w15:paraId="{para_id}" w15:done="0"/>',
        )

    ids = word / "commentsIds.xml"
    if not ids.exists():
        shutil.copy(TEMPLATE_DIR / "commentsIds.xml", ids)
    _append_xml(
        ids,
        "w16cid:commentsIds",
        f'<w16cid:commentId w16cid:paraId="{para_id}" w16cid:durableId="{durable_id}"/>',
    )

    extensible = word / "commentsExtensible.xml"
    if not extensible.exists():
        shutil.copy(TEMPLATE_DIR / "commentsExtensible.xml", extensible)
    _append_xml(
        extensible,
        "w16cex:commentsExtensible",
        f'<w16cex:commentExtensible w16cex:durableId="{durable_id}" w16cex:dateUtc="{ts}"/>',
    )

    action = "답글" if parent_id is not None else "주석"
    return para_id, f"{action} {comment_id} 추가 완료 (para_id={para_id})"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="DOCX 문서에 주석을 추가합니다")
    p.add_argument("unpacked_dir", help="언팩된 DOCX 디렉토리")
    p.add_argument("comment_id", type=int, help="주석 ID (고유값이어야 함)")
    p.add_argument("text", help="주석 텍스트")
    p.add_argument("--author", default="Claude", help="작성자 이름")
    p.add_argument("--initials", default="C", help="작성자 이니셜")
    p.add_argument("--parent", type=int, help="부모 주석 ID (답글인 경우)")
    args = p.parse_args()

    para_id, msg = add_comment(
        args.unpacked_dir,
        args.comment_id,
        args.text,
        args.author,
        args.initials,
        args.parent,
    )
    print(msg)
    if "오류" in msg:
        sys.exit(1)
    cid = args.comment_id
    if args.parent is not None:
        print(REPLY_MARKER_TEMPLATE.format(pid=args.parent, cid=cid))
    else:
        print(COMMENT_MARKER_TEMPLATE.format(cid=cid))
