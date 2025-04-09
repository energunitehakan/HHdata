# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/max_demand_calculator/run.py'],
    pathex=[],
    binaries=[],
    datas=[('src/max_demand_calculator/assets', 'src/max_demand_calculator/assets')],
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
    name='MaxDemandCalculator',
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
app = BUNDLE(
    exe,
    name='MaxDemandCalculator.app',
    icon=None,
    bundle_identifier=None,
)
