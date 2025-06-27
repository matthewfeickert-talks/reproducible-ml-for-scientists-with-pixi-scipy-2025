# Pixi: exercises
This page contains exercises to help you practice the concepts learned in the Pixi introduction. Each exercise is designed to reinforce your understanding of Pixi's features and capabilities.

## Exercise 1: Creating a project
1. Create a new Pixi project named `my-project` using the command line.
2. Add `python` as a dependency to your project.
3. Use the Pixi installed Python to print `"Hello, Pixi!"` to the console.
4. Run a command to print the version of Python used in your project. You can see the location of the interpreter by running: `import sys;print(sys.executable)`

:::{hint} Solution
:class: dropdown
```bash
# 1
pixi init my-project
cd my-project
# 2
pixi add python
# 3
pixi run python -c 'print("Hello, Pixi!")'
# 4
pixi run python -c 'import sys; print(sys.version); print(sys.executable)'
```
:::

## Exercise 2: Dependencies
1. Make your project work for Windows, macOS, and Linux.
2. Add `scipy` as a dependency through the command line.
3. Add `numpy` as a dependency through the command line.
4. Add `fastqc` as a dependency from `bioconda`. Hint: the channel has to be added first.
5. Add `pandas` as a `pypi` dependency through the command line.
6. Add a `pypi` + `git` dependency on [`pytest`](https://github.com/pytest-dev/pytest) to your project.
7. Visualize the locked dependencies in the command line.

:::{hint} Solution
:class: dropdown
```bash
# 1
pixi workspace platform add win-64 osx-arm64 osx-64 linux-64
# 2
pixi add scipy
# 3
pixi add numpy
# 4
pixi workspace channel add bioconda
pixi add bioconda::fastqc
# 5
pixi add pandas --pypi
# 6
pixi add pytest --pypi --git https://github.com/pytest-dev/pytest
# 7: Any of:
pixi list
pixi list -x
pixi tree
```
:::

## Exercise 3: Modifying dependencies
1. Replace `pandas` with a conda dependency on `pandas` from the `conda-forge` channel. Hint: make sure it worked by checking the environment with `pixi list pandas`
2. Require the `scipy` dependency to be version `1.15.1`.
3. Make the `pytest` use version `8.3.1` from the `git` repository.

:::{hint} Solution
:class: dropdown
```bash
# 1
pixi add pandas
pixi list pandas
# Optionally, you can remove the old pandas dependency:
pixi remove pandas --pypi
# 2
pixi add scipy==1.15.1
# 3
pixi add pytest --pypi --git https://github.com/pytest-dev/pytest.git --tag 8.3.1
```
:::

## Exercise 4: Multiple environments
1. Make `pytest` part of the `test` feature.
2. Create a new environment named `test` that includes the `test` feature.
3. Install the `test` environment.
4. Run the `pytest` command in the `test` environment to ensure it works correctly.
5. Create a `format` feature that includes `ruff`.
6. Create a new environment named `format` that includes the `format` feature but not the `default` and `test` features.
7. Run `ruff  --version`.
8. Now make sure the `test` and `default` environments are using the same solve group.
9. Compare the dependencies with `pixi list --explicit --environment ENV_NAME`. Validate the versions of the dependencies in both environments are the same.

::::{hint} Solution
:class: dropdown
1: move `pytest` from `[pypi-dependencies]` to `[feature.test.pypi-dependencies]` in `pixi.toml`:
:::{code}diff
:filename: pixi.toml
-[pypi-dependencies]
+[feature.test.pypi-dependencies]
pytest = { git = "https://github.com/pytest-dev/pytest.git", tag = "8.3.1" }
:::
```bash
# 2
pixi workspace environment add test --feature test
# 3
pixi install --environment test
# Or short:
pixi i -e test
# 4
pixi run -e test pytest # Expect the test to fail as there are no tests ;).
# 5
pixi add ruff --feature format
# 6
pixi workspace environment add format --feature format --no-default-feature
# 7
pixi run -e format ruff --version
# 8
pixi workspace environment add test --feature test --solve-group group1 --force
pixi workspace environment add default --solve-group group1 --force
# 9
pixi list -x -e test
pixi list -x
```
::::


## Exercise 5: Task running
1. Create a task named `hello` that prints `"Hello, Pixi!"` to the console.
2. Create a task named `greet` that prints `"Hello, <name>!"` to the console, where `<name>` is a argument passed to the task.
3. Create a task named `greet-YOUR_NAME` that prints `"Hello, YOUR_NAME!"` to the console, where it depends on the `greet` task and gives it an argument.
4. Create a `start` task that runs the `hello` task first and then the `greet` task, but with the arguments passed to the `start` task, passed to the `greet` task.
5. Run all these tasks.
6. Add the task `fmt` to the `format` feature that runs `ruff --version`.
7. Run the `fmt` task.

:::{hint} Solution
:class: dropdown
```bash
# 1
pixi task add hello 'echo "Hello, Pixi!"'
# 2
pixi task add greet 'echo "Hello, {{ name }}!"' --arg name
# 3
pixi task add greet-YOUR_NAME --depends-on greet::YOUR_NAME
# 4
pixi task add start --depends-on hello --depends-on greet::{{ name }} --arg name
# 5
pixi run hello
pixi run greet your_name
pixi run greet-YOUR_NAME
pixi run start your_name
# 6
pixi task add fmt 'ruff --version' --feature format
# 7 Notice that it automatically runs in the `format` environment.
pixi run fmt
```
:::

## Exercise 6: Activation
1. Set an environment variable named `MY_ENV_VAR` to the value `Hello, Pixi!` in the `default` environment.
2. Create a task named `print-env` that prints the value of `MY_ENV_VAR` to the console.
3. Run the `print-env` task in the `default` environment to ensure it prints the correct value.
4. Use `pixi shell` to activate the environment in the current shell.
5. Verify that the `MY_ENV_VAR` is set in the current shell by running `echo $MY_ENV_VAR` (or `echo %MY_ENV_VAR%` on Windows).

::::{hint} Solution
:class: dropdown
1. Set the environment variable in the `pixi.toml` file:
:::{code} toml
:filename: pixi.toml
[activation.env]
MY_ENV_VAR = "Hello, Pixi!"
:::

```bash
# 2
pixi task add print-env 'echo $MY_ENV_VAR'
# 3
pixi run print-env
# 4
pixi shell
# 5
echo $MY_ENV_VAR
# Or on Windows:
echo %MY_ENV_VAR%
```
::::
