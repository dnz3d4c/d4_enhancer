# 기여 가이드

## 커밋 메시지 규칙

### 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `feat` | 새 기능 추가 | feat: 아이템 드롭 알림 기능 |
| `fix` | 버그 수정 | fix: 슬립 모드에서 TTS 중복 발화 |
| `improve` | 기존 기능 개선 | improve: 빈 문자열 필터링 성능 |
| `refactor` | 코드 구조 변경 (기능 동일) | refactor: RuleEngine 별도 파일 분리 |
| `docs` | 문서 변경 | docs: README 테스트 방법 추가 |
| `chore` | 빌드/설정 변경 | chore: .gitignore 업데이트 |

### feat vs improve vs fix

- **feat**: 완전히 새로운 기능
- **improve**: 기존 기능의 동작 방식 개선 (버그 아님)
- **fix**: 명확한 버그 수정

### 형식

```
<타입>: <간결한 설명>

<선택: 상세 내용>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### 좋은 예시

```
feat: 중복 텍스트 무시 규칙 추가

500ms 내 동일 텍스트 반복 시 음성 발화 안 함
```

```
fix: 게임 종료 시 로그 파일 닫히지 않는 문제

terminate() 호출 시점 수정
```

## 브랜치 전략

현재는 `main` 브랜치 직접 작업. 필요 시:
- `feat/<기능명>`: 새 기능
- `fix/<이슈>`: 버그 수정
