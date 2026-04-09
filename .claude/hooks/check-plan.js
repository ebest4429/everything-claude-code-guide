/**
 * check-plan.js
 * PreToolUse(Bash) 훅 — git commit/push 전 현재 플랜 업데이트 검증
 *
 * 동작:
 *   WORKSPACE.md의 "현재 플랜" 항목에서 활성 플랜 파일 경로를 읽어
 *   코드 파일(main/preload/renderer)보다 플랜이 최신인지 확인.
 *   코드가 더 최신이면 커밋 차단.
 *
 * 우회: 명령에 SKIP_PLAN_CHECK=1 포함 시 통과
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const WORKSPACE = path.join(ROOT, '.claude/WORKSPACE.md');
const CODE_DIRS = ['app'];

// 재귀적으로 디렉터리 내 파일 최신 mtime 반환
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

// WORKSPACE.md에서 "현재 플랜" 파일 경로 추출
// 예: | 현재 플랜 | `.claude/plans/value-up-phase5.md` |
function getActivePlanPath() {
  try {
    const content = fs.readFileSync(WORKSPACE, 'utf8');
    const match = content.match(/현재 플랜[^|]*\|[^`]*`([^`]+)`/);
    if (match && match[1]) {
      return path.join(ROOT, match[1]);
    }
  } catch {}
  return null;
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

    // WORKSPACE.md에서 현재 활성 플랜 경로 추출
    const activePlanPath = getActivePlanPath();

    if (!activePlanPath) {
      // 플랜 경로 파싱 실패 시 통과 (WORKSPACE.md 형식 문제)
      process.stderr.write(
        '\n⚠️  WORKSPACE.md에서 현재 플랜 경로를 읽지 못했습니다. 확인 후 커밋하세요.\n\n'
      );
      return;
    }

    // 활성 플랜 파일 mtime
    let planMtime = 0;
    try {
      planMtime = fs.statSync(activePlanPath).mtimeMs;
    } catch {
      process.stderr.write(
        `\n⚠️  플랜 파일을 찾을 수 없습니다: ${activePlanPath}\n\n`
      );
      return;
    }

    if (latestCode > planMtime) {
      const planName = path.basename(activePlanPath);
      process.stderr.write(
        '\n❌ 커밋 중지: 플랜 체크박스 업데이트 필요\n' +
        '\n' +
        `   코드가 현재 플랜(${planName})보다 최신입니다.\n` +
        '   해당 플랜의 체크박스를 업데이트하세요.\n\n'
      );
      process.exit(2);
    }

    // WORKSPACE.md도 코드보다 최신인지 확인
    let workspaceMtime = 0;
    try { workspaceMtime = fs.statSync(WORKSPACE).mtimeMs; } catch {}
    if (workspaceMtime && latestCode > workspaceMtime) {
      process.stderr.write(
        '\n❌ 커밋 중지: WORKSPACE.md 업데이트 필요\n' +
        '\n' +
        '   코드가 WORKSPACE.md보다 최신입니다.\n' +
        '   WORKSPACE.md 진행상황을 업데이트하세요.\n\n'
      );
      process.exit(2);
    }
  } catch {
    // 파싱 오류 시 통과
  }
});
