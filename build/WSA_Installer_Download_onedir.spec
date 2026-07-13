# -*- mode: python ; coding: utf-8 -*-
# WSA_Installer_Download_onedir.spec
# --onedir mode

from PyInstaller.utils.hooks import collect_submodules

import os
# SPECPATH in PyInstaller 6.x is already the directory containing the .spec file
# (from os.path.split in build_main.py:1140), so use it directly.
_project_root = os.path.abspath(SPECPATH)
_venv_site = os.path.join(_project_root, 'venv', 'Lib', 'site-packages')

# Resolve base Python DLLs from venv's pyvenv.cfg (portable, no hardcoded user path)
_dlls_dir = os.path.join(_project_root, 'venv', 'DLLs')
if not os.path.isdir(_dlls_dir):
    _pyvenv_cfg = os.path.join(_project_root, 'venv', 'pyvenv.cfg')
    if os.path.isfile(_pyvenv_cfg):
        with open(_pyvenv_cfg) as _f:
            for _line in _f:
                if _line.strip().startswith('home = '):
                    _dlls_dir = os.path.join(_line.split('=', 1)[1].strip(), 'DLLs')
                    break

a = Analysis(
    ['run.py'],
    pathex=[_venv_site],
    binaries=[
        ('widget_ui.pyd', '.'),
        ('playstore_patcher_mem.pyd', '.'),
        ('*.pyd', '.'),
        (os.path.join(_dlls_dir, 'sqlite3.dll'), '.'),
        (os.path.join(_dlls_dir, '_sqlite3.pyd'), '.'),
    ],
    datas=[('assets', 'assets')],
    hiddenimports=[
        'requests',
        'flet',
        'pyautogui',
        'pyperclip',
        'pywinauto',
        'PyQt6',
    ]
        + collect_submodules('requests')
        + collect_submodules('flet')
        + collect_submodules('pyautogui')
        + collect_submodules('pywinauto')
        + collect_submodules('PyQt6')
        + [
            'six',
            'flet_desktop', 'flet.utils',
            'email', 'email.message', 'email.mime',
            'http.client', 'widget_ui',
            'sqlite3', '_sqlite3',
        ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'unittest',
        'PySide6', 'rich', 'pygments', 'markdown_it',
        'yaml', 'cryptography', 'cffi', 'pycparser',
        'dateutil', 'arrow', 'tzdata', 'zstandard',
        'pyarmor', 'nuitka', 'PyInstaller',
        'altgraph', 'pefile', 'pywin32_ctypes', 'Cython', 'maturin',
        'chardet', 'click', 'colorama', 'jinja2', 'markupsafe',
        'slugify', 'cookiecutter', 'qrcode', 'watchdog',
        'setuptools', 'pip', 'flet_cli',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WSA Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='assets\\icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WSA Installer',
)
