# D4GameEnhancer - Diablo IV Game Enhancer
# Enhances Diablo IV gameplay experience for NVDA users
# Copyright 2025 GPL License
# Author: dnz3d4c

import pathlib

import api
import globalPluginHandler
import queueHandler
import speech
import ui
from NVDAHelper import WINFUNCTYPE, _setDllFuncPointer, c_long, c_wchar_p, localLib
from scriptHandler import script

from .d4_rule_engine import RuleEngine

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "D4GameEnhancer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logging_is_enabled = False
        # 로그 파일: globalPlugins 상위(애드온 루트)에 저장
        addon_root = pathlib.Path(__file__).parent.parent
        self.logfile = open(
            addon_root / "D4GameEnhancer.log", "a", encoding="UTF-8"
        )

        # RuleEngine 초기화
        rules_path = pathlib.Path(__file__).parent / "rules" / "d4_rules.json"
        self.rule_engine = RuleEngine(rules_path)

        self.processText = WINFUNCTYPE(c_long, c_wchar_p)(self.processText)
        _setDllFuncPointer(localLib, "_nvdaController_speakText", self.processText)

    def terminate(self):
        self.logfile.close()
        return super().terminate(self)

    def _check_log_size(self):
        """10MB 초과 시 로그 파일 삭제 후 재생성"""
        if self.logfile.closed:
            return
        self.logfile.flush()
        log_path = pathlib.Path(self.logfile.name)
        if log_path.exists() and log_path.stat().st_size > MAX_LOG_SIZE:
            self.logfile.close()
            log_path.unlink()
            self.logfile = open(log_path, "a", encoding="UTF-8")

    def processText(self, text):
        focus = api.getFocusObject()
        if focus.sleepMode == focus.SLEEP_FULL:
            return -1

        # 규칙 엔진 적용
        processed, meta = self.rule_engine.process(text)

        # ignore 규칙 매칭 시 발화 취소
        if processed is None:
            if self.logging_is_enabled:
                self._check_log_size()
                self.logfile.write(f"[IGNORED] {repr(text)}\n")
                self.logfile.flush()
            return 0

        # 로깅
        if self.logging_is_enabled:
            self._check_log_size()
            self.logfile.write(f"[RAW] {repr(text)}\n")
            self.logfile.flush()

        queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, processed)
        return 0

    @script(
        description="Enables or disables logging",
        gesture="KB:NVDA+ALT+d"
    )
    def script_toggle_logging(self, gesture):
        self.logging_is_enabled = not self.logging_is_enabled
        ui.message(
            f"Logging {'enabled' if self.logging_is_enabled else 'disabled'}"
        )
