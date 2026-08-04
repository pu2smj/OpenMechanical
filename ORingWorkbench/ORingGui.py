# -*- coding: utf-8 -*-

# ORingGui.py
# Integração GUI da ORingWorkbench.

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from ORingSelectionDialog import select_oring as _select_oring


class ORingGui:
    @staticmethod
    def select_oring(data_dir=None):
        return _select_oring(data_dir)
