# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from PySide6.QtCore import QTimer
from ui_check_passwd import Ui_MainWindow
from check_password import Password
from generator_password import Generator_Pwd, resource_path
from threads import PasswordAnalysisThread, HibpCheckThread
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("F-Keyfy")
        self.setFixedSize(800, 600)
    
        # Connect buttons and actions
        self.ui.btn_verify.clicked.connect(self.verify_passwd)
        self.ui.btn_page1.clicked.connect(self.go_to_page2)
        self.ui.btn_auto_generer.clicked.connect(self.go_to_page1)
        self.ui.act_quit_2.triggered.connect(self.quit_app)
        self.ui.act_help.triggered.connect(self.show_help)
        self.ui.act_propos.triggered.connect(self.show_about)
        self.ui.btn_api.clicked.connect(self.verify_api)
        self.ui.btn_copy.clicked.connect(self.copy_passwd)
        self.ui.btn_generer.clicked.connect(self.generer_passwd_choisi)
        self.ui.check_pwd_show.toggled.connect(self.show_passwd)
        
        # Hide progress bar at start
        self.ui.lineEdit_1.textChanged.connect(self.on_password_changed)
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.progressBar.hide() 
        self.ui.label_tips.hide()

        # Clipboard auto-clear timer (30 seconds)
        self._clipboard_timer = QTimer(self)
        self._clipboard_timer.setSingleShot(True)
        self._clipboard_timer.timeout.connect(self._clear_clipboard)

    # ====================== Callback when password changes ======================
    def on_password_changed(self, text):
        if not text:
            self.ui.progressBar.hide()
            self.ui.label_tips.hide()

    # ====================== Verify password ======================
    def verify_passwd(self):
        pwd = self.ui.lineEdit_1.text()
        if not pwd:
            self.ui.label_tips.show()
            self.ui.label_tips.setText("⚠️ Please enter a password.")
            return
        
        self.ui.progressBar.show()
        self.ui.progressBar.setRange(0, 0)
        self.ui.label_tips.show()
        self.ui.label_tips.setText("🔍 Analyzing...")
        self.ui.btn_verify.setEnabled(False)
        
        # Start background analysis
        self.analysis_thread = PasswordAnalysisThread(pwd)
        self.analysis_thread.analysis_complete.connect(self.on_analysis_complete)
        self.analysis_thread.start()

    # ====================== Callback when analysis completes ======================
    def on_analysis_complete(self, password_obj):
        self.ui.btn_verify.setEnabled(True)
        self.ui.progressBar.setRange(0, 100)
        self.update_progress_bar(password_obj.strength_label)
        
        result_text = password_obj.get_info()
        if password_obj.unicity > 0:
            result_text += f"\n\n⚠️ Password found {password_obj.unicity} times in leaks!"
        elif password_obj.unicity == -1:
            result_text += f"\n\n🌐 API verification impossible (network error)"
        
        self.ui.label_tips.setText(result_text)

    # ====================== Update progress bar according to password strength ======================
    def update_progress_bar(self, strength_label):
        strength_values = {
            "Very weak 🔴": 25,
            "Medium 🟠": 50, 
            "Good 🟢": 75,
            "Excellent 🟣": 100
        }
        value = strength_values.get(strength_label, 0)
        self.ui.progressBar.setValue(value)
        
        # Change color according to strength
        if "Excellent" in strength_label or "Good" in strength_label:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #28a745; }")
        elif "Medium" in strength_label:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #ffc107; }")
        else:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #dc3545; }")

    # ====================== Page navigation ======================
    def go_to_page2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
    
    def go_to_page1(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    # ====================== Quit application ======================
    def quit_app(self):
        QApplication.quit()

    # ====================== Copy password to clipboard ======================
    def copy_passwd(self):
        text = self.ui.lineEdit_2.text()
        if text.strip():
            QApplication.clipboard().setText(text)
            self._clipboard_timer.start(30_000)  # auto-clear after 30 seconds
            QMessageBox.information(self, "Success", "✅ Password copied! Clipboard will auto-clear in 30s.")
        else:
            QMessageBox.warning(self, "Error", "⚠️ No password to copy")

    def _clear_clipboard(self):
        """Wipe the clipboard after the safety timeout."""
        QApplication.clipboard().clear()

    # ====================== Generate password depending on user choice ======================
    def generer_passwd_choisi(self):
        if self.ui.checkBox_memonic.isChecked():
            self.generer_memonic_password(True)
        else:
            self.generer_passwd()

    # ====================== Generate standard password ======================
    def generer_passwd(self):
        length = self.ui.spinBox.value()
        generator = Generator_Pwd(length)
        self.ui.lineEdit_2.setText(generator.generated_password)

    # ====================== Generate mnemonic password ======================
    def generer_memonic_password(self, checked: bool = True):
        if checked:
            length = self.ui.spinBox.value()
            generator = Generator_Pwd(length)
            self.ui.lineEdit_2.setText(generator.memonic_password)

    # ====================== Show/hide password ======================
    def show_passwd(self, checked: bool):
        self.ui.lineEdit_1.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        
    # ====================== Verify password uniqueness via API (non-blocking) ======================
    def verify_api(self):
        pwd = self.ui.lineEdit_1.text()
        if not pwd:
            self.ui.label_tips.show()
            self.ui.label_tips.setText("⚠️ Please enter a password.")
            return

        self.ui.label_tips.show()
        self.ui.label_tips.setText("🔍 Checking against known leaks...")
        self.ui.btn_api.setEnabled(False)

        self._hibp_thread = HibpCheckThread(pwd)
        self._hibp_thread.check_complete.connect(self._on_hibp_result)
        self._hibp_thread.start()

    def _on_hibp_result(self, result):
        """Callback when HIBP check finishes."""
        self.ui.btn_api.setEnabled(True)
        if result == 0:
            self.ui.label_tips.setText("✅ Unique password, never exposed!")
        elif result > 0:
            self.ui.label_tips.setText(f"⚠️ This password has appeared {result} times in leaks!")
        else:
            self.ui.label_tips.setText("⚠️ Verification impossible (network or API error).")
  
   # ====================== Help display function ======================
    def show_help(self):
        help_text = """
        🔐 **User Guide - Password Manager Pro**

        📖 **MAIN FEATURES:**

        🔒 **PASSWORD VERIFICATION (Page 1)**
        • Analyze the strength of your password
        • Check if it has been compromised in data leaks
        • Provide personalized advice to improve it

        🎲 **PASSWORD GENERATION (Page 2)**
        • Classic generator: random secure passwords
        • Mnemonic generator: easy-to-remember passwords
        • Customize length (6-24 characters)

        💡 **RECOMMENDED BEST PRACTICES:**

        ✅ **Create strong passwords:**
        - Minimum 12 characters
        - Uppercase + lowercase + numbers + symbols
        - Avoid personal information
        - Unique for each account

        ✅ **Use our API verification:**
        - Check if your password has leaked
        - Protect yourself against reused compromised passwords

        ✅ **Secure management:**
        - Use a password manager
        - Enable two-factor authentication (2FA)
        - Change your passwords after a leak

        🛡️ **WHY PASSWORD SECURITY IS IMPORTANT:**
        • 80% of data breaches are due to weak passwords
        • Reused passwords multiply risks
        • Proactive checking can prevent identity theft

        📞 **SUGGESTIONS:**
        • Regularly verify important passwords via API
        • Mnemonic generator is ideal for passwords you need to remember
        • Copy directly to clipboard for added security

        ---
        Developed with ❤️ for your digital security
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Help - F-Keyfy")
        msg.setText(help_text)
        msg.exec()

    # ====================== About display function ======================
    def show_about(self): 
        about_text = """F-Keyfy v1.0

        Security tool developed to help users create, analyze, check if passwords have leaked, and strengthen their passwords.

        🔐 Checks password strength, entropy, and exposure.
        🧠 Generates strong passwords and mnemonic phrases.

        Developed by: Freemen HOUNGBEDJI
        Company: FreemenTech
        Year: 2025

        Contact: houngbedjifreemen.@gmail.com
        GitHub: @FreemenTech

        “Secure your world — one password at a time.”
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("About - F-Keyfy")
        msg.setText(about_text)
        msg.exec()



# ====================== Main function ======================
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("F-Keyfy")
    app.setApplicationVersion("1.0.0")

      # --- Load QSS style ---
    try:
        qss_path = resource_path("style.qss")
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Failed to load style.qss: {e}")

    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
