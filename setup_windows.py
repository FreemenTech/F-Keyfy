from cx_Freeze import setup, Executable
import sys
import os
import platform

# Configuration spécifique Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Cache la console pour les apps GUI Windows

# Fichiers à inclure
include_files = [
    "style.qss",
    "list.txt",
    "assets/icons/",  # cx_Freeze copiera tout le dossier
]

# Packages essentiels pour Windows
packages = [
    "PySide6", 
    "os", 
    "sys", 
    "pathlib",
    "random", 
    "string",
    "threading",
    "hashlib",
    "urllib.request",
    "json"
]

# Vos modules personnalisés
includes = [
    "check_password",
    "generator_password", 
    "threads",
    "ui_check_passwd"
]

# Options de build optimisées pour Windows
build_options = {
    "packages": packages,
    "includes": includes,
    "include_files": include_files,
    "excludes": [
        "tkinter", "test", "unittest", "email", 
        "pydoc", "pdb", "matplotlib", "scipy"
    ],
    "optimize": 2,
    "include_msvcr": True,  # ⬅️ CRITIQUE pour Windows
    "zip_include_packages": ["PySide6", "encodings"],
}

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="F-Keyfy.exe",  # ⬅️ .exe pour Windows
        icon="assets/icons/logo.ico",  # ⬅️ .ico obligatoire pour Windows
        copyright="Copyright © 2025 - F-Keyfy",
        shortcut_name="F-Keyfy Password Manager",
        shortcut_dir="ProgramMenuFolder",
    )
]

setup(
    name="F-Keyfy",
    version="1.0.0",
    description="Password Manager - Vérification et génération de mots de passe sécurisés",
    author="Votre Nom",
    options={"build_exe": build_options},
    executables=executables
)