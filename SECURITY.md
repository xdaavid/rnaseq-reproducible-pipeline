# Security policy

## Supported version

Security fixes are applied to the latest release on the default branch.

## Reporting

Do not open a public issue containing patient information, sequencing data, or
credentials. Report vulnerabilities privately through GitHub security
advisories when this repository is published.

## Data handling

This workflow does not upload data by itself. Container registries may be
contacted to download images. Users are responsible for:

- Running sensitive datasets in an approved environment.
- Reviewing container registry and cloud policies.
- Keeping credentials outside sample sheets and configuration files.
- Avoiding publication of human genomic data in issues or test fixtures.
