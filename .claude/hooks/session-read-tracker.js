/**
 * session-read-tracker.js
 * PostToolUse(Read) 훅 — 세션 초기화 게이트 추적
 *
 * 동작:
 *   Read된 파일이 gate의 required에 있으면 read 배열에 추가
 *   모두 읽히면 gate 파일 삭제 → 차단 해제
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

    const input    = JSON.parse(Buffer.concat(chunks).toString());
    const filePath = (input.tool_input && input.tool_input.file_path) || '';
    if (!filePath) return;

    const gate = JSON.parse(fs.readFileSync(GATE, 'utf8'));
    if (!gate.read) gate.read = [];

    const normalize = p => path.resolve(ROOT, p).replace(/\\/g, '/');
    const readNorm  = normalize(filePath);

    const matched = (gate.required || []).find(r => normalize(r) === readNorm);

    if (matched && !gate.read.includes(matched)) {
      gate.read.push(matched);

      if (gate.read.length >= gate.required.length) {
        fs.unlinkSync(GATE);
      } else {
        fs.writeFileSync(GATE, JSON.stringify(gate, null, 2));
      }
    }
  } catch {
    // 오류 시 무시
  }
});
