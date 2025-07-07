# General Hardware Acceleration with CUDA

So far we've focused on machine learning examples, but CUDA hardware accelerated workflows extend far beyond AI/ML.

## CuPy Example

Perhaps one of the most well known CUDA accelerated array programming libraries in [CuPy](https://cupy.dev/), which is designed to have APIs that are highly compatible with NumPy and SciPy so that people can think in the common Scientific Python idioms while still leveraging CUDA.

### Constructing the workspace

CuPy is distributed on PyPI and on conda-forge, so we can create a Pixi workspace that supports its CUDA requirements and then adds CuPy as well.

:::: {tip} Construct the CuPy workspace

```{literalinclude} code/cupy-example/pixi.toml
```

::: {hint} Walkthrough if needed
:class: dropdown

Initialize the workspace

```bash
pixi init ~/reproducible-ml-scipy-2025/cupy-example
cd ~/reproducible-ml-scipy-2025/cupy-example
```

add all the platforms we'd like people to be able to develop for, even though this will be run on `linux-64`

```bash
pixi workspace platform add linux-64 win-64
```

and add the CUDA system requirements

```bash
pixi workspace system-requirements add cuda 12
```

Then add the CuPy dependencies for the target platform of `linux-64`.

```bash
pixi add --platform linux-64 python cupy
```
```
✔ Added python >=3.13.5,<3.14
✔ Added cupy >=13.4.1,<14
Added these only for platform(s): linux-64
```

and you should now have the workspace.

:::
::::

which gives us access to CuPy's hardware acceleration, as shown in this [example from the CuPy documentation](https://docs.cupy.dev/en/stable/user_guide/basic.html)

```{literalinclude} code/cupy-example/cupy-example.py
```

```bash
pixi run python cupy-example.py
```
```
NumPy array 3.7416573867739413 on device: cpu
CuPy array 3.7416573867739413 on device: <CUDA Device 0>
```

## CuDF Example

There are other CUDA accelerated libraries for scientific Python as well.
NVIDIA has created the [RAPIDS](https://rapids.ai/) data science collection of libraries for running end-to-end data science pipelines fully on GPUs with CUDA.
One of the libraries is [CuDF](https://docs.rapids.ai/api/cudf/stable/) &mdash; a high level Python library for manipulating DataFrames on the GPU with Pandas-like idioms.

### Constructing the workspace

CuDF is not available on conda-forge, but it is available on the Python Package Index (PyPI) as [`cudf-cu12`](https://pypi.org/project/cudf-cu12/) and on the [`rapidsai` conda channel on Anaconda.org as `cudf`](https://anaconda.org/rapidsai/cudf).
We can install it through either method, but to keep working with conda package, we'll create a workspace that installs it from the `rapdsai` conda channel.

:::: {tip} Construct the CuDF workspace

```{literalinclude} code/cudf-example/pixi.toml
```

::: {hint} Walkthrough if needed
:class: dropdown

Initialize the workspace

```bash
pixi init ~/reproducible-ml-scipy-2025/cudf-example
cd ~/reproducible-ml-scipy-2025/cudf-example
```

As CuDF is available as a conda package only for `linux-64` we'll just set that as the platform

```bash
pixi workspace platform add linux-64
```

and add the CUDA system requirements

```bash
pixi workspace system-requirements add cuda 12
```

and then add the `rapidsai` conda channel but note that for things to work we need it to have **higher** priority than conda-forge

```bash
pixi workspace channel add --prepend rapidsai
```
```
✔ Added rapidsai (https://conda.anaconda.org/rapidsai/)
```

Then add the CuDF dependencies for the target platform of `linux-64` (`requests` and `aiohttp` are for an example).

```bash
pixi add --platform linux-64 cudf requests aiohttp
```
```
✔ Added cudf >=25.6.0,<26
✔ Added requests >=2.32.4,<3
✔ Added aiohttp >=3.12.13,<4
Added these only for platform(s): linux-64
```

and you should now have the workspace.

:::
::::

From this code snippet from a [user guide from NVIDIA](https://github.com/NVIDIA/accelerated-computing-hub/blob/2186298825b85ef38f08e779af7992b8d762289f/gpu-python-tutorial/6.0_cuDF.ipynb), we can now see that CuDF has very similar semantics and API to Pandas

```{literalinclude} code/cudf-example/cudf-example.py
```

```bash
pixi run python cudf-example.py
```
```
Pandas DataFrame
:    en.m                   Article_51  1  0
0    ja                       エレファモン  1  0
1   ang                Flocc:Scīrung  1  0
2    en  Panorama_(La_Dispute_album)  1  0
3  fa.m                  جاشوا_جکسون  1  0
4  fa.m                 خانواده_کندی  2  0
[1297577][09:12:17:950636][warning] Auto detection of compression type is supported only for file type buffers. For other buffer types, AUTO compression type assumes uncompressed input.

CuDF DataFrame
:    en.m                   Article_51  1  0
0    ja                       エレファモン  1  0
1   ang                Flocc:Scīrung  1  0
2    en  Panorama_(La_Dispute_album)  1  0
3  fa.m                  جاشوا_جکسون  1  0
4  fa.m                 خانواده_کندی  2  0
```

For time today, we won't cover CuDF fully, but there are [user guides for how to use CuDF](https://github.com/NVIDIA/accelerated-computing-hub/blob/2186298825b85ef38f08e779af7992b8d762289f/gpu-python-tutorial/6.0_cuDF.ipynb), as seen below.

::: {important} Further references

* The [NVIDIA Accelerated Computing Hub](https://github.com/NVIDIA/accelerated-computing-hub) is an open source GitHub repository that serves as a curated collection of educational resources related to general purpose GPU programming.
It contains many excellent examples.
* In the tutorials session before this one (morning of 2025-07-07), [Katrina Riehl](https://github.com/nv-kriehl) taught [The Accelerated Python Developer's Toolbox](https://cfp.scipy.org/scipy2025/talk/KA7ZYR/) which covers CUDA and Python in-depth.
* In the tutorials session before this one (morning of 2025-07-07), Allison Ding taught [Scaling Clustering for Big Data: Leveraging RAPIDS cuML](https://cfp.scipy.org/scipy2025/talk/WSSAU7/) which covers the cuML RAPIDS library.
* The RAPIDS documentation has a [CuDF user guide](https://docs.rapids.ai/api/cudf/stable/user_guide/).

:::
