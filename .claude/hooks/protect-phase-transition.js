/**
 * protect-phase-transition.js
 * PreToolUse(Write) 훅 — 새 페이지플랜 작성 시 WORKSPACE 아카이브 강제
 *
 * 동작:
 *   plans/ 직하위에 새 .md 플랜 파일을 Write하려 할 때
 *   현재 활성 플랜에 대한 WORKSPACE 아카이브가 존재하는지 확인.
 *   아카이브 없으면 차단.
 *
 * 통과 조건:
 *   - 대상 파일이 plans/ 직하위 .md가 아닌 경우 (designs/, hooks-guide/ 등 하위 제외)
 *   - 마스터플랜(-master.md) 작성인 경우
 *   - 활성 플랜과 동일한 파일인 경우 (재작성)
 *   - 활성 플랜을 읽지 못한 경우 (초기화 중)
 *   - WORKSPACE.{활성플랜stem}.md 아카이브가 이미 존재하는 경우
 */

const fs   = require('fs');
const path = require('path');

const ROOT      = path.resolve(__dirname, '../..');
const PLANS_DIR = path.join(ROOT, '.claude/plans');
const CLAUDE_DIR = path.join(ROOT, '.claude');

function getActivePlan() {
  try {
    const files = fs.readdirSync(PLANS_DIR).filter(f => f.endsWith('-master.md'));
    if (!files.length) return null;
    const master = fs.readFileSync(path.join(PLANS_DIR, files[0]), 'utf8');
    const match = master.match(/\*\*현재 활성 플랜:\*\*\s*`([^`]+)`/);
    return match ? match[1] : null;
  } catch { return null; }
}

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    const input    = JSON.parse(Buffer.concat(chunks).toString());
    const filePath = (input.tool_input && input.tool_input.file_path) || '';

    const resolved      = path.resolve(ROOT, filePath);
    const resolvedPlans = path.resolve(PLANS_DIR);

    // plans/ 하위인지 확인
    if (!resolved.startsWith(resolvedPlans + path.sep)) return;

    // plans/ 직하위만 대상 (designs/ 등 하위 폴더 제외)
    const relative = path.relative(resolvedPlans, resolved);
    if (relative.includes(path.sep)) return;

    // .md 파일만
    if (!resolved.endsWith('.md')) return;

    // 마스터플랜 제외
    if (resolved.endsWith('-master.md')) return;

    // 활성 플랜 확인
    const activePlan = getActivePlan();
    if (!activePlan) return; // 초기화 중 → 통과

    // 활성 플랜과 동일 파일 재작성 → 통과
    if (path.basename(resolved) === activePlan) return;

    // WORKSPACE 아카이브 확인
    const activeStem  = path.basename(activePlan, '.md');
    const archivePath = path.join(CLAUDE_DIR, `WORKSPACE.${activeStem}.md`);

    if (!fs.existsSync(archivePath)) {
      process.stderr.write(
        '\n❌ Phase 전환 차단: WORKSPACE.md 아카이브 필요\n\n' +
        `   현재 활성 플랜: ${activePlan}\n\n` +
        '   새 페이지플랜 작성 전 아래 순서로 처리하세요:\n\n' +
        `   1. WORKSPACE.md → WORKSPACE.${activeStem}.md 로 이름 변경 (Bash mv)\n` +
        '   2. 새 WORKSPACE.md 작성\n' +
        '   3. 마스터플랜 활성 플랜 포인터 업데이트\n\n'
      );
      process.exit(2);
    }
  } catch {
    // 파싱 오류 시 통과
  }
});
