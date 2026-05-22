locals {
  common_tags = {
    Project     = "NimbusKart"
    Environment = "staging"
    Owner       = "Saksham"
    ManagedBy   = "terraform"
  }
}

module "network" {
  source = "./modules/network"

  vpc_cidr             = "10.20.0.0/16"
  public_subnet_1_cidr = "10.20.1.0/24"
  public_subnet_2_cidr = "10.20.2.0/24"

  availability_zone_1 = "us-east-1a"
  availability_zone_2 = "us-east-1b"

  common_tags = local.common_tags
}

resource "aws_security_group" "web_sg" {
  name        = "nimbuskart-web-sg"
  description = "Security group for web servers"
  vpc_id      = module.network.vpc_id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      Name = "nimbuskart-web-sg"
    }
  )
}

resource "aws_instance" "web_1" {
  ami                    = "ami-12345678"
  instance_type          = var.instance_type
  subnet_id              = module.network.subnet_ids[0]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = merge(
    local.common_tags,
    {
      Name = "nimbuskart-web-1"
      Tier = "web"
    }
  )
}

resource "aws_instance" "web_2" {
  ami                    = "ami-12345678"
  instance_type          = var.instance_type
  subnet_id              = module.network.subnet_ids[1]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = merge(
    local.common_tags,
    {
      Name = "nimbuskart-web-2"
      Tier = "web"
    }
  )
}

resource "aws_s3_bucket" "logs" {
  bucket = "nimbuskart-app-logs"

  tags = merge(
    local.common_tags,
    {
      Name = "nimbuskart-app-logs"
    }
  )
}

resource "aws_s3_bucket_versioning" "logs_versioning" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Enabled"
  }
}
/*
resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.logs.id

  rule {
    id     = "expire-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
*/

resource "aws_ebs_volume" "orphan_volume" {
  availability_zone = var.availability_zone_1
  size              = 8

  tags = merge(
    local.common_tags,
    {
      Name = "orphan-ebs-volume"
    }
  )
}