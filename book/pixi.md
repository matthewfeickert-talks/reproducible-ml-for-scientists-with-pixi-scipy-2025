# Introduction to Pixi


![Pixi banner](https://github.com/prefix-dev/pixi/assets/4995967/a3f9ff01-c9fb-4893-83c0-2a3f924df63e)


Pixi is a cross-platform package manager that can manage complex development workflows.

There are two main features:
- Installing tools globally (`pixi global`)
- Project management

This tutorial will mainly focus on the Project management side of Pixi. More information about `pixi global` can be found [here](https://pixi.sh/latest/global_tools/introduction/)

# What does Pixi solve?
Pixi's goal is to solve fast reproducible developer and deployment workflows.
Often written as *"it worked on my machine"*.
Pixi gives the developer all the required tools to create an environment that they can share with colleagues and servers.
While being sure there is nothing missing from the environment to run the project.

There are some key focus points to solve this problem.

1. **Reproducibility**: Pixi always locks all packages it installs into the environments into a lockfile
2. **Speed**: By using modern technologies like Rust and a big focus on optimizations, Pixi is using as much of the machines capabilities to do it's work as fast as possible.
3. **Virtualization**: By separating environments in dedicated folders, users can easily set up, build, and test a project without worrying about their other projects break in the meantime.
4. **Cross-Platform**: With everything Pixi can do it tries to bridge the gaps between the different operating systems, making collaboration easier than before.
5. **Cross-Language**: While Python is well-supported language, Pixi doesn't stop there, it also focusses on C/C++, CUDA, Rust, Fortran and more.


All of these points are wrapped in a set of main functionalities.

1. **Virtual environment Management**: Pixi can create conda environments and activated them on demand.
2. **Package management**: Pixi can install/update/upgrade/remove packages from these environments
3. **Task management**: Pixi has a cross-platform task runner built-in, allowing users to share the same commands on all platforms.

We'll dive deeper into these topics.

# The conda and pypi ecosystem
Pixi is built on top of the conda and pypi ecosystem.
Pixi creates conda environments.
Pixi uses `uv` to install Python packages into these environments.
...

# The project workflow
Pixi is designed to be used in a project-based workflow.
This means that you can create a project and then use Pixi to manage the dependencies and tasks for that project.
...


# Creating a project


# Managing dependencies


# Managing tasks


# Managing environments


# Managing global tools
*Maybe add a section about managing global tools*
