# -*- coding: utf-8 -*-

# ORingUtils.py
# Utilitários de exibição para a ORingWorkbench.

import FreeCADGui as Gui


class ORingUtils:
    @staticmethod
    def apply_display_mode(part_obj, mode="Flat Lines"):
        """Trata DisplayMode com segurança para instâncias App::Part."""
        try:
            if not Gui.activeDocument():
                return

            gui_obj = Gui.activeDocument().getObject(part_obj.Name)
            if gui_obj is None:
                return

            if hasattr(gui_obj, "listDisplayModes"):
                modes = gui_obj.listDisplayModes()
                if mode in modes:
                    gui_obj.DisplayMode = mode
                elif "Shaded" in modes:
                    gui_obj.DisplayMode = "Shaded"
        except Exception:
            pass

    @staticmethod
    def set_color(obj, color_name=""):
        """Aplica cor ao objeto com base no nome da cor."""
        color_map = {
            "Black": (0.10, 0.10, 0.10),
            "White": (0.90, 0.90, 0.90),
            "Red": (0.80, 0.10, 0.10),
            "Green": (0.10, 0.70, 0.10),
            "Brown": (0.55, 0.35, 0.15),
            "Blue": (0.10, 0.30, 0.80),
        }
        try:
            if hasattr(obj, "ViewObject") and obj.ViewObject:
                rgb = color_map.get(color_name.strip(), (0.10, 0.10, 0.10))
                obj.ViewObject.ShapeColor = rgb
        except Exception:
            pass
