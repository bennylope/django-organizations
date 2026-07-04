# List available recipes
default:
    @just --list

# Install the package and dev dependencies
install:
    uv sync

# Remove build, test, Python artifacts
clean: clean-build clean-pyc clean-test-all

# Remove build artifacts
clean-build:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info

# Remove Python file artifacts
clean-pyc:
    find . -name '*.pyc' -delete
    find . -name '*.pyo' -delete
    find . -name '__pycache__' -type d -exec rm -rf {} +

# Remove test and coverage artifacts
clean-test:
    rm -rf .coverage coverage* htmlcov/

# Remove all test-related artifacts including tox
clean-test-all: clean-test
    rm -rf .tox/

# Format code with ruff
format:
    uv run ruff format src/ tests/

# Check style and formatting with ruff
lint:
    uv run ruff check .
    uv run ruff format --check .

# Run tests with the current Python
test *args:
    uv run pytest --verbose {{args}}

# Test with an HTML coverage report
test-coverage: clean-test
    uv run pytest --verbose
    uv run coverage html

# Test all supported Python and Django versions with tox
test-all:
    uv run tox

# Run all necessary steps to check validity of project
check: clean-build clean-pyc clean-test lint test-coverage

# Create distribution files for release
build: clean
    uv build

# Create distribution and publish to PyPI
release: build
    uvx twine check dist/*
    uvx twine upload dist/*

# Create source distribution only
sdist: clean
    uv build --sdist
    ls -l dist

# Build (and open) docs
docs:
    make -C docs clean
    make -C docs html
    open docs/_build/html/index.html
