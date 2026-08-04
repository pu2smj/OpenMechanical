# ENGINEERING_PRINCIPLES.md

# Engineering Principles

OpenBearingWorkbench is an engineering project before it is a software project.

These principles define how the project evolves and should guide every design decision, contribution and discussion.

---

## 1. Engineering First

Engineering data always comes before geometry.

Geometry is generated from verified engineering data.

Never the opposite.

---

## 2. Standards Before Implementation

Whenever an international standard exists (ISO, DIN, ANSI, ABNT, JIS, etc.), it shall be the primary reference.

The implementation must follow the standard—not the implementation convenience.

---

## 3. Every Dimension Has a Source

No engineering dimension shall be introduced without a documented technical reference.

Accepted sources include:

* International standards
* Manufacturer catalogues
* Technical manuals
* Peer-reviewed publications

Approximations must always be explicitly identified.

---

## 4. Parametric by Design

Every component should be generated from parameters.

Static geometry is considered a final representation—not the source of truth.

---

## 5. Data and Geometry Must Remain Independent

Engineering data shall never depend on CAD implementation.

The same engineering database should be usable by different CAD systems.

---

## 6. Simplicity Before Complexity

The simplest correct solution is preferred.

Complexity should only be introduced when it provides measurable engineering value.

---

## 7. Modular Architecture

Every subsystem should have a single responsibility.

Modules should be replaceable without affecting the remaining architecture.

---

## 8. Community Driven

Engineering discussions are encouraged.

Technical decisions should be based on documented evidence rather than individual preference.

---

## 9. Documentation Is Part of the Project

Code without documentation is incomplete.

Every significant feature should include:

* Documentation
* Examples
* References
* Validation

---

## 10. Validation Before Release

Every new component must be validated before becoming part of the official library.

Validation includes:

* Dimensional verification
* Parametric verification
* Geometry validation
* Regression testing

---

## 11. Open Engineering

Knowledge grows when shared.

This project exists to reduce repetitive engineering work and make standardized mechanical components accessible to everyone.

---

> **Engineering knowledge should be shared—not recreated.**

> **If engineers solve the same standard problem twice, it belongs in a library.**
