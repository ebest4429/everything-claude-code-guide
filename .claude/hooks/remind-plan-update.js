/**
 * remind-plan-update.js
 * PostToolUse(Edit/Write) 훅 — 작업순서 상태 관리
 *
 * 구현 파일(.js/.html/.sql/.css) 수정 → pending=true (3분 유예 시작)
 * 플랜/WORKSPACE(.claude/ 내 .md/.json) 수정 → pending=false (해제)
 *
 * pending 상태에서 3분 후 구현 파일 편집 시 check-work-order.js가 차단
 */

const fs   = require('fs');
const path = require('path');

const ROOT       = path.resolve(__dirname, '../..');
const STATE_FILE = path.join(ROOT, '.claude/hooks/.work-order-state.json');

function readState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch { return { pending: false, since: 0 }; }
}
function writeState(state) {
  try { fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2)); } catch {}
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

    const isPlanOrWs =
      /[/\\]\.claude[/\\]/.test(filePath) &&
      /\.(md|json)$/i.test(filePath);

    if (isImplFile) {
      const state = readState();
      if (!state.pending) {
        // 첫 구현 파일 수정 → pending 시작
        writeState({ pending: true, since: Date.now(), lastImplFile: filePath });
      }
      process.stderr.write(
        '\n📋 작업순서 확인: 구현 파일이 수정됐습니다.\n' +
        '   → 플랜 항목 [x] 표시 + WORKSPACE.md 업데이트 후 다음 구현을 진행하세요.\n\n'
      );
    } else if (isPlanOrWs) {
      // 플랜/WORKSPACE 수정 → pending 해제
      writeState({ pending: false, since: 0 });
    }
  } catch {
    // 파싱 오류 시 무시
  }
});
