# OpenMechanical Workbench — Translation System

This directory contains the internationalization (i18n) system for the
**OpenMechanical** FreeCAD workbench, based on the Qt `.ts`/`.qm` format —
the standard used by all FreeCAD workbenches.

## Files

| File                          | Description                                         |
|-------------------------------|------------------------------------------------------|
| `OpenMechanical.ts`           | Master template with all source strings             |
| `OpenMechanical_en.ts`        | English translation (default language)              |
| `OpenMechanical_pt-BR.ts`     | Brazilian Portuguese translation                    |
| `OpenMechanical_<locale>.ts`  | Translation for another language                    |
| `OpenMechanical_<locale>.qm`| Compiled binary loaded at runtime                   |
| `compile_translations.py`     | Compiles `.ts` → `.qm` with `lrelease`              |
| `update_translations.py`      | Extracts strings from source with `lupdate`         |
| `TRANSLATION_GUIDE.txt`       | Step-by-step guide for translators                  |

## Quick Start

For detailed instructions, see **`TRANSLATION_GUIDE.txt`** in this directory.
Summary:

1. **Extract strings** — `python compile_translations.py` (runs `lupdate`)
2. **Translate** — open the `.ts` file in Qt Linguist and fill in translations
3. **Compile** — `lrelease OpenMechanical_<locale>.ts` → generates `.qm`
4. The `.qm` file is automatically loaded by `load_translations()` in
   `OpenMechanicalWorkbench.py` based on the system locale.

## Adding a New Language

1. Copy `OpenMechanical.ts` → `OpenMechanical_<locale>.ts`
2. Open in Qt Linguist and translate all strings
3. Compile to `.qm`
4. Place the `.qm` file in `Resources/translations/`

## Translation Loading

Translations are loaded at workbench initialization via `load_translations()`
in `OpenMechanicalWorkbench.py`:

```python
def Initialize(self):
    load_translations()
    # ... rest of initialization
```

The loader detects the system locale and attempts to load
`OpenMechanical_<locale>.qm` from the translations directory.