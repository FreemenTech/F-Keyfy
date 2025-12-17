# 🔐 F-Keyfy

**F-Keyfy** - Application desktop de vérification de force , de non-compromision et génération de mots de passe sécurisés, développée avec PySide6 et Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Fonctionnalités

- ✅ **Vérification avancée** de la force des mots de passe
- 🔧 **Génération intelligente** de mots de passe sécurisés  
- 🎨 **Interface moderne** avec styles personnalisés
- ⚡ **Threads asynchrones** pour une expérience fluide
- 📊 **Analyse détaillée** de la sécurité des mots de passe
- 🎯 **Verification de "non-fuite"** du mot de passe

## 🚀 Installation & Utilisation

### Méthode 1 : Depuis les sources
```bash
# Cloner le repository
git clone https://github.com/freemen812/F-Keyfy.git
cd F-Keyfy

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py

Méthode 2 : Installation rapide


pip install PySide6
python main.py


🛠 Technologies Utilisées

    PySide6 - Framework GUI moderne

    Python 3.8+ - Langage de programmation

    QSS - Styling CSS-like pour l'interface

    Threading - Gestion des processus asynchrones

📦 Structure du Projet


F-Keyfy/
├── main.py                 # Point d'entrée principal
├── ui_check_password.py    # Interface utilisateur (PySide6)
├── check_password.py       # Logique de vérification
├── generator_password.py   # Génération de mots de passe
├── threads.py              # Gestion des threads
├── style.qss              # Styles CSS pour l'interface
├── requirements.txt       # Dépendances
└── assets/               # Ressources (logos, icônes)

🎯 Utilisation

    Lancez l'application avec python main.py

    Saisissez un mot de passe pour analyser sa force

    Ou générez un nouveau mot de passe sécurisé

    Consultez les recommandations de sécurité et vérifier si le mot de passe à déjà fuité

👨‍💻 Auteur

Freemen HOUNGBEDJI

    GitHub: @freemen812

    Projet: F-Keyfy

📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

⭐ N'hésitez pas à donner une star au projet si vous le trouvez utile !