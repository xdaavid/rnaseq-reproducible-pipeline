# Running on Windows with WSL2

Nextflow targets POSIX-compatible systems. On Windows, run this repository
inside Windows Subsystem for Linux 2 (WSL2), not directly from PowerShell.

## 1. Install WSL2

Open an administrator PowerShell window:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if requested, open Ubuntu, and complete the initial user
setup.

## 2. Install Java and basic tools

Inside the Ubuntu terminal:

```bash
sudo apt update
sudo apt install -y openjdk-17-jre-headless curl unzip
```

Install Nextflow:

```bash
curl -s https://get.nextflow.io | bash
sudo install nextflow /usr/local/bin/nextflow
nextflow -version
```

## 3. Choose an execution backend

For the Docker profile, install Docker Desktop, enable its WSL2 backend, and
turn on integration for the Ubuntu distribution. Verify from Ubuntu:

```bash
docker run --rm hello-world
```

Alternatively, use the `conda` profile after installing Conda or Mamba inside
WSL2.

## 4. Work inside the Linux filesystem

For better performance, clone the repository below the WSL home directory
instead of running it from `/mnt/c`:

```bash
cd ~
git clone https://github.com/xdaavid/rnaseq-reproducible-pipeline.git
cd rnaseq-reproducible-pipeline
```

## 5. Verify and run

Check workflow wiring without downloading the bioinformatics containers:

```bash
nextflow run main.nf -profile test -stub-run
```

Then run a real analysis:

```bash
nextflow run main.nf \
  -profile docker \
  --input /data/samplesheet.csv \
  --transcriptome /data/transcripts.fa \
  --outdir results
```

Use Linux-style paths inside the sample sheet. Files stored on the Windows
`C:` drive are visible under `/mnt/c`, although keeping active Nextflow work
directories in the Linux filesystem is recommended.

## Troubleshooting

- `nextflow: command not found`: confirm `/usr/local/bin` is in `PATH`.
- `docker: permission denied`: restart WSL and Docker Desktop, then verify
  Docker Desktop integration for the selected distribution.
- Windows paths are rejected: replace `C:\...` with `/mnt/c/...`, or copy the
  data into the WSL filesystem.
- A run was interrupted: repeat the same command with `-resume`.

See the official
[Nextflow development environment documentation](https://nextflow.io/docs/stable/developer-env.html)
for the current platform requirements.
