# value-up Phase 7 — Excel import/export

**참조 문서**
- 마이그레이션 계획: `.Source-Files/08-migration-plan.md`
- IPC 명세: `.Source-Files/04-ipc-api-spec.md`
- Phase 완료 조건 원본: `.Source-Files/07-phase-plan.md` Phase 7

---

## 목표

기본형 Excel 내보내기/가져오기 구현 후 동결
(Phase 6 방식과 동일 — 기본 구현 후 전면 재구상은 추후 별도 플랜)

---

## 시트 구조 설계 원칙

### 현재 (Phase 7 기준)
현재 앱 섹션 기준 **9개 시트**로 내보내기:

| 시트명 | 대상 테이블 |
|--------|-----------|
| 설정_법정동코드 | address_codes |
| 설정_코드목록 | code_items |
| 건축물정보 | properties + building_info |
| 토지이용정보 | land_info |
| 매매정보 | sale_info |
| 임대현황 | rental_units |
| 소유주정보 | owners |
| 임차인정보 | tenants |
| 상담내역 | consultations |

### 추후 (섹션 추가 시)
아파트섹션 / 공장섹션 / 분양권섹션 / 재개발섹션 등 추가될수록 시트 수 증가.
시트 구조 전면 재구상은 범용성 확보 이후 별도 보강 플랜에서 처리.
→ 참조: `.Source-Files/palnsource/엑셀통합관리-계획.md`

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| `main/ipc/excelIpc.js` | ✅ 구현 완료 (2026-03-28) |
| `excel:import` / `excel:export` IPC 채널 | ✅ 등록 완료 |
| preload excel 네임스페이스 | ✅ 기존재 확인 |
| Excel 파싱 라이브러리 | ✅ exceljs 설치 확정 |
| 법정동코드 API 연동 | ⏸ 운영계정 승인 대기 — 보류 |

> **Phase 7 동결 (2026-03-28)** — 기본 구현 완료 후 동결. 추후 보강 플랜에서 처리.

---

## 1. 선행 결정사항

### Excel 파싱 라이브러리
- ✅ **exceljs** 확정 (2026-03-28)

---

## 2. 내보내기(export) 기본 구현

### 2.1 excelIpc.js — excel:export

- ✅ `main/ipc/excelIpc.js`
  - `excel:export` — DB 조회 → 9시트 구조 Excel 생성 → `dialog.showSaveDialog` → 파일 저장

### 2.2 export 정책 (08-migration-plan.md §10)

- 기존 Excel 9시트 구조 최대한 유지
- 설정 시트 포함 가능
- 데이터 시트는 DB 기준으로 재생성
- 빈 더미행 생성 금지
- 숫자는 숫자형 저장
- PNU는 문자열로 유지

---

## 3. 가져오기(import) 기본 구현

### 3.1 구현 범위 (제한)

실제 사용자 Excel 파일 없음 → **목 데이터 Excel 파일 생성 후 가져오기 테스트로 마무리**

- [ ] 목 데이터 Excel 파일 생성 (9시트 표준 구조, 샘플 데이터 포함)
- [ ] `excel:import` 기본 구현 및 목 파일로 테스트

> 실제 사용자 파일 정규화 문제는 별도 계획으로 처리
> → 참조: `.Source-Files/palnsource/엑셀정규화-계획.md`

### 3.2 excelIpc.js — excel:import

- ✅ `excel:import` — `dialog.showOpenDialog` → Excel 파일 선택 → 파서 호출 → DB 마이그레이션

### 3.3 import 선행 정리 작업 (08-migration-plan.md §4)

- [ ] 시트 존재 여부 확인
- [ ] 1행 헤더 확인
- [ ] 완전 빈 행 제거
- [ ] `0 / nan / undefined / ''` 조합의 무효 행 제거
- [ ] 매물번호 0 행 제거
- [ ] PNU 0 행 제거
- [ ] 중복 매물번호 검사

### 3.4 import 순서 (08-migration-plan.md §6)

1. 설정_법정동코드 → address_codes
2. 설정_코드목록 → code_items
3. 건축물정보 → properties + building_info
4. 토지이용정보 → land_info
5. 매매정보 → sale_info
6. 임대현황 → rental_units
7. 소유주정보 → owners
8. 임차인정보 → tenants
9. 상담내역 → consultations

### 3.5 매칭 키 규칙 (08-migration-plan.md §7)

- property_no 우선 / pnu 보조
- property_no 충돌 시 경고 후 중단

### 3.6 import 후 검증 (08-migration-plan.md §9)

- [ ] 총 매물 수 일치 여부
- [ ] 임대현황 행 수 일치 여부
- [ ] 주요 매물 샘플 조회 비교
- [ ] ROI 계산값 재검산
- [ ] 주소/PNU 생성 규칙 일치 여부
- [ ] 이미지 제외 정책 확인

---

## 4. IPC / preload / UI 연결

- ✅ `main/index.js` — excelIpc 등록
- ✅ `preload/index.js` — excel 네임스페이스 기존재 확인
- ✅ `renderer/index.html` — "Excel 가져오기" / "Excel 내보내기" 버튼 활성화
- ✅ `renderer/app.js` — excel 핸들러 추가

---

## 5. 법정동코드 API 연동

- 운영계정 승인 대기 — Phase 7 범위에서 보류
- 승인 후 별도 처리

---

## 완료 조건 (기본형)

- [ ] Excel 내보내기 — 9시트 구조 파일 생성 및 저장 가능
- [ ] Excel 가져오기 — 목 데이터 파일 기준 DB import 정상 동작
- [ ] import 후 검증 항목 확인

---

## 동결 후 보강 방향

> 기본 구현 완료 후 동결. 아래 항목은 추후 별도 보강 플랜에서 처리.

| 항목 | 내용 | 참조 |
|------|------|------|
| 실사용자 Excel 정규화 | 불특정 다수의 임의 구조 Excel → 표준 구조 변환 도구 | `.Source-Files/엑셀정규화-계획.md` |
| 시트 구조 전면 재구상 | 범용 섹션(아파트/공장 등) 추가 후 export 재설계 | `.Source-Files/엑셀통합관리-계획.md` |
| 통합관리 시트 | Excel 내 분할 시트 통합 관리 | `.Source-Files/엑셀통합관리-계획.md` |
| 법정동코드 API 연동 | 운영계정 승인 후 처리 | — |

---

## 생성/수정 파일 목록

```
main/
├── index.js          (수정 — excelIpc 등록)
└── ipc/
    └── excelIpc.js   (신규)

preload/
└── index.js          (수정 — excel 네임스페이스 추가)

renderer/
├── index.html        (수정 — import/export 버튼 연결)
└── app.js            (수정 — excel 핸들러 추가)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| Phase 7 방침 | 기본 구현 후 동결 | Phase 6과 동일 — 범용성 확보 후 전면 재구상 예정 |
| Excel 파싱 라이브러리 | **exceljs** | 헤더 색상 적용 필요 (xlsx는 스타일링 제한) |
| 지원 파일 형식 | `.xlsx` 전용 | 구버전(.xls) 변환은 사용자 몫 |
| 헤더 색상 | 푸른색 계열 | 협의 확정 |
| 열 너비 자동조정 | 미적용 | 사용자 드래그 리사이즈로 충분 |
| 파일간 연결함수 | 불필요 | 9시트가 1파일 내 존재 — 통합관리시트는 범위 외 |
| import 방식 | 1회성/관리자 기능 | 08-migration-plan.md §2 원칙 |
| 가져오기 테스트 방식 | 목 데이터 파일 생성 후 테스트 | 실제 사용자 파일 없음 |
| 매칭 키 | property_no 우선, pnu 보조 | 08-migration-plan.md §7 |
| 계산값 처리 | 원본 저장 후 재계산 검증 | 08-migration-plan.md §5.5 권장 |
| 법정동코드 API | 승인 대기 — Phase 7 내 보류 | 운영계정 미확보 |
