# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

base = ""
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name="main",
      version="0.1",
      description="",
      executables=[Executable("main.py", base=base)],
      options={"build_exe": {"packages": ["multiprocessing", 'idna']}}
      )
