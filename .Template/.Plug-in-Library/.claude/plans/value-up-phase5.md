# value-up Phase 5 — 보안정보 및 이미지

**참조 문서**
- IPC 명세: `.Source-Files/04-ipc-api-spec.md`
- UI 명세: `.Source-Files/05-ui-spec.md`

---

## 목표

소유주 / 임차인 / 상담내역 / 이미지 기능 구현
보안정보는 인쇄 시 완전 제외

---

## 현재 상태 (Phase 5 진입 시점)

| 항목 | 상태 |
|------|------|
| owners / tenants / consultations / property_images Repository | ✅ Phase 2 구현 완료 |
| imageIpc.js | ❌ 미구현 |
| main/index.js imageIpc 등록 | ❌ 미등록 |
| mapper.js owners/tenants/consultations/images 매핑 | 확인 필요 |
| index.html 보안정보/이미지 섹션 | stub 상태 |
| app.js 연동 | ❌ 미연동 |

---

## 1. imageIpc.js 신규 구현

- [x] `main/ipc/imageIpc.js`
  - `image:upload` — `dialog.showOpenDialog` → 파일 선택 → `userData/uploads/` 복사 → `{ imagePath, originalName }` 반환
    - 파일명: `property_{propertyId}_{timestamp}{ext}`
    - 지원 확장자: jpg, jpeg, png, gif, webp
  - `image:delete` — 파일시스템에서 실제 파일 삭제 (DB 제거는 property.save에서 처리)
  - `image:getDataPath` — `app.getPath('userData')` 반환 (Renderer 미리보기용)

---

## 2. main/index.js 수정

- [x] `imageIpc = require('./ipc/imageIpc')` 추가
- [x] `imageIpc.register(ipcMain)` 추가

---

## 3. preload/index.js 수정

- [x] `image.getDataPath` 채널 추가
  ```javascript
  getDataPath: () => ipcRenderer.invoke('image:getDataPath'),
  ```

---

## 4. index.html 수정

### 4.1 이미지 섹션 (stub → 실제 UI)

- [x] 파일 선택 버튼
- [x] 이미지 썸네일 그리드 (미리보기)
- [x] 각 이미지: 썸네일 + 삭제 버튼 + sort_order
- [x] `<script src="form/imagesForm.js">` 추가

### 4.2 보안정보 섹션 (stub → 실제 UI)

- [x] `no-print` 클래스 적용 (섹션 전체)
- [x] 소유주 테이블: 성명 / 연락처 / 삭제 + 행추가 버튼
- [x] 임차인 테이블: 호실 / 성명 / 연락처 / 삭제 + 행추가 버튼
- [x] 상담내역 테이블: 상담일 / 상담유형 / 담당자 / 내용(textarea) / 후속조치 / 다음상담일 / 삭제 + 행추가 버튼
- [x] `<script src="form/ownersForm.js">` 추가
- [x] `<script src="form/tenantsForm.js">` 추가
- [x] `<script src="form/consultationsForm.js">` 추가

---

## 5. form 모듈 신규 구현

### 5.1 ownersForm.js

- [x] `renderer/form/ownersForm.js`
  - `init()` — 행추가 버튼 이벤트 바인딩
  - `addRow(data)` — 행 추가 (성명, 연락처 입력 + 자동 하이픈)
  - `getValues()` → `[{ owner_name, phone, sort_order }]`
  - `setValues(rows)` — DB 배열 → 행 렌더링
  - `reset()` — 테이블 비우기

### 5.2 tenantsForm.js

- [x] `renderer/form/tenantsForm.js`
  - `init()` — 행추가 버튼 이벤트 바인딩
  - `addRow(data)` — 행 추가 (호실, 성명, 연락처 + 자동 하이픈)
  - `getValues()` → `[{ room_no, tenant_name, phone, sort_order }]`
  - `setValues(rows)` / `reset()`

### 5.3 consultationsForm.js

- [x] `renderer/form/consultationsForm.js`
  - `init()` — 행추가 버튼 이벤트 바인딩
  - `addRow(data)` — 행 추가 (상담일, 상담유형, 담당자, 내용textarea, 후속조치, 다음상담일)
  - 날짜 필드: blur 시 YYYY-MM-DD 정규화
  - `getValues()` → `[{ consult_date, consult_type, consultant, content, follow_up, next_consult_date, sort_order }]`
  - `setValues(rows)` / `reset()`

### 5.4 imagesForm.js

- [x] `renderer/form/imagesForm.js`
  - `init()` — `appApi.image.getDataPath()` 로 userData 경로 확보, 파일 선택 버튼 이벤트
  - `addImage(meta)` — 썸네일 카드 생성 (`file://{dataPath}/{imagePath}`)
  - `onUploadClick()` — `appApi.image.upload()` → addImage()
  - `onDeleteClick(imageId, imagePath)` — `appApi.image.delete()` → 카드 제거
  - `getValues()` → `[{ image_path, original_name, sort_order }]`
  - `setValues(images)` — DB 배열 → 썸네일 렌더링
  - `reset()` — 그리드 비우기

---

## 6. mapper.js 확인 및 보완

- [x] `aggregateToForm(data)` — owners / tenants / consultations / images 매핑 확인 (Phase 2에서 완료)
- [x] `formToPayload()` — 각 form.getValues() 포함 확인 (Phase 2에서 완료)

---

## 7. app.js 수정

- [x] `ownersForm.init()` 추가
- [x] `tenantsForm.init()` 추가
- [x] `consultationsForm.init()` 추가
- [x] `imagesForm.init()` 추가
- [x] `clearForms()` — 4개 form reset 추가
- [x] `onPropertySelected()` — setValues 4개 추가
- [x] `onSave()` payload에 4개 getValues() 추가

---

## 8. 보완 구현 (검증 중 발견)

- [x] `format.js` formatPhone — 02 지역번호/일반전화/휴대폰 분기 수정
- [x] `migrate.js` — owners.note / tenants.note 컬럼 추가
- [x] `ownersRepository.js` / `tenantsRepository.js` — note 컬럼 INSERT 반영
- [x] `ownersForm.js` / `tenantsForm.js` — 비고 필드 추가
- [x] `consultationsForm.js` — 상담내용 별도 행(2행세트) + 상담일 오늘날짜 기본값 + textarea 자동높이
- [x] `index.html` — 테이블 헤더 비고 추가, 상담내역 헤더 수정, 이미지추가버튼 no-print
- [x] `imagesForm.js` — btn-del-image에 no-print 클래스 추가 (동작 검증 후 발견)

---

## 완료 조건

- [x] 소유주 저장/재조회 정상
- [x] 임차인 저장/재조회 정상
- [x] 상담내역 저장/재조회 정상
- [x] 이미지 업로드/미리보기/삭제 정상
- [x] 보안정보 섹션 `no-print` 적용 확인 (클래스 적용 완료, 실제 인쇄 제외는 Phase 6)

---

## 생성/수정 파일 목록

```
main/
├── index.js              (수정 — imageIpc 등록)
└── ipc/
    └── imageIpc.js       (신규)

preload/
└── index.js              (수정 — image.getDataPath 추가)

renderer/
├── index.html            (수정 — 이미지/보안정보 섹션 실제 UI)
├── app.js                (수정 — 4개 form 연동)
├── utils/
│   └── mapper.js         (확인/보완)
└── form/
    ├── ownersForm.js      (신규)
    ├── tenantsForm.js     (신규)
    ├── consultationsForm.js (신규)
    └── imagesForm.js      (신규)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| 이미지 저장 경로 | `{userData}/uploads/{filename}` | Electron userData 표준 경로 |
| 이미지 파일명 | `property_{propertyNo}_{timestamp}{ext}` | 매물번호 기준 관리 |
| 미리보기 | `file://` 절대경로 | Electron contextIsolation 환경 |
| 보안정보 인쇄 제외 | `no-print` CSS 클래스 | Phase 6 print.css에서 처리 |
| 상담유형 | 텍스트 자유입력 | 코드 그룹 없음, 다양한 유형 허용 |
| 연락처 자동 하이픈 | format.js `formatPhone()` 활용 | 기존 유틸 재사용 |
