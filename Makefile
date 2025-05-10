.PHONY: install format lint check clean format-check typecheck test test-integration test-coverage greet

# Install dependencies
install:
	@echo "Installing dependencies with uv..."
	uv sync

###############################################################################
# Tests
###############################################################################

# Run unit tests
test:
	@echo "Running fast tests..."
	python -m pytest -s -vv -m "not integration"

# Run all tests including slow tests
test-integration:
	@echo "Running all integration tests..."
	python -m pytest -s -vv -m "integration"

# Run fast tests with verbose output
test-all:
	@echo "Running fast tests with verbose output..."
	python -m pytest -s -vv

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage report..."
	# Note: This still does not work for main.py and bot.py
	python -m pytest -s -vv --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml

###############################################################################
# Formatting & Linting
###############################################################################

# Format code with Ruff
format:
	@echo "Formatting code with Ruff..."
	ruff format .

# Check code format with Ruff
format-check:
	@echo "Checking code format with Ruff..."
	ruff format . --check

# Run Ruff linter and complexity check
lint:
	@echo "Running Ruff linter and complexity check..."
	ruff check --fix main.py src/*

# --explicit-package-bases tells mypy to treat packages as package roots
# also exlcuded tests from type checking for now
typecheck:
	mypy --explicit-package-bases main.py src/

# Quick style and complexity check with Ruff and typecheck with mypy
check: format-check lint typecheck
	@echo "Running quick style check, complexity check, and typecheck..."

###############################################################################
# Cleanup
###############################################################################

# Clean up cache files
clean:
	@echo "Cleaning up cache and coverage files..."
	find . -type d -name "ai_starter.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf build
	rm -rf htmlcov
	rm -f .coverage
	rm -rf coverage.xml

###############################################################################
# Features
###############################################################################

greet:
	python main.py --name $(NAME)

greet-generated:
	python main.py --generate
