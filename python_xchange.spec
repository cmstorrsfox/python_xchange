# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['python_xchange.py'],
             pathex=['C:\\Users\\storr\\Documents\\0_coding\\python_xchange'],
             binaries=[],
             datas=[('C:\\Users\\storr\\Documents\\0_coding\\python_xchange\\NASDAQ.txt', '.')],
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
          name='python_xchange',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='stock.ico')
