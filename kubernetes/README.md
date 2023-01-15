# Kubernetes

## Connecting to the Kubernetes Cluster

Ensure you have configured your local awscli with your credentials:

```bash
aws configure
# AWS Access Key ID [None]: ***********
# AWS Secret Access Key [None]: ***********************************
# Default region name [None]: us-east-1
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
export CLUSTER_REGION="us-east-1"

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

## Configuring DNS

Next you'll need to configure a DNS record to point to your nginx ingress. This will be required for ingress traffic to reach your pods and also for cert-manager to issue a SSL certificate. 

Get the hostname from the associated ELB:

```bash
kubectl get service/ingress-nginx-controller -n ingress-nginx -o json | jq -rc '.status.loadBalancer.ingress[0].hostname'

#a3a5895b766d0429c93e13d1369d696c-12345677.us-east-1.elb.amazonaws.com
```

Go to your DNS provider and setup the following DNS Records:

| Type | Name | Content |
|------|------|---------|
|  CNAME   | helloworld.upwork-32487863.proj.chrisvfab.io | a3a5895b766d0429c93e13d1369d696c-12345677.us-east-1.elb.amazonaws.com

> Setup whichever domain you like and ensure it points to the external ip of the nginx ingress controller.

Once your DNS is configured, test everything is working:

```bash
ping helloworld.upwork-32487863.proj.chrisvfab.io
# PING a3a5895b766d0429c93e13d1369d696c-12345677.us-east-1.elb.amazonaws.com (3.92.153.99): 56 data bytes
```

Test that you can curl the endpoint:

```bash
curl http://helloworld.upwork-32487863.proj.chrisvfab.io
# <html>
# <head><title>308 Permanent Redirect</title></head>
# <body>
# <center><h1>308 Permanent Redirect</h1></center>
# <hr><center>nginx</center>
# </body>
# </html>
```

As expected, it's attempt to redirect to https as configured in the Ingress (`ingress.kubernetes.io/ssl-redirect: 'true'`). 

Test the https endpoint via curl:

```bash
curl https://helloworld.upwork-32487863.proj.chrisvfab.io
# curl: (60) SSL certificate problem: unable to get local issuer certificate
```

The above SSL certificate error may occur. This generally means cert-manager hasn't issued the certificate yet. This can take some time depending on the configured certificate authority. 

To check the status of a cert-manager Certificate, run the following: 

```bash
kubectl get orders
# NAME                          STATE   AGE
# helloworld-rdcvk-2644647259   valid   27s

export ORDER_NAME="helloworld-rdcvk-2644647259"

# Check events and wait for the order to complete 
kubectl get events --field-selector involvedObject.name=$ORDER_NAME
# LAST SEEN   TYPE     REASON     OBJECT                                                                 MESSAGE
# 2m3s        Normal   Complete   order/helloworld-rdcvk-2644647259   Order completed successfully
```

> Alternatively, use the [kubectl cert-manager plugin](https://cert-manager.io/v1.0-docs/usage/kubectl-plugin/) to check the status of a cert. Run `kubectl cert-manager status helloworld-rdcvk-2644647259`

Once the SSL Certificate is issued, you can try curling the endpoint again:

```bash
curl https://helloworld.upwork-32487863.proj.chrisvfab.io
HelloWorld version: 1.0.0, instance hello-world-64c4ff6db-957pn
```
