/**
 * remind-plan-update.js
 * PostToolUse(Edit/Write) 훅 — 구현 파일 수정 후 플랜 업데이트 상기
 *
 * 동작:
 *   .js/.html/.sql/.css 파일 수정 시 → 플랜 체크박스 확인 알림
 *   .claude/ 내부 파일 수정 시       → 무시 (플랜/설정 파일)
 */

const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(Buffer.concat(chunks).toString());
    const filePath = (input.tool_input && input.tool_input.file_path) || '';

    const isImplFile = /\.(js|html|sql|css)$/i.test(filePath);
    const isPlanFile = /[/\\]\.claude[/\\]/.test(filePath);

    if (isImplFile && !isPlanFile) {
      process.stderr.write(
        '\n📋 플랜 업데이트 확인: 구현 파일이 수정됐습니다.\n' +
        '   → .claude/plans/ 해당 항목 체크박스(✅)를 업데이트했나요?\n\n'
      );
    }
  } catch {
    // 파싱 오류 시 무시
  }
});
