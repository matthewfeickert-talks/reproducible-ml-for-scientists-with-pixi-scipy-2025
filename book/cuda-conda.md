# Introduction to CUDA conda packages

## CUDA

CUDA (Compute Unified Device Architecture) [is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs)](https://developer.nvidia.com/cuda-zone).
The CUDA ecosystem provides software developer software development kits (SDK) with APIs to CUDA that allow for software developers to write hardware accelerated programs with CUDA in various languages for NVIDIA GPUs.
CUDA supports a number of languages including C, C++, Fortran, Python, and Julia.
While there are other types of hardware acceleration development platforms, as of 2025 CUDA is the most abundant platform for scientific computing that uses GPUs and effectively the default choice for major machine learning libraries and applications.

CUDA is closed source and proprietary to NVIDIA, which means that NVIDIA has historically limited the download access of the CUDA toolkits and drivers to registered NVIDIA developers (while keeping the software free (monetarily) to use).
CUDA then required a [multi-step installation process](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) with manual steps and decisions based on the target platform and particular CUDA version.
This meant that when CUDA enabled environments were setup on a particular machine they were powerful and optimized, but brittle to change and could easily be broken if system wide updates (like for security fixes) occurred.
CUDA software environments were bespoke and not many scientists understood how to construct and curate them.

## CUDA packages on conda-forge

In [late 2018](https://github.com/conda-forge/conda-forge.github.io/issues/687) to better support the scientific developer community, NVIDIA started to release components of the CUDA toolkits on the [`nvidia` conda channel](https://anaconda.org/nvidia).
This provided the first access to start to create conda environments where the versions of different CUDA tools could be directly specified and downloaded.
However, all of this work was being done internally in NVIDIA and as it was on a separate channel it was less visible and it still required additional knowledge to work with.
In [2023](https://youtu.be/WgKwlGgVzYE?si=hfyAo6qLma8hnJ-N), NVIDIA's open source team began to move the release of CUDA conda packages from the `nvidia` channel to conda-forge, making it easier to discover and allowing for community support.
With significant advancements in system driver specification support, CUDA 12 became the first version of CUDA to be released as conda packages through conda-forge and included all CUDA libraries from the [CUDA compiler `nvcc`](https://github.com/conda-forge/cuda-nvcc-feedstock) to the [CUDA development libraries](https://github.com/conda-forge/cuda-libraries-dev-feedstock).
They also released [CUDA metapackages](https://github.com/conda-forge/cuda-feedstock/) that allowed users to easily describe the version of CUDA they required (e.g. `cuda-version=12.5`) and the CUDA conda packages they wanted (e.g. `cuda`).
This significantly improved the ability for researchers to easily create CUDA accelerated computing environments.

This is all possible via use of the `__cuda` [virtual conda package](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html), which is determined automatically by conda package managers from the hardware information associated with the machine the package manager is installed on.

With Pixi, a user can get this information with [`pixi info`](https://pixi.sh/latest/advanced/explain_info_command/), which could have output that looks something like

```bash
pixi info
```
```output
System
------------
       Pixi version: 0.48.0
           Platform: linux-64
   Virtual packages: __unix=0=0
                   : __linux=6.8.0=0
                   : __glibc=2.35=0
                   : __cuda=12.4=0
                   : __archspec=1=skylake
          Cache dir: /home/<username>/.cache/rattler/cache
       Auth storage: /home/<username>/.rattler/credentials.json
   Config locations: No config files found

Global
------------
            Bin dir: /home/<username>/.pixi/bin
    Environment dir: /home/<username>/.pixi/envs
       Manifest dir: /home/<username>/.pixi/manifests/pixi-global.toml

```

## CUDA use with Pixi

To be able to effectively use CUDA conda packages with Pixi, we make use of Pixi's [system requirement workspace table](https://pixi.sh/latest/workspace/system_requirements/), which specifies the **minimum**  system specifications needed to install and run a Pixi workspace's environments.

To do this for CUDA, we just add the minimum supported CUDA version (based on the host machine's NVIDIA driver API) we want to support to the table.

Example:

```toml
[system-requirements]
cuda = "12"  # Replace "12" with the specific CUDA version you intend to use
```

This ensures that packages depending on `__cuda >= {version}` are resolved correctly.

::: {important} Further references

[Wolf Vollprecht](https://github.com/wolfv) of prefix.dev GmbH has written two blog posts on topics covered in this section that provide an excellent overview and summary.
You are highly encouraged to read them!

* [What is a Conda package, actually?](https://prefix.dev/blog/what-is-a-conda-package) (2025-06-11)
* [Virtual Packages in the Conda ecosystem](https://prefix.dev/blog/virtual-packages-in-the-conda-ecosystem) (2025-06-18)

:::
