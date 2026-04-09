# value-up 보완2 — 주소구조 수정 + 토지 지번 추가 + 빌드 문제

> 이슈 1, 2는 상세 계획 포함. 이슈 3은 다음 세션에서 분석.
> 구현 순서: 이슈1 → 검증 → 이슈2 → 검증 → 이슈3

---

## 이슈 1 — 기본정보 주소 구조 DB 수정

### 문제
`seed.js` 167번 줄: `fullAddress.split(' ')` 단순 공백 분리
비자치구형 도시(청주시 등)에서 컬럼 밀림 발생 → 마지막 리(고은리 등) 유실.

**현재 DB 저장 결과 (잘못됨):**
```
충청북도 청주시 상당구 남일면 고은리
→ sido=충청북도, sigungu=청주시, eupmyeondong=상당구, ri=남일면, 고은리=유실
```

**올바른 저장 (항상 4개 필드):**
```
→ sido=충청북도, sigungu=청주시 상당구, eupmyeondong=남일면, ri=고은리
```

### 파싱 방향 (확정)

**원칙: 항상 4개 필드** — sido / sigungu / eupmyeondong / ri

| 유형 | 원본 예시 | sido | sigungu | eupmyeondong | ri |
|------|---------|------|---------|-------------|-----|
| 일반형 | 서울특별시 종로구 청운동 | 서울특별시 | 종로구 | 청운동 | null |
| 비자치구형 | 충청북도 청주시 상당구 가덕면 한계리 | 충청북도 | 청주시 상당구 | 가덕면 | 한계리 |
| 세종 | 세종특별자치시 조치원읍 원리 | 세종특별자치시 | 세종시(고정) | 조치원읍 | 원리 |
| 세종 | 세종특별자치시 반곡동 | 세종특별자치시 | 세종시(고정) | 반곡동 | null |

**판별 로직:**
```js
const addr = fullAddress.split(' ');
let sido, sigungu, eupmyeondong, ri;

if (addr[0] === '세종특별자치시') {
  // 세종: sigungu = '세종시' 고정 (법정동코드에 없지만 실무 표준)
  sido = addr[0];
  sigungu = '세종시';
  eupmyeondong = addr[1] || null;
  ri = addr[2] || null;
} else if (addr[1]?.endsWith('시') && addr[2]?.endsWith('구')) {
  // 비자치구형: 시+구 합쳐서 sigungu 1칸
  sido = addr[0];
  sigungu = addr[1] + ' ' + addr[2];
  eupmyeondong = addr[3] || null;
  ri = addr[4] || null;
} else {
  // 일반형
  sido = addr[0];
  sigungu = addr[1] || null;
  eupmyeondong = addr[2] || null;
  ri = addr[3] || null;
}
```

### 수정 파일 ✅
- `main/db/seed.js` — 파싱 로직 교체 (167번 줄)
- `main/db/migrate.js` — address_codes 기존 데이터 삭제 후 재seed
- DB 컬럼 변경 없음, UI 변경 없음

---

## 이슈 2 — 토지이용정보 지번 추가 (B8)

### 핵심 원칙 (이전 구현 실패 교훈)
1. 기존 `land_info` + `landForm.js` **절대 건드리지 않음** — 그대로 유지
2. `land_parcels`는 추가 지번 전용 신규 테이블 (land_info 대체 아님)
3. 주소 드롭다운: basicInfoForm.js에서 코드 **복사** (새로 작성 금지)
4. 계산 로직(㎡→평): landForm.js에서 코드 **복사** (새로 작성 금지)
5. land_parcels 필드 = 지번 식별에 필요한 것만 (land_info 전체 복사 금지)

### UI — 테이블 행 방식 (기존 토지이용정보 폼 아래 추가)

```
[기존 토지이용정보 폼 — 유지]

─── 추가 지번 ──────────────────────────────────────────────────────────────
 시도 | 시군구 | 읍면동 | 리 | 산 | 본번 | 부번 | 지목 | 용도지역 | 면적㎡ | 면적평 | 삭제
──────────────────────────────────────────────────────────────────────────
 [  ] | [    ] | [    ] | [ ]| [ ]| [  ] | [  ] | [  ] | [      ] | [    ] | [자동] | [삭]
[+ 지번 추가]
```

**너비 원칙**: 각 컬럼은 표시될 최장 텍스트 기준 최소 너비. 불필요하게 넓게 잡지 않음.

### land_parcels 테이블 필드 (확정)
```sql
id, property_id,
sido, sigungu, eupmyeondong, ri,
mountain_yn, main_no, sub_no, legal_dong_code, pnu,
land_category, use_district,
land_area_m2, land_area_py,
sort_order
```

### 수정 파일
- ✅ `main/db/schema.sql` — land_parcels 테이블 추가
- ✅ `main/db/migrate.js` — land_parcels CREATE (schema exec으로 처리, 별도 수정 불필요)
- ✅ `main/repositories/landParcelsRepository.js` — 신규 (replaceAll, findByPropertyId)
- ✅ `main/services/propertyService.js` — land_info 유지 + landParcels 추가
- ✅ `renderer/utils/mapper.js` — landInfo 유지 + landParcels 추가
- ✅ `renderer/form/landParcelsForm.js` — 신규 (테이블 행 방식, 시도 목록 init() 1회 캐시)
- ✅ `renderer/index.html` — 토지 섹션 하단 테이블 CSS + HTML + script 추가
- ✅ `renderer/app.js` — landParcelsForm 추가 (landForm 유지)
- ✅ 버그수정: pnuInput td 중복으로 thead 12개 / tbody 13개 컬럼 불일치 → tr.dataset.pnu 방식으로 수정
- ✅ 버그수정: 컬럼 너비 % 비율 수정 + 삭제버튼 ✕ + 산여부 일반/산

### landParcelsForm.js 구현 시 반드시
- 행 추가 시 시도 목록 즉시 로드 (addRow 호출 시마다)
- 주소 드롭다운 이벤트: basicInfoForm.js의 시도→시군구→읍면동→리 체인 그대로 복사
- 면적 자동계산: landForm.js의 calcLandPyeong() 그대로 복사
- 이슈1 파싱 로직 반영 후 구현 (비자치구형 주소 정상 표시 전제)

---

## 완료 조건

### 이슈 1
- [x] 충청북도 청주시 상당구 남일면 → 드롭다운 정상
- [x] 고은리 리 선택 가능
- [x] 기존 자치구형 정상 동작 유지

### 이슈 2
- [ ] 기존 토지이용정보 폼 그대로 동작
- [ ] 지번 추가 → 테이블 행 생성, 주소 드롭다운 종속 동작
- [ ] 면적(평) 자동 계산
- [ ] 저장/재조회 정상
