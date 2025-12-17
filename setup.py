from cx_Freeze import setup, Executable
import sys
import os

# Configuration de base
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Pour cacher la console sur Windows

# Tous les fichiers à inclure
include_files = [
    "style.qss",
    "list.txt",
    ("assets/icons/", "assets/icons/"),  # Garde la structure de dossier
]

# Packages et modules
packages = [
    "PySide6", 
    "os", 
    "sys", 
    "pathlib",
    "random", 
    "string",
    "threading",
    "time"
]

# Modules à inclure explicitement
includes = [
    "check_password",
    "generator_password", 
    "threads",
    "ui_check_passwd"
]

# Options de build
build_options = {
    "packages": packages,
    "includes": includes,
    "include_files": include_files,
    "excludes": ["tkinter", "test", "unittest", "email"],
    "optimize": 2,
    "include_msvcr": True  # Important pour Windows
}

# Configuration des exécutables
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="F-Keyfy",
        icon="assets/icons/logo.ico" if os.path.exists("assets/icons/logo.ico") else None
    )
]

setup(
    name="F-Keyfy",
    version="1.0.0",
    description="Application de vérification et génération de mots de passe sécurisés",
    options={"build_exe": build_options},
    executables=executables
)