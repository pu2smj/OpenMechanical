import Part
import FreeCAD as App

class BearingShields:
    def __init__(self, iso_data):
        self.iso = iso_data

    def build_shields(self):
        shield_type = getattr(self.iso, 'shield', 'Open')
        
        if shield_type == 'Open' or not shield_type:
            return []

        try:
            shield_thick = max(0.2, self.iso.B * 0.05)
            r_in = (self.iso.d1 / 2.0) + 0.2
            r_out = (self.iso.D1 / 2.0) - 0.2
            
            if r_in >= r_out:
                return []

            shields = []
            for z in [0.2, self.iso.B - shield_thick - 0.2]:
                try:
                    ocyl = Part.makeCylinder(r_out, shield_thick, App.Vector(0, 0, z))
                    icyl = Part.makeCylinder(r_in, shield_thick, App.Vector(0, 0, z))
                    shields.append(ocyl.cut(icyl))
                except Exception:
                    continue
            
            return shields
        except Exception:
            return []