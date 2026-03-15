# Contributing to TRITIUM-Watcher

Thank you for your interest in contributing to TRITIUM-Watcher! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report:
1. **Check existing issues** to avoid duplicates
2. **Collect information** about your environment:
   - OS and version
   - Python version
   - TRITIUM-Watcher version
   - Steps to reproduce

**Submit bugs via** [GitHub Issues](https://github.com/Aarav482011/TRITIUM-Watcher/issues) with:
- Clear, descriptive title
- Detailed description
- Exact steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Error messages and stack traces

### 💡 Suggesting Features

Feature requests are welcome! Please:
1. **Check if the feature already exists** or is planned
2. **Explain the use case** - why is this needed?
3. **Describe the solution** you'd like
4. **Consider alternatives** you've thought about

### 📝 Improving Documentation

Documentation improvements are always appreciated:
- Fix typos or clarify confusing sections
- Add examples for common use cases
- Improve API documentation
- Translate documentation (coming soon)

### 💻 Code Contributions

We welcome pull requests! See below for guidelines.

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv)

### Setup Steps

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork" button
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/TRITIUM-Watcher.git
   cd TRITIUM-Watcher
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Aarav482011/TRITIUM-Watcher.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   playwright install chromium
   ```

6. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

---

## Development Workflow

### 1. Create a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 2. Make Changes

- Write clean, readable code
- Follow PEP 8 style guide
- Add docstrings for functions/classes
- Write tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_watchdog.py

# Run with coverage
pytest --cov=tritium_watcher tests/

# Lint your code
flake8 tritium_watcher.py
black --check tritium_watcher.py
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: keyword highlighting in screenshots"
```

**Commit message guidelines:**
- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issue numbers: "Fixes #123"

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then on GitHub:
1. Navigate to your fork
2. Click "Compare & pull request"
3. Fill out the PR template
4. Wait for review

---

## Code Style Guidelines

### Python Style

Follow **PEP 8** with these specifics:

```python
# Good
def extract_keywords(url: str, keywords: list[str]) -> dict:
    """
    Extract keywords from a URL.
    
    Args:
        url: The URL to scrape
        keywords: List of keywords to search for
        
    Returns:
        Dictionary containing matches and metadata
    """
    result = {"matches": [], "url": url}
    return result

# Bad
def extract_keywords(url,keywords):
    result={"matches":[],"url":url}
    return result
```

### Key Points

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 88 characters (Black default)
- **Imports**: Organized (standard lib, third-party, local)
- **Type hints**: Use for function signatures
- **Docstrings**: Use Google-style format

### Formatting Tools

We use automated formatters:

```bash
# Format with Black
black tritium_watcher.py

# Sort imports
isort tritium_watcher.py

# Lint with flake8
flake8 tritium_watcher.py
```

---

## Testing Guidelines

### Writing Tests

```python
import pytest
from tritium_watcher import distill_essence

def test_distill_essence_valid_url():
    """Test that distill_essence works with valid URL"""
    result = distill_essence("https://example.com")
    assert "insights" in result
    assert len(result["insights"]) == 5

def test_distill_essence_invalid_url():
    """Test that invalid URL raises appropriate error"""
    with pytest.raises(ValueError):
        distill_essence("not-a-url")
```

### Test Coverage

- Aim for **80%+ code coverage**
- Test happy paths AND edge cases
- Test error handling
- Use mocks for external dependencies (web requests, file I/O)

### Running Tests

```bash
# All tests
pytest

# Specific test
pytest tests/test_watchdog.py::test_watchdog_creation

# With output
pytest -v

# Stop on first failure
pytest -x

# Generate coverage report
pytest --cov=tritium_watcher --cov-report=html
```

---

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted (Black, isort)
- [ ] Linting passes (flake8)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How was this tested?

## Screenshots (if applicable)

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. Maintainer reviews within 3-5 days
2. Address feedback in new commits
3. Once approved, maintainer will merge
4. Your contribution will be in the next release!

---

## Good First Issues

New to the project? Look for issues labeled:
- `good first issue` - Perfect for newcomers
- `help wanted` - We need assistance
- `documentation` - Docs improvements

### Example First Contributions

- Fix typos in documentation
- Add examples to README
- Improve error messages
- Add unit tests for existing functions
- Implement simple feature requests

---

## Project Structure

```
TRITIUM-Watcher/
├── tritium_watcher.py      # Main application code
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── tests/                  # Test files
│   ├── test_distill.py
│   ├── test_watchdog.py
│   └── test_persistence.py
├── docs/                   # Documentation
│   ├── API_REFERENCE.md
│   └── examples/
├── screenshots/            # Generated screenshots
├── WATCHDOG_LOG.md        # Generated log file
├── .gitignore
├── LICENSE
├── README.md
└── CONTRIBUTING.md         # This file
```

---

## Getting Help

Stuck? Have questions?

- **GitHub Discussions** - Ask questions, share ideas
- **GitHub Issues** - Bug reports, feature requests
- **Email** - sparklabs2011@gmail.com

---

## Recognition

Contributors are recognized in:
- GitHub contributors list
- CHANGELOG.md
- README.md (for significant contributions)

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (PolyForm Noncommercial License 1.0.0 for personal use).

---

**Thank you for contributing to TRITIUM-Watcher! Every contribution, no matter how small, is valuable.** 🎉
