.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock
test:
	tox -e test

pylint:
	pipenv run pylint skeleton

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=requests skeleton tests

clean:
	rm -fr dist .egg requests.egg-info build

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"