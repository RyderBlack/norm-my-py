# Python Norminette for 42 Schools

A Python code style checker inspired by 42 Paris' norminette for C, designed to enforce coding standards including **flake8**, **type hints**, and **docstrings**.

## 📋 Description

This norminette checks your Python code against the following standards:
- **Type hints**: Ensures all function arguments and return types are annotated
- **Docstrings**: Verifies that all classes and functions have documentation
- **Flake8**: Enforces PEP8 style guide and code quality standards

The tool displays errors in a format similar to 42's original norminette, making it easy to identify and fix issues.

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip

### Install dependencies

```bash
pip install flake8
```

### Download the norminette

```bash
# Download the script
curl -o norminette_py https://raw.githubusercontent.com/norm-my-py/norminette_py/main/norminette_py

# Make it executable
chmod +x norminette_py

# Optional: Move to PATH for global access
sudo mv norminette_py /usr/local/bin/
```

## 📖 Usage

### Basic usage

```bash
# Check a single file
./norminette_py my_file.py

# Check a directory
./norminette_py src/

# Check multiple files
./norminette_py file1.py file2.py

# Check all Python files in current directory
./norminette_py *.py
```

### Example output

```
============================================================
           NORMINETTE PYTHON - École 42
============================================================

main.py
Error:TYPE_HINT   (line:   15, col:   0): Function 'calculate' missing return type hint
Error:DOCSTRING   (line:   15, col:   0): Function 'calculate' missing docstring
Error:E501        (line:   20, col:  80): line too long (95 > 79 characters)

============================================================
✗ Norme: 3 error(s) in 1 file(s)
```

When all checks pass:
```
============================================================
           NORMINETTE PYTHON - École 42
============================================================

============================================================
✓ Norme: OK! (3 file(s) checked)
```

## 🎯 What it checks

### Type Hints
All function parameters (except `self` and `cls`) and return types must have type annotations:

```python
# ✅ Good
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# ❌ Bad - missing type hints
def add(a, b):
    return a + b
```

### Docstrings
All classes and functions must have docstrings (except magic methods other than `__init__`):

```python
# ✅ Good
class Calculator:
    """A simple calculator class"""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

# ❌ Bad - missing docstrings
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
```

### Flake8 (PEP8)
Follows Python's PEP8 style guide:
- Line length (max 79 characters)
- Proper indentation (4 spaces)
- Import organization
- Whitespace usage
- And many more...

## 🔧 Configuration

### Customize flake8 rules

Create a `.flake8` file in your project root:

```ini
[flake8]
max-line-length = 100
ignore = E203, W503
exclude = .git,__pycache__,venv
```

## 📝 Error Codes

| Code | Description |
|------|-------------|
| `TYPE_HINT` | Missing type annotation on function parameter or return type |
| `DOCSTRING` | Missing docstring on class or function |
| `E***` | Flake8 error codes (see [flake8 documentation](https://flake8.pycqa.org/)) |
| `W***` | Flake8 warning codes |
| `SYNTAX` | Python syntax error |
| `FATAL` | Critical error preventing file check |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

### Contributors

- **RyderBlack**
## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Ryhad Boughanmi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Inspired by [42 School](https://www.42.fr/)'s norminette for C
- Built with Python's `ast` module for code analysis
- Uses [flake8](https://flake8.pycqa.org/) for PEP8 compliance

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Happy coding! 🚀**
