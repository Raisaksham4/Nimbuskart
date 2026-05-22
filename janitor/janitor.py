import sys
import json
import os
import boto3
import argparse
from datetime import datetime, timezone, timedelta
from constants import GP2_COST_PER_GB

parser = argparse.ArgumentParser()

parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete orphan resources"
)

parser.add_argument(
    "--stopped-days-threshold",
    type=int,
    default=14,
    help="Days threshold for stopped EC2 instances"
)

args = parser.parse_args()

DRY_RUN = not args.delete

STOPPED_DAYS_THRESHOLD = args.stopped_days_threshold

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")

ec2 = boto3.client(
    "ec2",
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

volumes = ec2.describe_volumes()
instances = ec2.describe_instances()
addresses = ec2.describe_addresses()
required_tags = ["Project", "Environment", "Owner"]
findings = []

for address in addresses["Addresses"]:

    if not address.get("InstanceId"):

        eip_finding = {
            "resource_id": address["AllocationId"],
            "resource_type": "elastic_ip",
            "reason": "unassociated_eip",
            "estimated_monthly_cost_usd": 3.0,
            "suggested_action": "release",
            "safe_to_auto_delete": True,
            "tags": {
                 
                "Project": None,
                "Environment": None,
                "Owner": None
            },
            "missing_tags": required_tags
        }

        findings.append(eip_finding)

for reservation in instances["Reservations"]:
    for instance in reservation["Instances"]:
                if instance["State"]["Name"] == "stopped":


                    instance_tags = {}

                    for tag in instance.get("Tags", []):
                        instance_tags[tag["Key"]] = tag["Value"]

                    stopped_finding = {
                        "resource_id": instance["InstanceId"],
                        "resource_type": "ec2_instance",
                        "reason": "stopped_instance",
                        "estimated_monthly_cost_usd": 5.0,
                        "suggested_action": "terminate",
                        "safe_to_auto_delete": True,
                        "tags": instance_tags
                    }

                    findings.append(stopped_finding)

for volume in volumes["Volumes"]:
    if volume["State"] == "available":
        volume_age_days = (
            datetime.now(timezone.utc) - volume["CreateTime"]
        ).days

        volume_tags = {}

        for tag in volume.get("Tags", []):
            volume_tags[tag["Key"]] = tag["Value"]


        missing_tags = []

        for required_tag in required_tags:
            if required_tag not in volume_tags:
                missing_tags.append(required_tag)

        finding = {
            "resource_id": volume["VolumeId"],
            "resource_type": "ebs_volume",
            "reason": "unattached",
            "age_days": volume_age_days,
            "estimated_monthly_cost_usd": volume["Size"] * GP2_COST_PER_GB,
            "tags": volume_tags,
            "suggested_action": "delete",
            "safe_to_auto_delete": volume_tags.get("Protected") != "true"
        }

        if missing_tags:
            finding["missing_tags"] = missing_tags

        findings.append(finding)

report = {
    "scan_timestamp": datetime.now(timezone.utc).isoformat(),
    "account_id": "000000000000",
    "region": AWS_REGION,
    "mode": "dry-run" if DRY_RUN else "delete",
    "summary": {
        "total_orphans": len(findings),
        "estimated_monthly_waste_usd": sum(
            finding["estimated_monthly_cost_usd"]
            for finding in findings
        )
    },
    "findings": findings
}

with open("report.json", "w") as report_file:
    json.dump(report, report_file, indent=2)

print("report.json generated successfully")

markdown_summary = f"""# Cost Janitor Report

## Summary
- Total orphans found: {report["summary"]["total_orphans"]}
- Estimated monthly waste: ${report["summary"]["estimated_monthly_waste_usd"]}

## Findings
"""

for finding in findings:
    markdown_summary += f"""
### {finding["resource_id"]}
- Type: {finding["resource_type"]}
- Reason: {finding["reason"]}
- Estimated monthly cost: ${finding["estimated_monthly_cost_usd"]}
- Suggested action: {finding["suggested_action"]}
- Safe to auto delete: {finding.get("safe_to_auto_delete", False)}
- Tags: {finding["tags"]}
"""

with open("summary.md", "w") as summary_file:
    summary_file.write(markdown_summary)

print("summary.md generated successfully")

if DRY_RUN and findings:
    sys.exit(0)