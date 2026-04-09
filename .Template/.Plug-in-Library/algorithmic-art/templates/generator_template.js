/**
 * generator_template.js — p5.js 제너러티브 아트 구조 참조 템플릿
 * ================================================================
 * [역할]
 *   p5.js 기반 알고리즘 아트 구현 시 참고하는 코드 구조/패턴 가이드입니다.
 *   이 파일을 직접 실행하지 말고, viewer.html 안에 인라인으로 알고리즘을 작성하세요.
 *
 * [핵심 원칙]
 *   1. 시드 기반 무작위성  — 같은 시드 = 같은 결과 (randomSeed / noiseSeed)
 *   2. 파라미터 객체      — 조율 가능한 모든 값을 params에 집중 관리
 *   3. 철학 주도 설계     — 패턴 메뉴가 아닌 알고리즘 철학에서 코드 도출
 *   4. 인라인 임베드      — 별도 .js 파일 금지, viewer.html 내 <script>에 삽입
 *
 * [사용법]
 *   - 이 파일은 참조용 구조 예시입니다
 *   - 실제 구현은 viewer.html의 변수 섹션(<script> 내부)에 작성하세요
 *   - params 객체와 setup()/draw() 함수를 아트워크에 맞게 커스터마이즈하세요
 */

// ============================================================
// 파라미터 구성
// 아트의 조율 가능한 모든 속성을 여기에 정의합니다.
// UI 슬라이더/컨트롤과 1:1로 매핑됩니다.
// ============================================================
let params = {
  seed: 12345,          // 재현성을 위한 시드 (항상 포함)

  // 수량 파라미터 (얼마나 많이?)
  count: 500,           // 요소(파티클, 선, 원 등) 수

  // 스케일 파라미터 (얼마나 크게/빠르게?)
  scale: 0.003,         // 노이즈/패턴 스케일
  speed: 1.0,           // 이동 속도 또는 진화율

  // 비율 파라미터 (어떤 비례?)
  complexity: 0.5,      // 복잡성 수준 (0.0 ~ 1.0)

  // 색상 파라미터 (컬러 피커로 제어 시)
  primaryColor: '#FF6B6B',
  secondaryColor: '#4ECDC4',
  backgroundColor: '#1a1a2e',
};

// ============================================================
// 핵심 데이터 구조
// 철학이 요구하는 요소를 클래스로 표현합니다.
// ============================================================
class ArtElement {
  /**
   * 제너러티브 요소 생성자
   * @param {number} x - 초기 X 위치
   * @param {number} y - 초기 Y 위치
   */
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.lifespan = random(100, 300);  // 파티클 수명
    this.size = random(1, 4);
    this.col = color(params.primaryColor);
  }

  /**
   * 프레임마다 요소 상태를 업데이트합니다.
   * 힘, 속도, 위치 순으로 계산합니다.
   */
  update() {
    // 1단계: 힘 계산 (플로우 필드, 중력 등)
    let angle = noise(
      this.pos.x * params.scale,
      this.pos.y * params.scale
    ) * TWO_PI * 4;
    let force = p5.Vector.fromAngle(angle);
    force.mult(params.speed);

    // 2단계: 속도에 힘 적용
    this.vel.add(force);
    this.vel.limit(params.speed * 2);

    // 3단계: 위치 업데이트
    this.pos.add(this.vel);

    // 수명 감소
    this.lifespan--;
  }

  /**
   * 요소를 캔버스에 그립니다.
   */
  draw() {
    let alpha = map(this.lifespan, 0, 300, 0, 150);
    stroke(red(this.col), green(this.col), blue(this.col), alpha);
    strokeWeight(this.size);
    point(this.pos.x, this.pos.y);
  }

  /**
   * 요소가 활성 상태인지 확인합니다.
   * @returns {boolean} 수명이 남아있고 캔버스 내에 있으면 true
   */
  isAlive() {
    return (
      this.lifespan > 0 &&
      this.pos.x > 0 && this.pos.x < width &&
      this.pos.y > 0 && this.pos.y < height
    );
  }
}

// ============================================================
// p5.js 핵심 함수
// ============================================================

/** 시스템 초기화: 캔버스 생성, 시드 설정, 첫 프레임 준비 */
function setup() {
  // 캔버스를 #canvas-container에 부착
  let canvas = createCanvas(1200, 1200);
  canvas.parent('canvas-container');

  // 시드 기반 무작위성 초기화 (재현성 보장)
  randomSeed(params.seed);
  noiseSeed(params.seed);

  // 배경 설정
  background(params.backgroundColor);

  // 요소 풀 초기화
  initElements();
}

/** 매 프레임 실행: 알고리즘 철학을 시각화합니다. */
function draw() {
  // 잔상 효과 (생략 시 background()로 완전 초기화)
  // background(params.backgroundColor + '08');  // 투명 레이어

  // 요소 업데이트 및 렌더링
  for (let i = elements.length - 1; i >= 0; i--) {
    elements[i].update();
    elements[i].draw();

    // 소멸된 요소 제거 및 보충
    if (!elements[i].isAlive()) {
      elements.splice(i, 1);
      elements.push(new ArtElement(
        random(width),
        random(height)
      ));
    }
  }
}

// ============================================================
// 시스템 관리 함수
// ============================================================

/** 요소 풀을 초기화합니다. */
function initElements() {
  elements = [];
  for (let i = 0; i < params.count; i++) {
    elements.push(new ArtElement(random(width), random(height)));
  }
}

/**
 * 파라미터 변경 시 호출됩니다 (UI 슬라이더 연동).
 * @param {string} key   - params 객체의 키 이름
 * @param {any}    value - 새로운 값
 */
function updateParam(key, value) {
  // 숫자형 파라미터 변환
  if (typeof params[key] === 'number') {
    params[key] = parseFloat(value);
  } else {
    params[key] = value;
  }

  // 시드 변경 시 완전 재초기화
  if (key === 'seed') {
    regenerate();
    return;
  }

  // 수량/스케일 변경 시 요소 재초기화
  if (key === 'count') {
    initElements();
  }

  // 값 표시 업데이트
  let display = document.getElementById(key + '-value');
  if (display) {
    display.textContent = typeof params[key] === 'number'
      ? params[key].toFixed(key === 'count' ? 0 : 3)
      : params[key];
  }
}

/** 현재 시드로 아트워크를 재생성합니다. */
function regenerate() {
  randomSeed(params.seed);
  noiseSeed(params.seed);
  background(params.backgroundColor);
  initElements();
  loop();  // 정적 아트인 경우 noLoop() 후 redraw() 사용
}

/** 모든 파라미터를 기본값으로 초기화합니다. */
function resetParams() {
  params = { ...defaultParams };
  // UI 슬라이더 값 동기화
  Object.keys(params).forEach(key => {
    let el = document.getElementById(key);
    if (el) el.value = params[key];
    updateParam(key, params[key]);
  });
  regenerate();
}

// ============================================================
// 시드 탐색 헬퍼 함수 (viewer.html의 UI 버튼과 연동)
// ============================================================

/** 이전 시드로 이동합니다. */
function prevSeed() {
  params.seed = Math.max(1, params.seed - 1);
  document.getElementById('seed-display').textContent = params.seed;
  regenerate();
}

/** 다음 시드로 이동합니다. */
function nextSeed() {
  params.seed = params.seed + 1;
  document.getElementById('seed-display').textContent = params.seed;
  regenerate();
}

/** 무작위 시드로 이동합니다. */
function randomizeSeed() {
  params.seed = Math.floor(Math.random() * 99999) + 1;
  document.getElementById('seed-display').textContent = params.seed;
  regenerate();
}

/** 지정한 시드로 이동합니다. */
function goToSeed() {
  let input = document.getElementById('seed-input');
  let val = parseInt(input.value);
  if (!isNaN(val) && val > 0) {
    params.seed = val;
    document.getElementById('seed-display').textContent = params.seed;
    regenerate();
  }
}

// ============================================================
// PNG 다운로드
// ============================================================

/** 현재 캔버스를 PNG 파일로 저장합니다. */
function downloadPNG() {
  saveCanvas('algorithmic-art-seed-' + params.seed, 'png');
}
