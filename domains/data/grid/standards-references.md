# Standards and References

This file documents the reference standards used by the framework.

| Standard / Source | What it is | How Data Crafters uses it | Reference |
|---|---|---|---|
| DAMA-DMBOK2 | Data Management Body of Knowledge (DAMA International). Defines the recognised data quality dimensions. | Source of the DAMA Dimension column; the shared vocabulary for what good data means. | dama.org |
| ISO/IEC 25012:2008 | SQuaRE data quality model. Defines 15 data quality characteristics (inherent and system dependent). | Formal backing for our quality dimensions; citable for regulated or audit driven clients. | iso.org/standard/35736.html |
| ISO 8000 | International standard for master data quality, governance and exchange. | Reference for master and reference data checks (codes, vendors, cost centers, mappings). | iso.org (ISO 8000 series) |
| ISO/IEC/IEEE 29119 | International software testing standard series: vocabulary, process, documentation and techniques. | Backs our tiering, test planning and the Traditional Software tests. | softwaretestingstandard.org |
| ISTQB | International Software Testing Qualifications Board. Industry testing glossary and certification. | Shared testing vocabulary (unit, integration, regression, end to end). | istqb.org |
| Test Pyramid (M. Cohn) | Testing strategy: many fast unit tests at the base, fewer integration and end to end tests above. | Shapes where we spend test effort across the medallion layers. | Agile testing literature |
| DataOps Manifesto | Principles for continuous, automated, observable data delivery with shared ownership. | Our operating model: testing runs in the pipeline, not as a one time gate. | dataopsmanifesto.org |
| Reference tooling | dbt tests, Great Expectations, Soda, Deequ / PyDeequ. De facto data testing implementations. | The tool-agnostic approaches in the grid map to these; delivered on Fabric and Azure. | getdbt.com; greatexpectations.io; soda.io |
| SOX ITGC / COSO | Internal Control over Financial Reporting and IT General Controls framework. | Why Tier 1 output and cross-validation checks are zero tolerance for finance clients. | sox-online.com; coso.org |
| Five pillars of data observability | Industry model defining freshness, volume, distribution, schema, and lineage as the core monitoring dimensions for data systems. | Source of the observability pillar column in the DPPF attack surface map and test catalogs. | Monte Carlo Data; widely cited in data engineering literature |
| PTES (Penetration Testing Execution Standard) | Methodology for structuring a penetration testing engagement: reconnaissance, threat modeling, exploitation, post-exploitation, reporting. | Basis for the seven-phase DPPF engagement methodology in `domains/data/process/testing-strategy.md`. | pentest-standard.org |
| Chaos data engineering | Practice of deliberately injecting faults, bad data, duplicate floods, schema mutations, and dependency kills to validate pipeline resilience. | Source of the Adversarial domain test catalog in `domains/data/tests/adversarial.md` and the adversarial rows in the test grid. | Chaos Engineering (Rosenthal et al.); adapted to data systems |
| CVSS (Common Vulnerability Scoring System) | Standardized method for scoring the severity of security vulnerabilities on base, temporal, and environmental metrics. | Inspiration for the DPPF four-factor severity scoring model (blast radius, detectability, data criticality, recoverability) in `domains/data/framework/README.md`. | first.org/cvss |

> Note: These are reference points, not a single mandated certification. ISO and DAMA materials are licensed; cite them, do not redistribute the full texts.
