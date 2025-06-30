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
```
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

To demonstrate this a bit more explicitly, we can create a minimal project

```bash
pixi init ~/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-example
cd ~/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-example
```
```
✔ Created /home/<username>/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-example/pixi.toml
```

where we specify a `cuda` system requirement

```bash
pixi workspace system-requirements add cuda 12
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-example"
platforms = ["linux-64"]
version = "0.1.0"

[system-requirements]
cuda = "12"

[tasks]

[dependencies]
```

::: {caution} `system-requirements` table can't be target specific

As of [Pixi `v0.48.2`](https://github.com/prefix-dev/pixi/releases/tag/v0.48.2), [the `system-requirements` table can't be target specific](https://github.com/prefix-dev/pixi/issues/2714).
To work around this, if you're on a platform that doesn't support the `system-requirements` it will ignore them without erroring unless they are required for the platform specific packages or actions you have.
So, for example, you can have `osx-arm64` as a platform and a `system-requirements` of `cuda = "12"` defined

```toml
[workspace]
...
platforms = ["linux-64"]
...

[system-requirements]
cuda = "12"
```

Pixi will ignore that requirement unless you try to use CUDA packages in `osx-arm64` environments.

:::

and then install the [`cuda-version` metapacakge](https://github.com/conda-forge/cuda-version-feedstock/blob/main/recipe/README.md)

```bash
pixi add "cuda-version 12.9.*"
```
```
✔ Added cuda-version 12.9.*
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-example"
platforms = ["linux-64"]
version = "0.1.0"

[system-requirements]
cuda = "12"

[tasks]

[dependencies]
cuda-version = "12.9.*"
```

If we look at the metadata installed by the `cuda-version` package (the only thing it does)

```bash
cat .pixi/envs/default/conda-meta/cuda-version-*.json
```
```json
{
  "build": "h4f385c5_3",
  "build_number": 3,
  "constrains": [
    "cudatoolkit 12.9|12.9.*",
    "__cuda >=12"
  ],
  "depends": [],
  "license": "LicenseRef-NVIDIA-End-User-License-Agreement",
  "md5": "b6d5d7f1c171cbd228ea06b556cfa859",
  "name": "cuda-version",
  "noarch": "generic",
  "sha256": "5f5f428031933f117ff9f7fcc650e6ea1b3fef5936cf84aa24af79167513b656",
  "size": 21578,
  "subdir": "noarch",
  "timestamp": 1746134436166,
  "version": "12.9",
  "fn": "cuda-version-12.9-h4f385c5_3.conda",
  "url": "https://conda.anaconda.org/conda-forge/noarch/cuda-version-12.9-h4f385c5_3.conda",
  "channel": "https://conda.anaconda.org/conda-forge/",
  "extracted_package_dir": "/home/<username>/.cache/rattler/cache/pkgs/cuda-version-12.9-h4f385c5_3",
  "files": [],
  "paths_data": {
    "paths_version": 1,
    "paths": []
  },
  "link": {
    "source": "/home/<username>/.cache/rattler/cache/pkgs/cuda-version-12.9-h4f385c5_3",
    "type": 1
  }
}
```

we see that it now enforces constraints on the versions of `cudatoolkit` that can be installed as well as the required `__cuda` virtual package provided by the system

```json
{
  ...
  "constrains": [
    "cudatoolkit 12.9|12.9.*",
    "__cuda >=12"
  ],
  ...
}
```


::: {important} Use the `feature` table to solve environment that your platform doesn't support

CUDA is supported only by NVIDIA GPUs, which means that macOS operating system platforms (`osx-64`, `osx-arm64`) can't support it.
Similarly, if you machine doesn't have an NVIDIA GPU, then the `__cuda` virtual package won't exist and installs of CUDA packages will fail.
However, there's many situations in which you want to **solve and environment for a platform that you don't have** and we can do this for CUDA as well.

If we make the Pixi workspace multiplatform

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```
```
✔ Added linux-64
✔ Added osx-arm64
✔ Added win-64
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
```

We can then use Pixi's [platform specific `target` tables](https://pixi.sh/latest/reference/pixi_manifest/#the-target-table) to add dependencies for an environment to only a specific platform.
So, if we know that a dependency only exists for platform <platform> then we can have Pixi add it for only that platform with

```bash
pixi add --platform <platform> <dependency>
```

:::

This now means that if we ask for any CUDA enbabled packages, we will get ones that are built to support `cudatoolkit` `v12.9.*`

```bash
pixi add --platform linux-64 cuda
```
```
✔ Added cuda >=12.9.1,<13
Added these only for platform(s): linux-64
```

```bash
pixi list --platform linux-64 cuda
```
```
Package                      Version  Build       Size       Kind   Source
cuda                         12.9.1   ha804496_0  26.7 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-cccl_linux-64           12.9.27  ha770c72_0  1.1 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-command-line-tools      12.9.1   ha770c72_0  20 KiB     conda  https://conda.anaconda.org/conda-forge/
cuda-compiler                12.9.1   hbad6d8a_0  20.2 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-crt-dev_linux-64        12.9.86  ha770c72_1  92.2 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-crt-tools               12.9.86  ha770c72_1  28.2 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-cudart                  12.9.79  h5888daf_0  22.7 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-cudart-dev              12.9.79  h5888daf_0  23.1 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-cudart-dev_linux-64     12.9.79  h3f2d84a_0  380 KiB    conda  https://conda.anaconda.org/conda-forge/
cuda-cudart-static           12.9.79  h5888daf_0  22.7 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-cudart-static_linux-64  12.9.79  h3f2d84a_0  1.1 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-cudart_linux-64         12.9.79  h3f2d84a_0  192.6 KiB  conda  https://conda.anaconda.org/conda-forge/
cuda-cuobjdump               12.9.82  hbd13f7d_0  237.5 KiB  conda  https://conda.anaconda.org/conda-forge/
cuda-cupti                   12.9.79  h9ab20c4_0  1.8 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-cupti-dev               12.9.79  h9ab20c4_0  4.4 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-cuxxfilt                12.9.82  hbd13f7d_0  211.4 KiB  conda  https://conda.anaconda.org/conda-forge/
cuda-driver-dev              12.9.79  h5888daf_0  22.5 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-driver-dev_linux-64     12.9.79  h3f2d84a_0  36.8 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-gdb                     12.9.79  ha677faa_0  378.2 KiB  conda  https://conda.anaconda.org/conda-forge/
cuda-libraries               12.9.1   ha770c72_0  20 KiB     conda  https://conda.anaconda.org/conda-forge/
cuda-libraries-dev           12.9.1   ha770c72_0  20.1 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nsight                  12.9.79  h7938cbb_0  113.2 MiB  conda  https://conda.anaconda.org/conda-forge/
cuda-nvcc                    12.9.86  hcdd1206_1  24.3 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvcc-dev_linux-64       12.9.86  he91c749_1  13.8 MiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvcc-impl               12.9.86  h85509e4_1  26.6 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvcc-tools              12.9.86  he02047a_1  26.2 MiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvcc_linux-64           12.9.86  he0b4e1d_1  26.2 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvdisasm                12.9.88  hbd13f7d_0  5.3 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-nvml-dev                12.9.79  hbd13f7d_0  139.1 KiB  conda  https://conda.anaconda.org/conda-forge/
cuda-nvprof                  12.9.79  hcf8d014_0  2.5 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-nvprune                 12.9.82  hbd13f7d_0  69.3 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvrtc                   12.9.86  h5888daf_0  64.1 MiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvrtc-dev               12.9.86  h5888daf_0  35.7 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvtx                    12.9.79  h5888daf_0  28.6 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvvm-dev_linux-64       12.9.86  ha770c72_1  26.3 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvvm-impl               12.9.86  he02047a_1  20.4 MiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvvm-tools              12.9.86  he02047a_1  23.1 MiB   conda  https://conda.anaconda.org/conda-forge/
cuda-nvvp                    12.9.79  hbd13f7d_0  104.3 MiB  conda  https://conda.anaconda.org/conda-forge/
cuda-opencl                  12.9.19  h5888daf_0  30 KiB     conda  https://conda.anaconda.org/conda-forge/
cuda-opencl-dev              12.9.19  h5888daf_0  95.1 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-profiler-api            12.9.79  h7938cbb_0  23 KiB     conda  https://conda.anaconda.org/conda-forge/
cuda-runtime                 12.9.1   ha804496_0  19.9 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-sanitizer-api           12.9.79  hcf8d014_0  8.6 MiB    conda  https://conda.anaconda.org/conda-forge/
cuda-toolkit                 12.9.1   ha804496_0  20 KiB     conda  https://conda.anaconda.org/conda-forge/
cuda-tools                   12.9.1   ha770c72_0  19.9 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-version                 12.9     h4f385c5_3  21.1 KiB   conda  https://conda.anaconda.org/conda-forge/
cuda-visual-tools            12.9.1   ha770c72_0  19.9 KiB   conda  https://conda.anaconda.org/conda-forge/
```

To "prove" that this works, we can ask for the CUDA enabled version of PyTorch

```bash
pixi add --platform linux-64 pytorch-gpu
```
```
✔ Added pytorch-gpu >=2.7.1,<3
Added these only for platform(s): linux-64
```
```bash
pixi list --platform linux-64 torch
```
```
Package      Version  Build                           Size       Kind   Source
libtorch     2.7.1    cuda126_mkl_hc2b21a2_300        532.5 MiB  conda  https://conda.anaconda.org/conda-forge/
pytorch      2.7.1    cuda126_mkl_py312_h30b5a27_300  28 MiB     conda  https://conda.anaconda.org/conda-forge/
pytorch-gpu  2.7.1    cuda126_mkl_ha999a5f_300        46.6 KiB   conda  https://conda.anaconda.org/conda-forge/
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
cuda-version = "12.9.*"

[system-requirements]
cuda = "12"

[target.linux-64.dependencies]
cuda = ">=12.9.1,<13"
pytorch-gpu = ">=2.7.1,<3"
```


::: {note} Redundancy in example

Note that we added the `cuda` package here for demonstraton purposes, but we didn't _need_ to as it would already be installed as a dependency of `pytorch-gpu`.

```bash
cat .pixi/envs/default/conda-meta/pytorch-gpu-*.json
```
```json
{
  "build": "cuda126_mkl_ha999a5f_300",
  "build_number": 300,
  "depends": [
    "pytorch 2.7.0 cuda*_mkl*300"
  ],
  "license": "BSD-3-Clause",
  "license_family": "BSD",
  "md5": "84ecafc34c6f8933c2c9b00204832e38",
  "name": "pytorch-gpu",
  "sha256": "e1162a51e77491abae15f6b651ba8f064870181d57d40f9168747652d0f70cb0",
  "size": 47219,
  "subdir": "linux-64",
  "timestamp": 1746288556375,
  "version": "2.7.0",
  "fn": "pytorch-gpu-2.7.0-cuda126_mkl_ha999a5f_300.conda",
  "url": "https://conda.anaconda.org/conda-forge/linux-64/pytorch-gpu-2.7.0-cuda126_mkl_ha999a5f_300.conda",
  "channel": "https://conda.anaconda.org/conda-forge/",
  "extracted_package_dir": "/home/<username>/.cache/rattler/cache/pkgs/pytorch-gpu-2.7.0-cuda126_mkl_ha999a5f_300",
  "files": [],
  "paths_data": {
    "paths_version": 1,
    "paths": []
  },
  "link": {
    "source": "/home/<username>/.cache/rattler/cache/pkgs/pytorch-gpu-2.7.0-cuda126_mkl_ha999a5f_300",
    "type": 1
  }
}
```

:::

and **if on the supported `linux-64` platform with a valid `__cuda` virtual pacakge** (like we are with Brev) check that it can see and find GPUs

```python
# torch_detect_GPU.py
import torch
from torch import cuda

if __name__ == "__main__":
    if torch.backends.cuda.is_built():
        print(f"PyTorch build CUDA version: {torch.version.cuda}")
        print(f"PyTorch build cuDNN version: {torch.backends.cudnn.version()}")
        print(f"PyTorch build NCCL version: {torch.cuda.nccl.version()}")

        print(f"\nNumber of GPUs found on system: {cuda.device_count()}")

    if cuda.is_available():
        print(f"\nActive GPU index: {cuda.current_device()}")
        print(f"Active GPU name: {cuda.get_device_name(cuda.current_device())}")
    elif torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        print(f"PyTorch has active GPU: {mps_device}")
    else:
        print(f"PyTorch has no active GPU")
```

```bash
pixi run python torch_detect_GPU.py
```
```
PyTorch build CUDA version: 12.6
PyTorch build cuDNN version: 91001
PyTorch build NCCL version: (2, 27, 3)

Number of GPUs found on system: 1

Active GPU index: 0
Active GPU name: NVIDIA L4
```

:::: {tip} Multi-environment Pixi workspaces

Create a new Pixi workspace that:

* Contains an environment named `cpu` for `linux-64`, `osx-arm64`, and `win-64` that supports the CPU version of PyTorch
* Contains an environment named `gpu` for `linux-64` that supports the GPU version of PyTorch
* Supports CUDA `v12.9`

::: {hint} Solution
:class: dropdown

Create a new workspace

```bash
pixi init ~/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-exercise
cd ~/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-exercise
```
```
✔ Created /home/<username>/reproducible-ml-for-scientists-tutorial-scipy-2025/cuda-exercise/pixi.toml
```

Add support for all the target platforms

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```
```
✔ Added linux-64
✔ Added osx-arm64
✔ Added win-64
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-exercise"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
```

As a common requirement across all environments, let's add Python

```bash
pixi add python
```
```
✔ Added python >=3.13.5,<3.1
```

Now, add `pytorch-cpu` to a `cpu` feature

```bash
pixi add --feature cpu pytorch-cpu
```
```
✔ Added pytorch-cpu
Added these only for feature: cpu
```

and then create a `cpu` environment that contains the `cpu` feature

```bash
pixi workspace environment add --feature cpu cpu
```
```
✔ Added environment cpu
```

and then instantiate the `pytorch-cpu` package with a particular version and solve

```bash
pixi add --feature cpu pytorch-cpu
```
```
✔ Added pytorch-cpu >=2.7.1,<3
Added these only for feature: cpu
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-exercise"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"

[environments]
cpu = ["cpu"]
```

Now, for the GPU environment, add CUDA system-requirements for `linux-64` for the `gpu` feature

```bash
pixi workspace system-requirements add --feature gpu cuda 12
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-exercise"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"

[feature.gpu.system-requirements]
cuda = "12"

[environments]
cpu = ["cpu"]
```

and create a `gpu` environment with the `gpu` feature

```bash
pixi workspace environment add --feature gpu gpu
```
```
✔ Added environment gpu
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-exercise"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"

[feature.gpu.system-requirements]
cuda = "12"

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
```

then add the `cuda-version` metapackage and the `pytorch-gpu` pacakge for `linux-64` to the `gpu` feature

```bash
pixi add --platform linux-64 --feature gpu 'cuda-version 12.9.*' pytorch-gpu
```
```
✔ Added cuda-version 12.9.*
✔ Added pytorch-gpu >=2.7.1,<3
Added these only for platform(s): linux-64
Added these only for feature: gpu
```

```toml
[workspace]
channels = ["conda-forge"]
name = "cuda-exercise"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"

[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.target.linux-64.dependencies]
cuda-version = "12.9.*"
pytorch-gpu = ">=2.7.1,<3"

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
```

One can check the environment differences

```bash
pixi list --environment cpu
pixi list --environment gpu
```

and activate shells with different environments loaded

```bash
pixi shell --environment cpu
```

So in 24 lines of TOML

```bash
wc -l pixi.toml
```
```
24 pixi.toml
```

we created separate CPU and GPU computational environments that are now fully reproducible with the associated `pixi.lock`!

:::
::::


::: {important} Further references

[Wolf Vollprecht](https://github.com/wolfv) of prefix.dev GmbH has written two blog posts on topics covered in this section that provide an excellent overview and summary.
You are highly encouraged to read them!

* [What is a Conda package, actually?](https://prefix.dev/blog/what-is-a-conda-package) (2025-06-11)
* [Virtual Packages in the Conda ecosystem](https://prefix.dev/blog/virtual-packages-in-the-conda-ecosystem) (2025-06-18)

If you would also like a useful summary of different things related to CUDA, check out Modal's summary website of CUDA focused GPU concepts.

* [GPU Glossary](https://modal.com/gpu-glossary), by Modal

:::
