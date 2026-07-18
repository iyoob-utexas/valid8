# Correctness and Logic

Correctness testing confirms the code does what it claims to do across the full input space, not just the inputs the author happened to try.

## What to test

- Edge cases and boundaries
  - Empty inputs, single-element inputs, maximum-size inputs.
  - Off-by-one conditions on loops, array indices, and range checks.

- Null and undefined handling
  - Every code path that can receive a null, undefined, or missing value is checked before use.
  - Optional fields and nullable types are handled explicitly, not by accident.

- Type coercion and conversion
  - Implicit type coercion does not silently change comparison or arithmetic outcomes.
  - Numeric precision, rounding, and overflow are handled deliberately.

- Control flow and error propagation
  - Every branch (if/else, switch, exception handler) is reachable and does the right thing.
  - Errors are not swallowed; they propagate to a handler that can act on them.

- Concurrency correctness
  - Shared mutable state is protected against race conditions.
  - Ordering assumptions between async operations are explicit, not implicit.

- Algorithm correctness
  - The implemented algorithm matches its specification, including on adversarial or degenerate inputs.

- Requirement validation
  - Business logic requirements are reviewed for clarity, edge-case completeness, and testability before code is written, not discovered as ambiguity during implementation.

## Why it matters

A change can build, lint clean, and pass a shallow test suite while still producing the wrong answer on realistic input. Correctness testing is the layer that catches logic defects before they reach users.

---

## DPPF correctness test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| COR-001 | Boundary value handling | Functions behave correctly at minimum, maximum, and just-past-boundary input values | Off-by-one errors, truncated ranges, silent clamping | ISO/IEC 25010 Functional suitability | Authoring, Review, CI |
| COR-002 | Null and undefined safety | Every code path that can receive null, undefined, or missing values checks for them before dereferencing or using them | Null pointer exceptions, undefined-is-not-a-function errors, silent null propagation into downstream logic | ISO/IEC 25010 Functional suitability, CWE-476 | Authoring, Review, CI |
| COR-003 | Empty and degenerate input handling | Functions return correct, well-defined results for empty collections, empty strings, and zero-length inputs | Divide-by-zero, index-out-of-range on empty arrays, incorrect aggregate results on empty sets | ISO/IEC 25010 Functional suitability | Authoring, Review, CI |
| COR-004 | Type coercion safety | Comparisons and arithmetic do not rely on implicit type coercion producing an unintended result | Loose-equality bugs, string/number coercion errors, truthy/falsy misuse | ISO/IEC 25010 Functional suitability, CWE-704 | Review, CI |
| COR-005 | Numeric precision and overflow | Arithmetic on floating point, large integers, and currency values does not lose precision or overflow silently | Floating point rounding errors in financial calculations, integer overflow wraparound, precision loss in serialization | ISO/IEC 25010 Functional suitability, CWE-190 | Review, CI |
| COR-006 | Error propagation completeness | Exceptions and error return values are not caught and discarded without either handling or re-raising them | Silent failure, swallowed exceptions masking real defects, empty catch blocks | ISO/IEC 25010 Reliability | Review, CI |
| COR-007 | Branch and condition coverage | Every conditional branch, including default/else cases, produces the intended behavior | Unreachable dead branches, incorrect default fallthrough, missing else case | ISO/IEC 25010 Functional suitability | Review, CI |
| COR-008 | Race-condition-free shared state | Code accessing shared mutable state from concurrent contexts uses correct synchronization | Data races, lost updates, torn reads, non-deterministic test failures | ISO/IEC 25010 Reliability, CWE-362 | Review, CI |
| COR-009 | Async ordering correctness | Code that depends on the order of asynchronous operations does not assume an order the runtime does not guarantee | Race conditions between promises/futures, unawaited async calls, callback ordering bugs | ISO/IEC 25010 Functional suitability | Review, CI |
| COR-010 | Algorithm specification match | The implemented algorithm produces the specified output for representative and adversarial inputs, not only the happy path | Logic defects that pass a shallow test suite, incorrect edge-case behavior in core business logic | ISO/IEC 25010 Functional suitability | Authoring, Review, CI |
| COR-011 | Idempotent computation correctness | Pure functions and computations produce the same output for the same input on repeated calls | Hidden state leakage, non-deterministic output, test flakiness from impure functions | ISO/IEC 25010 Functional suitability | Review, CI |
| COR-012 | Resource cleanup on error paths | Code that acquires a resource (file handle, connection, lock) releases it on every exit path, including exceptions | Resource leaks under error conditions, deadlocks from unreleased locks | ISO/IEC 25010 Reliability, CWE-404 | Review, CI |
| COR-013 | Business rule fidelity | Implemented logic matches the documented business rule or acceptance criteria, not an approximation of it | Requirement drift, misinterpreted specification, silently incorrect calculations that pass tests written against the same misunderstanding | ISO/IEC 25010 Functional suitability | Review, Production |
| COR-014 | Requirement validation and testability | Each requirement, before implementation begins, is reviewed for clarity, edge-case completeness, and testability -- it states an observable, verifiable outcome | Ambiguous requirements discovered mid-implementation, untestable acceptance criteria that block writing COR-010/COR-013-style tests later, rework from a requirement that was never actually implementable as written | ISO/IEC 25010 Functional suitability, ISTQB requirements-based testing | Planning |
