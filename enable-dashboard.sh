#!/bin/bash

helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

echo "Waiting for all Deployments in kubernetes-dashboard..."
DEPLOYMENTS=$(kubectl get deployments -n kubernetes-dashboard -o jsonpath='{.items[*].metadata.name}')
for DEPLOYMENT in $DEPLOYMENTS; do # bash separation
  kubectl wait --for=condition=available --timeout=2m deployment/$DEPLOYMENT -n kubernetes-dashboard
done

kubectl apply -f dashboard/serviceAccount.yaml
sleep 2
kubectl apply -f dashboard/clusterRoleBinding.yaml
sleep 2
kubectl apply -f dashboard/bearerTokenSecret.yaml
sleep 3

echo "Bearer token:"
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
echo ""

kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
