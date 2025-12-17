from PySide6.QtCore import QThread, Signal
from check_password import Password

class PasswordAnalysisThread(QThread):
    analysis_complete = Signal(object)
    
    def __init__(self, password_text):
        super().__init__()
        self.password_text = password_text
        
    def run(self):
        # ⚡ Ceci s'exécute en arrière-plan
        password_obj = Password(self.password_text)
        
        # Forcer la vérification API (potentiellement lent)
        password_obj.unicite = password_obj.check_unicity()
        
        # Renvoyer le résultat
        self.analysis_complete.emit(password_obj)