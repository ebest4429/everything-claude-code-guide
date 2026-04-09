<!--
╔══════════════════════════════════════════════════════════════╗
║  road-name-merge.md  ·  English Prompt-only Version          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Version Notes]                                             ║
║    No bundled Python — Claude writes code at runtime         ║
║    Rules-only approach: single file, easy to maintain        ║
║    For the Python-embedded version → road-name-merge-code.md ║
║                                                              ║
║  [Installation]                                              ║
║    # Global (all projects)                                   ║
║    cp road-name-merge.md ~/.claude/commands/                 ║
║                                                              ║
║    # Project-level (current project only)                    ║
║    cp road-name-merge.md ./.claude/commands/                 ║
║                                                              ║
║  [Usage]  /road-name-merge [province] [folder-path]          ║
║                                                              ║
║  [Examples]                                                  ║
║    /road-name-merge Chungnam /Users/me/Chungnam_roads        ║
║    /road-name-merge Jeonbuk  C:\Users\me\Jeonbuk_roads       ║
║    /road-name-merge Gyeonggi ~/Downloads/Gyeonggi_roads      ║
║    /road-name-merge 충남      /Users/me/충남_도로명            ║
║                                                              ║
║  [Output]  [folder-path]/[province]_도로명정보조회.xlsx        ║
╚══════════════════════════════════════════════════════════════╝
-->
---
description: Merge Korean road-name lookup (도로명정보조회) xlsx files from a province folder into one consolidated file (prompt-only). Removes total-count rows and duplicate headers automatically. Usage: /road-name-merge [province] [folder-path]
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Road Name Information Excel Merger (English · Prompt-only)

## Parse Arguments

Extract province name and folder path from `$ARGUMENTS`.

- First token  = province name (e.g., Chungnam, Jeonbuk, Gyeonggi, or Korean: 충남)
- Second token = folder path  (e.g., /Users/me/Chungnam_roads)

If either value is missing, ask the user before proceeding.

## Processing Rules

Each source `.xlsx` file has this fixed structure:

```
Row 0  →  "총N건 (도로명수 : N)"  ← REMOVE from every file
Row 1  →  Column headers          ← Keep from FIRST file only
Row 2+ →  Actual data rows        ← Keep from ALL files
```

## Execution Steps

1. List all `.xlsx` files in the folder (exclude the output file itself)
2. Read each file with pandas, apply the rules above
3. Concatenate all data into a single DataFrame
4. Save with openpyxl including formatting:
   - Header row: blue background (#4472C4), white bold text, centered
   - Data rows: Arial 10pt, thin borders on all cells
   - Freeze row 1 (header lock)
5. Output path: `[folder-path]/[province]_도로명정보조회.xlsx`

## Report After Completion

- Provide the full path of the generated file
- Show total row count and number of source files merged
- On error, explain the cause and suggest a fix

## Province Name Reference

| Korean | Romanized  | Output filename example        |
|--------|------------|-------------------------------|
| 충북   | Chungbuk   | 충북_도로명정보조회.xlsx        |
| 충남   | Chungnam   | 충남_도로명정보조회.xlsx        |
| 전북   | Jeonbuk    | 전북_도로명정보조회.xlsx        |
| 전남   | Jeonnam    | 전남_도로명정보조회.xlsx        |
| 경기   | Gyeonggi   | 경기_도로명정보조회.xlsx        |
| 서울   | Seoul      | 서울_도로명정보조회.xlsx        |

Any custom name is accepted — the province parameter is unrestricted.
