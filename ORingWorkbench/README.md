# ORingWorkbench

**Status**: Fully implemented and stable (version 1.000)

This is the second most complete library in OpenMechanical. It provides
parametric generation of **O-rings** as torus geometry, driven entirely by
data from four normalized CSV files.

## Features

- **Parametric torus geometry** from data-driven parameters
- **AS 568 standard sizes** (inch + mm equivalents) — `o-ring_pol.csv`
- **Metric sizes** — `o-ring_mm.csv`
- **Manufacturer reference cross-reference** — `brand.csv`
- **Material catalog** (polymer / hardness / temperature / available colors) — `material.csv`
- **Component color selection** — choose the O-ring color based on material (e.g., Viton: Black, Green, Red)
- Support for both PySide2 (FreeCAD 0.19) and PySide6 (FreeCAD 1.x)

## Architecture

| File                          | Responsibility                          |
|-------------------------------|------------------------------------------|
| `o-ring_pol.csv`              | AS568 standard sizes (001–475)          |
| `o-ring_mm.csv`               | Metric sizes                            |
| `brand.csv`                   | Manufacturer reference                  |
| `material.csv`                | Material catalog (incl. available colors) |
| `ORingData.py`                | Loads CSVs + validation                 |
| `ORingGeometry.py`            | Torus geometry generation               |
| `ORingUtils.py`               | Display utilities                       |
| `ORingGui.py`                 | FreeCAD GUI integration                 |
| `ORingSelectionDialog.py`     | Component picker dialog                 |
| `main.py`                     | Entry point and `ORing` class API       |

## Usage (Python API)

```python
from ORingWorkbench.main import ORing

# Without color (defaults to black)
ring = ORing("Parker|2001")
print(ring.di, ring.w, ring.de)
ring.build()

# With color selection
ring = ORing("Parker|2001", color="Red")
ring.build()
```

## Usage (FreeCAD GUI)

Load the "Open Mechanical" workbench and click the **O-Ring** command — a
selection dialog opens, allowing you to pick from all standard sizes and
manufacturer references. A **color selector** appears based on the material's
available colors (e.g., Viton offers Black, Green, Red).
