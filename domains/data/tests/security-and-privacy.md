# Security and Privacy

Security and privacy are critical cross-cutting concerns for any data project.

## What to test

- Sensitive data classification
  - Identify PII/PHI and other sensitive fields in source and target datasets.
  - Confirm that classification metadata is stored and updated.

- Masking, redaction, and anonymization
  - Validate that sensitive values are masked or redacted where required.
  - Confirm anonymization preserves required analytics while protecting privacy.

- Access control
  - Verify row-level security and dataset permissions are configured correctly.
  - Confirm that only authorized roles can read, write, or export sensitive data.

- Encryption and transport
  - Check that data at rest and in transit is encrypted according to policy.
  - Validate endpoint and storage access controls.

- Compliance and retention
  - Confirm that data retention and purge policies are enforced.
  - Validate regulatory controls such as GDPR, HIPAA, or contractual restrictions.

## Why it matters

Data projects often process sensitive information. Security and privacy tests are necessary to prevent data leaks, ensure compliance, and maintain stakeholder trust.
