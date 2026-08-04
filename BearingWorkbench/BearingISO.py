import json
import os
from math import pi

class BearingISO:
    def __init__(self, designation, json_filename="bearing_data.json"):
        self.designation = designation
        self.d = None
        self.D = None
        self.B = None
        self.ball_diameter = None
        self.number_of_balls = None
        self.rmin = None
        self.shield = "Open"
        self.family = "DeepGroove"
        self.standard = "ISO15"
        self.cage = "Steel"
        self.clearance = "CN"
        
        self._load_data(json_filename)
        self._calculate_internal_params()

    def _load_data(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if self.designation in data:
            bearing = data[self.designation]
            dims = bearing["dimensions"]
            self.d = float(dims["d"])
            self.D = float(dims["D"])
            self.B = float(dims["B"])
            self.ball_diameter = float(bearing["ball_diameter"])
            self.number_of_balls = int(bearing["balls"])
            self.rmin = float(bearing["rmin"])
            self.shield = bearing.get("shield", "Open")
            self.family = bearing.get("family", "DeepGroove")
            self.standard = bearing.get("standard", "ISO15")
            self.cage = bearing.get("cage", "Steel")
            self.clearance = bearing.get("clearance", "CN")
            return
                
        raise ValueError(f"Rolamento '{self.designation}' não encontrado na base de dados.")

    def _calculate_internal_params(self):
        self.dm = (self.d + self.D) / 2.0
        radial_space = (self.D - self.d) / 2.0
        
        if self.ball_diameter is None or self.number_of_balls is None:
            if self.D <= 10:
                scale_factor, max_ball_ratio = 0.20, 0.70
            elif self.D <= 20:
                scale_factor, max_ball_ratio = 0.22, 0.75
            elif self.D <= 50:
                scale_factor, max_ball_ratio = 0.26, 0.80
            else:
                scale_factor, max_ball_ratio = 0.28, 0.85

            db = min(scale_factor * (self.D - self.d), max_ball_ratio * self.B)
            self.ball_diameter = max(min(db, 0.9 * self.B), 0.5)
            
            if self.ball_diameter > 0:
                nb = max(4, int(pi * self.dm / (self.ball_diameter * 2.0)))
                self.number_of_balls = min(nb, 14 if self.D > 50 else 10)
            else:
                self.number_of_balls = 6
        
        min_wall = max(0.3, self.ball_diameter * 0.12)
        self.d1 = self.d + min_wall + (radial_space - min_wall) * 0.55
        self.D1 = self.D - min_wall - (radial_space - min_wall) * 0.55