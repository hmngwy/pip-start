# `pip-start`

is a template for OSS pip packages, I designed this to help build sparser packages for [Microservices](https://en.wikipedia.org/wiki/Microservices) architecture based systems.

[![Build Status](https://travis-ci.org/hmngwy/pip-start.svg?branch=master)](https://travis-ci.org/hmngwy/pip-start) [![CircleCI](https://circleci.com/gh/hmngwy/pip-start.svg?style=svg)](https://circleci.com/gh/hmngwy/pip-start)

## Summary of Tools

#### Testing
- pytest
- pytest-runner

#### Development

- autopep8
- bumpversion
- pip-autoremove
- pip-tools _(for good measure)_
- pylint
- pycodestyle
- pydocstyle
- tox

## Setup Tools
Know that dependencies are cascaded (more below in Managing Dependencies), any of the commands below in this section will install the dependencies of the ones above it.

#### Install package
`pip install .` and __not__ `python setup.py install`, the latter can't use wheels.

#### Testing the package
`pip install -e .[test] && pytest`

`pytest` will only work if you at the least run `pip install -r requirements/test.txt`, the above command automates this step if necesarry.

#### Develop the package
`pip install -e '.[develop]'`

## Package Versioning
Do `bumpversion major/minor/patch`  to increment version. bumpversion uses Semver. Default command arguments defined in setup.cfg.

## Managing Dependencies
Using `pip-tools` packages are abstracted by use-case under `requirements/*.in` files, they are also cascading `base.in < test.in < develop.in`.

> ###### `base.in`
> will hold the minimum of dependencies, usually the only thing installed in production.
> ###### `test.in`
> will have additional packages just enough to run tests.
> ###### `develop.in`
> will have everything necessary to contribute to this package.

Additionally we have `deploy.in`, that depends on `test.txt`. Good for publishing packages to custom pypi (and or private) servers.

> ###### `deploy.in`
> will have everything necessary to deploy this package to a pypi server.

Once `make requirements` are run, `.txt` files should be versioned in the vcs because that's just how pip-tools rock, also because version pinning.

`.in` files cascades `.txt` and not `.in` files because, for example, we want tests to use the same pinned versions as base.

#### Building requirements .txt files
```bash
make rq_clean requirements
```

#### Adding a dependency
```bash
cat >> requirements/base.in
numpy [ctrl-d]
make requirements
```

#### Upgrading a dependency
```bash
sed '/ipython/d' -i requirements/*.txt # Careful with this
make requirements
```

## Unit Testing
Do `pytest` and __never__ ~~`python setup.py test`~~ in project root. Because of bdist_wheel, we can't use tests_require kwarg in setup() that is require by `setup.py test`.

Test cases live in `./tests`.

## Multi-environment Testing
Do `tox` in project root. This means your CI should only need `pip install tox` as a minimum to test this whole package.

## Continuous Integration
A basic TravisCI and CircleCI config that runs `tox` is included.

CircleCI needs `pyenv global x.x.x` because they just had to use pyenv.


## Multi-environment Testing
By default tox is configured to test

- Production installation of your package, aka `pip install .`
- Non-develop `tests`, aka `python setup.py test`
- Develop install, aka `pip install -e '.[develop]'`

## Building and Publishing/Deployment

If you have deployment dependencies, they're best placed in `requirements/deploy.in`. Then in your deployment flow, install the package via `pip install '.[deploy]'`.

Building is still done through setup tools, make sure you have `wheels` in your venv.

`python setup.py sdist --formats gztar bdist_wheel`

If you're uploading to PyPa, the currently official way of uploading to PyPa is using twine, the command `twine upload dist/*` is supported and twine is already in `deploy.in`.

## Package Custom Scripts/Commands
Automatically loaded by `setup.py` from `./bin`.



##### Inspiration
- [Better Package Management](http://nvie.com/posts/better-package-management/#virtue-2-have-your-envs-reflect-your-specs)
- [A successful pip-tools workflow for managing Python package requirements](http://jamescooke.info/a-successful-pip-tools-workflow-for-managing-python-package-requirements.html)
- [Open Sourcing a Python Project the Right Way](https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)
- [Cookiecutter PyPackage](https://github.com/audreyr/cookiecutter-pypackage)

> Why isn't this a `cookiecutter` package?
Because I plan on creating my own cli tool for this template.