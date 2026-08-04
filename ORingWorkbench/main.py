# -*- coding: utf-8 -*-

# main.py
# Ponto de entrada e API pública da ORingWorkbench.

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from ORingData import ORingData
from ORingGeometry import ORingGeometry


class ORing:
    def __init__(self, key, data_dir=None):
        self.data = ORingData(data_dir)
        self.record = self.data.get_record(key)
        self.key = self.record.key
        self.di = self.record.di_interno
        self.w = self.record.secao_w
        self.de = self.record.de_externo
        self.material = self.record.material
        self.polimero = self.record.polimero
        self.catalogo = self.record.catalogo
        self.codigo = self.record.codigo
        self.tabela = self.record.tabela

    def build(self):
        builder = ORingGeometry(self.record)
        return builder.generate()


# ==========================================
# EXECUÇÃO DO SCRIPT
# ==========================================
if __name__ == "__main__":
    from ORingSelectionDialog import select_oring

    selected_key = select_oring()
    if selected_key:
        ring = ORing(selected_key)
        ring.build()
