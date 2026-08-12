# Security model

CI builds the final `service-health` runtime image and scans that image with
Trivy. Fixable HIGH and CRITICAL vulnerabilities in operating-system and Python
packages block CI. HIGH and CRITICAL findings without an available fix are
reported but do not automatically block CI; unfixed CRITICAL findings require
human review before merge. An end-of-life operating system blocks CI.

## CPython coverage limitation

The CycloneDX SBOM inventories the CPython runtime. However, the official
Python image installs CPython under `/usr/local`, rather than as a Debian or
Python package, so the interpreter itself is not currently covered by the
Trivy vulnerability gate. A green CI run therefore does not prove that the
CPython interpreter has no known vulnerabilities.

Current mitigating controls are to:

- use a maintained official Python base image;
- rebuild the image frequently;
- keep the Python and base-image version current; and
- review Python security advisories when updating the runtime.

## SBOM and supply-chain limitations

The SBOM is an inventory of detected components, not an attestation or proof
that the image is secure or complete. The image is not currently signed or
promoted by immutable digest, and its base-image references are not currently
digest-pinned.
