from PySide6.QtCore import QThread, Signal
from check_password import Password


class PasswordAnalysisThread(QThread):
    """Full password analysis (strength + HIBP) in background."""
    analysis_complete = Signal(object)

    def __init__(self, password_text):
        super().__init__()
        self.password_text = password_text

    def run(self):
        password_obj = Password(self.password_text)
        self.analysis_complete.emit(password_obj)


class HibpCheckThread(QThread):
    """HIBP-only check in background (avoids blocking the UI)."""
    check_complete = Signal(int)  # emits the occurrence count (-1, 0, or N)

    def __init__(self, password_text):
        super().__init__()
        self.password_text = password_text

    def run(self):
        password_obj = Password.__new__(Password)  # skip full __init__
        password_obj.passwd_value = self.password_text
        result = password_obj.check_unicity()
        self.check_complete.emit(result)
