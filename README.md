🚧 _this is a work-in-progress demonstrator_ 🚧

## Dev Notes

### Zot (local)

```sh
bin/zot-darwin-arm64 serve examples/config-ui.json
```

### Quay (local)

using local quay with:

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
