# AWS identity OpenTofu root

This directory is a separate OpenTofu root module with its own state, independent
of the GitHub governance root in `infrastructure/`.

Authentication comes from the local AWS profile named `platform-lab`, and the
provider operates in `eu-north-1`. Do not store AWS access keys or other
credentials in this directory.

This first stage only reads the current AWS caller identity. It defines no
managed AWS resources and creates no infrastructure.
