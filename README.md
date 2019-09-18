# Python Differential Privacy Library

[![Python versions](https://img.shields.io/pypi/pyversions/differential-privacy.svg)](https://pypi.org/project/differential-privacy/)
[![PyPi version](https://img.shields.io/pypi/v/differential-privacy.svg)](https://pypi.python.org/pypi/differential-privacy)
[![Build Status](https://travis-ci.org/robomotic/differential-privacy.svg?branch=master)](https://travis-ci.org/robomotic/differential-privacy)
[![Coverage Status](https://coveralls.io/repos/github/robomotic/differential-privacy/badge.svg?branch=master)](https://coveralls.io/github/robomotic/differential-privacy?branch=master)

A library that contains implementations of differential privacy algorithms found in literature.

Usage
-----

## Setup

### Installation with `pip`

The library is designed to run with Python 3.
The library can be installed from the PyPi repository using `pip` (or `pip3`):

```bash
pip install differential-privacy
```

### Manual installation

For the most recent version of the library, either download the source code or clone the repository in your directory of choice:

```bash
git clone https://github.com/robomotic/differential-privacy.git
```

To install `differential-privacy`, do the following in the project folder (alternatively, you can run `python3 -m pip install .`):
```bash
pip install .
```

The library comes with a basic set of unit tests for `pytest`. To check your install, you can run all the unit tests by calling `pytest` in the install folder:

```bash
pytest
```

