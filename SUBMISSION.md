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
