from math import pi, sin, cos
import Part
import FreeCAD as App

class BearingBalls:
    def __init__(self, iso_data):
        self.iso = iso_data

    def build_balls(self):
        balls = []
        
        if not hasattr(self.iso, 'ball_diameter') or self.iso.ball_diameter is None:
            return balls
            
        try:
            pcd = self.iso.dm / 2.0
            r_ball = self.iso.ball_diameter / 2.0
            num_balls = getattr(self.iso, 'number_of_balls', 6)
            
            for i in range(num_balls):
                try:
                    angle = 2 * pi * i / num_balls
                    pos = App.Vector(pcd * cos(angle), pcd * sin(angle), self.iso.B / 2.0)
                    sphere = Part.makeSphere(r_ball, pos)
                    balls.append(sphere)
                except Exception:
                    continue
        except Exception:
            pass
            
        return balls