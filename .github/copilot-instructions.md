# Copilot instructions for this workspace

This repository is a small, tutorial-style Python workspace with simple example scripts, modules and classes. The guidance below is tailored to allow an AI coding assistant to be productive quickly.

- Big picture
  - This repo contains standalone example/demo Python files (top-level .py files) used for learning and demonstration. There is no single application entrypoint; scripts are executed directly with the Python interpreter (e.g., `python demo.py`).
  - Files of interest: `demo.py`, `DemoModule.py`, `DemoClass.py`, `BankAccount.py`, `Person.py`, `DemoSet.py`, `demoIndexing.py`.
  - Many files print output or create objects at import time (e.g., `DemoModule.py` prints "모듈이 로딩됩니다.", `BankAccount.py`/`DemoClass.py` create and print instances). Take care when importing: side-effects are intentional for demonstrations.

- Coding patterns and conventions
  - File-level examples: each top-level file is a runnable demo; prefer editing the file in place and run it rather than trying to integrate into a larger app.
  - Naming: classes use CamelCase (e.g., `BankAccount`, `Person`). Functions and file names use snake_case or mixed forms (this repo is informal).
  - Encapsulation: some classes use name mangling with double underscores for private fields (e.g., `DemoClass.BankAccount` uses `self.__id`). Be consistent when referencing these attributes.
  - Printing and side-effects: many files construct objects and call `print()` at module scope. When writing new modules or tests, avoid importing these demo files directly if you want to prevent printed output — import functions/classes in a way that avoids executing the demo code (or refactor into `if __name__ == "__main__":`).

- Developer workflow
  - Run a script: `python <filename>.py` from the workspace root (Windows PowerShell):
    - Example: `python .\\demo.py`
  - Debugging: Open the file in VS Code and use the built-in debugger. The demos are intentionally small and suitable for setting breakpoints in constructors or print statements.
  - No build/test system detected: there is no `requirements.txt`, `setup.py`, or tests. Assume plain CPython execution (recommended Python 3.8+).

- What to change/avoid when making edits
  - If you add new modules intended for import, place demo execution under `if __name__ == "__main__":` to avoid executing on import.
  - Avoid renaming files referenced by other demos without updating the import lines.
  - When adding private attributes, prefer single underscore for soft privacy unless you need name mangling semantics.

- Integration points & external deps
  - No external dependencies are declared. If you introduce third-party packages, add a `requirements.txt` and document how to install (`pip install -r requirements.txt`).

- Examples from the codebase
  - `DemoModule.py` prints on import and defines `x` and `printX()`; importing it will execute the print statement.
  - `BankAccount.py` and `DemoClass.py` both create `BankAccount` instances at module scope and print them; they illustrate string formatting in `__str__()`.
  - `Person.py` demonstrates default attribute initialization and instance mutation.

- Suggested quick tasks for contributors
  - Refactor demo files to avoid import-time side effects by moving demo code under `if __name__ == "__main__":`.
  - Add a `README.md` summarizing how to run each demo.
  - Add `requirements.txt` if external libraries are introduced.

If any part of the repo has additional hidden files or a specific workflow I didn't detect, tell me which files to inspect and I will merge that into this guidance.