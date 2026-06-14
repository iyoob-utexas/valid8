# valid8 Sandbox

Throwaway sample project for testing the valid8 framework end to end.

**To delete everything:** `rm -rf /Users/ilyasiyoob/code/valid8/_sandbox`

## What this is

A synthetic monthly sales reporting pipeline with intentional data defects baked in.
Used to run a full valid8 test profile and identify gaps in the framework documentation.

## How to run

```bash
cd /Users/ilyasiyoob/code/valid8/_sandbox

# Run the pipeline
python pipeline/ingest.py
python pipeline/transform.py
python pipeline/aggregate.py

# Run all valid8 checks
python tests/valid8_runner.py
```

Results land in `tests/results/`.
