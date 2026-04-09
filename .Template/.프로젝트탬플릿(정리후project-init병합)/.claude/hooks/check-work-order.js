/**
 * check-work-order.js
 * PreToolUse(Edit) 훅 — 구현 파일 편집 전 작업순서 게이트
 *
 * state 파일: .claude/hooks/.work-order-state.json
 *   { pending: bool, since: timestamp }
 *
 * 동작:
 *   pending=true이고 유예시간(3분) 초과 → exit 2 차단
 *   pending=false 또는 유예 기간 내 → 통과
 *
 * 유예 기간(3분): 같은 작업 배치 내 여러 파일 편집 허용
 */

const fs   = require('fs');
const path = require('path');

const ROOT       = path.resolve(__dirname, '../..');
const STATE_FILE = path.join(ROOT, '.claude/hooks/.work-order-state.json');
const BATCH_MS   = 3 * 60 * 1000; // 3분

function readState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch { return { pending: false, since: 0 }; }
}

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    const input    = JSON.parse(Buffer.concat(chunks).toString());
    const filePath = (input.tool_input && input.tool_input.file_path) || '';

    const isImplFile =
      /\.(js|html|sql|css)$/i.test(filePath) &&
      !/[/\\]\.claude[/\\]/.test(filePath);

    if (!isImplFile) return; // 플랜/설정 파일이면 통과

    const state   = readState();
    if (!state.pending) return; // 정상 상태

    const elapsed = Date.now() - (state.since || 0);
    if (elapsed <= BATCH_MS) return; // 3분 유예 내 → 같은 배치 허용

    process.stderr.write(
      '\n❌ 작업순서 위반 — 구현 파일 편집 차단\n\n' +
      '   이전 구현 후 플랜/WORKSPACE 미업데이트 상태입니다.\n\n' +
      '   다음을 완료한 후 다시 시도하세요:\n' +
      '     1. .claude/plans/ 해당 항목 [x] 표시\n' +
      '     2. .claude/WORKSPACE.md 진행상황 업데이트\n\n' +
      '   (CLAUDE.md 작업순서 원칙 위반)\n\n'
    );
    process.exit(2);
  } catch {
    // 파싱 오류 시 통과 (훅 오작동으로 작업 차단하지 않음)
  }
});
