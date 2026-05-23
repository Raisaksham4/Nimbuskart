# Submission Notes

## Project Summary

NimbusKart Cost Hygiene Automation is a DevOps-focused cloud cost optimization project that detects orphaned AWS resources using Python automation, Terraform, LocalStack, and GitHub Actions.

The project identifies:

- unattached EBS volumes
- stopped EC2 instances
- unassociated Elastic IPs
- missing required tags

and generates both JSON and Markdown reports.

---

## Repository Structure

```text
.
├── .github/workflows/
├── janitor/
├── terraform/
├── samples/
├── README.md
├── DESIGN.md
└── SUBMISSION.md
```

---

## Features Implemented

- Infrastructure provisioning with Terraform
- Local AWS emulation using LocalStack
- Automated orphan detection
- Estimated monthly waste calculation
- Missing tag validation
- Dry-run mode
- Delete mode
- JSON report generation
- Markdown summary generation
- GitHub Actions CI workflow
- Artifact uploads in CI

---

## CI/CD Workflow

The GitHub Actions pipeline:

1. Starts LocalStack
2. Initializes Terraform
3. Provisions infrastructure
4. Runs janitor scans
5. Uploads generated reports

Artifacts produced:

- report.json
- summary.md

---

## Sample Outputs

Sample outputs are available in:

```text
samples/
```

---

## Decisions and Deviations

### Dry-Run as Default

The janitor defaults to dry-run mode to prevent accidental destructive actions during testing and CI execution.

Delete behavior requires an explicit `--delete` flag.

This decision prioritizes operational safety over aggressive automation.

---

### Simplified Cost Estimation

Monthly waste estimates use simplified static pricing values instead of live AWS pricing APIs.

Reasoning:
- reduces complexity
- avoids external API dependencies
- keeps LocalStack-based testing deterministic

The implementation was intentionally optimized for reproducibility and demonstration purposes.

---

### Conservative Delete Design

Although delete mode exists, destructive behavior was intentionally kept conservative.

Resources are marked with:
- `safe_to_auto_delete`
- `suggested_action`

before any remediation logic is applied.

This reduces risk from false positives.

---

### Limited Resource Coverage

The implementation currently focuses on:

- unattached EBS volumes
- stopped EC2 instances
- unassociated Elastic IPs

instead of attempting broad AWS coverage.

Reasoning:
- prioritizing reliability and correctness
- keeping the project maintainable
- ensuring CI reproducibility within assignment scope

---

### GitHub Actions Behavior

The workflow uploads artifacts even when orphaned resources are detected.

The pipeline was intentionally designed to surface findings instead of failing infrastructure execution entirely.

This improves debugging and operational visibility.

---

## Assumptions

- LocalStack is used instead of real AWS accounts
- Estimated costs are simplified static estimates
- Dry-run mode is the default behavior
- Delete mode requires explicit CLI flag

---

## Known Limitations

- Limited AWS resource coverage
- Simplified cost calculations
- Basic delete workflow
- No persistence/database layer
