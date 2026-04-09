# value-up Phase 2 — 데이터 레이어

**참조 문서 (구현 전 반드시 읽기)**
- 아키텍처: `.Source-Files/02-architecture.md`
- DB 스키마: `.Source-Files/03-database-schema.md`
- IPC 명세: `.Source-Files/04-ipc-api-spec.md`
- Phase 완료 조건 원본: `.Source-Files/07-phase-plan.md` Phase 2

---

## 목표

UI 없이도 매물 aggregate 저장/조회가 가능한 데이터 레이어 구축

---

## 1. Repository 계층

> 규칙: SQL 쿼리만 담당. 비즈니스 로직 포함 금지.

- [x] `main/repositories/propertyRepository.js`
  - `upsert(data)` — properties 단일행 upsert
  - `findById(id)` — id 기준 조회
  - `findByPropertyNo(propertyNo)` — 매물번호 기준 조회
  - `findAll()` — 목록 조회 (id, property_no, full_address, author, updated_at)
  - `getMaxPropertyNo()` — 다음 번호 생성용
  - `deleteById(id)` — 삭제

- [x] `main/repositories/buildingInfoRepository.js`
  - `upsert(data)`
  - `findByPropertyId(propertyId)`
  - `deleteByPropertyId(propertyId)`

- [x] `main/repositories/landInfoRepository.js`
  - `upsert(data)`
  - `findByPropertyId(propertyId)`
  - `deleteByPropertyId(propertyId)`

- [x] `main/repositories/saleInfoRepository.js`
  - `upsert(data)`
  - `findByPropertyId(propertyId)`
  - `deleteByPropertyId(propertyId)`

- [x] `main/repositories/rentalUnitsRepository.js`
  - `replaceAll(propertyId, rows)` — 기존 삭제 후 전체 재삽입
  - `findByPropertyId(propertyId)`

- [x] `main/repositories/ownersRepository.js`
  - `replaceAll(propertyId, rows)`
  - `findByPropertyId(propertyId)`

- [x] `main/repositories/tenantsRepository.js`
  - `replaceAll(propertyId, rows)`
  - `findByPropertyId(propertyId)`

- [x] `main/repositories/consultationsRepository.js`
  - `replaceAll(propertyId, rows)`
  - `findByPropertyId(propertyId)`

- [x] `main/repositories/propertyImagesRepository.js`
  - `replaceAll(propertyId, rows)`
  - `findByPropertyId(propertyId)`

- [x] `main/repositories/codeItemsRepository.js`
  - `findAll()` — 전체 code_items 조회
  - `findByGroup(group)` — 그룹별 조회

- [x] `main/repositories/addressCodesRepository.js`
  - `getSidoList()` — 시도 목록 (DISTINCT)
  - `getSigunguList(sido)` — 시군구 목록
  - `getEupmyeondongList(sido, sigungu)` — 읍면동 목록
  - `getRiList(sido, sigungu, eupmyeondong)` — 리 목록
  - `findLegalDongCode(sido, sigungu, eupmyeondong, ri)` — 법정동코드 조회

---

## 2. Service 계층

> 규칙: 비즈니스 흐름 및 트랜잭션만 담당. SQL 직접 작성 금지.

- [x] `main/services/propertyService.js`
  - `savePropertyAggregate(payload)` — 전체 저장 (단일 트랜잭션)
    - properties upsert
    - building_info upsert
    - land_info upsert
    - sale_info upsert
    - rental_units replaceAll
    - owners replaceAll
    - tenants replaceAll
    - consultations replaceAll
    - property_images replaceAll
    - 오류 시 전체 rollback
  - `getPropertyAggregate(id)` — 전체 aggregate 조회
  - `getPropertyList()` — 목록 조회
  - `getNextPropertyNo()` — 다음 매물번호 계산
  - `deleteProperty(id)` — 삭제

---

## 3. IPC 채널 등록

> 규칙: Service 호출만 위임. 직접 DB 접근 금지.

### 3.1 property 네임스페이스
- [x] `main/ipc/propertyIpc.js`
  - `property:list` → `propertyService.getPropertyList()`
  - `property:getById` → `propertyService.getPropertyAggregate(id)`
  - `property:getByPropertyNo` → propertyRepository.findByPropertyNo
  - `property:getNextPropertyNo` → `propertyService.getNextPropertyNo()`
  - `property:save` → `propertyService.savePropertyAggregate(payload)`
  - `property:delete` → `propertyService.deleteProperty(id)`

### 3.2 codes 네임스페이스
- [x] `main/ipc/codesIpc.js`
  - `codes:getAll` → `codeItemsRepository.findAll()` (그룹별 객체로 변환)
  - `codes:getByGroup` → `codeItemsRepository.findByGroup(group)`
  - ※ 주의: author는 users 테이블로 분리됨 — codes:getAll 응답에서 제외

### 3.3 address 네임스페이스
- [x] `main/ipc/addressIpc.js`
  - `address:getSidoList`
  - `address:getSigunguList`
  - `address:getEupmyeondongList`
  - `address:getRiList`
  - `address:findLegalDongCode`

---

## 4. Preload 업데이트

- [x] `preload/index.js` — `window.appApi` 전체 노출
  - `property.*` (6개)
  - `codes.*` (2개)
  - `address.*` (5개)
  - `image.*` (placeholder — Phase 5에서 구현)
  - `backup.*` (placeholder — Phase 8에서 구현)
  - `excel.*` (placeholder — Phase 7에서 구현)

---

## 5. Main 진입점 업데이트

- [x] `main/index.js` — IPC 핸들러 등록 호출 추가
  - `propertyIpc.register(ipcMain)`
  - `codesIpc.register(ipcMain)`
  - `addressIpc.register(ipcMain)`

---

## 6. 동작 검증

- [ ] sqlite3 CLI 또는 IPC 직접 호출로 저장/수정/조회 확인
- [ ] 단일행 upsert 동작 확인
- [ ] 다중행 replace 동작 확인 (기존 삭제 후 재삽입)
- [ ] 저장 중 오류 시 rollback 동작 확인
- [ ] `codes:getAll` 응답 그룹 구조 확인

---

## 완료 조건 (전부 충족 시 Phase 2 완료)

- [ ] UI 없이 매물 aggregate 저장/조회 가능
- [ ] 단일행 upsert 정상 동작
- [ ] 다중행 replace 정상 동작
- [ ] 트랜잭션 rollback 정상 동작
- [ ] IPC 채널 전체 등록 완료 (13개 채널)
- [ ] preload window.appApi 노출 완료

---

## 생성 파일 목록

```
main/
├── repositories/
│   ├── propertyRepository.js
│   ├── buildingInfoRepository.js
│   ├── landInfoRepository.js
│   ├── saleInfoRepository.js
│   ├── rentalUnitsRepository.js
│   ├── ownersRepository.js
│   ├── tenantsRepository.js
│   ├── consultationsRepository.js
│   ├── propertyImagesRepository.js
│   ├── codeItemsRepository.js
│   └── addressCodesRepository.js
├── services/
│   └── propertyService.js
├── ipc/
│   ├── propertyIpc.js
│   ├── codesIpc.js
│   └── addressIpc.js
└── index.js  (수정)
preload/
└── index.js  (수정)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| author 처리 | codes:getAll에서 제외, users 테이블 별도 | users 테이블로 분리됨 (Phase 1 스키마 확장) |
| users IPC | Phase 3에서 추가 | UI에서 작성자 선택 기능 구현 시 추가 |
| image/backup/excel IPC | placeholder만 선언 | 각 Phase에서 구현 |
| 공통 응답 형식 | `{ success, data }` / `{ success, error }` | IPC 명세서 기준 |
