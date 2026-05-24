# Cost Janitor Report

## Summary
- Total orphans found: 3
- Estimated monthly waste: $8.64

## Findings

### eipalloc-36859bff
- Type: elastic_ip
- Reason: unassociated_eip
- Estimated monthly cost: $3.0
- Suggested action: release
- Safe to auto delete: True
- Tags: {'Project': None, 'Environment': None, 'Owner': None}

### i-4c1e719cce556814d
- Type: ec2_instance
- Reason: stopped_instance
- Estimated monthly cost: $5.0
- Suggested action: terminate
- Safe to auto delete: True
- Tags: {'Environment': 'staging', 'Owner': 'Saksham', 'Tier': 'web', 'Name': 'nimbuskart-web-2', 'ManagedBy': 'terraform', 'Project': 'NimbusKart'}

### vol-58967743
- Type: ebs_volume
- Reason: unattached
- Estimated monthly cost: $0.64
- Suggested action: delete
- Safe to auto delete: True
- Tags: {'Owner': 'Saksham', 'ManagedBy': 'terraform', 'Project': 'NimbusKart', 'Environment': 'staging', 'Name': 'orphan-ebs-volume'}
