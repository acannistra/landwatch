# Landwatch Computing Infrastructure 

This directory contains infrastructure pieces for both the data processing and web portions of the Landwatch project. 

## Data Infrastructure

To create the landwatch database we rely on a series of workflows. These workflows are written using the [Prefect Core](https://docs.prefect.io/core/) and managed using the [Prefect Cloud](https://www.prefect.io/cloud) free tier. The infrastructure necessary to run these workflows is hosted on Amazon Web Services, described in more detail below. 

### AWS Resources

To run Prefect flows in a scheduled fashion, we use several AWS services:
* an Elastic Compute Cloud cluster, configured to launch Fargate tasks 
* an Elastic Container Registry used to store Docker images used by Prefect task runners (_see below_)
* a small EC2 instance used to host the Prefect Agent
* S3 buckets used for storing data and other infrastructure-deployment things

These resources are provisioned programmatially using [Terraform](terraform.io). The templates used to create these resources are located in the [`templates/`](templates) directory. 

In order to run Prefect tasks on AWS infrastructure (specificially as ECS Fargate tasks) we need to build and provide a base image. We provide this image as `Dockerfile`, and rely on Prefect to build and push it during task registration. 

#### Terraform Configuration Details 
* we use the s3 backend to the AWS provider, which stores state in an S3 bucket (`us.landwatch.infra`).
* **TODO**: the EC2 instance template is not filled-out currently

#### Provisioning AWS Resources

`aws-vault` is required to manage credentials. 

```shell
cd templates
aws-vault exec <profile> -- terraform init
aws-vault exec <profile> -- terraform plan -var-file="variables.tfvars"
aws-vault exec <profile> -- terraform apply --var-file="variables.tfvars"
```

#### Building and Registering Prefect Flows
TBD

## Web Infrastructure
