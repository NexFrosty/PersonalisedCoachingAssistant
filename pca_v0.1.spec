# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

_data = [
	('E:\\akaruiyami\\documents\\p001\\python 3.10\\assingments\\personalisedcoachingassistant\\lib\\site-packages\\customtkinter\\', 'customtkinter/'),
	('E:\\AkaruiYami\\Documents\\P001\Python 3.10\\Assingments\\PersonalisedCoachingAssistant\\src\\assets\\', 'assets/'),
	('E:\\AkaruiYami\\Documents\\P001\\Python 3.10\\Assingments\\PersonalisedCoachingAssistant\\src\\data\\', 'data/'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pca_v0.1',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pca_v0.1',
)
