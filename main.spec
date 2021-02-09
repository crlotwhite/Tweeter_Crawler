# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
pf_foldr = 'C:\\ProgramData\\Anaconda3\\Library\\plugins\\platforms\\'

a = Analysis(['main.py'],
             pathex=['C:\\Users\\tama0\\Documents\\Git\\TweeterCrwaler'],
             binaries=[(pf_foldr+'qwindows.dll', '.'),
             (pf_foldr+'qdirect2d.dll', '.'),
             (pf_foldr+'qoffscreen.dll', '.'),
             (pf_foldr+'qminimal.dll', '.')
             ],
             datas=[('main.ui', '.'), ('imgview.ui', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='python.ico')
