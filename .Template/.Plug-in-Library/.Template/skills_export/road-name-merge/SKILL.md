---
name: road-name-merge
description: 시도별(충북, 충남, 전북, 경기 등) 도로명정보조회 xlsx 파일들을 하나의 통합 파일로 자동 병합하는 스킬. 폴더 내 모든 엑셀 파일을 탐색하여 총건수 행·중복 헤더를 제거하고 깔끔하게 합칩니다. 사용자가 "도로명 통합", "엑셀 합치기", "시도 도로명 파일 합치기", "폴더 안 xlsx 통합" 등을 언급하면 반드시 이 스킬을 사용하세요.
---

# 도로명정보조회 엑셀 통합 스킬

## 📖 사용법 가이드 (Usage Guide)

### ▶ 한국어 — Cowork에서 사용
```
시도 폴더의 도로명 엑셀 파일들을 하나로 통합해줘
  · 시도명: 충남
  · 폴더:   /Users/me/Documents/충남_도로명
```
또는 자연어로:
```
충남 폴더(/Desktop/충남) 안 도로명 xlsx 전부 합쳐서 충남_도로명정보조회.xlsx 만들어줘
```

### ▶ English — Using in Cowork
```
Merge all road-name Excel files into one.
  · Province : Chungnam (충남)
  · Folder   : /Users/me/Documents/Chungnam_roads
```

### ▶ Claude CLI (Claude Code) — slash command 등록 후
```bash
# 한글 명령어
/도로명통합 충남 /Users/me/Documents/충남_도로명

# English command
/road-name-merge Chungnam /Users/me/Documents/Chungnam_roads
```
> CLI 커맨드 설치 방법은 아래 **"CLI 등록 가이드"** 참고

---

## 입력 파라미터

| 파라미터 | 예시 | 설명 |
|----------|------|------|
| 시도명 (province) | 충북, 충남, 전북, 경기 | 출력 파일명 앞에 붙는 이름 |
| 폴더경로 (folder) | /path/to/folder | xlsx 파일들이 있는 폴더 |

---

## 실행 규칙

각 원본 파일의 구조:
```
Row 0  →  총N건 (도로명수 : N)   ← 모든 파일에서 제외
Row 1  →  헤더 (시군구, 도로명번호 …)  ← 첫 번째 파일만 포함
Row 2+ →  실제 데이터             ← 모든 파일에서 포함
```

---

## 스킬 실행 절차

### Step 1 — 입력값 확인
사용자 메시지에서 **시도명**과 **폴더경로**를 파악한다.
값이 없으면 AskUserQuestion 도구로 질문한다.

### Step 2 — 파일 목록 확인
```python
import os
folder = "<user_provided_folder>"
files = sorted([f for f in os.listdir(folder) if f.endswith('.xlsx')])
```
파일이 없으면 사용자에게 경로를 다시 확인하도록 안내한다.

### Step 3 — 스크립트 실행
이 스킬 폴더의 `scripts/merge_road_names.py`를 사용한다.

```bash
python "<SKILL_DIR>/scripts/merge_road_names.py" "[시도명]" "[폴더경로]"
```

`<SKILL_DIR>`은 이 SKILL.md가 위치한 디렉토리 경로로 치환한다.

### Step 4 — 결과 보고
- 통합 파일 경로를 `present_files` 도구로 사용자에게 전달
- 시군구별 건수 요약 출력 (선택)

---

## 출력 파일 규칙
- 파일명: `[시도명]_도로명정보조회.xlsx`
- 위치: 입력 폴더와 **동일한 폴더**
- 헤더 행: 파란색(#4472C4) 배경 + 흰색 볼드
- 열 너비: 자동 지정 (시군구 8, 도로명번호 12, 도로명 20, 로마자표기 30, …)
- 틀 고정: 1행 헤더 고정

---

## CLI 등록 가이드

Claude CLI (claude code)에서 `/도로명통합` 또는 `/road-name-merge` 슬래시 커맨드로
사용하려면 아래 단계를 따릅니다.

### 1. 커맨드 파일 복사

```bash
# 프로젝트별 등록 (해당 프로젝트에서만 사용)
cp cli-commands/도로명통합.md      /your/project/.claude/commands/
cp cli-commands/road-name-merge.md /your/project/.claude/commands/

# 전역 등록 (모든 프로젝트에서 사용)
cp cli-commands/도로명통합.md      ~/.claude/commands/
cp cli-commands/road-name-merge.md ~/.claude/commands/
```

### 2. scripts 폴더 접근 가능 위치에 복사

```bash
# 전역 사용 시 스크립트도 고정 경로에 복사 (예시)
mkdir -p ~/.claude/scripts/도로명통합
cp scripts/merge_road_names.py ~/.claude/scripts/도로명통합/
```

### 3. CLI에서 사용

```bash
# 프로젝트 디렉토리에서 claude 실행 후
/도로명통합 충남 /Users/me/Documents/충남_도로명
/road-name-merge Gyeonggi /Users/me/Documents/Gyeonggi_roads
```

---

## 지원 시도 예시

| 한글 | 영문 | 출력 파일명 예시 |
|------|------|-----------------|
| 충북 | Chungbuk | 충북_도로명정보조회.xlsx |
| 충남 | Chungnam | 충남_도로명정보조회.xlsx |
| 전북 | Jeonbuk  | 전북_도로명정보조회.xlsx |
| 전남 | Jeonnam  | 전남_도로명정보조회.xlsx |
| 경기 | Gyeonggi | 경기_도로명정보조회.xlsx |
| 경북 | Gyeongbuk| 경북_도로명정보조회.xlsx |
| 경남 | Gyeongnam| 경남_도로명정보조회.xlsx |
| 서울 | Seoul    | 서울_도로명정보조회.xlsx |

시도명에 제한 없음 — 임의의 이름을 사용할 수 있습니다.
