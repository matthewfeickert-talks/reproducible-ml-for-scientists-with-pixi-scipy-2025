# Introduction

Modern scientific analyses are complex software and logistical workflows that may span multiple software environments and require heterogenous software and computing infrastructure.
Scientific researchers need to keep track of all of this to be able to do their research, and to ensure the validity of their work, which can be difficult.
Scientific software enables all of this work to happen, but software isn't a static resource &mdash; software is continually developed, revised, and released, which can introduce large breaking changes or subtle computational differences in outputs and results.
Having the software you're using change without you intending it from day-to-day, run-to-run, or on different machines is problematic when trying to do high quality research and can cause software bugs, errors in scientific results, and make findings unreproducible.
All of these things are not desirable!

::: {note} Scientific software

When discussing scientific "software" in this tutorial we will primarily be meaning open source software that is openly developed (like the [Scientific Python](https://scientific-python.org/) ecosystem).
However, there are situations in which software might (for good reason) be:

* Closed development with open source release artifacts (e.g. [Pythia 8](https://gitlab.com/Pythia8/releases) (particle physics))
* Closed development and closed source with public binary distributions (e.g. [CUDA](https://developer.nvidia.com/cuda-zone))
* Closed development and closed source with proprietary licensed binary distributions (e.g. MATLAB, Mathematica)

:::

::: {tip} What are other challenges to reproducible research?
:class: dropdown

There are many! Here are some you might have thought of:

* (Not having) Access to data
* Required software packages be removed from mutable package indexes
* Unreproducible builds of software that isn't packaged and distributed on public package indexes
* Analysis code not being under version control
* Not having any environment definition configuration files

What did you come up with?

:::

## Computational reproducibility

"Reproducible" research can mean many things and is a multipronged problem.
This tutorial will focus primarily on computational reproducibility.
Like all forms of reproducibility, there are multiple "levels" of reproducibility.
For this tutorial we will focus on "full" reproducibility, meaning that reproducible software environments will:

* Be defined through high level user configuration files.
* Have machine produced hash level lock files with a full definition of all software in the environment.
* Specify target computer platforms for all environments solved.
* Have the resolution and "solving" of a platform's environments be machine agnostic.
* Have the software packages defined in the environments exist on immutable public package indexes.

### Hardware accelerated environments

Software the involves hardware acceleration on computing resources like GPUs requires additional information to be provided for full computational reproducibility.
In addition to the computer platform, information about the hardware acceleration device, its supported drivers, and compatible hardware accelerated versions of the software in the environment (GPU enabled builds) are required.
Traditionally this has been very difficult to do, but multiple recent technological advancements (made possible by social agreements and collaborations) in the scientific open source world now provide solutions to these problems.

::: {tip} What are possible challenges of reproducible hardware accelerated environments?
:class: dropdown

Here are some you might have thought of:

* Installing hardware acceleration drivers and libraries on the machine with the GPU
* Knowing what drivers are supported for the available GPUs
* Providing instructions to install the same drivers and libraries on multiple computing platforms
* Having the "deployment" machine's resources and environment where the analysis is done match the "development" machine's environment

What did you come up with?

:::

::: {tip} Does computational reproducibility mean that the exact same numeric results should be achieved every time?
:class: dropdown

Not necessarily.
Even though the computational software environment is identical there are things that can change between runs of software that could slightly change numerical results (e.g. random number generation seeds, file read order, machine entropy).
This isn't necessarily a problem, and in general one should be more concerned with getting answers that make sense within application uncertainties than matching down to machine precision.

What are additional reasons you thought of?

:::

## Computational reproducibility vs. scientific reuse

Aiming for computational reproducibility is the first step to making scientific research more beneficial to us.
For the purposes of a single analysis this should be the primary goal.
However, just because a software environment is fully reproducible does not mean that the research is automatically reusable.
Reuse allows for the tools and components of the scientific workflow to be composable tools that can interoperate together to
create a workflow.
The steps of the workflow might exist in radically different computational environments and require different software, or different versions of the same software tools.
Given these demands, reproducible computational software environments are a first step toward fully reusable scientific workflows.

This tutorial will focus on computational reproducibility of hardware accelerated scientific workflows (e.g. machine learning).
Scientifically reusable analysis workflows are a more extensive topic, but this tutorial will link to references on the topic.

::: {tip} What are challenges to your own research practices to making them reproducible and reusable?
:class: dropdown

Here are some you may have thought of:

* Technical expertise in reproducibility technologies
* Time to learn new tools
* Balancing reproducibility concerns with using tools the entire research team can understand

What did you come up with?

:::
