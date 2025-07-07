# General Hardware Acceleration with CUDA

So far we've focused on machine learning examples, but CUDA hardware accelerated workflows extend far beyond AI/ML.

## CuPy Example

Perhaps one of the most well known CUDA accelerated array programming libraries in [CuPy](https://cupy.dev/), which is designed to have APIs that are highly compatible with NumPy and SciPy so that people can think in the common Scientific Python idioms while still leveraging CUDA.

### Constructing the workspace

CuPy is distributed on PyPI and on conda-forge, so we can create a Pixi workspace that supports its CUDA requirements and then adds CuPy as well.

:::: {tip} Construct the CuPy workspace

:::{code} toml
:filename: pixi.toml
[workspace]
channels = ["conda-forge"]
name = "cupy-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[system-requirements]
cuda = "12"

[target.linux-64.dependencies]
cupy = ">=13.4.1,<14"
:::

::: {hint} Walkthrough if needed
:class: dropdown

Initialize the workspace

```bash
pixi init ~/reproducible-ml-scipy-2025/cupy-example
cd ~/reproducible-ml-scipy-2025/cupy-example
```

add all the platforms we'd like people to be able to develop for, even though this will be run on `linux-64`

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```

and add the CUDA system requirements

```bash
pixi workspace system-requirements add cuda 12
```

Then add Python as a common dependency to help ensure the latest Python is picked up

```bash
pixi add python
```
```
✔ Added python >=3.13.5,<3.14
```

and then add the CuPy dependencies for the target platform of `linux-64`.

```bash
pixi add --platform linux-64 cupy
```
```
✔ Added cupy >=13.4.1,<14
Added these only for platform(s): linux-64
```

and you should now have the workspace.

:::
::::
