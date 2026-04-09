# value-up — 도로명주소 자동완성 플랜

> Phase 3 완료 후 별도 작업으로 처리 (Phase 3.5 또는 Phase 4 전 선택)

---

## 배경

현재: 도로명주소 = 수동 입력 텍스트박스
목표: 읍면동 선택 완료 시 해당 읍면동 소속 도로명 드롭다운 자동 활성화

---

## 소스 데이터

| 파일 | 행수 | 위치 |
|------|------|------|
| `도로명코드.csv` | 203,809행 | `.Source-Files/도로명코드.csv` |

### CSV 컬럼 구조
```
시군구(5), 도로명코드(7), 도로명, 읍면동일련번호(2),
시도명, 시군구명, 읍면동구분(0=읍면/1=동), 읍면동코드(3), 읍면동명
```

예시:
```
11110, 2005001, 세종대로, 01, 서울특별시, 종로구, 1(동), 119, 세종로
```

---

## 법정동코드 ↔ 도로명코드 연계 규칙

```
법정동코드 10자리: [시도2][시군구3][읍면동3][리2]
도로명코드 CSV:    시군구(5자리) + 읍면동코드(3자리)

→ 법정동코드[0:5] = 도로명CSV.시군구(5자리)
→ 법정동코드[5:8] = 도로명CSV.읍면동코드(3자리)
→ 8자리 일치 시 해당 읍면동의 도로명 목록 조회 가능
```

---

## 구현 항목

### 1. DB — road_name_codes 테이블 추가

```sql
CREATE TABLE IF NOT EXISTS road_name_codes (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  sigungu_code     TEXT NOT NULL,   -- 5자리
  road_code        TEXT NOT NULL,   -- 7자리
  road_name        TEXT NOT NULL,
  eupmyeondong_seq TEXT,            -- 읍면동일련번호
  sido_name        TEXT,
  sigungu_name     TEXT,
  eupmyeondong_type INTEGER,        -- 0=읍면, 1=동
  eupmyeondong_code TEXT,           -- 3자리
  eupmyeondong_name TEXT
);
CREATE INDEX idx_road_sigungu_emd ON road_name_codes(sigungu_code, eupmyeondong_code);
```

### 2. seed — 도로명코드.csv 파싱

- `main/db/seed.js` 에 도로명코드 파싱 로직 추가
- CSV 파싱 방식: 법정동코드 seed와 동일 방식
- 203,809건 삽입

### 3. Repository — roadNameCodesRepository.js (신규)

```javascript
// main/repositories/roadNameCodesRepository.js
findRoadNameList(sigunguCode, eupmyeondongCode)
// → road_name_codes WHERE sigungu_code=? AND eupmyeondong_code=?
// → DISTINCT road_name ORDER BY road_name
```

### 4. IPC — addressIpc.js 채널 추가

```javascript
ipcMain.handle('address:getRoadNameList', (_, { sigunguCode, eupmyeondongCode }) => ...)
```

### 5. Preload — window.appApi.address 추가

```javascript
getRoadNameList: (sigunguCode, eupmyeondongCode) =>
  ipcRenderer.invoke('address:getRoadNameList', { sigunguCode, eupmyeondongCode })
```

### 6. basicInfoForm.js — 도로명 드롭다운 추가

- 읍면동 선택 완료 → `legalDongCode` 확정 → `sigunguCode = legalDongCode.slice(0,5)`, `eupmyeondongCode = legalDongCode.slice(5,8)`
- `address.getRoadNameList(sigunguCode, eupmyeondongCode)` 호출
- `roadName` select 드롭다운 활성화
- 읍면동구분 = 0(읍면) → 리 선택 필요, 1(동) → 리 선택 불필요

### 7. index.html — 도로명 드롭다운 필드 추가

- 기존 도로명주소 텍스트 입력 위 또는 대체
- `<select id="roadName">` 추가
- 건물번호 본번/부번은 기존 `mainNo`/`subNo` 숫자 입력 그대로 사용

### 8. 도로명주소 자동 조합

```
도로명주소 = 시도명 + 시군구명 + 도로명 + 본번 + (-부번)
예: 서울특별시 종로구 세종대로 1 → roadAddress 자동 채움
```

---

## 완료 조건

- [x] 읍면동 선택 시 해당 읍면동 도로명 드롭다운 자동 로드
- [x] 도로명 선택 + 건물번호 입력 → 도로명주소 자동 조합
  - roadMainNo / roadSubNo 별도 입력 필드로 지번 본번/부번과 분리
- [ ] 도로명주소 road_address 컬럼 저장/재조회 정상 (앱 검증 필요)
- [ ] 읍면동구분(0/1)으로 리 드롭다운 표시 여부 제어 (추후 보완)

---

## 읍면동구분 활용 (기존 리 드롭다운 개선)

현재 리 드롭다운은 항상 표시됨.
도로명코드의 `읍면동구분` 정보 활용:
- `0` (읍면) → 리 드롭다운 표시
- `1` (동) → 리 드롭다운 숨김

구현 위치: `basicInfoForm.js` 의 `loadEupmyeondong()` 콜백에서 읍면동구분 판별 후 리 드롭다운 표시/숨김 처리.

---

## 주의사항

- 203,809건 seed → 최초 앱 설치 시 seed 시간 증가 예상 (진행 상황 표시 권장)
- 도로명은 `DISTINCT`로 중복 제거 필수
- 읍면동 하나에 여러 도로명이 존재 (예: 세종대로는 종로1가, 종로2가 양쪽에 걸침)
