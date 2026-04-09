"""
[add_slide.py]
====================
[역할] 압축 해제된 PPTX 디렉토리에 새 슬라이드를 추가합니다.

[주요 기능]
  - 기존 슬라이드를 복제하여 새 슬라이드 생성
  - 슬라이드 레이아웃을 기반으로 새 슬라이드 생성
  - Content_Types.xml 및 presentation.xml.rels 자동 업데이트

[사용법]
  python add_slide.py <압축해제_디렉토리> <소스>

  소스 종류:
    slide2.xml        - 기존 슬라이드 복제
    slideLayout2.xml  - 레이아웃 템플릿으로 생성

[예시]
  python add_slide.py unpacked/ slide2.xml
  python add_slide.py unpacked/ slideLayout2.xml

[주요 함수]
  - duplicate_slide()          : 기존 슬라이드 복제
  - create_slide_from_layout() : 레이아웃으로 새 슬라이드 생성
"""

import re
import shutil
import sys
from pathlib import Path


def get_next_slide_number(slides_dir: Path) -> int:
    existing = [int(m.group(1)) for f in slides_dir.glob("slide*.xml")
                if (m := re.match(r"slide(\d+)\.xml", f.name))]
    return max(existing) + 1 if existing else 1


def create_slide_from_layout(unpacked_dir: Path, layout_file: str) -> None:
    slides_dir = unpacked_dir / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"
    layouts_dir = unpacked_dir / "ppt" / "slideLayouts"

    layout_path = layouts_dir / layout_file
    if not layout_path.exists():
        print(f"오류: {layout_path} 를 찾을 수 없습니다", file=sys.stderr)
        sys.exit(1)

    next_num = get_next_slide_number(slides_dir)
    dest = f"slide{next_num}.xml"
    dest_slide = slides_dir / dest
    dest_rels = rels_dir / f"{dest}.rels"

    slide_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>'''
    dest_slide.write_text(slide_xml, encoding="utf-8")

    rels_dir.mkdir(exist_ok=True)
    rels_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{layout_file}"/>
</Relationships>'''
    dest_rels.write_text(rels_xml, encoding="utf-8")

    _add_to_content_types(unpacked_dir, dest)

    rid = _add_to_presentation_rels(unpacked_dir, dest)

    next_slide_id = _get_next_slide_id(unpacked_dir)

    print(f"{layout_file} 로부터 {dest} 생성 완료")
    print(f'presentation.xml <p:sldIdLst>에 추가: <p:sldId id="{next_slide_id}" r:id="{rid}"/>')


def duplicate_slide(unpacked_dir: Path, source: str) -> None:
    slides_dir = unpacked_dir / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"

    source_slide = slides_dir / source

    if not source_slide.exists():
        print(f"오류: {source_slide} 를 찾을 수 없습니다", file=sys.stderr)
        sys.exit(1)

    next_num = get_next_slide_number(slides_dir)
    dest = f"slide{next_num}.xml"
    dest_slide = slides_dir / dest

    source_rels = rels_dir / f"{source}.rels"
    dest_rels = rels_dir / f"{dest}.rels"

    shutil.copy2(source_slide, dest_slide)

    if source_rels.exists():
        shutil.copy2(source_rels, dest_rels)

        rels_content = dest_rels.read_text(encoding="utf-8")
        rels_content = re.sub(
            r'\s*<Relationship[^>]*Type="[^"]*notesSlide"[^>]*/>\s*',
            "\n",
            rels_content,
        )
        dest_rels.write_text(rels_content, encoding="utf-8")

    _add_to_content_types(unpacked_dir, dest)

    rid = _add_to_presentation_rels(unpacked_dir, dest)

    next_slide_id = _get_next_slide_id(unpacked_dir)

    print(f"{source} 로부터 {dest} 생성 완료")
    print(f'presentation.xml <p:sldIdLst>에 추가: <p:sldId id="{next_slide_id}" r:id="{rid}"/>')


def _add_to_content_types(unpacked_dir: Path, dest: str) -> None:
    content_types_path = unpacked_dir / "[Content_Types].xml"
    content_types = content_types_path.read_text(encoding="utf-8")

    new_override = f'<Override PartName="/ppt/slides/{dest}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'

    if f"/ppt/slides/{dest}" not in content_types:
        content_types = content_types.replace("</Types>", f"  {new_override}\n</Types>")
        content_types_path.write_text(content_types, encoding="utf-8")


def _add_to_presentation_rels(unpacked_dir: Path, dest: str) -> str:
    pres_rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels = pres_rels_path.read_text(encoding="utf-8")

    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels)]
    next_rid = max(rids) + 1 if rids else 1
    rid = f"rId{next_rid}"

    new_rel = f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/{dest}"/>'

    if f"slides/{dest}" not in pres_rels:
        pres_rels = pres_rels.replace("</Relationships>", f"  {new_rel}\n</Relationships>")
        pres_rels_path.write_text(pres_rels, encoding="utf-8")

    return rid


def _get_next_slide_id(unpacked_dir: Path) -> int:
    pres_path = unpacked_dir / "ppt" / "presentation.xml"
    pres_content = pres_path.read_text(encoding="utf-8")
    slide_ids = [int(m) for m in re.findall(r'<p:sldId[^>]*id="(\d+)"', pres_content)]
    return max(slide_ids) + 1 if slide_ids else 256


def parse_source(source: str) -> tuple[str, str | None]:
    if source.startswith("slideLayout") and source.endswith(".xml"):
        return ("layout", source)

    return ("slide", None)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python add_slide.py <압축해제_디렉토리> <소스>", file=sys.stderr)
        print("", file=sys.stderr)
        print("소스 종류:", file=sys.stderr)
        print("  slide2.xml        - 기존 슬라이드 복제", file=sys.stderr)
        print("  slideLayout2.xml  - 레이아웃 템플릿으로 생성", file=sys.stderr)
        print("", file=sys.stderr)
        print("사용 가능한 레이아웃 확인: ls <압축해제_디렉토리>/ppt/slideLayouts/", file=sys.stderr)
        sys.exit(1)

    unpacked_dir = Path(sys.argv[1])
    source = sys.argv[2]

    if not unpacked_dir.exists():
        print(f"오류: {unpacked_dir} 를 찾을 수 없습니다", file=sys.stderr)
        sys.exit(1)

    source_type, layout_file = parse_source(source)

    if source_type == "layout" and layout_file is not None:
        create_slide_from_layout(unpacked_dir, layout_file)
    else:
        duplicate_slide(unpacked_dir, source)
