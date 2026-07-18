# Architecture and Design

Architecture and design testing confirms the code's structure supports change instead of resisting it. A system can be locally correct and still be architecturally unsound, which shows up later as every small change requiring edits in a dozen unrelated files.

## What to test

- SOLID compliance
  - Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.

- Coupling and cohesion
  - Modules depend on stable abstractions, not on each other's internals.
  - Related behavior lives together; unrelated behavior is not forced into the same module.

- Layering
  - Dependencies flow in one direction (e.g., presentation depends on domain, not the reverse).

- Circular dependencies
  - No module-level or package-level import cycles.

- Abstraction integrity
  - Interfaces do not leak implementation detail to callers.

- God objects and inappropriate intimacy
  - No single class or module accumulates unrelated responsibilities.
  - Modules do not reach into each other's private state.

- API design and compatibility
  - Public APIs are versioned deliberately; breaking changes are explicit, not incidental.

- Threat modeling
  - Architecture is evaluated for security gaps before code is written: trust boundaries, data flow, and privilege boundaries are diagrammed and reviewed against a threat framework (e.g., STRIDE).

## Why it matters

Architectural decay is gradual and rarely shows up in a single code review. Left unchecked, it turns every feature into a cross-cutting change and every fix into a risk of unrelated breakage. Architecture tests catch the trend before it becomes a rewrite.

---

## DPPF architecture and design test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| ARC-001 | Single responsibility conformance | Each class or module has one reason to change and one clearly stated responsibility | God classes accumulating unrelated logic, changes to unrelated features requiring edits to the same file | SOLID: Single Responsibility Principle | Review |
| ARC-002 | Open/closed extensibility | New behavior can be added by extension (new implementation, new case) without modifying existing, tested code paths | Fragile modification of stable code to add unrelated behavior, regressions introduced by feature additions | SOLID: Open/Closed Principle | Review |
| ARC-003 | Liskov substitution safety | Subtypes can be used anywhere their base type is expected without altering the correctness of the caller | Subclasses that violate base-class contracts, runtime type-check workarounds signaling a broken hierarchy | SOLID: Liskov Substitution Principle | Review |
| ARC-004 | Interface segregation | Interfaces expose only the methods a given client actually needs, rather than one large interface all clients depend on | Fat interfaces forcing unrelated implementations, unnecessary coupling from unused methods | SOLID: Interface Segregation Principle | Review |
| ARC-005 | Dependency inversion | High-level modules depend on abstractions, not on concrete low-level implementations | Tight coupling to concrete implementations, untestable code that cannot be mocked, framework lock-in | SOLID: Dependency Inversion Principle | Review |
| ARC-006 | Coupling bound | Modules interact through stable, minimal public interfaces rather than reaching into each other's internals or shared mutable globals | Change amplification where a small edit ripples across unrelated modules, tight coupling that blocks independent deployment | ISO/IEC 25010 Maintainability | Review |
| ARC-007 | Cohesion strength | Code within a module is functionally related; unrelated concerns are not co-located for convenience | Low-cohesion modules that are hard to name, test, or reuse independently | ISO/IEC 25010 Maintainability | Review |
| ARC-008 | Layering direction consistency | Dependencies between architectural layers flow in one agreed direction with no layer skipping or reverse dependency | Presentation logic leaking into domain logic, data-access code called directly from UI, layer violations that block independent testing | ISO/IEC 25010 Maintainability | Review |
| ARC-009 | Circular dependency absence | No import or dependency cycle exists between modules or packages | Build order fragility, inability to test modules in isolation, cascading initialization bugs | ISO/IEC 25010 Maintainability | Review, CI |
| ARC-010 | Abstraction leak prevention | Public interfaces and APIs do not expose internal implementation types, storage details, or framework-specific objects to callers | Callers coupling to internal detail that then blocks refactoring, breaking changes triggered by unrelated internal changes | ISO/IEC 25010 Maintainability | Review |
| ARC-011 | Inappropriate intimacy absence | Modules do not access each other's private fields, internal state, or undocumented behavior | Hidden coupling that breaks silently when the depended-on internals change, tests that pass only by accident | ISO/IEC 25010 Maintainability | Review |
| ARC-012 | API backward compatibility | Public API changes follow semantic versioning; breaking changes are deliberate, documented, and version-bumped, not incidental | Silent breaking changes to consumers, downstream integration failures after a routine release | Semantic Versioning (SemVer) | Review, Pre-deployment |
| ARC-013 | Threat modeling coverage | Every new service or significant architecture change has a documented threat model (trust boundaries, data flow, privilege boundaries) reviewed before implementation begins | Security gaps baked into the architecture that no amount of later code-level testing can fully compensate for, late discovery of a design-level flaw after implementation is complete | STRIDE, OWASP Threat Modeling, ISO/IEC 25010 Security | Planning, Design |
| ARC-014 | Code provenance and non-infringement review | Verbatim code blocks copied from an external source (Stack Overflow, another repository, an AI assistant trained on licensed code) are reviewed for license compatibility and attribution before merge; zero unreviewed verbatim blocks from an incompatible-license or unattributed source | Undisclosed license violation discovered during a buyer's or investor's legal due diligence, copied code carrying an incompatible license obligation into a proprietary or commercial codebase | Copyright and open-source license compliance practice | Review |
