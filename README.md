# Starter Python project

Starter Python project for own use.

## Features

- Scrape and download digital catalogs from Aldi, Lidl, and Spar websites.
- Analyze catalog pages using vision AI to extract discount details.
- Save the extracted discount data in CSV and JSON formats.
- Modular and extensible architecture for adding new stores or analysis methods.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tardigrde/python-ai-starter.git
cd python-ai-starter
```

2. Install dependencies using `uv`:

```bash
# Install
uv sync
# Activate
. .venv/bin/activate
```

3. Create a `.env` file with your API keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

Use the provided Makefile targets to run the project.

### Greet user

```bash
make greet NAME=World
```

## Development

Use the provided Makefile targets for development tasks.

### Run Tests

```bash
make test
```

### Run Integration Tests

```bash
make test-integration
```

### Check Code Formatting and Linting

```bash
make check
```

### Format Code

```bash
make format
```

### Run Type Checking

```bash
make typecheck
```

### Clean Project Files

```bash
make clean
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
