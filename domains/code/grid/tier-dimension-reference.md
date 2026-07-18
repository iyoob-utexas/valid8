# Tier and Quality Characteristic Reference

This file describes the severity tiers and the ISO/IEC 25010 software quality characteristics used by the framework.

## Severity tiers

| Tier | Meaning | Behavior |
|---|---|---|
| Tier 1, Critical | Zero tolerance. Failure blocks the merge or blocks the release. Bad code must not reach production. Run on every PR and every release candidate. | Block the merge or block the release. |
| Tier 2, Important | Warn and investigate. Fix-before-release action or an alert; the PR may merge under review. Run on every PR or on a daily CI cadence. | Investigate and review; allow controlled continuation when appropriate. |
| Tier 3, Good practice | Monitor and trend. Dashboarded to catch drift and tech-debt accumulation early; no hard gate. Reviewed on a cadence. | Track over time and improve the process. |

## ISO/IEC 25010 software quality characteristics

| Characteristic | What it means |
|---|---|
| Functional suitability | Does the software provide functions that meet stated and implied needs, completely and correctly? |
| Performance efficiency | Does the software use time, resources, and capacity appropriately under stated conditions? |
| Compatibility | Can the software exchange information with other systems and coexist without adverse effects? |
| Usability | Can specified users achieve specified goals effectively, efficiently, and with satisfaction? |
| Reliability | Does the software perform specified functions under specified conditions for a specified period, including under failure and recovery? |
| Security | Does the software protect information and data so that authorized access is the only access permitted? |
| Maintainability | Can the software be modified effectively and efficiently by intended maintainers? |
| Portability | Can the software be transferred effectively and efficiently between environments? |

## How this framework's domains map to ISO/IEC 25010

| Test domain | Primary characteristic(s) |
|---|---|
| Correctness and logic | Functional suitability, Reliability |
| Structure and style | Maintainability |
| Security | Security |
| Architecture and design | Maintainability, Compatibility |
| Testing and coverage | Functional suitability (verification), Maintainability, Usability, Portability, Compatibility |
| Performance and scalability | Performance efficiency |
| Reliability and operability | Reliability |
| Adversarial | Security, Reliability |

Usability, Portability, and Compatibility are now touched by baseline checks in `tests/testing-and-coverage.md` (TST-014 usability, TST-017 accessibility, TST-018 localization/portability, TST-019 cross-browser/cross-device compatibility), but these remain lightweight, heuristic-level checks, not a substitute for a dedicated UX, accessibility, localization, or platform-compatibility testing practice. See the "What this domain does not include" section of `domains/code/README.md`.
