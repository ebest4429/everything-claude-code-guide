---
description: Merge Korean road-name lookup (도로명정보조회) xlsx files from a province folder into a single consolidated file. Automatically removes total-count rows and duplicate headers. Usage: /road-name-merge [province] [folder-path]
allowed-tools: Bash, Read, Write, Edit, Glob
---

# 🗺️ Road Name Information Excel Merger

## 📖 Usage

```
/road-name-merge [province] [folder-path]
```

**Examples:**
```
/road-name-merge Chungnam  /Users/me/Documents/Chungnam_roads
/road-name-merge Jeonbuk   C:/Users/me/Desktop/Jeonbuk_roads
/road-name-merge Gyeonggi  ~/Downloads/Gyeonggi_roads
/road-name-merge 충남       /Users/me/Documents/충남_도로명
```

**Parameters:**
- `[province]` — Province / region name prefixed to the output filename (e.g., Chungnam, 충남, Gyeonggi)
- `[folder-path]` — Path to the folder containing the `.xlsx` files to merge

**Output file:** `[folder-path]/[province]_도로명정보조회.xlsx`

---

## ⚙️ Processing Rules

Each source Excel file has this structure:
```
Row 0  →  Total-count header  (e.g., "총1,929건…")  ← EXCLUDED from all files
Row 1  →  Column headers      (시군구, 도로명번호 …)  ← Included from FIRST file only
Row 2+ →  Actual data rows                           ← Included from ALL files
```

---

## 🚀 Execution

Parse province name and folder path from `$ARGUMENTS`.

Follow these steps in order:

### Step 1 — Parse Arguments
```python
args = "$ARGUMENTS".strip().split()
# args[0] = province name
# args[1] = folder path
```
If arguments are missing, ask the user for the province name and folder path before proceeding.

### Step 2 — Verify Source Files
```bash
ls "[folder-path]"/*.xlsx
```
If no xlsx files are found, ask the user to verify the folder path.

### Step 3 — Run the Merge

Execute the following Python code inline (substitute `[folder-path]` and `[province]` with the actual values):

```python
import os, sys, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def merge(folder_path, province_name):
    folder_path = os.path.abspath(folder_path)
    output_filename = f"{province_name}_도로명정보조회.xlsx"
    output_path = os.path.join(folder_path, output_filename)

    files = sorted([f for f in os.listdir(folder_path)
                    if f.endswith(".xlsx") and f != output_filename])
    if not files:
        raise FileNotFoundError(f"No xlsx files found in '{folder_path}'.")

    print(f"Processing {len(files)} file(s)...")
    all_data, header = [], None
    for i, fname in enumerate(files):
        df = pd.read_excel(os.path.join(folder_path, fname), sheet_name=0, header=None)
        if i == 0:
            header = df.iloc[1].tolist()   # capture header from first file only
        all_data.append(df.iloc[2:].reset_index(drop=True))  # skip rows 0 & 1
        print(f"  [{i+1:02d}] {fname}  →  {len(df)-2:,} rows")

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal merged rows: {len(combined):,}")

    # Write with formatting
    wb = Workbook()
    ws = wb.active
    ws.title = "도로명정보조회"
    thin = Side(style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    hdr_font  = Font(name="Arial", bold=True, size=10, color="FFFFFF")
    hdr_fill  = PatternFill(fill_type="solid", start_color="4472C4", end_color="4472C4")
    hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    dat_font  = Font(name="Arial", size=10)
    dat_align = Alignment(vertical="center")

    for c, name in enumerate(header, 1):
        cell = ws.cell(row=1, column=c, value=name)
        cell.font = hdr_font; cell.fill = hdr_fill
        cell.alignment = hdr_align; cell.border = border

    for r, row in enumerate(combined.itertuples(index=False), 2):
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c)
            cell.value = None if pd.isna(val) else (int(val) if isinstance(val, float) and val == int(val) else val)
            cell.font = dat_font; cell.alignment = dat_align; cell.border = border

    widths = [8, 12, 20, 30, 10, 8, 14, 8, 8, 10]
    for i in range(len(header)):
        ws.column_dimensions[get_column_letter(i+1)].width = widths[i] if i < len(widths) else 15
    ws.row_dimensions[1].height = 20
    ws.freeze_panes = "A2"
    wb.save(output_path)
    return output_path

result = merge("[folder-path]", "[province]")
print(f"\n✅ Done: {result}")
```

> **Note:** Replace `[folder-path]` and `[province]` with the actual user-provided values before running.

### Step 4 — Report Results
- Share the path of the generated file
- Optionally show a row-count summary by district (시군구명)
- On error, explain the cause and suggest a fix

---

## 📂 Province Name Examples

| Korean | English / Romanized | Output Filename |
|--------|---------------------|-----------------|
| 충북 | Chungbuk  | 충북_도로명정보조회.xlsx |
| 충남 | Chungnam  | 충남_도로명정보조회.xlsx |
| 전북 | Jeonbuk   | 전북_도로명정보조회.xlsx |
| 전남 | Jeonnam   | 전남_도로명정보조회.xlsx |
| 경기 | Gyeonggi  | 경기_도로명정보조회.xlsx |
| 경북 | Gyeongbuk | 경북_도로명정보조회.xlsx |
| 경남 | Gyeongnam | 경남_도로명정보조회.xlsx |
| 서울 | Seoul     | 서울_도로명정보조회.xlsx |

Any custom name is accepted — the province parameter is not restricted.

---

## 🔧 CLI Installation Guide

To register `/road-name-merge` (and `/도로명통합`) as slash commands in Claude CLI:

```bash
# Project-level (works only in this project)
cp cli-commands/도로명통합.md      /your/project/.claude/commands/
cp cli-commands/road-name-merge.md /your/project/.claude/commands/

# Global (works in all projects)
mkdir -p ~/.claude/commands
cp cli-commands/도로명통합.md      ~/.claude/commands/
cp cli-commands/road-name-merge.md ~/.claude/commands/
```

After copying, restart your Claude CLI session. The commands will appear in `/help`.
