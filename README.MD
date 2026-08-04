# OpenMechanical

An Open Source Parametric Mechanical Component Library for FreeCAD
License: MIT | Python | FreeCAD 0.19+ (supports 1.x)

________________________________________

## Mission

OpenMechanical is an open-source project dedicated to providing a professional, parametric library of standardized mechanical components for FreeCAD.
More than generating 3D models, the project aims to make engineering knowledge reusable, verifiable and accessible to everyone.
Our goal is simple:
Give engineers back the time to engineer.

________________________________________

## Why?

Mechanical engineers spend countless hours searching for manufacturer models, downloading STEP files, simplifying geometry or redrawing standard components.
These activities add little engineering value.
Standardized components should already exist inside the CAD environment, allowing engineers to focus on what really matters:

- Designing
- Innovating
- Validating
- Building better products

If engineers solve the same standard problem twice, it belongs in a library.

________________________________________

## Project Philosophy

OpenMechanical follows one fundamental principle:
If engineers solve the same standard problem twice, it belongs in a library.

Engineering knowledge should be shared — not recreated.

________________________________________

## Engineering First

This project follows an Engineering First philosophy.
Every component is developed using the following workflow:

```
Engineering Standards -> Technical Data -> Parametric Definition -> Geometry Generation
```

Geometry is the consequence of engineering data — not the other way around.
Every dimension must have a documented technical reference (ISO/DIN/ANSI standard or manufacturer catalog).
Data and geometry remain independent: the same engineering database can serve different CAD systems.

________________________________________

## Core Principles

- Standards before geometry.
- Parametric models instead of static STEP files.
- Technical data must always have a documented source.
- Data and geometry remain independent.
- Modular architecture.
- Community-driven development.
- Open documentation.
- Automated validation whenever possible.
- Clean and maintainable code.

________________________________________

## Current Libraries

| Library | Status | Details |
|---------|--------|---------|
| **Bearings** | Fully parametric, data-driven | Deep groove bearings, ISO 15 database, shields (Z/ZZ), seals (RS/2RS), component selection dialog |
| **O-Rings** | Parametric, data-driven | 4 normalized CSVs (`o-ring_pol.csv` AS568 inch+mm, `o-ring_mm.csv` metric, `brand.csv` manufacturer refs, `material.csv`); torus geometry; selection dialog with filters |
| **Bushings** | Placeholder | Hardcoded geometry pending data-driven implementation |
| **Couplings** | Placeholder | Hardcoded geometry pending data-driven implementation |
| **Seals** | Placeholder | Hardcoded geometry pending data-driven implementation |

Bushing, Coupling and Seal currently generate placeholder geometry from `OpenMechanicalWorkbench.py`. These are temporary and will be replaced by parametric, data-driven libraries.

________________________________________

## Vision

OpenMechanical builds an ecosystem of open mechanical libraries for FreeCAD.
Future libraries may include:

- O-Rings
- Oil Seals
- Circlips
- Bushings
- Keys
- Springs
- Couplings
- Pulleys
- Gears
- Shafts

All sharing the same architecture and engineering philosophy.

________________________________________

## Roadmap

Version 0.1
- Deep Groove Bearings
- ISO 15 database
- Parametric geometry
- Basic FreeCAD integration

Version 0.2
- Metal Shields (Z / ZZ)
- Rubber Seals (RS / 2RS)
- Improved raceway geometry

Version 0.3
- Angular Contact Bearings

Version 0.4
- Needle Bearings

Version 0.5
- Thrust Bearings

Version 0.6
- Self-Aligning Bearings

Version 0.7
- O-Rings (data-driven, ISO 3601 / AS568) — implemented
- Component selection dialog for O-Rings

Version 0.8
- Bushings (data-driven)

Version 0.9
- Couplings (data-driven)

Version 1.0
- Complete FreeCAD Workbench
- Component Browser
- Dynamic Preview
- STEP/STL Export
- BOM Support

________________________________________

## Installation

### Via Addon Manager (recommended)

1. Open FreeCAD.
2. Tools → Addon Manager.
3. Install **OpenMechanical** from the workbenches list.

### Manual

Copy the `OpenMechanical` folder to your FreeCAD `Mod` directory:
- Linux: `~/.local/share/FreeCAD/Mod/OpenMechanical`
- Windows: `%APPDATA%\FreeCAD\Mod\OpenMechanical`
- macOS: `~/Library/Preferences/FreeCAD/Mod/OpenMechanical`

Restart FreeCAD and select the **Open Mechanical** workbench.

________________________________________

## Usage

### FreeCAD GUI

Select the **Open Mechanical** workbench. The toolbar/menu exposes:

- **Bearing** — opens the component selection dialog and builds the chosen bearing
- **Bushing** — placeholder geometry
- **Coupling** — placeholder geometry
- **O-Ring** — opens the component selection dialog and builds the chosen o-ring
- **Seal** — placeholder geometry

### Python API

```python
# BearingWorkbench
from BearingWorkbench.main import Bearing

b = Bearing("608ZZ")
print(b.d, b.D, b.ball_diameter)
b.build()

# ORingWorkbench
from ORingWorkbench.main import ORing

ring = ORing("Parker|2001")
print(ring.di, ring.w, ring.de)
ring.build()
```

________________________________________

## Documentation

- `ENGINEERING_PRINCIPLES.md` — design principles (read first)
- `MANIFESTO.md` — project philosophy
- `docs/user_guide.md.txt` — user guide (TODO)

________________________________________

## Open Engineering

This project is not only about CAD models.
It is about sharing engineering knowledge.
Every contribution helps:

- Improve engineering quality.
- Reduce repetitive work.
- Create reusable mechanical standards.
- Make FreeCAD even better.

Whether you contribute with:

- Code
- Documentation
- Technical validation
- Standards
- Testing
- Ideas

you are helping the entire engineering community.

________________________________________

## Long-Term Goal

Our ambition is simple.
We want engineers to stop searching for standard components and start engineering.
Model the design, not the standard parts.

________________________________________

## Acknowledgements

This project was born from a simple observation shared by many mechanical designers:
Finding a standard bearing model that truly fits a project often takes longer than it should.
Rather than repeatedly searching, adapting and redrawing the same standard components, we chose to build an open library that anyone can use, improve and share.
If this project saves even a few hours of engineering work for someone else, it has already fulfilled its purpose.

________________________________________

## License

This project is released under the MIT License.

________________________________________

## Welcome!

OpenMechanical is an open community project.
Whether you are a mechanical engineer, software developer, FreeCAD user, student or simply someone passionate about engineering, you are invited to contribute.
Together we can build the open mechanical library that engineers have been waiting for.
