# Setup

## Requirements

### Software

This tutorial requires minimal software to be installed in advance:

* A computer running an 64 bit version of Linux, macOS, or Windows.
* Pixi

### Hardware (optional)

* An NVIDIA GPU

This tutorial focuses on hardware acceleration for {term}`CUDA` environments which require an NVIDIA GPU to use.
While an NVIDIA GPU is not required to be able to work through the tutorial, access to one will be required to run the examples.

## Installation

### Pixi

To install Pixi follow [the installation instructions](https://pixi.sh/latest/#installation) for your particular machine and then restart your shell.

#### Unix (Linux and macOS)

```
curl -fsSL https://pixi.sh/install.sh | sh
```

#### Windows

```
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

### Pixi Shell completions

Additionally, install the [Pixi shell completions](https://pixi.sh/latest/global_tools/introduction/#shell-completions) for your particular shell choice.
