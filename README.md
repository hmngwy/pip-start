# `pip-start`

is a template for OSS pip packages, I designed this to help build sparser packages for [Microservices](https://en.wikipedia.org/wiki/Microservices) architecture.

#### Summary of Tools

##### Test
- pytest
- pytest-runner

##### Develop

- autopep8
- bumpversion
- pip-autoremove
- pip-tools _(for good measure)_
- pylint
- pycodestyle
- pydocstyle
- tox

### Setup Tools
Know that dependencies are cascaded (more below in Managing Dependencies), any of the commands below in this section will install the dependencies of the ones above it.

##### Installing your package
`pip install .` and __not__ `python setup.py install`, the latter can't use wheels.

##### Test Package
`python setup.py test`

##### Develop Package
`pip install -e '.[develop]'`

### Package Versioning
Do `bumpversion major/minor/patch`  to increment version. bumpversion uses Semver. Default command arguments defined in setup.cfg.

### Managing Dependencies
Packages are abstracted by use-case under requirements/*.in files, they are also cascaded `base.in < test.in < develop.in`.

`base.in` will hold the minimum of dependencies, usually the only thing installed in production.

`test.in` will have additional packages just enough to run tests.

`develop.in` will have everything necessary to contribute to this package.

Once `make requirements` are run, `.txt` files should be versioned in the vcs because that's just how pip-tools rock, also because version pinning. 

`.in` files cascades `.txt` and not `.in` files because, for example, we want tests to use the same pinned versions as base.

##### Building requirements .txt files
```bash
make rq_clean requirements
```

##### Adding a dependency
```bash
cat >> requirements/base.in
numpy
make requirements
```

##### Upgrading a dependency
```bash
sed '/ipython/d' -i requirements/*.txt # Careful with this
make requirements
```

### Unit Testing
Do `pytest` or `python setup.py test` in project root, also aliased as `test`. Test cases live in `./tests`.

### Continuous Integration
A basic TravisCI config that runs `tox` is included. 

### Multi-environment Testing 
By default tox is configured to test

- Production installation of your package, aka `pip install .`
- Non-develop `tests`, aka `python setup.py test`
- Develop install, aka `pip install -e '.[develop]'`

### Package Custom Scripts/Commands
Automatically loaded by `setup.py` from `./bin`.