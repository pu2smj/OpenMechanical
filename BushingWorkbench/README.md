# BushingWorkbench

**Status**: Placeholder — not yet implemented.

This directory is reserved for a future data-driven, parametric bushing library
following the same engineering-first principles as `BearingWorkbench/` and
`ORingWorkbench/`.

## Current State

The bushing command in `OpenMechanicalWorkbench.py` (`make_bushing()`) currently
uses placeholder geometry (a simple cylinder with a hole). This will be replaced
when the `BushingWorkbench` library is implemented.

## Planned Direction

- Data source: ISO 281 (rolling bearings) or relevant bushing standards
- Follow the same modular pattern as `BearingWorkbench/`
- Generate geometry from parameters, not the other way around
