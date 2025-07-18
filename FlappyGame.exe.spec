# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/home/keith123/Flappy-Game/windows/../game/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/keith123/Flappy-Game/windows/../assets', 'assets'), ('/home/keith123/Flappy-Game/windows/../game', 'game')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlappyGame.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
