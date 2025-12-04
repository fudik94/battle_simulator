# ⚔️ RPG Battle Simulator

A small, single-file RPG battle simulator written in Python.  
This project demonstrates the four OOP pillars, uses a simple Factory pattern, and includes unit tests (pytest). It is intentionally small and easy to run — ready to show in a short demo and to defend design decisions.

Contents
- rpg_battle.py — main code (Hero base class, concrete classes, factory, battle logic)
- tests/
  - test_rpg.py — pytest unit tests (3 meaningful tests)
- requirements.txt — project dependencies (pytest)

Quick summary
- Language: Python 3.x
- Purpose: small, complete demo of OOP + unit tests for a course assignment
- Design pattern used: Factory (HeroFactory)

How to run (Windows PowerShell — recommended)
1. Open PowerShell.
2. Change to project folder (example for your path):
3. (Optional but recommended) Create and activate a virtual environment:
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```
4. Install test dependency (pytest):
```powershell
pip install -r requirements.txt
```
5. Run the demo:
```powershell
python .\rpg_battle.py
```
6. Run tests:
```powershell
python -m pytest -q -s
```
- To run a single test:
```powershell
python -m pytest .\tests\test_rpg.py::test_specials_effects -q -s
```

How to run (generic / Linux / macOS)
```bash
cd /path/to/project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python rpg_battle.py
python -m pytest -q -s
```

Project structure (example)
```
rpg_battle.py
requirements.txt
tests/
  test_rpg.py
```

What the code demonstrates (mapping to assignment requirements)
- Abstraction
  - `Hero(ABC)` is an abstract base class with an abstract method `use_special`.
- Inheritance
  - Concrete classes (`Wizard`, `Fighter`, `Cleric`, `Barbarian`, `Druid`, `Warlock`) inherit from `Hero`.
- Polymorphism
  - Each subclass implements its own `use_special` — the battle logic calls `use_special` without knowing the concrete type.
- Encapsulation
  - Health and damage are changed via methods `take_damage`, `heal`, `hit` and `set_damage` rather than writing to fields everywhere.
- Design pattern
  - `HeroFactory` is a simple Factory that centralizes creation of hero instances.

Unit tests (what they cover)
- `test_take_damage_and_heal` — verifies damage and healing logic, including bounds.
- `test_victory_condition_deterministic` — runs a deterministic battle (monkeypatching randomness) and checks victory condition.
- `test_specials_effects` — verifies special abilities (damage/heal effects).

Why tests, briefly
- Tests are repeatable, help catch regressions, and make your behaviour expectations explicit. They are useful for demonstration during defense and for automated checks.

Good demo flow for the presentation
1. Short explanation (30–60s):
   - “This is a small RPG battle simulator to demonstrate OOP principles. Hero is an abstract base class — concrete classes implement special actions. I used a Factory to create heroes and wrote unit tests to verify core behaviors.”
2. Run the demo:
   - `python rpg_battle.py`
3. Run tests:
   - `python -m pytest -q -s`
4. Describe how to add a new hero or change behavior (one sentence).

Common defense questions & short answers
- Q: Why did you use an abstract class for Hero?
  - A: To define a contract (method `use_special`) that every hero must implement and to group shared logic (hit, heal, take_damage).
- Q: Why Factory pattern?
  - A: It centralizes hero creation and decouples the calling code from concrete types; adding new hero types only requires extending the factory.
- Q: How would you add a new attack type or mechanic?
  - A: Add a new method or strategy; for attacks that vary at runtime you can introduce a Strategy pattern to swap attack behaviors.
- Q: Why tests?
  - A: Tests automate checks, prevent regressions, and allow demonstrating correctness reproducibly during your defense.
- Q: Why not use direct field access for health?
  - A: Centralizing health changes via `take_damage`/`heal` enforces invariants (no negative HP, cap at max health) and reduces duplication.

Ideas for small future improvements (if asked)
- Replace prints with a logger or an EventLog class (Observer-style) to decouple UI from logic.
- Add Strategy pattern for attack behaviors (melee/spell/fallback) so that attack logic can be swapped at runtime.
- Add more unit tests for edge cases (invalid inputs, zero damage, race bonus tests).
- Use a registry-based factory to remove `if/elif` chain when adding new classes.

Troubleshooting
- ModuleNotFoundError for `rpg_battle` in tests:
  - Make sure you run pytest from the project root (where `rpg_battle.py` is located).
  - Or set PYTHONPATH temporarily:
    - PowerShell: `$env:PYTHONPATH = (Get-Location).Path`
- If `python` command is not found, try `py -3` or `python3`.

Short usage examples
- Run demo:
```powershell
cd 'C:\path\to\project'
python rpg_battle.py
```
- Run tests:
```powershell
python -m pytest -q -s
```

License & author
- Author: Fuad Ismayilbayli (adapted)
- This is a small educational project for course demonstration.

If you want, I can also:
- create a short exportable defense script (2–3 slides worth of text),
- add a run_tests.bat / run_demo.bat so you can double-click to run on Windows,
- or split the code into multiple modules (cleaner architecture) while keeping the demo the same.




