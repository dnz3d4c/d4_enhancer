# D4GameEnhancer

디아블로 IV가 NVDA에 보내는 텍스트를 정제하여 읽어주는 NVDA 추가 기능.

## 주요 기능

### 텍스트 정제

디아블로 IV는 `nvdaController_speakText`를 호출하여 게임 텍스트를 NVDA에 전달한다. 이 애드온은 해당 텍스트를 가로채서 정제한 뒤 NVDA 음성으로 넘긴다.

- **빈 문자열/공백 필터링** — 장비 속성, 던전 속성, 설정 항목 사이에 끼어 있는 빈 줄을 제거하여 속성을 끊김 없이 연속으로 읽어줌
- **HTML 엔티티 디코딩** — `&lt;`, `&gt;`, `&quot;`, `&apos;` 등을 실제 문자로 변환 (클랜 태그, 아이템 설명 인용문 등에서 발생)
- **규칙 커스터마이징** — JSON 규칙 파일로 필터링/치환 규칙을 직접 편집 가능

### 메시지 모니터링

`NVDA+ALT+D`로 켜고 끌 수 있다. 게임에서 읽히는 모든 텍스트를 `D4GameEnhancer.log`에 기록한다. 10MB 초과 시 자동 정리된다.

## 요구 사항

- NVDA 2023.1 이상
- 디아블로 IV

## 설치

1. [Releases](https://github.com/dnz3d4c/d4_enhancer/releases)에서 `.nvda-addon` 다운로드
2. 다운로드한 파일을 실행하면 NVDA가 설치를 안내함

## 단축키

| 단축키 | 기능 |
|--------|------|
| `NVDA+ALT+D` | 메시지 모니터링 켜기/끄기 |

## 개인정보 고지

- 이 애드온은 `nvdaController_speakText`를 후킹한다. 디아블로 IV뿐 아니라 같은 함수를 사용하는 **모든 프로그램의 텍스트가 가로채어진다.**
- 메시지 모니터링을 켜면 가로챈 모든 텍스트가 `D4GameEnhancer.log`에 기록된다.
- 기본값은 모니터링 꺼짐이다.
- 로그 파일을 다른 사람과 공유할 때 민감한 정보가 포함되어 있지 않은지 확인할 것.

## 규칙 커스터마이징

`globalPlugins/rules/d4_rules.json`에서 필터링/치환 규칙을 편집할 수 있다.

- **ignore** — 매칭되는 텍스트를 읽지 않음 (정규식, 정확히 일치, 포함)
- **replace** — 매칭되는 텍스트를 치환 (정규식, 정확히 일치)

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

결과물은 `dist/D4GameEnhancer-v0.1.0.nvda-addon`에 생성된다.

## 라이선스

GPL-3.0
