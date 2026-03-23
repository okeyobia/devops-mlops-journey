terraform {
  required_providers {
    minikube = {
        source = "scott-the-programmer/minikube"
        version = "0.4.4" # Latest stable in 2026
    }
    kubernetes = {
        source = "hashicorp/kubernetes"
        version = ">= 2.30.0" # Latest stable in 2026
    }
  }
}

provider "minikube" {}

# 1. Create the Minikube Cluster
resource "minikube_cluster" "dev_lab" {
  driver       = "docker"
  cluster_name = "minikube-dev"
  nodes        = 1 # Standard for local dev
  cpus         = 4
  memory       = "8192mb"
  
  # Addons: Enabling the Dashboard and Ingress by default
  addons = [
    "dashboard",
    "ingress",
    "metrics-server"
  ]
}

# 2. Configure the Kubernetes Provider 
# This tells Terraform how to talk to the cluster once it's up.
provider "kubernetes" {
  host                   = minikube_cluster.dev_lab.host
  client_certificate     = minikube_cluster.dev_lab.client_certificate
  client_key             = minikube_cluster.dev_lab.client_key
  cluster_ca_certificate = minikube_cluster.dev_lab.cluster_ca_certificate
}