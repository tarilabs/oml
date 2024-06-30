🚧 _this is a work-in-progress demonstrator_ 🚧

## Dev Notes

### Zot (local)

```sh
bin/zot-darwin-arm64 serve examples/config-ui.json
```

### Quay (local)

using local quay 

```sh
make local-dev-up
```

with:

```diff
diff --git a/local-dev/stack/config.yaml b/local-dev/stack/config.yaml
index 8104b060..eb447d26 100644
--- a/local-dev/stack/config.yaml
+++ b/local-dev/stack/config.yaml
@@ -86,3 +86,4 @@ FEATURE_USER_METADATA: True
 #  VERIFIED_EMAIL_CLAIM_NAME: email
 #  PREFERRED_USERNAME_CLAIM_NAME: preferred_username
 #  LOGIN_SCOPES: ['openid']
+IGNORE_UNKNOWN_MEDIATYPES: True
```

### Helpful podman commands

```
podman build --build-arg "SSHPUBKEY=$(cat ~/.ssh/id_rsa.pub)" \
       --security-opt label=disable \
	   --cap-add SYS_ADMIN \
	   -f Containerfile.bootc \
	   -t mmortari/ml-iris:v1-bootc .

# inside bootc, tested R/O fs with
# podman run -p 8080:8080 --volume /models:/models --security-opt label=disable docker.io/kserve/sklearnserver:latest python -m sklearnserver --model_dir /models


export DISK_IMAGE=/Users/mmortari/git/oml/tmp/podman-build-disk-image/image/disk.raw
vfkit --cpus 2 --memory 2048 \
    --bootloader efi,variable-store=./efi-variable-store,create \
    --device virtio-blk,path=$DISK_IMAGE \
    --device virtio-serial,stdio \
    --device virtio-net,nat,mac=72:20:43:d4:38:62 \
    --device virtio-rng \
    --device virtio-input,keyboard \
    --device virtio-input,pointing \
    --device virtio-gpu,width=1920,height=1080 \
    --gui
```

```
curl -s -H "Content-Type: application/json" -d @./data/input0.json http://192.168.64.3:8080/v2/models/model/infer | jq
curl -s -H "Content-Type: application/json" -d @./data/input1.json http://192.168.64.3:8080/v2/models/model/infer | jq
curl -s -H "Content-Type: application/json" -d @./data/input4.json http://192.168.64.3:8080/v2/models/model/infer | jq
```


### Helpful KServe commands

```
kubectl get isvc my-inference-service
NAME                   URL                                               READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                    AGE
my-inference-service   http://my-inference-service.default.example.com   True           100                              my-inference-service-predictor-00001   5m11s

kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                                      AGE
istio-ingressgateway   LoadBalancer   10.96.23.147   <pending>     15021:31088/TCP,80:30151/TCP,443:30327/TCP   28m

INGRESS_GATEWAY_SERVICE=$(kubectl get svc --namespace istio-system --selector="app=istio-ingressgateway" --output jsonpath='{.items[0].metadata.name}')
kubectl port-forward --namespace istio-system svc/${INGRESS_GATEWAY_SERVICE} 8080:80
```

and then,

```
export INGRESS_HOST=localhost
export INGRESS_PORT=8080

SERVICE_HOSTNAME=$(kubectl get isvc my-inference-service -n default -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -s -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" -d @./data/input0.json http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models/my-inference-service/infer | jq
```

### Helpful KServe RAW commands

From https://kserve.github.io/website/latest/admin/kubernetes_deployment/#2-install-cert-manager

Used
1. skipped Istio
2. install Cert manager
3. etc.

```
kubectl port-forward -n default service/my-inference-service-predictor 8080:80
```

and then,

```
export INGRESS_HOST=localhost
export INGRESS_PORT=8080
curl -s -H "Content-Type: application/json" -d @./data/input0.json http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models/my-inference-service/infer | jq
```

#### Helpful KServe RAW commands using OCI-Artifact CSI

Applied CSI

```
kubectl port-forward -n default service/my-inference-ociartifact-predictor 8080:80
```

and then,

```
export INGRESS_HOST=localhost
export INGRESS_PORT=8080
curl -s -H "Content-Type: application/json" -d @./data/input0.json http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models/my-inference-ociartifact/infer | jq
```