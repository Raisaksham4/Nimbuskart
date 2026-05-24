# Design Notes

## Architecture Overview

NimbusKart Cost Hygiene Automation is a lightweight cloud cost governance tool designed to detect orphaned AWS infrastructure resources and estimate unnecessary cloud spend.

The implementation combines:

- Python for automation logic
- Terraform for reproducible infrastructure provisioning
- LocalStack for local AWS emulation
- GitHub Actions for CI/CD automation

The system scans cloud resources, evaluates orphan conditions, validates tagging requirements, calculates estimated waste, and exports both JSON and Markdown reports.

---

# Multi-Cloud Reality

NimbusKart plans to support GCP and Azure in the future. To avoid rewriting the core logic, the janitor can be restructured into provider-specific scanner modules with a shared core abstraction layer.

Example structure:

```text
janitor/
├── core/
│   ├── scanner.py
│   ├── reporting.py
│   ├── policies.py
│   └── remediation.py
├── providers/
│   ├── aws/
│   ├── gcp/
│   └── azure/
```

## Core Layer Responsibilities

The shared core layer would handle:

- report generation
- tagging validation
- cost aggregation
- remediation policy evaluation
- export formatting
- CLI handling

## Provider Layer Responsibilities

Each cloud provider module would independently implement:

- authentication
- resource discovery
- orphan detection logic
- provider-specific deletion workflows

This design minimizes coupling and allows future cloud providers to be added without modifying the reporting or policy engine.

---

# Permissions

## Dry-Run Mode Permissions

Dry-run mode only requires read-only permissions:

- `ec2:DescribeInstances`
- `ec2:DescribeVolumes`
- `ec2:DescribeAddresses`

Dry-run mode intentionally avoids destructive actions.

## Delete Mode Permissions

Delete mode additionally requires:

- `ec2:DeleteVolume`
- `ec2:TerminateInstances`
- `ec2:ReleaseAddress`

Delete operations are only enabled when the `--delete` CLI flag is explicitly provided.

## Minimal Read-Only IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeAddresses"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Safety Net

## Failure Mode 1 — False Positive EC2 Cleanup

A stopped EC2 instance may belong to a disaster recovery environment or temporary maintenance workflow.

Naive auto-deletion could remove critical standby infrastructure.

### Guardrails

- dry-run mode enabled by default
- configurable stopped-instance threshold
- explicit delete flag required
- reporting before remediation

---

## Failure Mode 2 — Shared Resource Misclassification

An unattached Elastic IP or EBS volume may still be reserved for planned deployments or external workflows.

Automatic deletion could break future provisioning processes.

### Guardrails

- required tag validation
- `safe_to_auto_delete` evaluation
- approval-based deletion workflows
- quarantine/report-only phase before deletion

---

# Observability

The following operational metrics would help the FinOps team monitor janitor effectiveness.

| Metric | Source | Alert Threshold |
|---|---|---|
| Total orphan resources detected | report.json summary | > 20 resources |
| Estimated monthly waste | report aggregation | > $100/month |
| Failed janitor scans | GitHub Actions workflow status | Any failed run |
| Resources auto-deleted | janitor delete logs | Sudden spike |
| Missing mandatory tags | tag validation results | > 10 resources |

## Recommended Destinations

Metrics could be published to:

- CloudWatch
- Prometheus
- Grafana dashboards
- GitHub Actions summaries

---

# Reporting Design

Two report formats were implemented.

## JSON Report

Machine-readable output intended for:

- automation workflows
- integrations
- API consumption

## Markdown Summary

Human-readable output intended for:

- operational reviews
- CI summaries
- quick inspection

---

# Cost Estimation Notes

Static pricing values were used for simplified monthly waste estimation.

Reference pricing:

- AWS gp3 EBS pricing: approximately $0.08 per GB-month
- Elastic IP pricing: simplified flat estimate for demonstration purposes

Pricing references:

- https://aws.amazon.com/ebs/pricing/
- https://aws.amazon.com/vpc/pricing/

---

# CI/CD Design

The GitHub Actions workflow automatically:

1. Starts LocalStack
2. Initializes Terraform
3. Provisions infrastructure
4. Runs janitor scans
5. Uploads generated reports as workflow artifacts

This ensures reproducible infrastructure validation in CI.

---

# What I Did Not Build

Several production-scale features were intentionally excluded in order to keep the project lightweight, reproducible, and aligned with assignment scope.

The following were intentionally not implemented:

- real AWS billing API integration
- persistent databases
- distributed scanning
- multi-account orchestration
- asynchronous remediation workflows
- Slack or PagerDuty integrations
- advanced policy engines
- Kubernetes resource scanning

These features would significantly increase operational complexity and infrastructure requirements beyond the intended LocalStack-based demonstration environment.
