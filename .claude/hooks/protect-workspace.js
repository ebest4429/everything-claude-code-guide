/**
 * protect-workspace.js
 * PreToolUse(Write) 훅 — WORKSPACE.md 덮어쓰기 차단
 *
 * 동작:
 *   Write 도구로 WORKSPACE.md를 쓰려 할 때 파일이 이미 존재하면 차단.
 *   기존 WORKSPACE.md를 다른 이름으로 변경한 후 새 파일을 작성해야 함.
 *
 * 통과 조건:
 *   - 대상 파일이 WORKSPACE.md가 아닌 경우
 *   - WORKSPACE.md가 아직 존재하지 않는 경우 (최초 생성)
 */

const fs   = require('fs');
const path = require('path');

const ROOT      = path.resolve(__dirname, '../..');
const WORKSPACE = path.join(ROOT, '.claude/WORKSPACE.md');

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    const input    = JSON.parse(Buffer.concat(chunks).toString());
    const filePath = (input.tool_input && input.tool_input.file_path) || '';

    // WORKSPACE.md 대상인지 확인 (경로 끝 기준)
    const isWorkspace = /[/\\]WORKSPACE\.md$/i.test(filePath);
    if (!isWorkspace) return; // 무관한 파일 → 통과

    // 파일이 존재하면 차단
    if (fs.existsSync(WORKSPACE)) {
      process.stderr.write(
        '\n❌ WORKSPACE.md 덮어쓰기 차단\n\n' +
        '   기존 WORKSPACE.md가 있습니다.\n' +
        '   먼저 파일명을 변경한 후 새 WORKSPACE.md를 작성하세요.\n\n' +
        '   예) WORKSPACE.PHASE1.md\n' +
        '       WORKSPACE.스킬수정플랜.md\n\n' +
        '   mv .claude/WORKSPACE.md .claude/WORKSPACE.{이름}.md\n\n'
      );
      process.exit(2);
    }

    // 파일 없음 → 최초 생성 허용
  } catch {
    // 파싱 오류 시 통과
  }
});
