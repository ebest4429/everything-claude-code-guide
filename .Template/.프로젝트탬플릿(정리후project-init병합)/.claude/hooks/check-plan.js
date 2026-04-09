const fs = require('fs');
const path = require('path');

const ROOT = 'C:/Users/admin/Project/Main-Project/ebest-portal';
const PLAN_FILE = path.join(ROOT, '.claude/plans/ebest-portal-refactor.md');
const CODE_DIRS = ['app', 'features', 'components', 'lib'];

function getLatestMtime(dir) {
  let latest = 0;
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        const sub = getLatestMtime(full);
        if (sub > latest) latest = sub;
      } else if (entry.isFile()) {
        const mtime = fs.statSync(full).mtimeMs;
        if (mtime > latest) latest = mtime;
      }
    }
  } catch {}
  return latest;
}

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(Buffer.concat(chunks).toString());
    const cmd = (input.tool_input && input.tool_input.command) || '';

    if (!/git\s+(commit|push)/.test(cmd)) return;

    // 명시적 우회
    if (/SKIP_PLAN_CHECK=1/.test(cmd)) return;

    // 코드 파일 최신 수정 시간
    let latestCode = 0;
    for (const dir of CODE_DIRS) {
      const mtime = getLatestMtime(path.join(ROOT, dir));
      if (mtime > latestCode) latestCode = mtime;
    }

    if (!latestCode) return; // 코드 파일 없으면 통과

    // plans 파일 수정 시간
    let planMtime = 0;
    try {
      planMtime = fs.statSync(PLAN_FILE).mtimeMs;
    } catch {}

    if (latestCode > planMtime) {
      process.stderr.write(
        '\n❌ 커밋 중지: 플랜 체크박스 업데이트 필요\n' +
        '\n' +
        '   코드가 플랜보다 최신입니다.\n' +
        '   .claude/plans/ebest-portal-refactor.md 체크박스를 업데이트하세요.\n\n'
      );
      process.exit(2);
    }
  } catch {
    // 파싱 오류 시 통과
  }
});
