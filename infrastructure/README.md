# OpenTofu repository governance

This root module manages the minimum branch-protection policy for this
repository. It protects `master`, requires pull requests without requiring an
approval in this single-developer repository, and requires the existing GitHub
Actions checks to pass before merge.

The GitHub provider reads authentication from runtime configuration. Set
`GITHUB_TOKEN` to a token with repository administration permission before
planning or applying. Do not store the token in this directory or in OpenTofu
variables.

Run from this directory:

```sh
tofu init
tofu fmt -check
tofu validate
GITHUB_TOKEN="..." tofu plan
```

Review every plan carefully. Applying this module changes the repository's
merge and push policy; it does not create application infrastructure.
