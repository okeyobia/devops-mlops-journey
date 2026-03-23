#!/bin/bash
# Install Argo CD on Minikube using Helm
set -euo pipefail

NAMESPACE=argocd
CHART_VERSION=6.7.7

# Create namespace if it doesn't exist
kubectl get ns "$NAMESPACE" >/dev/null 2>&1 || kubectl create ns "$NAMESPACE"

# Add and update Argo Helm repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install or upgrade Argo CD
helm upgrade --install argocd argo/argo-cd \
  --namespace "$NAMESPACE" \
  --version "$CHART_VERSION" \
  --set server.service.type=ClusterIP \
  --set server.ingress.enabled=false \
  --set controller.replicas=1 \
  --set repoServer.replicas=1 \
  --set applicationSet.replicas=1

# Wait for Argo CD server pod to be ready
kubectl rollout status deployment/argocd-server -n "$NAMESPACE" --timeout=180s

echo "Argo CD installed. To access the UI:"
echo "kubectl port-forward svc/argocd-server -n $NAMESPACE 8080:443"
echo "Initial admin password:"
kubectl -n $NAMESPACE get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
