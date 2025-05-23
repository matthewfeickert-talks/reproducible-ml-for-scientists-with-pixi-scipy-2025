# Introduction to Pixi


![Pixi banner](https://github.com/prefix-dev/pixi/assets/4995967/a3f9ff01-c9fb-4893-83c0-2a3f924df63e)


Pixi is a cross-platform package manager that can manage complex development workflows.

There are two main features:
- Installing tools globally (`pixi global`)
- Project workflow

This tutorial will mainly focus on the Project workflow side of Pixi. More information about `pixi global` can be found [here](https://pixi.sh/latest/global_tools/introduction/)

# What does Pixi solve?
Pixi's goal is to solve fast reproducible developer and deployment workflows.
Often written as *"it worked on my machine"*.
Pixi gives the developer all the required tools to create an environment that they can share with colleagues and servers.
While being sure there is nothing missing from the environment to run the project.

There are some key focus points to solve this problem.

1. **Reproducibility**: Pixi always locks all packages it installs into the environments into a lockfile
2. **Speed**: By using modern technologies like Rust and a big focus on optimizations, Pixi is using as much of the machines capabilities to do it's work as fast as possible.
3. **Virtualization**: By separating environments in dedicated folders, users can easily set up, build, and test a project without worrying about their other projects break in the meantime.
4. **{term}`Cross-Platform`**: With everything Pixi can do it tries to bridge the gaps between the different operating systems, making collaboration easier than before.
5. **{term}`Cross-Language`**: While Python is well-supported language, Pixi doesn't stop there, it also focusses on C/C++, CUDA, Rust, Fortran and more.


All of these points are wrapped in a set of main functionalities.

1. **Virtual environment Management**: Pixi can create conda environments and activate them on demand.
2. **Package management**: Pixi can install/update/upgrade/remove packages from these environments
3. **Task management**: Pixi has a cross-platform task runner built-in, allowing users to share the same commands on all platforms.

We'll dive deeper into these topics later on.

# The conda and PyPI ecosystem
Pixi is built on top of the conda and PyPI ecosystem.

Conda is a {term}`cross-platform`, {term}`cross-language` package ecosystem that allows users to install packages and manage environments.
It is widely used in the data science and machine learning community, but it is also used in other fields.
It's power comes from the fact that it always installs binary packages, meaning that it doesn't need to compile anything.
This makes the ecosystem very fast and easy to use.

What makes the conda ecosystem even more powerful is the fact that it can install packages from multiple channels.
The preferred channel these days is the `conda-forge` channel, which is a community-driven channel that provides a lot of packages.
This shared community effort makes the packages significantly more reliable.
The binary nature of the packages allows the conda ecosystem to be easily used outside the Python ecosystem, making it a great choice for C/C++ and Fortran packages as well.
Especially combining languages can be a pain, where conda shines.

PyPI is the Python Package Index, which is the main package manager for Python.
It is a much larger ecosystem than conda, especially because the boundary to upload packages is lower.
This means that there are a lot of packages available, but it also means that the quality of the packages is not always as high as in the conda ecosystem.
Pixi can install packages from both ecosystems, but it is recommended to use conda packages whenever possible.

| Feature | Conda | PyPI |
| ------- | ----- | ---- |
| Package format | Binary | Source & Binary (wheel) |
| Package managers | [`conda`](https://github.com/conda/conda), [`mamba`](https://github.com/mamba-org/mamba), [`micromamba`](https://github.com/mamba-org/mamba), [`pixi`](https://github.com/prefix-dev/pixi), [`rattler`](https://github.com/conda/rattler) | [`pip`](https://github.com/pypa/pip), [`poetry`](https://github.com/python-poetry/poetry), [`uv`](https://github.com/astral-sh/uv), [`pdm`](https://github.com/pdm-project/pdm), [`hatch`](https://github.com/pypa/hatch), [`rye`](https://github.com/astral-sh/rye), [`pixi`](https://github.com/prefix-dev/pixi) |
| Environment management | [`conda`](https://github.com/conda/conda), [`mamba`](https://github.com/mamba-org/mamba), [`micromamba`](https://github.com/mamba-org/mamba), [`pixi`](https://github.com/prefix-dev/pixi) | [`venv`](https://docs.python.org/3/library/venv.html), [`virtualenv`](https://virtualenv.pypa.io/en/latest/), [`pipenv`](https://pipenv.pypa.io/en/latest/), [`pyenv`](https://github.com/pyenv/pyenv), [`uv`](https://github.com/astral-sh/uv), [`rye`](https://github.com/astral-sh/rye), [`poetry`](https://github.com/python-poetry/poetry), [`pixi`](https://github.com/prefix-dev/pixi) |
| Package building | [`conda-build`](https://github.com/conda/conda-build), [`pixi`](https://github.com/prefix-dev/pixi) | [`setuptools`](https://github.com/pypa/setuptools), [`poetry`](https://github.com/python-poetry/poetry), [`flit`](https://github.com/pypa/flit), [`hatch`](https://github.com/pypa/hatch), [`uv`](https://github.com/astral-sh/uv), [`rye`](https://github.com/astral-sh/rye) |
| Package index | [`conda-forge`](https://prefix.dev/channels/conda-forge), [`bioconda`](https://prefix.dev/channels/bioconda), and more | [pypi.org](https://pypi.org) |

## Why do I need conda if I have PyPI? (Shared Libraries)
Conda packages are designed with the idea of shared libraries in mind.
This means that when you install a package, it will also install all the dependencies that are required to run the package.
These dependencies have to be ABI compatible with the package, meaning that they have to be compiled with the same compiler and flags as the package itself.
This is important because many packages require shared libraries to run, and these libraries are often not included in the package itself.
This is important because many packages require shared libraries to run, and these libraries are often not included in the package itself.
A good example of this is the `numpy` package, which requires the `openblas` library to run.
When you install `numpy` using conda, it will automatically install these libraries for you.
This is not the case with PyPI, where you often have to install these libraries manually, or use a package manager like `apt` or `brew` to install them.

This is also one of the reasons Linux distributions like Ubuntu and Debian have their own package managers, like `apt` and `dpkg`.
These package managers are designed to install packages that are compatible with the system libraries, and they often have a lot of dependencies that need to be installed as well.

:::{note} PyPI wheels
These days, PyPI wheels often ship their required shared libraries within the wheel itself.
This is a great step forward, but it's not always the case. And doesn't guarantee the ABI compatibility across the different packages.
:::

---

# The project workflow
Pixi is designed to be used in a project-based workflow.
Tools like `poetry`, `uv`, `npm`, `deno`, `cargo`, `maven` and `pixi` are all designed to be used in a project-based workflow.
This means that you can create a project and then use Pixi to manage the dependencies and tasks for that project.
You can think of a project as a self-contained directory that contains all the files and configurations needed to build and run your application.
Often the project will keep the environment it installs close to the project folder itself, so it will not clutter the system.
This is a great way to keep your projects organized and to avoid conflicts between different projects.

### Project-based vs Environment-based vs System-based
To give a little background why Pixi is designed this way, let's take a look at the different ways to manage packages and environments.

::::{tab-set}
:::{tab-item}Project-based workflow
**Supporting tools:** `pixi`, `poetry`, `uv`, `npm`, `deno`, `cargo`, `maven`

**Pros:**
- Isolated environments per project (no conflicts)
- Easy to reproduce and share with others (declarative)
- Keeps dependencies close to the project

**Cons:**
- Can use more disk space (multiple environments)
- Slightly more setup per project
:::
:::{tab-item}Environment-based workflow
**Supporting tools:** `conda`, `mamba`, `micromamba`, `pip`, `pipenv`, `uv pip`

**Pros:**
- Easy to share environments across multiple projects
- Isolated environments (no conflicts)

**Cons:**
- Risk of dependency conflicts between projects
- Harder to reproduce exact environments later

:::
:::{tab-item}System-based workflow
**Supporting tools:** `apt`, `rpm`, `brew`, `choco`, `winget`, `scoop`, `flatpak`

**Pros:**
- Simple, everything installed globally
- Every OS has a default package manager
- Guaranteed to work with system libraries

**Cons:**
- Very High risk of dependency/version conflicts with other projects (especially Python)
- Hard to reproduce or share setups
- Limited flexibility when it comes to versions
:::
::::


# Creating a project
As Pixi uses the project-based workflow, it uses a manifest file to keep track of the dependencies and tasks for the project.
This is also known as **declarative** configuration, where you describe what you want, and Pixi will take care of the rest.
The manifest file is called `pixi.toml`, or you can use `pyproject.toml`, and it is located in the root of the project.


To create a new project, you can use the `pixi init` command.
::::{tab-set}
:::{tab-item}pixi.toml
```bash
pixi init my_project
```
This will create a new directory called `my_project` and initialize a new `pixi.toml` file in it.
```bash
my_project
├── .gitattributes
├── .gitignore
└── pixi.toml
```

The `pixi.toml` file is a {term}`TOML` file that contains the configuration for the project.

```{code} toml
:filename: pixi.toml
:linenos:

[workspace]
authors = ["Jane Doe <jane.doe@example.com>"]
channels = ["https://prefix.dev/conda-forge"]
name = "my_project"
platforms = ["osx-arm64"]
version = "0.1.0"

[tasks]

[dependencies]
```

The `pixi.toml` doesn't have the basic Python package structure like the `pyproject.toml` file, because it is not a Python package by default.

As `pixi.toml` has a JSON schema, it is possible to use IDE's like VSCode to edit the field with autocompletion.
Install the [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) VSCode extension to get the best experience. Or use the integrated schema support in PyCharm.

:::

:::{tab-item}pyproject.toml
```bash
pixi init my_pyproject --format pyproject
```
This will create a new directory called `my_pyproject` and initialize a new `pyproject.toml` file in it.
It will also create a `src` directory with a `my_pyproject` subdirectory and an `__init__.py` file in it, to make it a simple Python package.
```bash
my_project
├── .gitattributes
├── .gitignore
├── pyproject.toml
└── src
    └── my_pyproject
        └── __init__.py
```

The `pyproject.toml` file is a {term}`TOML` file that contains the configuration for the project.

```{code} toml
:filename: pyproject.toml
:linenos:
[project]
authors = [{name = "Jane Doe", email = "jane.doe@example.com"}]
dependencies = []
name = "my_pyproject"
requires-python = ">= 3.11"
version = "0.1.0"

[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[tool.pixi.workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["osx-arm64"]

[tool.pixi.pypi-dependencies]
my_pyproject = { path = ".", editable = true }

[tool.pixi.tasks]
```
Note that the `pyproject.toml` file is a little different from the `pixi.toml` file.
The `pyproject.toml` file is a standard file used by many Python tools, thus it makes it easier to share the project with others.
The only difference between the two files is that the `pyproject.toml` file has a `[tool.pixi` prefix to the Pixi specific sections.
:::
::::

For the rest of this tutorial, we will use the `pixi.toml` file as the main file.

## Platforms
The `platforms` field in the manifest file is used to specify the platforms
**TODO**

## Channels
The `channels` field in the manifest file is used to specify the channels
**TODO**


# Managing dependencies
After creating the project, you can start adding dependencies to the project.
Pixi uses the `pixi add` command to add dependencies to the project.
This command will , by default, add the conda dependency to the `pixi.toml` or `pyproject.toml` file, solve the dependencies, write the lockfile and install the package in the environment. e.g. lets add `numpy` and `pytest` to the project.
```bash
pixi add numpy pytest
```
This will result in the following manifest file:

```{code}
:filename: pixi.toml
:linenos:
:emphasize-lines: 11
[workspace]
authors = ["Jane Doe <jane.doe@example.com>"]
channels = ["https://prefix.dev/conda-forge"]
name = "my_project"
platforms = ["osx-arm64"]
version = "0.1.0"

[tasks]

[dependencies]
numpy = ">=2.2.6,<3"
pytest = ">=8.3.5,<9"
```

## PyPI dependencies
Pixi can also install packages from PyPI, it does this through it's integration with `uv`.
In the Rust code Pixi depends on the `uv` package manager to install the packages from PyPI.
This means that you can use the `pixi add --pypi` command to install packages from PyPI.

```bash
pixi add --pypi pydantic
```

Which results in it being added to the manifest file as:
::::{tab-set}
:::{tab-item}pixi.toml
In the `pixi.toml` file, it will be added to the `[pypi-dependencies]` section.
```{code} toml
:filename: pixi.toml
:linenos:
[pypi-dependencies]
pydantic = ">=2.11.5, <3"
```
:::
:::{tab-item}pyproject.toml
In the `pyproject.toml` file, it will be added to the `[project]` section in the normal case.
```{code} toml
:filename: pyproject.toml
:linenos:
[project]
# ...
dependencies = ["pydantic>=2.11.5,<3"]
```
Things like `path` and `editable` are added through the Pixi specific section.
For example:
```{code} toml
:filename: pyproject.toml
:linenos:
[tool.pixi.pypi-dependencies]
my_pyproject = { path = ".", editable = true }
```
:::
::::


What pixi does differently from managing PyPI packages through other package managers, is that it will install the packages in the same environment as the conda packages, but will not overwrite the conda packages.
We've got a mapping between the conda packages and the PyPI packages, so that we can let `uv` know which packages to install and which packages to ignore because they are already installed.

::: {note} Pixi doesn't install `uv`!
While Pixi uses `uv` to install the PyPI packages, it doesn't install `uv` itself.
So you cannot us `uv` directly in the project, without installing it first.
:::

## Special types of dependencies
Pixi has a few special types of dependencies that you can use in the project.
- `git`: You can use the `git` dependency to install packages from a git repository.
- `path`: You can use the `path` dependency to install packages from a local directory.
- `editable`: You can use the `editable` dependency to install packages in editable mode.
- `url`: You can use the `url` dependency to install packages from a URL.
**TODO**: Add more information about these dependencies.

## Removing dependencies
**TODO**: Add information about removing dependencies.

## Updating dependencies
**TODO**: Add information about updating dependencies.



## Lockfile
The lockfile is a file that contains the exact versions of the packages that were installed in the environment.
This file is used to ensure that the same versions of the packages are installed in the environment when the project is shared with others.
What should you know about the lockfile?
- The lockfile is called `pixi.lock` and is located in the root of the project, next to the `pixi.toml` or `pyproject.toml` file.
- The lockfile is a YAML file that contains the exact versions of the packages that were installed in the environment.
- The lockfile is automatically (re-)generated when you `add`, `remove`, `update` a package in the project, or when you run `pixi install/run/shell/lock` and it's not existing yet.
- The lockfile is meant to be shared with others, so that they can reproduce the same environment.
- The lockfile is not meant to be edited manually, as it is automatically generated by Pixi.

```{code} yaml
:filename: pixi.lock
:caption: Example lockfile, highly simplified for readability
:linenos:
version: 6
environments:
  default:
    channels:
    - url: https://prefix.dev/conda-forge/
    indexes:
    - https://pypi.org/simple
    packages:
      osx-arm64:
      - conda: https://prefix.dev/conda-forge/osx-arm64/bzip2-1.0.8-h99b78c6_7.conda
      - pypi: ...
packages:
- conda: https://prefix.dev/conda-forge/osx-arm64/bzip2-1.0.8-h99b78c6_7.conda
  sha256: adfa71f158cbd872a36394c56c3568e6034aa55c623634b37a4836bd036e6b91
  md5: fc6948412dbbbe9a4c9ddbbcfe0a79ab
  depends:
  - __osx >=11.0
  license: bzip2-1.0.6
  license_family: BSD
  size: 122909
  timestamp: 1720974522888
- pypi: ...
```


# Managing tasks
Pixi has a built-in {term}`cross-platform` task runner that allows you to define tasks in the manifest.
This is a great way to share tasks with others and to ensure that the same tasks are run in the same environment.
The tasks are defined in the `[tasks]` section.

## Basic tasks

You can use the `pixi task` command to modify the tasks in the project.
```bash
pixi task add hello "echo Hello World"
```
This will add a new task called `hello` to the project, which will print `Hello World` to the console.
```{code} toml
:filename: pixi.toml
:linenos:
[tasks]
hello = "echo Hello World"
```
You can also use the `pixi run` command to run the tasks in the project.
```bash
pixi run hello
```
This will run the `hello` task and print `Hello World` to the console.

## Task arguments
Now also have the ability to receive arguments in the task.
```bash
pixi task add greet "echo Hello {{name | capitalize}}" --arg name
```
This will add a new task called `greet` to the project, which will print `Hello {{name}}` to the console.
You can also use the `pixi run` command to run the tasks in the project.
```bash
pixi run greet matthew
```
This will run the `greet` task and print `Hello Matthew` to the console.
Using the [MiniJinja](https://github.com/mitsuhiko/minijinja) templating engine integration, it has capitalized the name.

Failing to provide the argument will result in an error.
So it's sometimes recommended to provide a default value for the argument.
You can replace the old task definition with the following:
```{code} toml
:filename: pixi.toml
greet = { cmd = "echo Hello {{name | capitalize}}", args = ["name"] }
```
with the following, this uses a nested table to make it more readable:

```{code} toml
:filename: pixi.toml
:linenos:
:emphasize-lines: 3
[tasks.greet]
cmd = "echo Hello {{name | capitalize}}"
args = [{arg = "name", default = "World"}]
```

and run the task again:

```bash
➜ pixi run greet
✨ Pixi task (greet): echo Hello World
Hello World
```

This will run the `greet` task and print `Hello World` to the console.

## Task Graph
Pixi has a built-in task graph that allows you to define tasks that depend on other tasks.

```toml
[tasks]
greet-matthew = [{ task = "greet", args = ["Matthew"] }]

[tasks.greet]
cmd = "echo Hello {{name | capitalize}}"
args = [{arg = "name", default = "World"}]
```
This will add a new task called `greet-matthew` that depends on the `greet` task.
It also shows how to use the `args` field to pass arguments to the task.

You can also have multiple tasks that depend on the same task.
A classic pseudo example would be to have a `build` task that depends on a `fmt` and `test` task.
```toml
[tasks]
fmt = "echo formatting"
test = "echo testing"
build = { cmd = "echo build command", depends-on = ["fmt","test"] }
```
Resulting in:
```bash
➜ pixi run build
✨ Pixi task (fmt): echo formatting
formatting

✨ Pixi task (test): echo testing
testing

✨ Pixi task (build): echo build command
build command
```

## Task caching
Pixi has a built-in task caching system that allows you to cache the results of tasks.
This is a great way to speed up the build process and to avoid running the same tasks multiple times.

You can add the files you want to base the cache on in the task definition.
```toml
[tasks.generate]
cmd = "echo foo > generated.txt"
inputs = ["pixi.toml"]
outputs = ["generated.txt"]
```

Now when you run the task, it will check if the `pixi.toml` file has changed and if the `generated.txt` file exists.
If the `pixi.toml` file has not changed and the `generated.txt` file exists, it will skip the task and use the cached result.

This feature is very useful for tasks that take a long time to run, like building a package or running tests.
Often used for building or downloading large files.

# Activating environments
Now you know the basics of dealing with the Pixi manifest.
Next step is actually using the environments.
You have already seen the `pixi run` command, which will run the task in the environment.
You can also use the `pixi shell` command to open a shell in the environment.

Both commands will automatically activate the environment for you, so you don't have to worry about that.
Activating an environment is not much more than running a script that sets the environment variables for you.
To investigate this, you can use `pixi shell` to view what the shell script looks like.
```bash
pixi shell-hook
```
This will print the shell script that is used to activate the environment.

- `pixi shell` will open a new shell and run that script in it.
- `pixi run` will run the script in a subshell and then parse the changes to the environment variables. Which are then forwarded to the task runner.
- `eval "$(pixi shell-hook)"` will run the script in the current shell and activate the environment in the running shell, this is the closest to `conda activate` or `source .venv/bin/activate`, but not recommended.



# Managing global tools
*Maybe add a section about managing global tools*
