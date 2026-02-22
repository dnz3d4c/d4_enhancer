# D4GameEnhancer - Rule Engine
# TTS 텍스트 필터링 규칙 엔진

import html
import json
import pathlib
import re
from typing import Optional


class RuleEngine:
    """TTS 텍스트 처리 규칙 엔진"""

    def __init__(self, rules_path: pathlib.Path):
        self.rules_path = rules_path
        self.rules = self._load_rules()
        self._compiled_patterns: dict[str, re.Pattern] = {}
        self._compile_patterns()

    def _load_rules(self) -> dict:
        """규칙 파일 로드"""
        if not self.rules_path.exists():
            return {"version": "1.0", "rules": {"ignore": [], "replace": [], "priority": []}}

        with open(self.rules_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _compile_patterns(self) -> None:
        """정규식 패턴 미리 컴파일"""
        for rule in self.rules.get("rules", {}).get("ignore", []):
            if rule.get("type") == "regex":
                pattern_id = rule["id"]
                self._compiled_patterns[pattern_id] = re.compile(rule["pattern"])

        for rule in self.rules.get("rules", {}).get("replace", []):
            if rule.get("type") == "regex":
                pattern_id = rule["id"]
                self._compiled_patterns[pattern_id] = re.compile(rule["pattern"])

    def reload_rules(self) -> None:
        """규칙 파일 다시 로드"""
        self.rules = self._load_rules()
        self._compiled_patterns.clear()
        self._compile_patterns()

    def process(self, text: str) -> tuple[Optional[str], dict]:
        """
        텍스트에 규칙 적용

        Returns:
            (processed_text, metadata)
            processed_text가 None이면 발화 취소
        """
        meta = {"ignored": False, "matched_rule": None}

        # 1. ignore 규칙 체크
        for rule in self.rules.get("rules", {}).get("ignore", []):
            if self._matches_rule(text, rule):
                meta["ignored"] = True
                meta["matched_rule"] = rule["id"]
                return (None, meta)

        # 2. HTML 엔티티 디코딩
        processed = html.unescape(text)

        # 3. replace 규칙 적용
        for rule in self.rules.get("rules", {}).get("replace", []):
            processed = self._apply_replace(processed, rule)

        return (processed, meta)

    def _matches_rule(self, text: str, rule: dict) -> bool:
        """텍스트가 규칙에 매칭되는지 확인"""
        rule_type = rule.get("type", "exact")
        pattern = rule.get("pattern", "")

        if rule_type == "regex":
            compiled = self._compiled_patterns.get(rule["id"])
            if compiled:
                return bool(compiled.match(text))
        elif rule_type == "exact":
            return text == pattern
        elif rule_type == "contains":
            return pattern in text

        return False

    def _apply_replace(self, text: str, rule: dict) -> str:
        """치환 규칙 적용"""
        rule_type = rule.get("type", "exact")
        pattern = rule.get("pattern", "")
        replacement = rule.get("replacement", "")

        if rule_type == "regex":
            compiled = self._compiled_patterns.get(rule["id"])
            if compiled:
                return compiled.sub(replacement, text)
        elif rule_type == "exact":
            return text.replace(pattern, replacement)

        return text
