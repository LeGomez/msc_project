data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
    source = "terraform-aws-modules/vpc/aws"
    version = "2.77.0"

    name = "project"
    cidr = "10.0.0.0/16"
    azs = data.aws_availability_zones.available.names
    public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
    enable_dns_hostnames = true
    enable_dns_support = true
}

resource "aws_db_subnet_group" "project" {
    name = "project"
    subnet_ids = module.vpc.public_subnets

    tags = {
      "Name" = "Project"
    }
  
}

resource "aws_security_group" "rds" {
  name   = "project_rds"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "project_rds"
  }
}

resource "aws_db_parameter_group" "project" {
    name = "project"
    family = "postgres14"

    parameter {
      name = "log_connections"
      value = "1"
    }
}

resource "aws_db_instance" "project" {
    identifier = "project"
    instance_class = "db.t3.micro"
    allocated_storage = 5
    engine = "postgres"
    engine_version = "14.2"
    username =  "${var.db_username}"
    password =  "${var.db_password}"
    db_subnet_group_name = aws_db_subnet_group.project.name
    vpc_security_group_ids = [aws_security_group.rds.id]
    parameter_group_name = aws_db_parameter_group.project.name
    publicly_accessible = false
    skip_final_snapshot = true
}

output "rds_hostname" {
  value = aws_db_instance.project.address
  sensitive = true
}

output "rds_port" {
  value = aws_db_instance.project.port
  sensitive = true
}

output "rds_username" {
  value = aws_db_instance.project.username
  sensitive = true
}