import Part
import FreeCAD as App

class BearingRings:
    def __init__(self, iso_data):
        self.iso = iso_data

    def _make_base_ring(self, outer_r, inner_r, height, chamfer):
        ocyl = Part.makeCylinder(outer_r, height)
        icyl = Part.makeCylinder(inner_r, height)
        ring = ocyl.cut(icyl)
        
        if 0 < chamfer < (outer_r - inner_r) * 0.4:
            edges = []
            for e in ring.Edges:
                try:
                    if hasattr(e, 'Curve') and hasattr(e.Curve, 'Center'):
                        z_center = e.Curve.Center.z
                        if abs(z_center) < 1e-3 or abs(z_center - height) < 1e-3:
                            edges.append(e)
                except Exception:
                    continue
            
            if edges:
                try:
                    ring = ring.makeChamfer(min(chamfer, 0.5), edges)
                except Exception:
                    pass
        return ring

    def build_inner_ring(self):
        base = self._make_base_ring(self.iso.d1/2.0, self.iso.d/2.0, self.iso.B, self.iso.rmin)
        groove_r = self.iso.ball_diameter * 0.55
        if (self.iso.d1 - self.iso.d) > groove_r * 1.5:
            torus = Part.makeTorus(self.iso.dm / 2.0, groove_r)
            torus.translate(App.Vector(0, 0, self.iso.B / 2.0))
            return base.cut(torus)
        return base

    def build_outer_ring(self):
        base = self._make_base_ring(self.iso.D/2.0, self.iso.D1/2.0, self.iso.B, self.iso.rmin)
        groove_r = self.iso.ball_diameter * 0.55
        if (self.iso.D - self.iso.D1) > groove_r * 1.5:
            torus = Part.makeTorus(self.iso.dm / 2.0, groove_r)
            torus.translate(App.Vector(0, 0, self.iso.B / 2.0))
            return base.cut(torus)
        return base