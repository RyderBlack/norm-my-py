#!/usr/bin/env python3
"""
Python Norminette for 42 School
Checks: flake8, type hints, docstrings
"""

import ast
import sys
import subprocess
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class NormError:
    """Represents a norm error"""
    file: str
    line: int
    col: int
    code: str
    message: str
    severity: str = "Error"


class PythonNorminette:
    """Python code checker 42 style"""
    
    def __init__(self):
        self.errors: List[NormError] = []
        self.files_checked = 0
        self.total_errors = 0
    
    def check_file(self, filepath: str) -> List[NormError]:
        """Check a Python file"""
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=filepath)
            
            errors.extend(self._check_type_hints(tree, filepath))
            errors.extend(self._check_docstrings(tree, filepath))
            errors.extend(self._check_flake8(filepath))
            
        except SyntaxError as e:
            errors.append(NormError(
                file=filepath,
                line=e.lineno or 0,
                col=e.offset or 0,
                code="SYNTAX",
                message=f"Syntax error: {e.msg}"
            ))
        except Exception as e:
            errors.append(NormError(
                file=filepath,
                line=0,
                col=0,
                code="FATAL",
                message=f"Cannot check file: {e}"
            ))
        
        return errors
    
    def _check_type_hints(self, tree: ast.AST, filepath: str) -> List[NormError]:
        """Check for type hints presence"""
        errors = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('__') and node.name.endswith('__'):
                    continue
                
                if node.returns is None:
                    errors.append(NormError(
                        file=filepath,
                        line=node.lineno,
                        col=node.col_offset,
                        code="TYPE_HINT",
                        message=(
                            f"Function '{node.name}' missing return "
                            f"type hint"
                        )
                    ))
                
                for arg in node.args.args:
                    if arg.arg == 'self' or arg.arg == 'cls':
                        continue
                    if arg.annotation is None:
                        errors.append(NormError(
                            file=filepath,
                            line=node.lineno,
                            col=node.col_offset,
                            code="TYPE_HINT",
                            message=(
                                f"Argument '{arg.arg}' in function "
                                f"'{node.name}' missing type hint"
                            )
                        ))
        
        return errors
    
    def _check_docstrings(self, tree: ast.AST, filepath: str) -> List[NormError]:
        """Check for docstrings presence"""
        errors = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    errors.append(NormError(
                        file=filepath,
                        line=node.lineno,
                        col=node.col_offset,
                        code="DOCSTRING",
                        message=f"Class '{node.name}' missing docstring"
                    ))
            
            elif isinstance(node, ast.FunctionDef):
                is_magic = (
                    node.name.startswith('__') and
                    node.name.endswith('__') and
                    node.name != '__init__'
                )
                if is_magic:
                    continue
                
                if not ast.get_docstring(node):
                    errors.append(NormError(
                        file=filepath,
                        line=node.lineno,
                        col=node.col_offset,
                        code="DOCSTRING",
                        message=f"Function '{node.name}' missing docstring"
                    ))
        
        return errors
    
    def _check_flake8(self, filepath: str) -> List[NormError]:
        """Run flake8 on file"""
        errors = []
        
        try:
            format_str = (
                '--format=%(path)s:%(row)d:%(col)d: '
                '%(code)s %(text)s'
            )
            result = subprocess.run(
                ['flake8', filepath, format_str],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue
                    
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        file_path = parts[0]
                        line_num = int(parts[1])
                        col_num = int(parts[2])
                        msg_parts = parts[3].strip().split(' ', 1)
                        code = msg_parts[0]
                        message = msg_parts[1] if len(msg_parts) > 1 else ""
                        
                        errors.append(NormError(
                            file=file_path,
                            line=line_num,
                            col=col_num,
                            code=code,
                            message=message
                        ))
        
        except FileNotFoundError:
            warning_msg = (
                "\033[33mWarning: flake8 not installed. "
                "Install with: pip install flake8\033[0m"
            )
            print(warning_msg)
        except Exception as e:
            print(f"\033[33mWarning: flake8 check failed: {e}\033[0m")
        
        return errors
    
    def print_errors(self, errors: List[NormError]):
        """Display errors norminette 42 style"""
        if not errors:
            return
        
        files: Dict[str, List[NormError]] = {}
        for error in errors:
            if error.file not in files:
                files[error.file] = []
            files[error.file].append(error)
        
        for filepath, file_errors in files.items():
            print(f"\033[1m{filepath}\033[0m")
            
            for err in sorted(file_errors, key=lambda x: (x.line, x.col)):
                color = (
                    "\033[31m" if err.severity == "Error" else "\033[33m"
                )
                print(
                    f"{color}Error:{err.code:12} \033[0m"
                    f"(line: {err.line:4}, col: {err.col:3}): "
                    f"{err.message}"
                )
            
            print()
    
    def run(self, paths: List[str]) -> int:
        """Run norminette on files/directories"""
        all_errors = []
        
        for path_str in paths:
            path = Path(path_str)
            
            if path.is_file():
                if path.suffix == '.py':
                    self.files_checked += 1
                    errors = self.check_file(str(path))
                    all_errors.extend(errors)
            
            elif path.is_dir():
                for py_file in path.rglob('*.py'):
                    self.files_checked += 1
                    errors = self.check_file(str(py_file))
                    all_errors.extend(errors)
        
        self.total_errors = len(all_errors)
        self.errors = all_errors
        
        self.print_errors(all_errors)
        
        print("\033[1m" + "=" * 60 + "\033[0m")
        if self.total_errors == 0:
            msg = (
                f"\033[32m✓ Norme: OK! "
                f"({self.files_checked} file(s) checked)\033[0m"
            )
            print(msg)
            return 0
        else:
            msg = (
                f"\033[31m✗ Norme: {self.total_errors} error(s) "
                f"in {self.files_checked} file(s)\033[0m"
            )
            print(msg)
            return 1


def main():
    """Entry point"""
    if len(sys.argv) < 2:
        print("Usage: norminette_py <file_or_directory> [...]")
        print("\nExample:")
        print("  norminette_py my_file.py")
        print("  norminette_py src/")
        print("  norminette_py *.py")
        sys.exit(1)
    
    print("\033[1m" + "=" * 60)
    print("           PYTHON NORMINETTE - 42 School")
    print("=" * 60 + "\033[0m\n")
    
    norminette = PythonNorminette()
    exit_code = norminette.run(sys.argv[1:])
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
