/**
 * session-gate.js
 * PreToolUse(Bash/Edit/Write) 훅 — 세션 초기화 게이트
 *
 * 동작:
 *   .session-gate.json 존재 시 → 미읽은 파일 목록 출력 → exit(2) 차단
 *   .session-gate.json 없음 → 통과
 */

const fs   = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const GATE = path.join(ROOT, '.claude/.session-gate.json');

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    if (!fs.existsSync(GATE)) return;

    const gate      = JSON.parse(fs.readFileSync(GATE, 'utf8'));
    const read      = gate.read || [];
    const remaining = (gate.required || []).filter(f => !read.includes(f));

    if (remaining.length === 0) {
      fs.unlinkSync(GATE);
      return;
    }

    process.stderr.write(
      '\n❌ 세션 초기화 미완료 — Bash/Edit/Write 차단\n\n' +
      '   아래 파일을 Read 도구로 읽어야 해제됩니다:\n' +
      remaining.map(f => `   - ${f}`).join('\n') + '\n\n'
    );
    process.exit(2);
  } catch {
    // 오류 시 통과
  }
});
