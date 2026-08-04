import FreeCADGui as Gui

class BearingUtils:
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
    def set_colors(inner_obj, outer_obj, shield_objs=None):
        try:
            if hasattr(inner_obj, "ViewObject") and inner_obj.ViewObject:
                inner_obj.ViewObject.ShapeColor = (0.85, 0.85, 0.88)
        except Exception:
            pass
        try:
            if hasattr(outer_obj, "ViewObject") and outer_obj.ViewObject:
                outer_obj.ViewObject.ShapeColor = (0.70, 0.70, 0.75)
        except Exception:
            pass
        if shield_objs:
            for s in shield_objs:
                try:
                    if hasattr(s, "ViewObject") and s.ViewObject:
                        s.ViewObject.ShapeColor = (0.2, 0.2, 0.2)
                except Exception:
                    pass