terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = "us-east-1"
}

module "public_eks_cluster" {
  #   source         = "git::https://github.com/chrisvfabio/python-eks-terraform?ref=main"
  source         = "../modules/simple-eks"
  vpc_name       = "upwork-32487863"
  cluster_name   = "k8s-helloworld"
  desired_size   = 1
  min_size       = 1
  max_size       = 2
  instance_types = ["t2.small"]
}
