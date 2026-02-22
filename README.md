# D4GameEnhancer

디아블로 IV가 NVDA에 보내는 텍스트를 다듬어서 읽어주는 NVDA 추가 기능입니다.

## 주요 기능

### 텍스트 다듬기

디아블로 IV는 `nvdaController_speakText`를 써서 게임 텍스트를 NVDA에 보냅니다. 이 애드온은 그 텍스트를 가로채서 다듬은 뒤 NVDA로 넘깁니다.

- **빈 문자열/공백 필터링** — 장비 속성, 던전 속성, 설정 항목 사이의 빈 줄을 걸러서 끊김 없이 읽어줌
- **HTML 엔티티 디코딩** — `&lt;`, `&gt;`, `&quot;`, `&apos;` 같은 HTML 엔티티를 실제 문자로 변환
- **규칙 커스터마이징** — JSON 파일로 필터링/바꾸기 규칙 편집 가능

### 메시지 모니터링

`NVDA+ALT+D`로 켜고 끕니다. 게임이 읽어주는 모든 텍스트를 `D4GameEnhancer.log`에 기록합니다. 10MB 넘으면 자동으로 비웁니다.

## 요구 사항

- NVDA 2023.1 이상
- 디아블로 IV

## 설치

1. [Releases](https://github.com/dnz3d4c/d4_enhancer/releases)에서 `.nvda-addon` 다운로드
2. 파일 실행하면 NVDA가 설치 안내

## 단축키

| 단축키 | 기능 |
|--------|------|
| `NVDA+ALT+D` | 메시지 모니터링 켜기/끄기 |

## 개인정보 고지

- 이 애드온은 `nvdaController_speakText`를 후킹합니다. 디아블로 IV뿐 아니라 같은 함수를 쓰는 **모든 프로그램의 텍스트도 가로챕니다.**
- 모니터링을 켜면 가로챈 텍스트가 전부 `D4GameEnhancer.log`에 기록됩니다.
- 기본값은 꺼짐입니다.
- 로그 파일 공유 전에 민감한 정보가 없는지 확인하세요.

## 규칙 커스터마이징

`globalPlugins/rules/d4_rules.json`에서 규칙을 편집할 수 있습니다.

- **ignore** — 맞는 텍스트를 읽지 않음 (정규식, 정확히 일치, 포함)
- **replace** — 맞는 텍스트를 바꿈 (정규식, 정확히 일치)

```json
{
  "rules": {
    "ignore": [
      {"id": "empty_string", "pattern": "^$", "type": "regex", "description": "빈 문자열 무시"}
    ],
    "replace": []
  }
}
```

## 빌드

```bash
uv run python scripts/build.py
```

`dist/D4GameEnhancer-v0.1.0.nvda-addon`에 생성됩니다.

## 라이선스

GPL-3.0
