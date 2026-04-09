<!--
╔══════════════════════════════════════════════════════════════╗
║  road-name-merge-code.md  ·  English Python-embedded Version ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Version Notes]                                             ║
║    Python code fully embedded — same code runs every time    ║
║    Consistent, validated logic; no variation between runs    ║
║    For the prompt-only version → road-name-merge.md          ║
║                                                              ║
║  [Installation]                                              ║
║    # Global (all projects)                                   ║
║    cp road-name-merge-code.md ~/.claude/commands/            ║
║                                                              ║
║    # Project-level (current project only)                    ║
║    cp road-name-merge-code.md ./.claude/commands/            ║
║                                                              ║
║  [Usage]  /road-name-merge-code [province] [folder-path]     ║
║                                                              ║
║  [Examples]                                                  ║
║    /road-name-merge-code Chungnam /Users/me/Chungnam_roads   ║
║    /road-name-merge-code Jeonbuk  C:\Users\me\Jeonbuk_roads  ║
║    /road-name-merge-code 경기      ~/Downloads/경기_도로명    ║
║                                                              ║
║  [Output]  [folder-path]/[province]_도로명정보조회.xlsx        ║
║                                                              ║
║  [Requirements]  pip install pandas openpyxl                 ║
╚══════════════════════════════════════════════════════════════╝
-->
---
description: Merge Korean road-name lookup (도로명정보조회) xlsx files into one consolidated file (Python-embedded). Removes total-count rows and duplicate headers; saves with full formatting. Usage: /road-name-merge-code [province] [folder-path]
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Road Name Information Excel Merger (English · Python-embedded)

## Parse Arguments

Extract province name and folder path from `$ARGUMENTS`.

- First token  = province name (e.g., Chungnam, Jeonbuk, Gyeonggi, or Korean: 충남)
- Second token = folder path  (e.g., /Users/me/Chungnam_roads)

If either value is missing, ask the user before proceeding.

## Processing Rules

```
Row 0  →  "총N건 (도로명수 : N)"  ← REMOVE from every file
Row 1  →  Column headers          ← Keep from FIRST file only
Row 2+ →  Actual data rows        ← Keep from ALL files
```

## Execution

Run the Python code below **exactly as written** using the Bash tool.
Only substitute `PROVINCE` and `FOLDER` with the user-provided values.

```python
import os, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── Configuration ─────────────────────────────────────────────
PROVINCE = "[province]"      # e.g., Chungnam
FOLDER   = "[folder-path]"   # e.g., /Users/me/Chungnam_roads
# ─────────────────────────────────────────────────────────────

FOLDER   = os.path.abspath(FOLDER)
OUT_FILE = f"{PROVINCE}_도로명정보조회.xlsx"
OUT_PATH = os.path.join(FOLDER, OUT_FILE)

files = sorted([f for f in os.listdir(FOLDER)
                if f.endswith(".xlsx") and f != OUT_FILE])

if not files:
    raise FileNotFoundError(f"No .xlsx files found in '{FOLDER}'.")

print(f"Files found: {len(files)}\n")
all_data, header = [], None

for i, fname in enumerate(files):
    df = pd.read_excel(os.path.join(FOLDER, fname), sheet_name=0, header=None)
    if i == 0:
        header = df.iloc[1].tolist()          # header from first file only
    chunk = df.iloc[2:].reset_index(drop=True)  # skip rows 0 & 1
    all_data.append(chunk)
    print(f"  [{i+1:02d}] {fname}  →  {len(chunk):,} rows")

combined = pd.concat(all_data, ignore_index=True)
print(f"\nMerged: {len(combined):,} rows × {len(header)} columns")

# ── Save with openpyxl formatting ─────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = "도로명정보조회"

thin   = Side(style="thin")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

H_FONT  = Font(name="Arial", bold=True, size=10, color="FFFFFF")
H_FILL  = PatternFill(fill_type="solid", start_color="4472C4", end_color="4472C4")
H_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
D_FONT  = Font(name="Arial", size=10)
D_ALIGN = Alignment(vertical="center")

for c, name in enumerate(header, 1):
    cell = ws.cell(row=1, column=c, value=name)
    cell.font = H_FONT; cell.fill = H_FILL
    cell.alignment = H_ALIGN; cell.border = border

for r, row in enumerate(combined.itertuples(index=False), 2):
    for c, val in enumerate(row, 1):
        cell = ws.cell(row=r, column=c)
        if pd.isna(val):
            cell.value = None
        elif isinstance(val, float) and val == int(val):
            cell.value = int(val)
        else:
            cell.value = val
        cell.font = D_FONT; cell.alignment = D_ALIGN; cell.border = border

COL_WIDTHS = [8, 12, 20, 30, 10, 8, 14, 8, 8, 10]
for i in range(len(header)):
    ws.column_dimensions[get_column_letter(i+1)].width = (
        COL_WIDTHS[i] if i < len(COL_WIDTHS) else 15)

ws.row_dimensions[1].height = 20
ws.freeze_panes = "A2"
wb.save(OUT_PATH)
print(f"\n✅ Saved: {OUT_PATH}")
```

## Report After Completion

- Provide the full path of the generated file
- Show total row count and number of source files merged
- Optionally show per-district (시군구명) row counts
- On error, explain the cause and suggest a fix

## Province Name Reference

| Korean | Romanized  | Output filename                |
|--------|------------|-------------------------------|
| 충북   | Chungbuk   | 충북_도로명정보조회.xlsx        |
| 충남   | Chungnam   | 충남_도로명정보조회.xlsx        |
| 전북   | Jeonbuk    | 전북_도로명정보조회.xlsx        |
| 전남   | Jeonnam    | 전남_도로명정보조회.xlsx        |
| 경기   | Gyeonggi   | 경기_도로명정보조회.xlsx        |
| 서울   | Seoul      | 서울_도로명정보조회.xlsx        |

Any custom province name is accepted.
