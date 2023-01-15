# k8s-helloworld

This Terraform project uses the simple-eks terraform module to provision a Kubernetes cluster in AWS. 

## Prerequisites

* Install the AWS CLI
* Instal The Terraform CLI
* Access ID and Secret Key credentials for your AWS account
* Install Kubernetes CLI

## Getting Started

### Configuring AWS CLI

Configuring your aws cli with your credentials:

```bash
aws configure
# AWS Access Key ID [None]: ***********
# AWS Secret Access Key [None]: ***********************************
# Default region name [None]: ap-southeast-2
# Default output format [None]:
```

Alternatively, you can set the following environment variables instead: 

```bash
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
```

Terraform uses these credentials when it's making API calls to the cloud provider. 

### Apply Terraform to create infrastructure

Change directory into the terraform source code. We'll be running commands from this directory as the terraform command-line tool will scan for `.tf` files.

```bash
cd k8s-helloworld/
```

Download the required terraform providers for this project by running the following:

```bash
terraform init
```

This will create `.terraform/` directory which will include the downloaed providers (ie. aws).

Next we'll want to apply the terraform which will attempt to create the infrastructure in the cloud provider. 

```bash
terraform apply
```

This will generate a plan output first for you to review. The plan output will outline what infrastructure will be created, updated or destroyed. Review this carefully as this can be dangerous and deleting infrastructure!

Type in `yes` to approve the plan, which the proceed to make API calls to the cloud provider to manipulate the infrastructure. 


