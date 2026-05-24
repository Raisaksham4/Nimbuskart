# Design Decisions

## Architecture Overview

The NimbusKart Cost Hygiene Automation project was designed as a lightweight cloud cost governance tool focused on detecting orphaned AWS infrastructure resources.

The system combines:

- Python for automation logic
- Terraform for infrastructure provisioning
- LocalStack for local AWS emulation
- GitHub Actions for CI/CD automation

## Why Python

Python was selected because:

- boto3 provides strong AWS SDK support
- fast iteration for automation workflows
- simple JSON and Markdown report generation
- excellent compatibility with DevOps tooling

## Why Terraform

Terraform was used to:

- provision reproducible cloud infrastructure
- simulate real orphaned resources
- maintain infrastructure-as-code practices
- support automated CI workflows

## Why LocalStack

LocalStack enabled:

- local AWS emulation without real AWS costs
- reproducible testing environments
- CI pipeline infrastructure validation
- isolated infrastructure testing

## Detection Strategy

The janitor currently detects:

- unattached EBS volumes
- stopped EC2 instances
- unassociated Elastic IPs

The detection flow:

1. Query AWS resources using boto3
2. Evaluate orphan/resource state
3. Calculate estimated waste
4. Validate required tags
5. Generate findings
6. Export reports

## Reporting Design

Two report formats were implemented:

### JSON Report

Machine-readable output intended for:

- automation pipelines
- integrations
- API consumption

### Markdown Summary

Human-readable output intended for:

- pull request summaries
- operational reviews
- quick inspection

## CI/CD Design

GitHub Actions workflow automatically:

1. Starts LocalStack
2. Applies Terraform infrastructure
3. Runs janitor scans
4. Uploads reports as workflow artifacts

This ensures reproducible infrastructure validation.

## Safety Design

The project defaults to dry-run mode to avoid accidental destructive actions.

Delete mode requires explicit CLI usage:

```bash
python janitor/janitor.py --delete
```

## Cost Estimation Notes

Static pricing values were used for simplified monthly waste estimation.

Reference pricing:
- AWS gp3 EBS pricing: approximately $0.08 per GB-month
- Elastic IP pricing: simplified flat estimate for demonstration purposes

Pricing references:
https://aws.amazon.com/ebs/pricing/
https://aws.amazon.com/vpc/pricing/

## Future Improvements

Potential future enhancements include:

- configurable YAML policies
- scheduled scans
- Slack alerts
- multi-account scanning
- CloudWatch integration
- automated remediation workflows
- additional AWS resource support