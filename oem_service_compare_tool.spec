# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['source/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('input/*', 'input'),
        ('output/*', 'output'),
        ('logs/*', 'logs'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='oem_service_compare_tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='oem_service_compare_tool'
)
