# Reproducible Machine Learning Workflows for Scientists with Pixi

Taught at [SciPy 2025](https://www.scipy2025.scipy.org/) as a [tutorial](https://cfp.scipy.org/scipy2025/talk/GDN8PN/) on Monday July 7th, 2025

## Abstract

Scientific researchers need reproducible software environments for complex applications that can run across heterogeneous computing platforms.
Modern open source tools, like Pixi, provide automatic reproducibility solutions for all dependencies while providing a high level interface well suited for researchers.

This tutorial will provide a practical introduction to using Pixi to easily create scientific and AI/ML environments that benefit from hardware acceleration, across multiple machines and platforms.
The focus will be on applications using the PyTorch and JAX Python machine learning libraries with CUDA enabled, as well as deploying these environments to production settings in Linux container images.

## SciPy Logistical Information

* Tutorial name: [Reproducible Machine Learning Workflows for Scientists with Pixi](https://cfp.scipy.org/scipy2025/talk/GDN8PN/)
* Date: 2025-07-07
* Time: 13:30 to 17:30
* Location: Room 315

## Rough Outline

**0:00 &ndash; 0:20 (20 min):**

* Overview of importance of, and challenges to, reproducible scientific workflows.
* Introduction of `pixi` and `pixi` environment management philosophy.

**0:20 &ndash; 0:40 (20 min):**

* Work through the [`pixi` Python tutorial](https://pixi.sh/latest/tutorials/python/).

**0:40 &ndash; 1:00 (20 min):**

* Exercise 1: Create a multi-platform multi-environment `pixi` project to run a provided "Scientific Python" (e.g., SciPy, NumPy, Matplotlib) example workflow that does not use machine learning.

**1:00 &ndash; 1:15 (15 min):**

* Break

**1:15 &ndash; 1:30 (15 min):**

* Discussion over solutions to Exercise 1.
* Discuss and answer questions participants have.

**1:30 &ndash; 2:50 (20 min):**

* Introduction to the concepts of [conda-forge](https://github.com/conda-forge), the CUDA software stack on conda-forge, and [CUDA `system-requirements` in `pixi`](https://pixi.sh/latest/features/system_requirements/#using-cuda-in-pixi).

**1:50 &ndash; 2:20 (30 min):**

* Exercise 2: Create a `pixi` project to run an example PyTorch machine learning workflow on GPUs with CUDA `v12`.
* Exercise 3: Extend the `pixi` project from Exercise 2 to provide a new environment to run an example JAX machine learning workflow on GPUs with CUDA v11.8.

**2:20 &ndash; 2:35 (15 min):**

* Break

**2:35 &ndash; 2:55 (20 min):**

* Discussion over solutions to Exercises 2 and 3.
* Introduction to environments that install from multiple package indexes (e.g. conda-forge and PyPI).

**2:55 &ndash; 3:15 (20 min):**

* Exercise 4: Create a `pixi` project to run an example machine learning workflow on GPUs with CUDA that installs dependencies from both conda-forge and PyPI.
* Discussion over solutions to Exercise 4.

**3:15 &ndash; 3:25 (10 min):**

* Very brief introduction the concepts of "production environments" and Linux containers.
As Linux containers are their own technology that can be quite complex, all Linux container components of the tutorial will be pre-prepared for participants.

**3:25 &ndash; 3:45 (20 min):**

* Exercise 5: Containerize the `pixi` project environment from Exercise 2 in a Linux container image and run a Pytorch machine learning workflow on GPUs with the deployed container.

**3:45 &ndash; 4:00 (15 min):**

* Discussion over solutions to Exercise 5.
* Time for participants to start exploring their own projects with `pixi`.
* General question and answer time with instructor team.

SciPy 2025 tutorial on

```{literalinclude} ../pixi.toml
:lang: toml
```
