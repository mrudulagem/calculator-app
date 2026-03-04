# Calculator App — AI-Powered Auto Testing

A Python calculator with an **AI agent that automatically generates and runs unit tests** whenever you change your source code.

---

## How It Works

```
You save calculator.py
        ↓
watch_and_test.py detects the file change
        ↓
Claude Code reads the updated source code
        ↓
Claude generates comprehensive pytest unit tests
        ↓
Tests are written to tests/test_calculator.py
        ↓
pytest runs automatically and reports results
```

Every time you add or modify a function in `src/calculator.py`, the AI agent wakes up, reads your code, and writes fresh tests for it — including normal cases, edge cases, and exception handling. No manual test writing required.

---

## Project Structure

```
Calculator/
├── src/
│   ├── calculator.py            # Your application code
│   ├── watch_and_test.py        # AI agent — watches for changes and generates tests
│   └── agent_generate_tests.py  # One-shot test generator (manual use)
├── tests/
│   ├── __init__.py
│   └── test_calculator.py       # Auto-generated tests (do not edit manually)
└── README.md
```

---

## Prerequisites

- Python 3.8+
- Node.js 18+
- A Claude Pro or Max subscription (claude.ai)
- Claude Code CLI installed

---

## Installation

### 1. Install Claude Code

```powershell
winget install Anthropic.ClaudeCode
```

Or via PowerShell:
```powershell
irm https://claude.ai/install.ps1 | iex
```

Verify it works:
```powershell
claude --version
```

### 2. Install Python dependencies

```powershell
pip install pytest pytest-cov watchdog
```

### 3. Clone the repo

```powershell
git clone https://github.com/YOUR_USERNAME/calculator-app.git
cd calculator-app
```

---

## Running the AI Test Agent

### Auto mode — watches for changes (recommended)

Start the watcher from the project root:

```powershell
python src\watch_and_test.py
```

You will see:
```
👀 Watching for changes in 'src'...
   Save any .py file to auto-generate its tests. Ctrl+C to stop.
```

Now just **save any `.py` file** in `src/` and the agent will:
1. Detect the change
2. Call Claude to generate tests
3. Write them to `tests/test_calculator.py`
4. Run pytest and show you the results

Press `Ctrl+C` to stop the watcher.

### Manual mode — generate tests once

```powershell
python src\agent_generate_tests.py
```

This reads `src/calculator.py` and writes tests to `tests/test_calculator.py` once, without watching.

---

## Running Tests Manually

To run the test suite at any time:

```powershell
pytest tests/ -v
```

To run with a coverage report:

```powershell
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Example

Add a new function to `calculator.py`:

```python
def square_root(x):
    if x < 0:
        raise ValueError("Cannot take square root of a negative number")
    return x ** 0.5
```

Save the file. The agent immediately generates tests like:

```python
def test_square_root_positive_number():
    assert square_root(9) == pytest.approx(3.0)

def test_square_root_zero():
    assert square_root(0) == 0.0

def test_square_root_negative_raises_value_error():
    with pytest.raises(ValueError, match="Cannot take square root of a negative number"):
        square_root(-1)
```

All without you writing a single test.

---

## CI/CD — Automated Testing on Pull Requests

> 🚧 Coming soon — not yet configured.

Tests run automatically on every Pull Request via GitHub Actions. The workflow:

1. Triggers on every PR to `main`
2. Installs Python dependencies
3. Runs the full test suite
4. Reports pass/fail directly on the PR

The PR cannot be merged if any tests fail.

See `.github/workflows/ci.yml` for the full workflow configuration.

---

## How the Agent Works (Technical Details)

`watch_and_test.py` uses the `watchdog` library to monitor the `src/` directory for file changes. When a `.py` file is saved, it:

1. Reads the source file contents
2. Builds a prompt instructing Claude to write pytest tests for that code
3. Calls Claude Code CLI in headless mode (`--print` flag) with the prompt
4. Captures Claude's output (raw Python code)
5. Strips any markdown formatting if present
6. Writes the output directly to the corresponding test file in `tests/`
7. Runs `pytest` on the new test file and prints results

The agent ignores `watch_and_test.py` and `agent_generate_tests.py` themselves to avoid infinite loops.

---

## Troubleshooting

**Tests not updating after saving?**
- Make sure `watch_and_test.py` is still running in your terminal
- Check that Claude Code is authenticated: run `claude --version`

**`watchdog` not found?**
```powershell
pip install watchdog
```

**Claude Code not found?**
- Reinstall using `winget install Anthropic.ClaudeCode` and restart your terminal

**Tests fail after generation?**
- This can happen if Claude generates an import path mismatch. Check the import at the top of `test_calculator.py` matches your project structure.
