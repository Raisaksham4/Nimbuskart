# NimbusKart Cost Hygiene Automation

## Overview

NimbusKart Cost Hygiene Automation is a lightweight cloud cost governance project built using Python, Terraform, LocalStack, and GitHub Actions. The tool detects orphaned AWS resources such as unattached EBS volumes, stopped EC2 instances, and unassociated Elastic IPs, then generates JSON and Markdown reports with estimated monthly waste and remediation suggestions.

---

## How to run locally

### Clone Repository

```bash
git clone https://github.com/Raisaksham4/Nimbuskart.git
cd nimbuskart-cost-hygiene
```

### Install Dependencies

```bash
pip install -r janitor/requirements.txt
pip install terraform-local
```

### Start LocalStack

```bash
docker run -d -p 4566:4566 localstack/localstack:3.5
```

### Apply Terraform Infrastructure

```bash
cd terraform
tflocal init
tflocal apply -auto-approve
```

### Run Janitor

```bash
cd ..
python janitor/janitor.py
```

### Run Delete Mode

```bash
python janitor/janitor.py --delete
```

---

## Architecture

```text
                    +----------------------+
                    |  GitHub Actions CI   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     LocalStack       |
                    |  AWS Cloud Emulator  |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                                         |
          v                                         v
+-------------------+                  +-------------------+
| Terraform         |                  | Python Janitor    |
| Infrastructure    |                  | Resource Scanner  |
+-------------------+                  +-------------------+
                                                  |
                                                  v
                                   +-----------------------------+
                                   | JSON + Markdown Reports     |
                                   +-----------------------------+
```

---

## Decisions & deviations

- SSH access from `0.0.0.0/0` was intentionally treated as unsafe because exposing port 22 publicly is not recommended in production environments.
- Delete mode requires an explicit `--delete` flag because automatic remediation without approval can accidentally remove legitimate infrastructure.
- Dry-run mode was made the default behavior to reduce the risk of destructive actions during testing and CI execution.
- Static pricing values were used instead of live AWS pricing APIs because reproducible LocalStack-based testing was prioritized over pricing accuracy.
- The implementation only scans EBS volumes, EC2 instances, and Elastic IPs because broader AWS coverage would reduce reliability within assignment scope.
- Additional fields like `missing_tags` and `mode` were added to improve operational visibility without removing required schema fields.
- GitHub Actions uploads reports even when orphaned resources are detected because visibility and debugging were prioritized over failing the pipeline immediately.
- Resource deletion logic was intentionally kept conservative because orphan detection can produce false positives in real production environments.
- A configurable stopped-instance threshold was implemented because temporarily stopped instances should not immediately be classified as waste.

---

## Trade-offs

With one additional week, I would improve the project by adding real AWS pricing API integration, scheduled scans, multi-account support, and broader AWS resource coverage. I would also improve remediation safety with approval-based deletion workflows and persistent scan history storage.

---

## AI usage disclosure

AI tools were used during development for:

- debugging GitHub Actions and LocalStack issues
- Terraform and AWS provider troubleshooting
- improving documentation structure
- refining report formatting and workflow setup

One issue suggested incorrectly during development was related to S3 path-style configuration. The actual root cause was a LocalStack container licensing/runtime issue discovered through CI log inspection.

The core janitor detection flow and resource scanning logic were manually reviewed, modified, and tested during implementation to ensure the behavior matched the assignment requirements.
