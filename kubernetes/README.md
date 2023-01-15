# Kubernetes

## Connecting to the Kubernetes Cluster

Ensure you have configured your local awscli with your credentials:

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

Generate the Kube Config credentials for your EKS cluster:

```bash
export CLUSTER_NAME="k8s-helloworld"
export CLUSTER_REGION="ap-southeast-2"

aws eks --region $CLUSTER_REGION update-kubeconfig --name $CLUSTER_NAME
```

## Installing Kubernetes Helm Charts

We'll need a few different helm charts to handle ingress and ssl certificate issuing. You can learn more by checking out the ingress-nginx and cert-manager docs.

Installing ingress-nginx helm chart: 

```bash
# Install ingress-nginx via Helm
kubectl create ns ingress-nginx
helm upgrade ingress-nginx ./ingress-nginx --install --namespace ingress-nginx --values ./ingress-nginx/values.yaml --wait
```

Installing cert-manager helm chart:

```bash
# Install cert-manager via Helm
kubectl create ns cert-manager
helm upgrade cert-manager ./cert-manager --install --namespace cert-manager --values ./cert-manager/values.yaml --wait
```
Applying a ClusterIssuer object which tells cert-manager how and which CA to issuer SSL certificates from: 

```bash
# Install LetsEncrypt ClusterIssuer
kubectl -n cert-manager apply -f ./cert-manager-issuers
```

## Deploying our hello world app

We'll be using kustomize to bundle the relevant Kubernetes manifests for your application. These manifests include:
* Deployment
* Service
* Ingress
* Horizontal Pod Autoscaler

Run the following command to apply the app into the default namespace:

```bash
kustomize build ./helloworld | kubectl apply -f -
```