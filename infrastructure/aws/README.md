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

## Hermes setup

`setup-hermes.sh` runs the official Hermes setup wizard interactively in a
temporary container. Run it as root on the agent host through an AWS Systems
Manager Session Manager session:

```sh
sudo bash setup-hermes.sh
```

The script pins the immutable image
`nousresearch/hermes-agent@sha256:f5efd66dfdc0a434adf20af4030ac856eea6631405f7d44a827c6d7a76bf083e`
so reviewed setup executions cannot silently change when a mutable image tag is
updated. It invokes the wizard with:

```sh
docker run --rm -it \
  --volume /var/lib/hermes:/opt/data \
  nousresearch/hermes-agent@sha256:f5efd66dfdc0a434adf20af4030ac856eea6631405f7d44a827c6d7a76bf083e \
  setup
```

In the currently pinned image, the Hermes Blank Slate preset still enables the
`terminal`, `file`, `vision`, and `skills` CLI toolsets. After the setup wizard
exits successfully, the wrapper therefore explicitly enforces the tested
model-only baseline with a second temporary container:

```sh
docker run --rm \
  --volume /var/lib/hermes:/opt/data \
  nousresearch/hermes-agent@sha256:f5efd66dfdc0a434adf20af4030ac856eea6631405f7d44a827c6d7a76bf083e \
  hermes tools disable terminal file vision skills --platform cli
```

No tool is enabled by the wrapper. Tool and sandbox capabilities will be
enabled deliberately in a later security stage rather than inherited from the
preset.

Hermes configuration, credentials, and state written to `/opt/data` persist on
the host in `/var/lib/hermes`. Treat that host directory as sensitive: do not
print, copy into the repository, or expose its contents. The script creates it
with restrictive permissions and does not impose a host UID or GID ownership
scheme on Hermes.

Only the Hermes data directory is mounted. The Docker socket and host repository
are not mounted, no ports are published, and host networking or extra container
privileges are not enabled.

This setup step does not deploy a persistent Hermes gateway or system service.
Gateway/service deployment is a later stage. Sandbox and egress isolation also
remain required security work before any meaningful autonomous execution.
