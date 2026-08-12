# OpenTofu foundation

This provider-free root module is a learning and CI foundation. It evaluates a
service name and output without provisioning infrastructure or requiring
credentials.

Run from this directory:

```sh
tofu init
tofu fmt -check
tofu validate
tofu plan
```

Add providers, remote state, modules, and resources only when the repository
has a concrete infrastructure target.
