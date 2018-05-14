.PHONY: clean-pyc clean-build docs clean

TEST_FLAGS=--verbose
COVER_FLAGS=--cov=organizations

help:
	@echo "install - install all requirements including for testing"
	@echo "install-quite - same as install but pipes all output to /dev/null"
	@echo "clean - remove all artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-test-all - remove all test-related artifacts including tox"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-coverage - run tests with coverage report"
	@echo "test-all - run tests on every Python version with tox"
	@echo "check - run all necessary steps to check validity of project"
	@echo "release - package and upload a release"
	@echo "dist - package"

install:
	pip install -r requirements-dev.txt

install-quiet:
	pip install -r requirements-dev.txt > /dev/null

clean: clean-build clean-pyc clean-test-all

clean-build:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

clean-pyc:
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf &> /dev/null

clean-test:
	rm -rf .coverage coverage*
	rm -rf tests/.coverage test/coverage*
	rm -rf htmlcov/

clean-test-all: clean-test
	rm -rf .tox/

format:
	black organizations tests example test_abstract test_accounts test_custom test_vendors

lint:
	flake8 organizations

test:
	pytest ${TEST_FLAGS}

test-coverage: clean-test
	-pytest ${COVER_FLAGS} ${TEST_FLAGS}
	@exit_code=$?
	@-coverage html
	@exit ${exit_code}

test-all:
	tox


check: clean-build clean-pyc clean-test lint test-coverage

build: clean  ## Create distribution files for release
	pytest -k test_no_missing_migrations
	python setup.py sdist bdist_wheel

release: build  ## Create distribution files and publish to PyPI
	python setup.py check -r -s
	twine upload dist/*

sdist: clean  ##sdist Create source distribution only
	python setup.py sdist
	ls -l dist

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html
