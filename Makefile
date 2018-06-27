.PHONY: clean-pyc clean-build docs clean

TEST_FLAGS=--verbose
COVER_FLAGS=--cov=organizations

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## install all requirements including for testing
	pip install -r requirements-dev.txt

install-quiet:  ## same as install but pipes all output to /dev/null
	pip install -r requirements-dev.txt > /dev/null

clean: clean-build clean-pyc clean-test-all  ## remove all artifacts

clean-build:  ## remove build artifacts
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

clean-pyc:  ## remove Python file artifacts
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf &> /dev/null

clean-test:  ## remove test and coverage artifacts
	rm -rf .coverage coverage*
	rm -rf tests/.coverage test/coverage*
	rm -rf htmlcov/

clean-test-all: clean-test  ## remove all test-related artifacts including tox 
	rm -rf .tox/

format:  ## format the code with Black
	black organizations tests example test_abstract test_accounts test_custom test_vendors

lint:  ## check style with flake8
	flake8 organizations

test:  ## run tests quickly with the default Python
	pytest ${TEST_FLAGS}

test-coverage: clean-test  ## run tests with coverage report
	-pytest ${COVER_FLAGS} ${TEST_FLAGS}
	@exit_code=$?
	@-coverage html
	@exit ${exit_code}

test-all:  ## run tests on every Python version with tox
	tox

check: clean-build clean-pyc clean-test lint test-coverage  ## run all necessary steps to check validity of project

build: clean  ## Create distribution files for release
	# pytest -k test_no_missing_migrations
	python setup.py sdist bdist_wheel

release: build  ## Create distribution files and publish to PyPI
	python setup.py check -r -s
	twine upload dist/*

sdist: clean  ## Create source distribution only
	python setup.py sdist
	ls -l dist

docs:  ## Build and open docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html
