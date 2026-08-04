# BearingWorkbench

**Status**: Fully implemented and stable (version 1.000)

This is the most complete library in OpenMechanical. It provides parametric
generation of **deep groove ball bearings** following ISO 15 dimensional standards.

## Features

- **Deep groove bearings** — ISO 15 data (`bearing_data.json`)
- **Shields** — Z / ZZ (metal shields)
- **Seals** — RS / 2RS (rubber seals)
- Support for both PySide2 (FreeCAD 0.19) and PySide6 (FreeCAD 1.x)

## Architecture

| File                          | Responsibility                          |
|-------------------------------|------------------------------------------|
| `bearing_data.json`           | Engineering data source (ISO 15)        |
| `BearingISO.py`               | ISO standard definitions and validation |
| `BearingRings.py`             | Inner/outer ring geometry               |
| `BearingBalls.py`             | Ball geometry                           |
| `BearingShields.py`           | Shield/seal geometry                    |
| `BearingGeometry.py`          | Complete bearing assembly               |
| `BearingUtils.py`             | Display utilities (colors, modes)       |
| `BearingGui.py`               | FreeCAD GUI integration                 |
| `BearingSelectionDialog.py`   | Component picker dialog                 |
| `main.py`                     | Entry point and `Bearing` class API     |

## Usage (Python API)

```python
from BearingWorkbench.main import Bearing

b = Bearing("608ZZ")
print(b.d, b.D, b.ball_diameter)
b.build()
```

## Usage (FreeCAD GUI)

Load the "Open Mechanical" workbench and click the **Bearing** command — a
selection dialog opens, allowing you to pick from all bearing sizes in the
ISO 15 dataset.
