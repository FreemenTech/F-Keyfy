# main.py 
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from ui_check_passwd import Ui_MainWindow
from check_password import Password
from generator_password import Generator_Pwd
from threads import PasswordAnalysisThread 
import sys
from PySide6.QtGui import QIcon
import os
from pathlib import Path


# === FONCTIONS POUR CX_FREEZE ===
def resource_path(relative_path):
    """Get absolute path to resource - compatible cx_Freeze"""
    if getattr(sys, 'frozen', False):
        # Mode application compilée
        base_path = sys._MEIPASS
    else:
        # Mode développement
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

def load_stylesheet():
    """Charge le fichier de style QSS"""
    try:
        style_path = resource_path("style.qss")
        with open(style_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Style non chargé: {e}")
        return ""

def set_app_icon(window):
    """Définit l'icône de l'application"""
    icon_paths = [
        "assets/icons/logo.ico",
        "assets/icons/logo.png",
        "logo.ico",
        "logo.png"
    ]
    
    for path in icon_paths:
        full_path = resource_path(path)
        if os.path.exists(full_path):
            window.setWindowIcon(QIcon(full_path))
            print(f"Icône chargée: {full_path}")
            break

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("F-Keyfy")
        self.setFixedSize(800, 600)
        
        # Charger le style
        stylesheet = load_stylesheet()
        if stylesheet:
            self.setStyleSheet(stylesheet)
        
        # Définir l'icône
        set_app_icon(self)
    
        #=============== Connection button to function ================
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
        
        #  cette connexion pour cacher la progress bar quand le texte change
        self.ui.lineEdit_1.textChanged.connect(self.on_password_changed)
        self.ui.lineEdit_2.setReadOnly(True)

        # Cacher les label AU DÉPART
        self.ui.progressBar.hide() 
        self.ui.label_tips.hide()


    def on_password_changed(self, text):
        """Cache la progress bar quand le mot de passe est modifié"""
        if not text:  # Si le champ est vide
            self.ui.progressBar.hide()
            self.ui.label_tips.hide()

    def verify_passwd(self):
        pwd = self.ui.lineEdit_1.text()
        if not pwd:
            self.ui.label_tips.show()
            self.ui.label_tips.setText("⚠️ Veuillez entrer un mot de passe.")
            return
        
        # Afficher la progress bar
        self.ui.progressBar.show()
        self.ui.progressBar.setRange(0, 0)  # Mode chargement
        self.ui.label_tips.show()
        self.ui.label_tips.setText("🔍 Analyse en cours...")
        
        self.ui.btn_verify.setEnabled(False)
        
        #  Lancer l'analyse en arrière-plan
        self.analysis_thread = PasswordAnalysisThread(pwd)
        self.analysis_thread.analysis_complete.connect(self.on_analysis_complete)
        self.analysis_thread.start()

    def on_analysis_complete(self, password_obj):

        """Callback quand l'analyse est terminée"""
        # Réactiver le bouton
        self.ui.btn_verify.setEnabled(True)
        self.ui.progressBar.setRange(0, 100)  # Retour au mode normal
        
        # Afficher les résultats (progress bar reste visible)
        self.update_progress_bar(password_obj.strength_label)
        
        # Afficher le résultat complet
        result_text = password_obj.get_info()
        if password_obj.unicite > 0:
            result_text += f"\n\n⚠️ Mot de passe trouvé {password_obj.unicite} fois dans des fuites!"
        elif password_obj.unicite == -1:
            result_text += f"\n\n🌐 Vérification API impossible (erreur réseau)"
        
        self.ui.label_tips.setText(result_text)

    def update_progress_bar(self, strength_label):
        """Met à jour la progress bar selon la force du mot de passe"""
        strength_values = {
            "Très faible 🔴": 25,
            "Moyen 🟠": 50, 
            "Bon 🟢": 75,
            "Excellent 🟣": 100
        }
        
        value = strength_values.get(strength_label, 0)
        self.ui.progressBar.setValue(value)
        
        # Changer la couleur selon la force
        if "Excellent" in strength_label or "Bon" in strength_label:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #28a745; }")
        elif "Moyen" in strength_label:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #ffc107; }")
        else:
            self.ui.progressBar.setStyleSheet("QProgressBar::chunk { background-color: #dc3545; }")

#===========Autre fonction importante =======
    def go_to_page2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
    
    def go_to_page1(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def quit_app(self):
        QApplication.quit()

    def copy_passwd(self):
        texte = self.ui.lineEdit_2.text()      
        # Vérifier si le champ n'est pas vide
        if texte.strip():  # Si y a du texte
            clipboard = QApplication.clipboard() 
            clipboard.setText(texte)           
            QMessageBox.information(self, "Succès", "✅ Mot de passe copié dans le presse-papier !")
        else:
            QMessageBox.warning(self,"Erreur","⚠️ Aucun mot de passe à copier")

    def generer_passwd_choisi(self):
        if self.ui.checkBox_memonic.isChecked():
            self.generer_memonic_password(True)
        else:
            self.generer_passwd()

    def generer_passwd(self):
        lenght = self.ui.spinBox.value()
        generator = Generator_Pwd(lenght)
        self.ui.lineEdit_2.setText(generator.password_generer)

    def generer_memonic_password(self, checked: bool = True):
        if checked:  
            lenght = self.ui.spinBox.value()
            generator = Generator_Pwd(lenght)
            self.ui.lineEdit_2.setText(generator.memonic_pwd)

    def show_passwd(self, checked: bool):
        if checked:
            self.ui.lineEdit_1.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.lineEdit_1.setEchoMode(QLineEdit.Password)
        
    def verify_api(self):
        self.password_obj = Password(self.ui.lineEdit_1.text())
        self.ui.label_tips.show()
        result = self.password_obj.check_unicity()
        if result == 0:
            self.ui.label_tips.setText("✅ Mot de passe unique, jamais exposé !")
        elif result > 0:
            self.ui.label_tips.setText(f"⚠️ Ce mot de passe est déjà apparu {result} fois dans des fuites !")
        else:
            self.ui.label_tips.setText("⚠️ Vérification impossible (erreur réseau ou API).")
  
       
 #================== Fonction d'afffichage d'aide ======================

    def show_help(self):
            help_text = """
        🔐 **Guide d'utilisation - Password Manager Pro**

        📖 **FONCTIONNALITÉS PRINCIPALES :**

        🔒 **VÉRIFICATION DE MOT DE PASSE (Page 1)**
        • Analyse la force de votre mot de passe
        • Vérifie s'il a été compromis dans des fuites de données
        • Donne des conseils personnalisés pour l'améliorer

        🎲 **GÉNÉRATION DE MOTS DE PASSE (Page 2)**
        • Générateur classique : mots de passe sécurisés aléatoires
        • Générateur mnémonique : mots de passe faciles à retenir
        • Personnalisation de la longueur (6-24 caractères)

        💡 **BONNES PRATIQUES RECOMMANDÉES :**

        ✅ **Créez des mots de passe robustes :**
        - Minimum 12 caractères
        - Majuscules + minuscules + chiffres + symboles
        - Évitez les informations personnelles
        - Unique pour chaque compte

        ✅ **Utilisez notre vérification API :**
        - Contrôlez si votre mot de passe a fuité
        - Protégez-vous contre le réemploi de mots de passe compromis

        ✅ **Gestion sécurisée :**
        - Utilisez un gestionnaire de mots de passe
        - Activez la double authentification (2FA)
        - Changez vos mots de passe après une fuite

        🛡️ **POURQUOI LA SÉCURITÉ DES MOTS DE PASSE EST IMPORTANTE :**
        • 80% des fuites de données sont dues à des mots de passe faibles
        • Les mots de passe réutilisés multiplient les risques
        • La vérification proactive peut prévenir le vol d'identité

        📞 **SUGGESTIONS :**
        • Utilisez régulièrement la vérification API pour vos mots de passe importants
        • Le générateur mnémonique est idéal pour les mots de passe que vous devez retenir
        • Copiez directement dans le presse-papier pour plus de sécurité

        ---
        Développé avec ❤️ pour votre sécurité numérique
        """
            msg = QMessageBox(self)
            msg.setWindowTitle("Aide - F-Keyfy")
            msg.setText(help_text)
            msg.exec()

    def show_about(self): 

        about_text ="""F-Keyfy v1.0

        Outil de sécurité développé pour aider les utilisateurs à créer, analyser, voir si le mot de passe à fuité et renforcer leurs mots de passe.

        🔐 Vérifie la force, l’entropie et l’exposition des mots de passe.
        🧠 Génère des mots de passe et des phrases mnémotechniques puissants.


        Développé par : Freemen HOUNGBEDJI
        Entreprise : X-Security
        Année : 2025

        Contact : hfreemen9.@gmail.com
        GitHub : github.com/freemen812

        “Secure your world — one password at a time.”
        
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Aide - F-Keyfy")
        msg.setText(about_text)
        msg.exec()




def main():
    app = QApplication(sys.argv)
    app.setApplicationName("F-Keyfy")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
