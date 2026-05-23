# NimbusKart Cost Hygiene Automation

## Overview

NimbusKart Cost Hygiene Automation is a DevOps-focused cloud cost optimization tool that detects orphaned AWS resources using Python, Terraform, LocalStack, and GitHub Actions.

The tool identifies unused cloud resources, estimates monthly waste, generates reports, and automates infrastructure scanning workflows.

## Features

- Detect unattached EBS volumes
- Detect stopped EC2 instances
- Detect unassociated Elastic IPs
- Detect missing mandatory tags
- Generate JSON reports
- Generate Markdown summaries
- Dry-run and delete modes
- GitHub Actions CI integration
- Terraform + LocalStack infrastructure automation

## Tech Stack

- Python
- Terraform
- LocalStack
- GitHub Actions
- AWS SDK (boto3)

## Project Structure

```text
.
├── .github/workflows/
├── janitor/
├── terraform/
├── samples/
├── README.md
```

## Local Setup

### Prerequisites

- Python 3.13+
- Terraform
- Docker
- LocalStack
- terraform-local

### Install Dependencies

```bash
pip install -r janitor/requirements.txt
```

### Start LocalStack

```bash
docker run -d -p 4566:4566 localstack/localstack:3.5
```

### Initialize Terraform

```bash
cd terraform
tflocal init
tflocal apply -auto-approve
```

## Running the Janitor

### Dry Run Mode

```bash
python janitor/janitor.py
```

### Delete Mode

```bash
python janitor/janitor.py --delete
```

## GitHub Actions Workflow

The project includes a GitHub Actions workflow that:

1. Starts LocalStack
2. Initializes Terraform infrastructure
3. Provisions sample AWS resources
4. Runs the janitor scanner
5. Uploads generated reports as artifacts

## Sample Outputs

Example outputs are available under:

```text
samples/
```

- `sample-report.json`
- `sample-summary.md`


## AI Usage Disclosure

AI tools were used during development for:

- debugging GitHub Actions and LocalStack issues
- Terraform and AWS provider troubleshooting
- improving documentation structure
- refining report formatting and workflow setup

One issue suggested incorrectly during development was related to S3 path-style configuration. The actual root cause was a LocalStack container licensing/runtime issue discovered through CI log inspection.

The core janitor detection flow and resource scanning logic were manually reviewed, modified, and tested during implementation to ensure the behavior matched the assignment requirements.