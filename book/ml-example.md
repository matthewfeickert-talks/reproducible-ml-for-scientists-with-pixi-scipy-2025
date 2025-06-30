# Machine Learning workflows in a Pixi workspace

Now that we know how to build a CUDA Pixi environment in our example workspace and NVIDIA GPUs on Brev, let's run an example machine learning workflow using our Pixi workspace.

## Training the machine learning model

Let's write a very standard tutorial example of training a deep neral network on the [MNIST dataset](https://en.wikipedia.org/wiki/MNIST_database) with PyTorch and then run it on the GPUs on Brev.

### The neural network code

We'll download Python code that uses a convocational neural network written in PyTorch to learn to identify the handwritten number of the MNIST dataset and place it under a `src/` directory.
This is a modified example from the PyTorch documentation (https://github.com/pytorch/examples/blob/main/mnist/main.py) which is [licensed under the BSD 3-Clause license](https://github.com/pytorch/examples/blob/abfa4f9cc4379de12f6c340538ef9a697332cccb/LICENSE).

```bash
curl -sLO https://raw.githubusercontent.com/matthewfeickert/nvidia-gpu-ml-library-test/36c725360b1b1db648d6955c27bd3885b29a3273/torch_MNIST.py
mkdir -p src
mv torch_MNIST.py src/
```

### The Pixi environment

Now let's think about what we need to use this code.
Looking at the imports of `src/torch_MNIST.py` we can see that `torch` and `torchvision` are the only imported libraries that aren't part of the Python standard library, so we will need to depend on PyTorch and `torchvision`.
We also know that we'd like to use CUDA accelerated code, so that we'll need CUDA libraries and versions of PyTorch that support CUDA.

::::: {tip} Create the environment

Create a Pixi workspace that:

* Has PyTorch and `torchvision` in it.
* Has the ability to support CUDA v12.
* Has an environment that has the CPU version of PyTorch and `torchvision` that can be installed on `linux-64`, `osx-arm64`, and `win-64`.
* Has an environment that has the GPU version of PyTorch and `torchvision`.

:::: {hint} Solution
:class: dropdown

This is just expanding the exercises from the CUDA conda packages exercise.

Create a new workspace

```bash
pixi init ~/reproducible-ml-for-scientists-tutorial-scipy-2025/ml-example
cd ~/reproducible-ml-for-scientists-tutorial-scipy-2025/ml-example
```
```
✔ Created /home/<username>/reproducible-ml-for-scientists-tutorial-scipy-2025/ml-example/pixi.toml
```

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
name = "ml-example"
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
name = "ml-example"
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

Now that we have the environments solved, let's do a comparison of training in the CPU environment and the GPU environment.

To validate that things are working with the CPU code, let’s do a short training run for only 2 epochs in the `cpu` environment.

```bash
pixi run --environment cpu python src/torch_MNIST.py --epochs 2 --save-model --data-dir data
```
```
100.0%
100.0%
100.0%
100.0%
Train Epoch: 1 [0/60000 (0%)]	Loss: 2.329474
Train Epoch: 1 [640/60000 (1%)]	Loss: 1.425185
Train Epoch: 1 [1280/60000 (2%)]	Loss: 0.826808
Train Epoch: 1 [1920/60000 (3%)]	Loss: 0.556883
Train Epoch: 1 [2560/60000 (4%)]	Loss: 0.483756
...
Train Epoch: 2 [57600/60000 (96%)]	Loss: 0.146226
Train Epoch: 2 [58240/60000 (97%)]	Loss: 0.016065
Train Epoch: 2 [58880/60000 (98%)]	Loss: 0.003342
Train Epoch: 2 [59520/60000 (99%)]	Loss: 0.001542

Test set: Average loss: 0.0351, Accuracy: 9874/10000 (99%)
```

That took some time and we only got 2 epochs into training, but it ran!

Let's speed things up using the `gpu` environment.

```bash
pixi run --environment gpu python src/torch_MNIST.py --epochs 14 --save-model --data-dir data
```
```
Train Epoch: 1 [0/60000 (0%)]   Loss: 2.281690
Train Epoch: 1 [640/60000 (1%)]	Loss: 1.459567
Train Epoch: 1 [1280/60000 (2%)]	Loss: 0.927929
Train Epoch: 1 [1920/60000 (3%)]	Loss: 0.632228
Train Epoch: 1 [2560/60000 (4%)]	Loss: 0.384857
...
Train Epoch: 14 [56960/60000 (95%)]	Loss: 0.009351
Train Epoch: 14 [57600/60000 (96%)]	Loss: 0.001419
Train Epoch: 14 [58240/60000 (97%)]	Loss: 0.024142
Train Epoch: 14 [58880/60000 (98%)]	Loss: 0.004241
Train Epoch: 14 [59520/60000 (99%)]	Loss: 0.003314

Test set: Average loss: 0.0268, Accuracy: 9919/10000 (99%)
```

::::: {tip} Add `train-cpu` and `train-gpu` tasks to the Pixi workspace

:::: {hint} Solution
:class: dropdown

Let's add the `train-cpu` task first with [`pixi task add`](https://pixi.sh/latest/reference/cli/pixi/task/add/)

```bash
pixi task add --feature cpu --description "Train MNIST on CPU" train-cpu "python src/torch_MNIST.py --epochs 2 --save-model --data-dir data"
```
```
✔ Added task `train-cpu`: python src/torch_MNIST.py --epochs 2 --save-model --data-dir data, description = "Train MNIST on CPU"
```

and then do the same with the `train-gpu` task

```bash
pixi task add --feature gpu --description "Train MNIST on GPU" train-gpu "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data"
```
```
✔ Added task `train-gpu`: python src/torch_MNIST.py --epochs 14 --save-model --data-dir data, description = "Train MNIST on GPU"
```

We can now get a nice summary of the tasks available with [`pixi task list`](https://pixi.sh/latest/reference/cli/pixi/task/list/)

```bash
pixi task list
```
```
Tasks that can run on this machine:
-----------------------------------
train-cpu, train-gpu
Task       Description
train-cpu  Train MNIST on CPU
train-gpu  Train MNIST on GPU
```

```toml
[workspace]
channels = ["conda-forge"]
name = "ml-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.cpu.tasks]
train-cpu = { cmd = "python src/torch_MNIST.py --epochs 2 --save-model --data-dir data", description = "Train MNIST on CPU" }

[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.target.linux-64.dependencies]
pytorch-gpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.gpu.tasks]
train-gpu = { cmd = "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data", description = "Train MNIST on GPU" }

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
```

::: {note} task specific subtables

You'll note that using the [`pixi task`](https://pixi.sh/latest/reference/cli/pixi/task/) CLI API adds the tasks to the feature `tasks` subtable but places all of the `task` components (e.g. `cmd`, `description`) on a single line.
It can sometimes be visually cleaner to give each task its own subtable, where

```toml
[feature.gpu.tasks]
train-gpu = { cmd = "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data", description = "Train MNIST on GPU" }
```

can be rewritten as

```toml
[feature.gpu.tasks.train-gpu]
description = "Train MNIST on GPU"
cmd = "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data"
```

```toml
[workspace]
channels = ["conda-forge"]
name = "ml-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.cpu.tasks.train-cpu]
description = "Train MNIST on CPU"
cmd = "python src/torch_MNIST.py --epochs 2 --save-model --data-dir data"

[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.target.linux-64.dependencies]
pytorch-gpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.gpu.tasks.train-gpu]
description = "Train MNIST on GPU"
cmd = "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data"

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
```

:::

::::
:::::

::: {note} Task specification at the CLI

Note that to run these tasks now we can just run the task name

```bash
pixi run train-gpu
```
```
✨ Pixi task (train-gpu in gpu): python src/torch_MNIST.py --epochs 14 --save-model --data-dir data: (Train MNIST on GPU)
```

without having to specify the task's environment

```bash
pixi run --environment gpu train-gpu
```

as the task name was unique in the workspace and so Pixi is able to determine its environment automatically.

:::

## Performing inference with the trained model

Now that we've trained our model we'd like to be able to use it to perform machine learning inference (model prediction).
However, we might want to perform inference in a _different software_ environment than the environment we used for model _training_.

We'll download Python code that uses the same PyTorch convocational neural network architecture in `Mtorch_MNIST.py` to load the model and an image and make a predict what number the image contains and place it under a `src/` directory.
This code is [licensed under the MIT license](https://github.com/matthewfeickert/nvidia-gpu-ml-library-test/blob/36c725360b1b1db648d6955c27bd3885b29a3273/LICENSE).

```bash
curl -sLO https://github.com/matthewfeickert/nvidia-gpu-ml-library-test/blob/36c725360b1b1db648d6955c27bd3885b29a3273/torch_MNIST_inference.py
mkdir -p src
mv torch_MNIST_inference.py src/
```

:::: {tip} Add an `inference` environment that uses the `gpu` feature and an `inference` feature

::: {hint} Solution
:class: dropdown

Add additional dependencies that we'll want for use in inference environments

```bash
pixi add --feature inference matplotlib
```
```
✔ Added matplotlib
Added these only for feature: inference
```

and add the `gpu` and `inference` features to an `inference` environment

```bash
pixi workspace environment add --feature gpu --feature inference inference
```
```
✔ Added environment inference
```

and then instantiate the feature with specific versions

```bash
pixi upgrade --feature inference
```

```toml
[workspace]
channels = ["conda-forge"]
name = "ml-example"
platforms = ["linux-64", "osx-arm64", "win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = ">=3.13.5,<3.14"

[feature.cpu.dependencies]
pytorch-cpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.cpu.tasks.train-cpu]
description = "Train MNIST on CPU"
cmd = "python src/torch_MNIST.py --epochs 2 --save-model --data-dir data"

[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.target.linux-64.dependencies]
pytorch-gpu = ">=2.7.1,<3"
torchvision = ">=0.22.0,<0.23"

[feature.gpu.tasks.train-gpu]
description = "Train MNIST on GPU"
cmd = "python src/torch_MNIST.py --epochs 14 --save-model --data-dir data"

[feature.inference.dependencies]
matplotlib = ">=3.10.3,<4"

[environments]
cpu = ["cpu"]
gpu = ["gpu"]
inference = ["gpu", "inference"]
```

:::
::::

Now that we've added an `inference` environment to the workspace, use it to predict the value of the default image.

```bash
pixi run --environment inference python src/torch_MNIST_inference.py --model-path ./mnist_cnn.pt --image-path ./test_image.png
```
```
Label: 4, Prediction: 4
```

As we didn't have an image yet to run on, we loaded one from the MNIST training set, and as we know the labels there we include the label output.
If we load the image from disk without knowing this, then we get just the prediction values.

```bash
pixi run --environment inference python src/torch_MNIST_inference.py --model-path ./mnist_cnn.pt --image-path ./test_image.png
```
```
Prediction: 4
```

::: {note} Real world model inference

In the real world you're probably not writing a from scratch Python script to perform ML inference, but using a tool like [NVIDIA Triton Inference Server](https://github.com/triton-inference-server/server).
However, for this tutorial it is fine to do this more explicit, but less useful, example.

:::
