terraform {
  required_version = ">= 0.12"

  backend "s3" {
    region  = "us-west-2"
    profile = ""
    bucket  = "us.landwatch.infra" 
    key     = "terraform.tfstate"
  }
}

variable "tags" {}
variable "app" {}
variable "environment" {}

/**
 * main.tf
 * The main entry point for Terraform run
 * See variables.tf for common variables
 * See ecr.tf for creation of Elastic Container Registry for all environments
 * See state.tf for creation of S3 bucket for remote state
 */


provider "aws" {
    version = ">= 2.23.0"
}

/*
 * Outputs
 * Results from a successful Terraform run (terraform apply)
 * To see results after a successful run, use `terraform output [name]`
 */

 # Returns the name of the ECR registry, this will be used later in various scripts
output "docker_registry" {
  value = aws_ecr_repository.app.repository_url
}

