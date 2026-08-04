import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from BearingISO import BearingISO
from BearingGeometry import BearingGeometry
from BearingSelectionDialog import select_bearing

class Bearing:
    def __init__(self, designation):
        self.iso = BearingISO(designation)
        self.d = self.iso.d
        self.D = self.iso.D
        self.B = self.iso.B
        self.ball_diameter = self.iso.ball_diameter
        self.number_of_balls = self.iso.number_of_balls
        self.rmin = self.iso.rmin
        self.shield = self.iso.shield
        self.family = self.iso.family
        self.standard = self.iso.standard

    def build(self):
        builder = BearingGeometry(self.iso)
        return builder.generate()

# ==========================================
# EXECUÇÃO DO SCRIPT
# ==========================================
if __name__ == "__main__":
    selected_model = select_bearing()
    if selected_model:
        bearing = Bearing(selected_model)
        bearing.build()