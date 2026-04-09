# 지식 MCP 검색 전략

플러그인 커스터마이징 중 조직 컨텍스트를 수집하기 위한 쿼리 패턴입니다.

## 도구 이름 찾기

**소스 관리:**
- 검색: "GitHub" OR "GitLab" OR "Bitbucket"
- 검색: "pull request" OR "merge request"
- 찾을 것: 저장소 링크, CI/CD 언급

**프로젝트 관리:**
- 검색: "Asana" OR "Jira" OR "Linear" OR "Monday"
- 검색: "sprint" AND "tickets"
- 찾을 것: 태스크 링크, 프로젝트 보드 언급

**채팅:**
- 검색: "Slack" OR "Teams" OR "Discord"
- 찾을 것: 채널 언급, 통합 논의

**애널리틱스:**
- 검색: "Datadog" OR "Grafana" OR "Mixpanel"
- 검색: "monitoring" OR "observability"
- 찾을 것: 대시보드 링크, 알림 설정

**디자인:**
- 검색: "Figma" OR "Sketch" OR "Adobe XD"
- 찾을 것: 디자인 파일 링크, 핸드오프 논의

**CRM:**
- 검색: "Salesforce" OR "HubSpot"
- 찾을 것: 딜 언급, 고객 레코드 링크

## 조직 값 찾기

**워크스페이스/프로젝트 ID:**
- 기존 통합 또는 북마크된 링크 검색
- 관리자/설정 문서 확인

**팀 관례:**
- 검색: "story points" OR "estimation"
- 검색: "workflow" OR "ticket status"
- 엔지니어링 프로세스 문서 확인

**채널/팀 이름:**
- 검색: "standup" OR "engineering" OR "releases"
- 채널 명명 패턴 확인

## 지식 MCP를 사용할 수 없는 경우

지식 MCP가 설정되지 않은 경우, 자동 검색을 건너뛰고 모든 카테고리에 대해 바로 AskUserQuestion을 진행합니다. 참고: AskUserQuestion은 항상 건너뛰기 버튼과 자유 입력창을 포함하므로 `없음` 또는 `기타` 옵션을 선택지에 추가하지 않습니다.
