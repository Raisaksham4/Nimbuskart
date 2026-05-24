# Submission — DevOps Engineer Assignment

Candidate Name: Saksham Rai  
Email: raisaksham204@gmail.com  
Date submitted: 2026-05-24  
Hours spent (approximate): 18–22 hours

## Deliverables checklist

- [x] Part A: Terraform code under /terraform applies cleanly on LocalStack
- [x] Part A: `terraform validate` and `terraform fmt -check` both pass
- [x] Part B: Janitor script runs in --dry-run mode and produces report.json
- [x] Part B: GitHub Actions workflow runs green on a fresh PR
- [x] Part B: --delete mode respects Protected=true tag
- [x] Part C: DESIGN.md is present and within 2 pages
- [x] Walkthrough video link below is accessible (unlisted is fine)

## Walkthrough video

Link (Google Drive):  
https://drive.google.com/file/d/1NRccu0Mu6JDy0ZNctDtQki--DCjYa-Ii/view?usp=sharing


Length: max 5 minutes

## Sample report

Path to a sample report.json produced by your script:

```text
samples/report.example.json
```

## Known limitations

- Cost estimation uses simplified static pricing values instead of real AWS billing APIs.
- The implementation currently supports only EC2 instances, EBS volumes, and Elastic IP detection.
- LocalStack behavior differs slightly from real AWS behavior for some services.
- The project is designed for demonstration/testing scope and not production-scale orchestration.

## AI usage disclosure

AI tools were used during development for:

- debugging GitHub Actions and LocalStack issues
- Terraform and AWS provider troubleshooting
- improving documentation structure
- refining report formatting and workflow setup

One issue suggested incorrectly during development was related to S3 path-style configuration. The actual root cause was a LocalStack container licensing/runtime issue discovered through CI log inspection.

The core janitor detection flow and resource scanning logic were manually reviewed, modified, and tested during implementation to ensure the behavior matched the assignment requirements.