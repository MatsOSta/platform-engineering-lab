# AWS identity OpenTofu root

This directory is a separate OpenTofu root module with its own state, independent
of the GitHub governance root in `infrastructure/`.

Authentication comes from the local AWS profile named `platform-lab`, and the
provider operates in `eu-north-1`. Do not store AWS access keys or other
credentials in this directory.

## Hermes agent-host bootstrap

`bootstrap-agent-host.sh` installs and starts the Amazon Linux 2023 Docker
package on the existing Hermes agent host. It is intended to be transferred to
the host and run as root through an AWS Systems Manager Session Manager session:

```sh
sudo bash bootstrap-agent-host.sh
```

The script is safe to run repeatedly: `dnf install` leaves an installed package
in place, and `systemctl enable --now` converges the Docker service to enabled
and active. It also verifies the Docker binary, service, and daemon before
reporting the installed version, service state, and machine architecture.

No interactive user, including `ssm-user`, is added to the `docker` group.
Docker group membership is effectively root-level access and should not be
granted as a bootstrap convenience. Hermes deployment, its service identity,
and sandbox isolation are separate later stages.
