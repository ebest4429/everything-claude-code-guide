"""
[redlining.py]
====================
[역할] Word 문서의 변경 내용 추적(tracked changes)을 유효성 검사합니다.

[주요 기능]
  - 지정 작성자의 변경 내용 추적 여부 검사
  - 변경 추적 제거 후 원본/수정본 텍스트 동일성 비교
  - git word-diff를 활용한 상세 차이 보고
  - 잘못된 중첩 삽입/삭제 패턴 감지

[주요 클래스]
  - RedliningValidator: Word 문서 변경 내용 추적 검사기
"""

import subprocess
import tempfile
import zipfile
from pathlib import Path


class RedliningValidator:

    def __init__(self, unpacked_dir, original_docx, verbose=False, author="Claude"):
        self.unpacked_dir = Path(unpacked_dir)
        self.original_docx = Path(original_docx)
        self.verbose = verbose
        self.author = author
        self.namespaces = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        }

    def repair(self) -> int:
        return 0

    def validate(self):
        modified_file = self.unpacked_dir / "word" / "document.xml"
        if not modified_file.exists():
            print(f"실패 - 수정된 document.xml을 찾을 수 없습니다: {modified_file}")
            return False

        try:
            import xml.etree.ElementTree as ET

            tree = ET.parse(modified_file)
            root = tree.getroot()

            del_elements = root.findall(".//w:del", self.namespaces)
            ins_elements = root.findall(".//w:ins", self.namespaces)

            author_del_elements = [
                elem
                for elem in del_elements
                if elem.get(f"{{{self.namespaces['w']}}}author") == self.author
            ]
            author_ins_elements = [
                elem
                for elem in ins_elements
                if elem.get(f"{{{self.namespaces['w']}}}author") == self.author
            ]

            if not author_del_elements and not author_ins_elements:
                if self.verbose:
                    print(f"통과 - {self.author}의 변경 내용 추적 없음")
                return True

        except Exception:
            pass

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            try:
                with zipfile.ZipFile(self.original_docx, "r") as zip_ref:
                    zip_ref.extractall(temp_path)
            except Exception as e:
                print(f"실패 - 원본 docx 압축 해제 오류: {e}")
                return False

            original_file = temp_path / "word" / "document.xml"
            if not original_file.exists():
                print(
                    f"실패 - {self.original_docx} 내 원본 document.xml을 찾을 수 없습니다"
                )
                return False

            try:
                import xml.etree.ElementTree as ET

                modified_tree = ET.parse(modified_file)
                modified_root = modified_tree.getroot()
                original_tree = ET.parse(original_file)
                original_root = original_tree.getroot()
            except ET.ParseError as e:
                print(f"실패 - XML 파일 파싱 오류: {e}")
                return False

            self._remove_author_tracked_changes(original_root)
            self._remove_author_tracked_changes(modified_root)

            modified_text = self._extract_text_content(modified_root)
            original_text = self._extract_text_content(original_root)

            if modified_text != original_text:
                error_message = self._generate_detailed_diff(
                    original_text, modified_text
                )
                print(error_message)
                return False

            if self.verbose:
                print(f"통과 - {self.author}의 모든 변경 사항이 올바르게 추적됨")
            return True

    def _generate_detailed_diff(self, original_text, modified_text):
        error_parts = [
            f"실패 - {self.author}의 변경 내용 추적 제거 후 문서 텍스트가 일치하지 않습니다",
            "",
            "가능한 원인:",
            "  1. 다른 작성자의 <w:ins> 또는 <w:del> 태그 내부에서 텍스트를 수정함",
            "  2. 변경 내용 추적 없이 편집함",
            "  3. 다른 작성자의 삽입을 삭제할 때 <w:ins> 내부에 <w:del>을 중첩하지 않음",
            "",
            "기존에 redline이 있는 문서의 경우 올바른 패턴을 사용하세요:",
            "  - 다른 작성자의 삽입을 거부: 해당 <w:ins> 내부에 <w:del> 중첩",
            "  - 다른 작성자의 삭제를 복원: 해당 <w:del> 이후에 새 <w:ins> 추가",
            "",
        ]

        git_diff = self._get_git_word_diff(original_text, modified_text)
        if git_diff:
            error_parts.extend(["차이점:", "============", git_diff])
        else:
            error_parts.append("단어 diff를 생성할 수 없습니다 (git 미설치)")

        return "\n".join(error_parts)

    def _get_git_word_diff(self, original_text, modified_text):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                original_file = temp_path / "original.txt"
                modified_file = temp_path / "modified.txt"

                original_file.write_text(original_text, encoding="utf-8")
                modified_file.write_text(modified_text, encoding="utf-8")

                result = subprocess.run(
                    [
                        "git",
                        "diff",
                        "--word-diff=plain",
                        "--word-diff-regex=.",  
                        "-U0",  
                        "--no-index",
                        str(original_file),
                        str(modified_file),
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.stdout.strip():
                    lines = result.stdout.split("\n")
                    content_lines = []
                    in_content = False
                    for line in lines:
                        if line.startswith("@@"):
                            in_content = True
                            continue
                        if in_content and line.strip():
                            content_lines.append(line)

                    if content_lines:
                        return "\n".join(content_lines)

                result = subprocess.run(
                    [
                        "git",
                        "diff",
                        "--word-diff=plain",
                        "-U0",  
                        "--no-index",
                        str(original_file),
                        str(modified_file),
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.stdout.strip():
                    lines = result.stdout.split("\n")
                    content_lines = []
                    in_content = False
                    for line in lines:
                        if line.startswith("@@"):
                            in_content = True
                            continue
                        if in_content and line.strip():
                            content_lines.append(line)
                    return "\n".join(content_lines)

        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

        return None

    def _remove_author_tracked_changes(self, root):
        ins_tag = f"{{{self.namespaces['w']}}}ins"
        del_tag = f"{{{self.namespaces['w']}}}del"
        author_attr = f"{{{self.namespaces['w']}}}author"

        for parent in root.iter():
            to_remove = []
            for child in parent:
                if child.tag == ins_tag and child.get(author_attr) == self.author:
                    to_remove.append(child)
            for elem in to_remove:
                parent.remove(elem)

        deltext_tag = f"{{{self.namespaces['w']}}}delText"
        t_tag = f"{{{self.namespaces['w']}}}t"

        for parent in root.iter():
            to_process = []
            for child in parent:
                if child.tag == del_tag and child.get(author_attr) == self.author:
                    to_process.append((child, list(parent).index(child)))

            for del_elem, del_index in reversed(to_process):
                for elem in del_elem.iter():
                    if elem.tag == deltext_tag:
                        elem.tag = t_tag

                for child in reversed(list(del_elem)):
                    parent.insert(del_index, child)
                parent.remove(del_elem)

    def _extract_text_content(self, root):
        p_tag = f"{{{self.namespaces['w']}}}p"
        t_tag = f"{{{self.namespaces['w']}}}t"

        paragraphs = []
        for p_elem in root.findall(f".//{p_tag}"):
            text_parts = []
            for t_elem in p_elem.findall(f".//{t_tag}"):
                if t_elem.text:
                    text_parts.append(t_elem.text)
            paragraph_text = "".join(text_parts)
            if paragraph_text:
                paragraphs.append(paragraph_text)

        return "\n".join(paragraphs)


if __name__ == "__main__":
    raise RuntimeError("This module should not be run directly.")
