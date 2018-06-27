# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable

setup(name = "main" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("main.py")],
      options={"build_exe": {"packages": ["multiprocessing", 'idna']}}
)
