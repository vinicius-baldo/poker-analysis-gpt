# Development Guide

## Code Formatting

This project uses automated code formatting to maintain consistent code style. The following tools are used:

- **black**: Python code formatter
- **isort**: Import statement organizer

### Pre-commit Setup

The project includes a pre-commit hook that automatically runs formatting tools before each commit:

1. **Pre-commit script**: `./pre-commit` - Runs black and isort on staged Python files
2. **Git hook**: `.git/hooks/pre-commit` - Automatically executes the pre-commit script

### Manual Formatting

You can also run the formatting tools manually:

```bash
# Format all Python files
black *.py
isort *.py

# Format specific files
black file1.py file2.py
isort file1.py file2.py
```

### Installation Requirements

Make sure you have the formatting tools installed:

```bash
# Using Homebrew (macOS)
brew install black isort

# Using pip
pip install black isort
```

## Development Workflow

1. **Make changes** to your code
2. **Stage files** for commit: `git add .`
3. **Commit changes**: `git commit -m "Your message"`
   - The pre-commit hook will automatically run black and isort
   - If formatting changes are made, they will be automatically staged
4. **Push changes**: `git push`

## Code Style

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 88 characters (black default)
- **Import organization**: Standard library → Third-party → Local (isort default)
- **Quote style**: Double quotes (black default)

## Troubleshooting

### Pre-commit hook not working

If the pre-commit hook isn't running:

1. Check if the hook is executable: `ls -la .git/hooks/pre-commit`
2. Make it executable: `chmod +x .git/hooks/pre-commit`
3. Verify the pre-commit script exists: `ls -la pre-commit`

### Formatting tools not found

If you get errors about missing tools:

```bash
# Install with Homebrew
brew install black isort

# Or install with pip
pip install black isort
```

### Skipping pre-commit (emergency)

If you need to skip the pre-commit hook in an emergency:

```bash
git commit --no-verify -m "Emergency commit"
```

**Note**: This should only be used in emergencies. The pre-commit hook helps maintain code quality.
