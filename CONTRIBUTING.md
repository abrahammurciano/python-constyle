# Poetry

This project uses poetry to manage dependencies. To get your development environment set up, run:

```sh
$ poetry install
```

The activate your shell environment by running:

```sh
$ poetry shell
```

All future commands assume you have already run that in the current shell.

# Tests

This project uses pytest to run tests. To run tests locally, run:

```sh
$ pytest
```

Tests will be triggered by opening a pull request to main.

# Documentation

Documentaion is generated using pdoc3. To generate documentation, run:

```sh
$ pdoc constyle --html -o docs/ -f -c show_source_code=False
```

If you don't, it will be generated automatically on merge to main.

# Code style

Code is formatted with black. Please keep it that way.

```sh
$ black constyle
```

If you don't, it will be formatted automatically on merge to main.

# Deployment

To deploy a new version simply create a release on GitHub. The version will be automatically detected from the tag name. It should start with `v` and be followed by the actual version string.

Versions are deployed to PyPI and Anaconda automatically.