import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

import json
from BearingSelectionDialog import select_bearing as _select_bearing

class BearingGui:
    @staticmethod
    def select_bearing(json_filename="bearing_data.json"):
        return _select_bearing(json_filename)