# -*- mode: python ; coding: utf-8 -*-
# F-Keyfy.spec — PyInstaller build configuration
# Usage:  pyinstaller F-Keyfy.spec

import sys
from pathlib import Path

block_cipher = None
ROOT = Path(SPECPATH)

# Platform-specific icon
if sys.platform == 'win32':
    app_icon = str(ROOT / 'assets' / 'icons' / 'logo.ico')
elif sys.platform == 'darwin':
    icns_path = ROOT / 'assets' / 'icons' / 'logo.icns'
    app_icon = str(icns_path) if icns_path.exists() else None
else:
    app_icon = None

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / 'style.qss'), '.'),
        (str(ROOT / 'list.txt'),  '.'),
        (str(ROOT / 'assets' / 'icons' / 'logo.png'), 'assets/icons'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Trim unused Qt modules to shrink the build
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineWidgets',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DRender',
        'PySide6.QtMultimedia',
        'PySide6.QtNetwork',  # not needed — requests uses its own stack
    ],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],                    # leave empty for --onedir mode
    exclude_binaries=True, # True = --onedir (more reliable, no antivirus issues)
    name='F-Keyfy',
    icon=app_icon,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,         # windowed mode, no terminal popup
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='F-Keyfy',
)
