# -*- coding: utf-8 -*-

# ORingGeometry.py
# Geração do toro paramétrico a partir dos dados do o-ring.
# Geometria: toro com raio médio (major_radius) e seção (minor_radius).

import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

import FreeCAD as App
import Part
from ORingUtils import ORingUtils


class ORingGeometry:
    def __init__(self, ring_record):
        self.ring = ring_record

    def build_torus(self):
        return Part.makeTorus(self.ring.major_radius, self.ring.minor_radius)

    def generate(self):
        App.Console.PrintMessage(f"OpenMechanical: Gerando o-ring {self.ring.key}\n")

        try:
            doc = App.activeDocument() or App.newDocument(f"ORing_{self.ring.key}")
        except Exception:
            doc = App.newDocument(f"ORing_{self.ring.key}")

        container = doc.addObject("App::Part", f"ORing_{self.ring.key}")

        try:
            torus = self.build_torus()
            obj = doc.addObject("Part::Feature", "ORingTorus")
            obj.Shape = torus
            container.addObject(obj)
            App.Console.PrintMessage("OpenMechanical: Toro do o-ring criado com sucesso\n")
        except Exception as e:
            App.Console.PrintError(f"OpenMechanical: Erro ao criar toro do o-ring: {str(e)}\n")

        try:
            doc.recompute()
        except Exception:
            pass

        try:
            ORingUtils.set_color(obj)
        except Exception:
            pass

        try:
            ORingUtils.apply_display_mode(container, "Flat Lines")
        except Exception:
            pass

        App.Console.PrintMessage(f"OpenMechanical: O-ring {self.ring.key} gerado com sucesso!\n")
        return container
