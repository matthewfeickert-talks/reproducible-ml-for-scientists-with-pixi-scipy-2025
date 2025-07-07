# Reproducible Machine Learning Workflows for Scientists with Pixi

Taught at [SciPy 2025](https://www.scipy2025.scipy.org/) as a [tutorial](https://cfp.scipy.org/scipy2025/talk/GDN8PN/) on Monday July 7th, 2025

## Abstract

Scientific researchers need reproducible software environments for complex applications that can run across heterogeneous computing platforms.
Modern open source tools, like Pixi, provide automatic reproducibility solutions for all dependencies while providing a high level interface well suited for researchers.

This tutorial will provide a practical introduction to using Pixi to easily create scientific and AI/ML environments that benefit from hardware acceleration, across multiple machines and platforms.
The focus will be on applications using the PyTorch and JAX Python machine learning libraries with CUDA enabled, as well as deploying these environments to production settings in Linux container images.

## SciPy Logistical Information

* Tutorial name: [Reproducible Machine Learning Workflows for Scientists with Pixi](https://matthewfeickert-talks.github.io/reproducible-ml-for-scientists-with-pixi-scipy-2025/)
* Date: 2025-07-07
* Time: 13:30 to 17:30
* Location: Ballroom C (Greater Tacoma Convention Center, 3rd Floor, 1500 Commerce St.)

## Rough Outline

**00:00 &ndash; 00:05 (5 min):**
* Personal Introductions

**00:05 &ndash; 00:15 (10 min):**
* [Setup instructions](setup.md), setup your machine for the tutorial.

**00:15 &ndash; 00:30 (15 min):**
* [Introduction to Philosophy](introduction.md), an overview of the philosophy behind this tutorial.

**00:30 &ndash; 01:00 (30 min):**
* [Pixi introduction](pixi.md), an overview of Pixi's features and capabilities.

**01:00 &ndash; 01:40 (40 min):**
* [Pixi exercises](pixi-exercise.md), play around with Pixi and create a reproducible Python environment

**01:40 &ndash; 01:55 (15 min):**
* Break, grab a snack and stretch your legs.

**01:55 &ndash; 02:35 (40 min):**
* [Introduction to CUDA and CUDA conda packages](cuda-conda.md), the history and overview of how to use CUDA with Pixi and conda packages.

**02:35 &ndash; 02:45 (10 min):**
* Break, grab a snack and stretch your legs.

**02:45 &ndash; 03:10 (25 min):**
* [Intro to Machine Learning applications with Pixi](ml-example.md), an overview of how to use Pixi for machine learning applications, including PyTorch.

**03:10 &ndash; 03:30 (20 min):**
* [General hardware acceleration using CUDA](cuda-hardware-acceleration.md), an overview of how to use CUDA for general hardware acceleration like replacing NumPy with CuPy.

**03:30 &ndash; 04:00 (30 min):**
* [Deployment using Linux containers](containers.md), an overview of how to use Pixi to create reproducible Linux CUDA container images.

This tutorial was supported by the [US Research Software Sustainability Institute (URSSI)](https://urssi.us/) via grant [G-2022-19347](https://sloan.org/grant-detail/g-2022-19347) from the Sloan Foundation, [prefix.dev GmbH](https://prefix.dev/), [NVIDIA](https://www.nvidia.com/), and the [University of Wisconsin&ndash;Madison Data Science Institute](https://dsi.wisc.edu/).
