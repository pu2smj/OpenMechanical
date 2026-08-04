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
    def set_color(obj):
        try:
            if hasattr(obj, "ViewObject") and obj.ViewObject:
                obj.ViewObject.ShapeColor = (0.10, 0.10, 0.10)
        except Exception:
            pass
