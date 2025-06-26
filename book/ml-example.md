# Machine Learning workflows in a Pixi workspace

Now that we know how to build a CUDA Pixi environment in our example workspace and NVIDIA GPUs on Brev, let's run an example machine learning workflow using our Pixi workspace.

## Training the machine learning model

Let's write a very standard tutorial example of training a deep neral network on the [MNIST dataset](https://en.wikipedia.org/wiki/MNIST_database) with PyTorch and then run it on GPUs in an HTCondor worker pool.

#### The neural network code

We'll download Python code that uses a convocational neural network written in PyTorch to learn to identify the handwritten number of the MNIST dataset and place it under a `src/` directory.
This is a modified example from the PyTorch documentation (https://github.com/pytorch/examples/blob/main/mnist/main.py) which is [licensed under the BSD 3-Clause license](https://github.com/pytorch/examples/blob/abfa4f9cc4379de12f6c340538ef9a697332cccb/LICENSE).

```bash
curl -sLO https://raw.githubusercontent.com/matthewfeickert/nvidia-gpu-ml-library-test/c7889222544928fb6f9fdeb1145767272b5cfec8/torch_MNIST.py
mkdir -p src
mv torch_MNIST.py src/
```

#### The Pixi environment

Now let's think about what we need to use this code.
Looking at the imports of `src/torch_MNIST.py` we can see that `torch` and `torchvision` are the only imported libraries that aren't part of the Python standard library, so we will need to depend on PyTorch and `torchvision`.
We also know that we'd like to use CUDA accelerated code, so that we'll need CUDA libraries and versions of PyTorch that support CUDA.

::::: {note} Create the environment

Create a Pixi workspace that:

* Has PyTorch and `torchvision` in it.
* Has the ability to support CUDA v12.
* Has an environment that has the CPU version of PyTorch and `torchvision` that can be installed on `linux-64`, `osx-arm64`, and `win-64`.
* Has an environment that has the GPU version of PyTorch and `torchvision`.

:::: {hint} Solution
:class: dropdown

This is just expanding the exercises from the CUDA conda packages exercise.

Let's first add all the platforms we want to work with to the workspace

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```
```
✔ Added linux-64
✔ Added osx-arm64
✔ Added win-64
```

We know that in both environment we'll want to use Python, and so we can install that in the `default` environment and have it be used in both the `cpu` and `gpu` environment.

```bash
pixi add python
```
```
✔ Added python >=3.13.5,<3.14
```

Let's now add the CPU requirements to a feature named `cpu`

```bash
pixi add --feature cpu pytorch-cpu torchvision
```
```
✔ Added pytorch-cpu
✔ Added torchvision
Added these only for feature: cpu
```

and then create an environment named `cpu` with that feature

```bash
pixi workspace environment add --feature cpu cpu
```
```
✔ Added environment cpu
```

and insatiate it with particular versions

```bash
pixi upgrade --feature cpu
```

```toml
[workspace]
channels = ["conda-forge"]
name = "htcondor"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[environments]
cpu = ["cpu"]
```

Now let's add the GPU environment and dependencies.
Let's start with the CUDA system requirements

```bash
pixi workspace system-requirements add --feature gpu cuda 12
```

::: {attention} Override the `__cuda` virtual package

Remember that if you're on a platform that doesn't support the `system-requirement` you'll need to override the checks to solve the environment.

```bash
export CONDA_OVERRIDE_CUDA=12
```

:::

and create an environment from the feature

```bash
pixi workspace environment add --feature gpu gpu
```
```
✔ Added environment gpu
```

and then add the GPU dependencies for the target platform of `linux-64` (where we'll run in production).

```bash
pixi add --platform linux-64 --feature gpu pytorch-gpu torchvision
```
```
✔ Added pytorch-gpu >=2.7.1,<3
✔ Added torchvision >=0.22.0,<0.23
Added these only for platform(s): linux-64
Added these only for feature: gpu
```

```toml
[workspace]
channels = ["conda-forge"]
name = "htcondor"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.target.linux-64.dependencies]
pytorch-gpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
```

::::
:::::

## Performing inference with the trained model

TODO
