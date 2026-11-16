# -*- coding: utf-8 -*-
"""贵阳生活 100 题的 C++ 参考答案（源码在 tools/gen/guiyang_100.py 中统一维护）。"""
import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_GEN = os.path.join(os.path.dirname(_HERE), "gen", "guiyang_100.py")
_spec = importlib.util.spec_from_file_location("guiyang_100_gen", _GEN)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

SOL = dict(_mod.SOL)
