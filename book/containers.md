# Deploying Pixi environments with Linux containers

## Deploying Pixi environments

We now know how to create Pixi workspaces that contain environments that can support CUDA enabled code.
However, unless your production machine learning environment is a lab desktop with GPUs and lots of disk [^footnote1] that you can install Pixi on and run your code then we still need to be able to get our Pixi environments to our production machines.

There is one very straightforward solution:

1. Version control your Pixi manifest and Pixi lock files with your analysis code with a version control system (e.g. Git).
1. Clone your repository to the machine that you want to run on.
1. Install Pixi onto that machine.
1. Install the locked Pixi environment that you want to use.
1. Execute your code in the installed environment.

That's a nice and simple story, and it can work!
However, in most realistic scenarios the worker compute nodes that are executing code share resource pools of storage and memory and are regulated to smaller allotments of both.
CUDA binaries are relatively large files and amount of memory and storage to just unpack them can easily exceed a standard 2 GB memory limit on most high throughput computing (HTC) facility worker nodes.
This also requires direct access to the public internet, or for you to setup a [S3 object store](https://pixi.sh/latest/deployment/s3/) behind your compute facility's firewall with all of your conda packages mirrored into it.
In many scenarios, public internet access at HTC and high performance computing (HPC) facilities is limited to only a select "allow list" of websites or it might be fully restricted for users.

## Building Linux containers with Pixi environments

A more standard and robust way of distributing computing environments is the use of [Linux container](https://pixi.sh/latest/deployment/container/) technology &mdash; like Docker or Apptainer.

[^footnote1]: Which is a valid and effective solution.

::: {note} Conceptualizing the role of Linux containers

Linux containers are powerful technologies that allow for arbitrary software environments to be distributed as a single binary.
However, it is important to **not** think of Linux containers as _packaging_ technologies (like conda packages) but as _distribution_ technologies.
When you build a Linux container you provide a set of imperative commands as a build script that constructs different layers of the container.
When the build is finished, all layers of the build are compressed together to form a container image binary that can be distributed through Linux container image registries.

Packaging technologies allow for defining requirements and constraints on a unit of software that we call a "package".
Packages can be installed together and their metadata allows them to be composed programmatically into software environments.

Linux containers take defined software environments and instantiate them by installing them into the container image during the build and then distribute that entire computing environment for a **single platform**.

:::

::: {seealso} Resources on Linux containers
:class: dropdown

Linux containers are a full topic unto themselves and we won't cover them in this lesson.
If you're not familiar with Linux containers, here are introductory resources:

* [Reproducible Computational Environments Using Containers: Introduction to Docker](https://carpentries-incubator.github.io/docker-introduction/), a [The Carpentries Incubator](https://github.com/carpentries-incubator/proposals/#the-carpentries-incubator) lesson
* [Introduction to Docker and Podman](https://hsf-training.github.io/hsf-training-docker/index.html) by the [High Energy Physics Software Foundation](https://hepsoftwarefoundation.org/)
* [Reproducible computational environments using containers: Introduction to Apptainer](https://carpentries-incubator.github.io/apptainer-introduction/), a [The Carpentries Incubator](https://github.com/carpentries-incubator/proposals/#the-carpentries-incubator) lesson

:::

Docker is a very common Linux container runtime technology and Linux container builder.
We can use [`docker build`](https://docs.docker.com/build/) to build a Linux container from a `Dockerfile` instruction file.
Luckily, to install Pixi environments into Docker container images there is **effectively only one `Dockerfile` recipe** that needs to be used, and then can be reused across projects.

::: {note} Moving tutorial files

To use it later, move `torch_detect_GPU.py` from the end of the CUDA conda packages examples to `./app/torch_detect_GPU.py`.

```bash
mkdir -p app
mv torch_detect_GPU.py app/
```

:::

```dockerfile
FROM ghcr.io/prefix-dev/pixi:noble AS build

WORKDIR /app
COPY . .
ENV CONDA_OVERRIDE_CUDA=<cuda version>
RUN pixi install --locked --environment <environment>
RUN echo "#!/bin/bash" > /app/entrypoint.sh && \
    pixi shell-hook --environment <environment> -s bash >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh

FROM ghcr.io/prefix-dev/pixi:noble AS final

WORKDIR /app
COPY --from=build /app/.pixi/envs/<environment> /app/.pixi/envs/<environment>
COPY --from=build /app/pixi.toml /app/pixi.toml
COPY --from=build /app/pixi.lock /app/pixi.lock
# The ignore files are needed for 'pixi run' to work in the container
COPY --from=build /app/.pixi/.gitignore /app/.pixi/.gitignore
COPY --from=build /app/.pixi/.condapackageignore /app/.pixi/.condapackageignore
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh
COPY ./app /app/src

EXPOSE <PORT>
ENTRYPOINT [ "/app/entrypoint.sh" ]
```

:::: {important} Dockerfile walkthrough
:class: dropdown

Let's step through this to understand what's happening.
`Dockerfile`s (intentionally) look very shell script like, and so we can read most of it as if we were typing the commands directly into a shell (e.g. Bash).

* The `Dockerfile` assumes it is being built from a version control repository where any code that it will need to execute later exists under the repository's `src/` directory and the Pixi workspace's `pixi.toml` manifest file and `pixi.lock` lock file exist at the top level of the repository.
* The entire repository contents are [`COPY`](https://docs.docker.com/reference/dockerfile/#copy)ed from the container build context into the `/app` directory of the container build.

```dockerfile
WORKDIR /app
COPY . .
```

* It is not reasonable to expect that the container image build machine contains GPUs.
To have Pixi still be able to install an environment that uses CUDA when there is no virtual package set the `__cuda` [override environment variable `CONDA_OVERRIDE_CUDA`](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-virtual.html#overriding-detected-packages).

```dockerfile
ENV CONDA_OVERRIDE_CUDA=<cuda version>
```

* The `Dockerfile` uses a [multi-stage](https://docs.docker.com/build/building/multi-stage/) build where it first installs the target environment `<environment>` and then creates an [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint) script using [`pixi shell-hook`](https://pixi.sh/latest/reference/cli/pixi/shell-hook/) to automatically activate the environment when the container image is run.

```dockerfile
RUN pixi install --locked --environment <environment>
RUN echo "#!/bin/bash" > /app/entrypoint.sh && \
    pixi shell-hook --environment <environment> -s bash >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh
```

* The next stage of the build starts from a new container instance and then [`COPY`](https://docs.docker.com/reference/dockerfile/#copy)s the installed environment and files **from** the build container image into the production container image.
This can reduce the total size of the final container image if there were additional build tools that needed to get installed in the build phase that aren't required for runtime in production.

```dockerfile
FROM ghcr.io/prefix-dev/pixi:noble AS final

WORKDIR /app
COPY --from=build /app/.pixi/envs/<environment> /app/.pixi/envs/<environment>
COPY --from=build /app/pixi.toml /app/pixi.toml
COPY --from=build /app/pixi.lock /app/pixi.lock
# The ignore files are needed for 'pixi run' to work in the container
COPY --from=build /app/.pixi/.gitignore /app/.pixi/.gitignore
COPY --from=build /app/.pixi/.condapackageignore /app/.pixi/.condapackageignore
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh
```

* Code that is specific to application purposes (e.g. environment diagnostics) from the repository is [`COPY`](https://docs.docker.com/reference/dockerfile/#copy)ed into the final container image as well

```dockerfile
COPY ./app /app/src
```

::: {caution} Knowing what code to copy

Generally you do **not** want to containerize your development source code, as you'd like to be able to quickly iterate on it and have it be transferred into a Linux container to be evaluated.

You **do** want to containerize your development source code if you'd like to archive it as an executable into the future.

:::

* Any ports that need to be exposed for i/o are exposed

```dockerfile
EXPOSE <PORT>
```

* The [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint) script is set for activation


```dockerfile
ENTRYPOINT [ "/app/entrypoint.sh" ]
```

::::

With this `Dockerfile` the container image can then be built with [`docker build`](https://docs.docker.com/reference/cli/docker/buildx/build/).

::: {tip} Write a `Dockerfile` that will create a Linux container with the `gpu` environment from the previous exercises Pixi workspace.
:class: dropdown

```dockerfile
FROM ghcr.io/prefix-dev/pixi:noble AS build

WORKDIR /app
COPY . .
ENV CONDA_OVERRIDE_CUDA=12
RUN pixi install --locked --environment gpu
RUN echo "#!/bin/bash" > /app/entrypoint.sh && \
    pixi shell-hook --environment gpu -s bash >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh

FROM ghcr.io/prefix-dev/pixi:noble AS final

WORKDIR /app
COPY --from=build /app/.pixi/envs/gpu /app/.pixi/envs/gpu
COPY --from=build /app/pixi.toml /app/pixi.toml
COPY --from=build /app/pixi.lock /app/pixi.lock
# The ignore files are needed for 'pixi run' to work in the container
COPY --from=build /app/.pixi/.gitignore /app/.pixi/.gitignore
COPY --from=build /app/.pixi/.condapackageignore /app/.pixi/.condapackageignore
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
```

:::

## Automation with GitHub Actions workflows

In the personal GitHub repository that we've been working in create a GitHub Actions workflow directory

```bash
mkdir -p .github/workflows
```

and then add the following workflow file as `.github/workflows/docker.yaml`

```yaml
name: Docker Images

on:
  push:
    branches:
      - main
    tags:
      - 'v*'
    paths:
      - 'cuda-exercise/pixi.toml'
      - 'cuda-exercise/pixi.lock'
      - 'cuda-exercise/Dockerfile'
      - 'cuda-exercise/.dockerignore'
      - 'cuda-exercise/app/**'
  pull_request:
    paths:
      - 'cuda-exercise/pixi.toml'
      - 'cuda-exercise/pixi.lock'
      - 'cuda-exercise/Dockerfile'
      - 'cuda-exercise/.dockerignore'
      - 'cuda-exercise/app/**'
  release:
    types: [published]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions: {}

jobs:
  docker:
    name: Build and publish images
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            ghcr.io/${{ github.repository }}
          # generate Docker tags based on the following events/attributes
          tags: |
            type=raw,value=noble-cuda-12.9
            type=raw,value=latest
            type=sha

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Test build
        id: docker_build_test
        uses: docker/build-push-action@v6
        with:
          context: cuda-exercise
          file: cuda-exercise/Dockerfile
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          pull: true

      - name: Deploy build
        id: docker_build_deploy
        uses: docker/build-push-action@v6
        with:
          context: cuda-exercise
          file: cuda-exercise/Dockerfile
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          pull: true
          push: ${{ github.event_name != 'pull_request' }}
```

This will build your Dockerfile in GitHub Actions CI into a [`linux/amd64` platform](https://docs.docker.com/build/building/multi-platform/) Docker container image and then deploy it to the [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (`ghcr`) associated with your repository.

When your container image has finished building, you can view it and its tags on GitHub at: `https://github.com/<your GitHub username>/reproducible-ml-scipy-2025/pkgs/container/reproducible-ml-scipy-2025`

## Using the containerized environment on Brev

::: {note} Why use containers on Brev?

This segment of the tutorial is meant to highlight how to use containerized software environments **at different computing centers or resources**.
In the case of Brev, _this isn't needed_, as the login node and the compute note are the same, but with an HTC or HPC environment where you need to transport your computing environment to the worker nodes, having containers significantly simplifies the process.

:::

To verify that things are visible to other computers, install the Linux container utility [`crane`](https://github.com/google/go-containerregistry/tree/main/cmd/crane) with `pixi global`

```bash
pixi global install crane
```
```
└── crane: 0.20.5 (installed)
    └─ exposes: crane
```

and then use [`crane ls`](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_ls.md) to list all of the container images in your container registry for the particular image

```bash
crane ls ghcr.io/<your GitHub username>/reproducible-ml-scipy-2025
```

Our Brev environment already has Docker installed on it, so we can now pull down the Docker container using [`docker pull`](https://docs.docker.com/reference/cli/docker/image/pull/).

```bash
docker pull ghcr.io/<your GitHub username>/reproducible-ml-scipy-2025:sha-<the commit sha short>
```

Once that is finished we can confirm that the container image exists in our local container registry with

```bash
docker images
```

We can then use [`docker run`](https://docs.docker.com/reference/cli/docker/container/run/) to start and then attach a container instance with our software environment active inside of it

```bash
docker run \
    --rm \
    -ti \
    --gpus all \
    -v $PWD:/work \
    ghcr.io/<your GitHub username>/reproducible-ml-scipy-2025:sha-<the commit sha short> bash
```

::: {important} `docker run` walkthrough
:class: dropdown

Let's step through the `docker run` command to understand what's happening.

* [`--rm`](https://docs.docker.com/reference/cli/docker/container/run/#rm) : Automatically remove the container and its associated anonymous volumes when it exits
* [`-t, --tty`](https://docs.docker.com/reference/cli/docker/container/run/#tty) : Allocate a pseudo-TTY (for interactive use)
* [`-i, --interactive`](https://docs.docker.com/reference/cli/docker/container/run/#interactive) : Keep STDIN open even if not attached (for interactive use)
* [`--gpus`](https://docs.docker.com/reference/cli/docker/container/run/#gpus) : GPU devices to add to the container (`all` to pass all GPUs)
* [`-v, --volume`](https://docs.docker.com/reference/cli/docker/container/run/#volume) : Bind mount a volume from `<path on host machine>:<path inside Docker container>`

:::

::: {important} Further references

For today we're focusing on Docker containers, but if you run your workflows at High-Throughput Computing (HTC) or High-Performance Computing (HPC) centers with orchestration systems like HTCondor or SLURM you will probably be restricted to using a different Linux container system called Apptainer.

The [Reproducible Machine Learning Workflows for Scientists](https://carpentries-incubator.github.io/reproducible-ml-workflows/) Carpentries Incubator lesson has [further information and examples for using Apptainer with these workflows](https://carpentries-incubator.github.io/reproducible-ml-workflows/pixi_deployment.html).

:::
