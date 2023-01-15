# simple-eks Terraform Module

This terraform module creates a simple Elastic Kubernetes Service (EKS) cluster including seting up the VPC and IAM policies required.

## Usage

```terraform
module "eks_cluster" {
  source         = "git::https://github.com/chrisvfabio/python-eks-terraform?ref=main"
  
  vpc_name       = "my-vpc"
  vpc_cidr       = "10.0.0.0/16"
  cluster_name   = "my-cluster"
  desired_size   = 2
  max_size       = 2
  min_size       = 1
  instance_types = ["t2.small"]
}
```