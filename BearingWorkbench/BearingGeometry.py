import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

import FreeCAD as App
from BearingRings import BearingRings
from BearingBalls import BearingBalls
from BearingShields import BearingShields
from BearingUtils import BearingUtils

class BearingGeometry:
    def __init__(self, iso_data):
        self.iso = iso_data

    def generate(self):
        App.Console.PrintMessage(f"OpenMechanical: Gerando rolamento {self.iso.designation}\n")
        
        try:
            doc = App.activeDocument() or App.newDocument(f"Bearing_{self.iso.designation}")
        except Exception:
            doc = App.newDocument(f"Bearing_{self.iso.designation}")
        
        container = doc.addObject("App::Part", f"Bearing_{self.iso.designation}")

        rings = BearingRings(self.iso)
        balls_builder = BearingBalls(self.iso)
        shields_builder = BearingShields(self.iso)

        inner_obj = None
        outer_obj = None
        shield_objs = []

        try:
            App.Console.PrintMessage("OpenMechanical: Criando anel interno...\n")
            inner_shape = rings.build_inner_ring()
            inner_obj = doc.addObject("Part::Feature", "InnerRing")
            inner_obj.Shape = inner_shape
            container.addObject(inner_obj)
            App.Console.PrintMessage("OpenMechanical: Anel interno criado com sucesso\n")
        except Exception as e:
            App.Console.PrintError(f"OpenMechanical: Erro ao criar anel interno: {str(e)}\n")

        try:
            App.Console.PrintMessage("OpenMechanical: Criando anel externo...\n")
            outer_shape = rings.build_outer_ring()
            outer_obj = doc.addObject("Part::Feature", "OuterRing")
            outer_obj.Shape = outer_shape
            container.addObject(outer_obj)
            App.Console.PrintMessage("OpenMechanical: Anel externo criado com sucesso\n")
        except Exception as e:
            App.Console.PrintError(f"OpenMechanical: Erro ao criar anel externo: {str(e)}\n")

        try:
            App.Console.PrintMessage(f"OpenMechanical: Criando {self.iso.number_of_balls} esferas...\n")
            balls = balls_builder.build_balls()
            for i, shape in enumerate(balls):
                ball_obj = doc.addObject("Part::Feature", f"Ball_{i+1:02d}")
                ball_obj.Shape = shape
                container.addObject(ball_obj)
            App.Console.PrintMessage("OpenMechanical: Esferas criadas com sucesso\n")
        except Exception as e:
            App.Console.PrintError(f"OpenMechanical: Erro ao criar esferas: {str(e)}\n")

        try:
            App.Console.PrintMessage("OpenMechanical: Criando shields...\n")
            shields = shields_builder.build_shields()
            for i, shape in enumerate(shields):
                s_obj = doc.addObject("Part::Feature", f"Shield_{i+1:02d}")
                s_obj.Shape = shape
                container.addObject(s_obj)
                shield_objs.append(s_obj)
            App.Console.PrintMessage(f"OpenMechanical: {len(shield_objs)} shields criados\n")
        except Exception as e:
            App.Console.PrintError(f"OpenMechanical: Erro ao criar shields: {str(e)}\n")

        try:
            doc.recompute()
        except Exception:
            pass
        
        try:
            BearingUtils.set_colors(inner_obj, outer_obj, shield_objs)
        except Exception:
            pass
        
        try:
            BearingUtils.apply_display_mode(container, "Flat Lines")
        except Exception:
            pass

        App.Console.PrintMessage(f"OpenMechanical: Rolamento {self.iso.designation} gerado com sucesso!\n")
        return container
